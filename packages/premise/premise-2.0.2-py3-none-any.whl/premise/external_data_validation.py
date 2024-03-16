"""
Validates datapackages that contain external scenario data.
"""

from typing import Union

import numpy as np
import pandas as pd
import yaml
from datapackage import exceptions, validate
from schema import And, Optional, Schema, Use

from .geomap import Geomap
from .utils import load_constants

config = load_constants()


def find_iam_efficiency_change(
    variable: Union[str, list], location: str, efficiency_data, year: int
) -> float:
    """
    Return the relative change in efficiency for `variable` in `location`
    relative to 2020.
    :param variable: IAM variable name
    :param location: IAM region
    :return: relative efficiency change (e.g., 1.05)
    """

    scaling_factor = 1

    if variable in efficiency_data.variables.values:
        scaling_factor = (
            efficiency_data.sel(region=location, variables=variable).interp(year=year)
        ).values.item(0)

        if scaling_factor in (np.nan, np.inf):
            scaling_factor = 1

    return scaling_factor


def flag_activities_to_adjust(
    dataset: dict, scenario_data: dict, year: int, dataset_vars: dict
) -> dict:
    """
    Flag datasets that will need to be adjusted.
    :param dataset: dataset to be adjusted
    :param scenario_data: external scenario data
    :param year: year of the external scenario
    :param dataset_vars: variables of the dataset
    :return: dataset with additional info on variables to adjust
    """

    regions = scenario_data["production volume"].region.values.tolist()
    if "except regions" in dataset_vars:
        regions = [r for r in regions if r not in dataset_vars["except regions"]]

    dataset["regions"] = regions

    # add potential technosphere or biosphere filters
    if "efficiency" in dataset_vars:
        if len(dataset_vars["efficiency"]) > 0:
            dataset["adjust efficiency"] = True

            d_tech_filters = {
                k.get("variable"): [
                    k.get("includes").get("technosphere"),
                    {
                        region: find_iam_efficiency_change(
                            k["variable"],
                            region,
                            scenario_data["efficiency"],
                            year,
                        )
                        for region in regions
                    },
                ]
                for k in dataset_vars["efficiency"]
                if "technosphere" in k.get("includes", {})
            }

            d_tech_filters.update(
                {
                    k.get("variable"): [
                        None,
                        {
                            region: find_iam_efficiency_change(
                                k["variable"],
                                region,
                                scenario_data["efficiency"],
                                year,
                            )
                            for region in regions
                        },
                    ]
                    for k in dataset_vars["efficiency"]
                    if "includes" not in k
                }
            )

            d_bio_filters = {
                k.get("variable"): [
                    k.get("includes").get("biosphere"),
                    {
                        region: find_iam_efficiency_change(
                            k["variable"],
                            region,
                            scenario_data["efficiency"],
                            year,
                        )
                        for region in regions
                    },
                ]
                for k in dataset_vars["efficiency"]
                if "biosphere" in k.get("includes", {})
            }

            d_bio_filters.update(
                {
                    k.get("variable"): [
                        None,
                        {
                            region: find_iam_efficiency_change(
                                k["variable"],
                                region,
                                scenario_data["efficiency"],
                                year,
                            )
                            for region in regions
                        },
                    ]
                    for k in dataset_vars["efficiency"]
                    if "includes" not in k
                }
            )

            if d_tech_filters:
                dataset["technosphere filters"] = d_tech_filters

            if d_bio_filters:
                dataset["biosphere filters"] = d_bio_filters

        # define exclusion filters
        for k in dataset_vars["efficiency"]:
            if "excludes" in k:
                if "technosphere" in k.get("excludes", {}):
                    dataset["excludes technosphere"] = {
                        k["variable"]: k["excludes"]["technosphere"]
                    }
                if "biosphere" in k.get("excludes", {}):
                    dataset["excludes biosphere"] = {
                        k["variable"]: k["excludes"]["biosphere"]
                    }

    if dataset_vars["replaces"]:
        dataset["replaces"] = dataset_vars["replaces"]

    if dataset_vars["replaces in"]:
        dataset["replaces in"] = dataset_vars["replaces in"]

    if dataset_vars["replacement ratio"] != 1.0:
        dataset["replacement ratio"] = dataset_vars["replacement ratio"]

    if dataset_vars["regionalize"]:
        dataset["regionalize"] = dataset_vars["regionalize"]

    if "production volume variable" in dataset_vars:
        dataset["production volume variable"] = dataset_vars[
            "production volume variable"
        ]

    return dataset


def check_inventories(
    configuration: dict,
    inventory_data: list,
    scenario_data: dict,
    database: list,
    year: int,
    model: str,
):
    """
    Check that the inventory data is valid.
    :param configuration: config file
    :param inventory_data: inventory data to check
    :param scenario_data: external scenario data
    :param database: database
    :param year: scenario year
    :param model: IAM model
    """

    geo = Geomap(model=model)

    d_datasets = {
        (
            val["ecoinvent alias"]["name"],
            val["ecoinvent alias"]["reference product"],
        ): {
            "exists in original database": val["ecoinvent alias"].get(
                "exists in original database", True
            ),
            "new dataset": val["ecoinvent alias"].get("new dataset", False),
            "regionalize": val["ecoinvent alias"].get("regionalize", False),
            "mask": val["ecoinvent alias"].get("mask", None),
            "except regions": val.get(
                "except regions",
                [
                    "World",
                ],
            ),
            "efficiency": val.get("efficiency", []),
            "replaces": val.get("replaces", []),
            "replaces in": val.get("replaces in", []),
            "replacement ratio": val.get("replacement ratio", 1),
            "production volume variable": val.get("production volume", {}).get(
                "variable"
            ),
        }
        for val in configuration["production pathways"].values()
    }

    # direct regionalization
    if "regionalize" in configuration:
        d_datasets.update(
            {
                (val["name"], val["reference product"]): {
                    "exists in original database": val.get(
                        "exists in original database", False
                    ),
                    "regionalize": True,
                    "new dataset": False,
                    "except regions": configuration["regionalize"].get(
                        "except regions", []
                    ),
                    "efficiency": val.get("efficiency", []),
                    "replaces": val.get("replaces", []),
                    "replaces in": val.get("replaces in", []),
                    "replacement ratio": val.get("replacement ratio", 1),
                }
                for val in configuration["regionalize"]["datasets"]
            }
        )

    list_datasets = [(i["name"], i["reference product"]) for i in inventory_data]

    try:
        assert all(
            (i[0], i[1]) in list_datasets
            for i, v in d_datasets.items()
            if not v["exists in original database"] and not v.get("new dataset")
        )
    except AssertionError as e:
        list_missing_datasets = [
            i[0]
            for i, v in d_datasets.items()
            if not v["exists in original database"]
            and not v.get("new dataset")
            and (i[0], i[1]) not in list_datasets
        ]

        raise AssertionError(
            f"The following datasets are not in the inventory data: {list_missing_datasets}"
            f"\n Available datasets are: \n"
            f"{[list_datasets]}"
        ) from e

    # flag imported inventories
    for i, dataset in enumerate(inventory_data):
        key = (dataset["name"], dataset["reference product"])
        if key in d_datasets:
            if d_datasets[key]["exists in original database"] is False:
                dataset["custom scenario dataset"] = True
                data_vars = d_datasets[(dataset["name"], dataset["reference product"])]
                inventory_data[i] = flag_activities_to_adjust(
                    dataset, scenario_data, year, data_vars
                )

    # flag inventories present in the original database
    for key, val in d_datasets.items():
        if val.get("exists in original database"):
            potential_candidates = [
                ds
                for ds in database + inventory_data
                if ds["name"] == key[0] and ds["reference product"] == key[1]
            ]

            # if a mask is provided, we want to use it
            if val.get("mask"):
                potential_candidates = [
                    ds for ds in potential_candidates if val["mask"] not in ds["name"]
                ]

            if len(potential_candidates) == 0:
                # maybe it is in inventory_data
                if (
                    len(
                        [
                            d
                            for d in inventory_data
                            if d["name"] == key[0] and d["reference product"] == key[1]
                        ]
                    )
                    == 0
                ):
                    raise ValueError(
                        f"Dataset {key[0]} and {key[1]} is not found in the original database."
                    )
                else:
                    continue
            elif len(potential_candidates) == 1:
                potential_candidates[0] = flag_activities_to_adjust(
                    potential_candidates[0], scenario_data, year, val
                )

            else:
                # we want to short list the candidates
                # that make the most sense according to `regions`
                short_listed = {
                    r: None for r in scenario_data["production volume"].region.values
                }
                for potential_candidate in potential_candidates:
                    if (
                        potential_candidate["location"]
                        in scenario_data["production volume"].region.values
                    ):
                        short_listed[potential_candidate["location"]] = (
                            potential_candidate
                        )

                # check if any remaining candidates to find
                if None in short_listed.values():
                    for region in short_listed:
                        if short_listed[region] is None:
                            for potential_candidate in potential_candidates:

                                try:
                                    if region in geo.geo.contained(
                                        potential_candidate["location"]
                                    ):
                                        short_listed[region] = potential_candidate
                                        break
                                except KeyError:
                                    continue

                                try:
                                    if region in geo.geo.intersects(
                                        potential_candidate["location"]
                                    ):
                                        short_listed[region] = potential_candidate
                                        break
                                except KeyError:
                                    continue

                                if region in geo.ecoinvent_to_iam_location(
                                    potential_candidate["location"]
                                ):
                                    short_listed[region] = potential_candidate
                                    break

                if None in short_listed.values():
                    # check with IAM regions
                    for region in short_listed:
                        if short_listed[region] is None:
                            for potential_candidate in potential_candidates:
                                if region in geo.map_ecoinvent_to_iam(
                                    potential_candidate["location"]
                                ):
                                    short_listed[region] = potential_candidate
                                    break

                if None in short_listed.values():
                    # resort to candidates with locations "GLO", "RoW", "World" and "GLO"
                    for region in short_listed:
                        if short_listed[region] is None:
                            for fallback_location in ["GLO", "RoW", "World"]:
                                for potential_candidate in potential_candidates:
                                    if (
                                        potential_candidate["location"]
                                        == fallback_location
                                    ):
                                        short_listed[region] = potential_candidate
                                        break

                for loc, ds in short_listed.items():
                    if ds is not None:
                        flag_activities_to_adjust(ds, scenario_data, year, val)
                    else:
                        print(
                            f"No candidate found for {key[0]} and {key[1]} for {loc}."
                        )

    return inventory_data, database


def check_datapackage(datapackages: list):
    # validate package descriptor
    for datapackage in datapackages:
        try:
            validate(datapackage.descriptor)
        except exceptions.ValidationError as exception:
            raise exception

    for d, datapackage in enumerate(datapackages):
        if "config" in [
            i.name for i in datapackage.resources
        ] and "scenario_data" not in [i.name for i in datapackage.resources]:
            raise ValueError(
                "If the resource 'config' is present in the datapackage,"
                "so must the resource 'scenario_data'."
            )

        if "scenario_data" in [
            i.name for i in datapackage.resources
        ] and "config" not in [i.name for i in datapackage.resources]:
            raise ValueError(
                "If the resource 'scenario_data' is present in the datapackage,"
                " so must the resource 'config'."
            )

        assert (
            datapackage.descriptor["ecoinvent"]["version"]
            in config["SUPPORTED_EI_VERSIONS"]
        ), f"The ecoinvent version in datapackage  {d + 1} is not supported. Must be one of {config['SUPPORTED_EI_VERSIONS']}."

        if (
            sum(
                s.name == y.name
                for s in datapackage.resources
                for y in datapackage.resources
            )
            / len(datapackage.resources)
            > 1
        ):
            raise ValueError(
                f"Two or more resources in datapackage {d + 1} are similar."
            )


def list_all_iam_regions(configuration):
    """
    List all IAM regions in the config file.
    :param configuration: config file
    :return: list of IAM regions
    """

    list_regions = []

    for k, v in configuration.items():
        if k.startswith("LIST_"):
            list_regions.extend(v)

    return list_regions


def check_config_file(datapackages):
    for i, dp in enumerate(datapackages):
        resource = dp.get_resource("config")
        config_file = yaml.safe_load(resource.raw_read())

        file_schema = Schema(
            {
                "production pathways": {
                    str: {
                        "production volume": {
                            "variable": str,
                        },
                        "ecoinvent alias": {
                            "name": str,
                            "reference product": str,
                            Optional("exists in original database"): bool,
                            Optional("mask"): str,
                            Optional("new dataset"): bool,
                            Optional("regionalize"): bool,
                            Optional("ratio"): float,
                        },
                        Optional("efficiency"): [
                            {
                                "variable": str,
                                Optional("reference year"): And(
                                    Use(int), lambda n: 2005 <= n <= 2100
                                ),
                                Optional("includes"): {
                                    Optional("technosphere"): list,
                                    Optional("biosphere"): list,
                                },
                                Optional("excludes"): {
                                    Optional("technosphere"): list,
                                    Optional("biosphere"): list,
                                },
                            }
                        ],
                        Optional("except regions"): And(
                            list,
                            Use(list),
                            lambda s: all(i in list_all_iam_regions(config) for i in s),
                        ),
                        Optional("replaces"): [
                            {
                                "name": str,
                                "product": str,
                                Optional("location"): str,
                                Optional("operator"): str,
                            }
                        ],
                        Optional("replaces in"): [
                            {
                                Optional("name"): str,
                                Optional("reference product"): str,
                                Optional("location"): str,
                                Optional("operator"): str,
                            }
                        ],
                        Optional("replacement ratio"): float,
                    },
                },
                Optional("markets"): [
                    {
                        "name": str,
                        "reference product": str,
                        "unit": str,
                        "includes": And(
                            list,
                            Use(list),
                            lambda s: all(
                                i in config_file["production pathways"] for i in s
                            ),
                        ),
                        Optional("add"): [
                            {
                                Optional("name"): str,
                                Optional("reference product"): str,
                                Optional("categories"): str,
                                Optional("unit"): str,
                                Optional("amount"): float,
                            }
                        ],
                        Optional("except regions"): And(
                            list,
                            Use(list),
                            lambda s: all(
                                i
                                in config["LIST_REMIND_REGIONS"]
                                + config["LIST_IMAGE_REGIONS"]
                                for i in s
                            ),
                        ),
                        Optional("replaces"): [
                            {
                                "name": str,
                                "product": str,
                                Optional("location"): str,
                                Optional("operator"): str,
                            }
                        ],
                        Optional("replaces in"): [
                            {
                                Optional("name"): str,
                                Optional("reference product"): str,
                                Optional("location"): str,
                                Optional("operator"): str,
                            }
                        ],
                        Optional("is fuel"): dict,
                        Optional("replacement ratio"): float,
                        Optional("waste market"): bool,
                        Optional("efficiency"): [
                            {
                                "variable": str,
                                Optional("reference year"): And(
                                    Use(int), lambda n: 2005 <= n <= 2100
                                ),
                                Optional("includes"): {
                                    Optional("technosphere"): list,
                                    Optional("biosphere"): list,
                                },
                                Optional("excludes"): {
                                    Optional("technosphere"): list,
                                    Optional("biosphere"): list,
                                },
                            }
                        ],
                    }
                ],
                Optional("regionalize"): {
                    "datasets": [
                        {
                            "name": str,
                            "reference product": str,
                            Optional("exists in original database"): bool,
                        }
                    ],
                    Optional("except regions"): And(
                        list,
                        Use(list),
                        lambda s: all(
                            i
                            in config["LIST_REMIND_REGIONS"]
                            + config["LIST_IMAGE_REGIONS"]
                            for i in s
                        ),
                    ),
                },
            }
        )

        file_schema.validate(config_file)

        if "markets" in config_file:
            # check that providers composing the market
            # are listed

            for market in config_file["markets"]:
                try:
                    [
                        (
                            config_file["production pathways"][a]["ecoinvent alias"][
                                "name"
                            ],
                            config_file["production pathways"][a]["ecoinvent alias"][
                                "reference product"
                            ],
                        )
                        for a in market["includes"]
                    ]
                except KeyError as err:
                    raise ValueError(
                        "One of more providers listed under `markets/includes` is/are not listed "
                        "under `production pathways`."
                    ) from err

    needs_imported_inventories = [False for _ in datapackages]

    for i, dp in enumerate(datapackages):
        resource = dp.get_resource("config")
        config_file = yaml.safe_load(resource.raw_read())

        if len(list(config_file["production pathways"].keys())) != sum(
            get_recursively(
                config_file["production pathways"], "exists in original database"
            )
        ):
            needs_imported_inventories[i] = True

    return sum(needs_imported_inventories)


def check_scenario_data_file(datapackages, iam_scenarios):
    for i, dp in enumerate(datapackages):
        scenarios = dp.descriptor["scenarios"]

        rev_scenarios = {}

        for scenario, lst_iam_scen in scenarios.items():
            for iam_scen in lst_iam_scen:
                if (iam_scen["model"], iam_scen["pathway"]) not in rev_scenarios:
                    rev_scenarios[(iam_scen["model"], iam_scen["pathway"])] = [scenario]
                else:
                    rev_scenarios[(iam_scen["model"], iam_scen["pathway"])].append(
                        scenario
                    )

        for iam_scen, lst_ext_scen in rev_scenarios.items():
            if len(lst_ext_scen) > 1:
                if iam_scen in [(x["model"], x["pathway"]) for x in iam_scenarios]:
                    print(
                        f"{iam_scen} can be used with more than one external scenarios: {lst_ext_scen}."
                    )
                    print(f"Choose the scenario to associate {iam_scen} with:")
                    for s, scen in enumerate(lst_ext_scen):
                        print(f"{s} - {scen}")
                    usr_input = ""

                    while usr_input not in list(range(len(lst_ext_scen))):
                        usr_input = int(input("Scenario no.: "))
                    rev_scenarios[iam_scen] = [lst_ext_scen[int(usr_input)]]

        for iam_scen in iam_scenarios:
            try:
                if "external scenarios" in iam_scen:
                    iam_scen["external scenarios"].append(
                        rev_scenarios[(iam_scen["model"], iam_scen["pathway"])][0]
                    )
                else:
                    iam_scen["external scenarios"] = [
                        rev_scenarios[(iam_scen["model"], iam_scen["pathway"])][0]
                    ]
            except KeyError as err:
                raise KeyError(
                    f"External scenario no. {i + 1} is not compatible with {iam_scen['model'], iam_scen['pathway']}."
                ) from err

        resource = dp.get_resource("scenario_data")
        scenario_data = resource.read()
        scenario_headers = resource.headers

        df = pd.DataFrame(scenario_data, columns=scenario_headers)

        resource = dp.get_resource("config")
        config_file = yaml.safe_load(resource.raw_read())

        mandatory_fields = [
            "model",
            "pathway",
            "scenario",
            "region",
            "variables",
            "unit",
        ]
        if not all(v in df.columns for v in mandatory_fields):
            raise ValueError(
                f"One or several mandatory column are missing "
                f"in the scenario data file no. {i + 1}. Mandatory columns: {mandatory_fields}."
            )

        years_cols = []
        for header in scenario_headers:
            try:
                years_cols.append(int(header))
            except ValueError:
                continue

        if not all(2005 <= y <= 2100 for y in years_cols):
            raise ValueError(
                f"One or several of the years provided in the scenario data file no. {i + 1} are "
                "out of boundaries (2005 - 2100)."
            )

        if not all(
            min(years_cols) <= y <= max(years_cols)
            for y in [s["year"] for s in iam_scenarios]
        ):
            raise ValueError(
                f"The list of years you wish to create a database for are not entirely covered"
                f" by the scenario data file no. {i + 1}."
            )

        if len(pd.isnull(df).sum()[pd.isnull(df).sum() > 0]) > 0:
            raise ValueError(
                f"The following columns in the scenario data file no. {i + 1}"
                f"contains empty cells.\n{pd.isnull(df).sum()[pd.isnull(df).sum() > 0]}."
            )

        if any(
            m not in df["model"].unique() for m in [s["model"] for s in iam_scenarios]
        ):
            raise ValueError(
                f"One or several model name(s) in the list of scenarios to create "
                f"is/are not found in the scenario data file no. {i + 1}. "
            )

        if any(
            s not in df["pathway"].unique()
            for s in [p["pathway"] for p in iam_scenarios]
        ):
            raise ValueError(
                f"One or several pathway name(s) in the scenario data file no. {i + 1} "
                "is/are not found in the list of scenarios to create."
            )

        if any(
            m not in df["pathway"].unique()
            for m in [s["pathway"] for s in iam_scenarios]
        ):
            raise ValueError(
                f"One or several pathway name(s) in the list of scenarios to create "
                f"is/are not found in the scenario data file no. {i + 1}."
            )

        d_regions = {}

        for model in config["SUPPORTED_MODELS"]:
            for k, v in config.items():
                if k.startswith("LIST_") and model.lower() in k.lower():
                    d_regions[model] = v

        list_ei_locs = [
            i if isinstance(i, str) else i[-1]
            for i in list(Geomap(model="remind").geo.keys())
        ]

        for irow, r in df.iterrows():
            if (
                r["region"] not in d_regions[r["model"]]
                and r["region"] not in list_ei_locs
            ):
                raise ValueError(
                    f"Region {r['region']} indicated "
                    f"in row {irow} is not a valid region for model {r['model'].upper()}"
                    f"and is not found within ecoinvent locations."
                )

        available_scenarios = df["scenario"].unique()

        if not all(
            s in available_scenarios for s in scenarios
        ):  # check that all scenarios are available in the scenario file
            print(
                "The following scenarios listed in the json file "
                "are not available in the scenario data file:"
            )
            print(set(s for s in scenarios if s not in available_scenarios))
            raise ValueError(
                f"One or several scenarios are not available in the scenario file no. {i + 1}."
            )

        # check that all scenarios in `iam_scenarios` are listed in `scenarios`

        if not any(
            (iam_s["model"], iam_s["pathway"])
            in [(t["model"], t["pathway"]) for s in scenarios.values() for t in s]
            for iam_s in iam_scenarios
        ):
            raise ValueError(
                f"One or several scenarios are not available in the external scenario file no. {i + 1}."
            )

        if not all(
            v in df["variables"].unique()
            for v in get_recursively(config_file, "variable")
        ):
            list_unfound_variables = [
                p
                for p in get_recursively(config_file, "variable")
                if p not in df["variables"].unique()
            ]

            raise ValueError(
                "The following variables from the configuration file "
                f"cannot be found in the scenario file no. {i + 1}.: {list_unfound_variables}"
            )

        if not all(
            v in df["variables"].unique()
            for v in get_recursively(config_file, "variable")
        ):
            missing_variables = [
                v
                for v in get_recursively(config_file, "variable")
                if v not in df["variables"].unique()
            ]
            raise ValueError(
                f"One or several variable names in the configuration file {i + 1} "
                f"cannot be found in the scenario data file: {missing_variables}."
            )

        try:
            np.array_equal(df.iloc[:, 6:], df.iloc[:, 6:].astype(float))
        except ValueError as e:
            raise TypeError(
                f"All values provided in the time series must be numerical "
                f"in the scenario data file no. {i + 1}."
            ) from e

    return datapackages, iam_scenarios


def get_recursively(search_dict, field):
    """Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():
        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found


def check_external_scenarios(datapackage: list, iam_scenarios: list) -> tuple:
    """
    Check that all required keys and values are found to add a custom scenario.
    :param datapackage: scenario dictionary
    :return: scenario dictionary
    """

    # Validate datapackage
    check_datapackage(datapackage)

    # Validate yaml config file
    check_config_file(datapackage)

    # Validate scenario data
    datapackage, iam_scenarios = check_scenario_data_file(datapackage, iam_scenarios)

    return datapackage, iam_scenarios


def fetch_dataset_description_from_production_pathways(
    configuration: dict, item: str
) -> tuple:
    for p, v in configuration["production pathways"].items():
        if p == item:
            if "exists in original database" not in v["ecoinvent alias"]:
                v["ecoinvent alias"].update({"exists in original database": True})

            if "new dataset" not in v["ecoinvent alias"]:
                v["ecoinvent alias"].update({"new dataset": False})

            return (
                v["ecoinvent alias"]["name"],
                v["ecoinvent alias"]["reference product"],
                v["ecoinvent alias"]["exists in original database"],
                v["ecoinvent alias"]["new dataset"],
            )
    return None, None, None, None

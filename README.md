<p align="center">
    <img src="https://github.com/javedali99/si2023-compound-flooding/assets/15319503/f2a06762-adfa-44e2-a9c0-67504b982e1b" alt="disaster" width="150" height="150">
  </a>
  <h2 align="center">Analyzing Contributions of Storm Drivers to Compound Flooding Using Coupled Modeling and Machine Learning Approaches</h2>
</p>

<br>

## Storms in NYC

| Name                    | Date of Landfall | Date of Impact on NYC | CFE Time Bounds  | Year |
| ----------------------- | ---------------- | --------------------- | ---------------- | ---- |
| Tropical Storm Barry    | 2-Jun-2007       | 5-Jun-2007            | 31-May to 6-Jun  | 2007 |
| Hurricane Hanna         | 6-Sep-2008       | 6-Sep-2008            | 4-Sep to 8-Sep   | 2008 |
| Hurricane Bill          | 22-Aug-2009      | 22-Aug-2009           | 20-Aug to 24-Aug | 2009 |
| Hurricane Irene         | 29-Aug-2011      | 27-Aug to 28-Aug-2011 | 26-Aug to 30-Aug | 2011 |
| Hurricane Sandy         | 29-Oct-2012      | 28-Oct to 29-Oct-2012 | 26-Oct to 31-Oct | 2012 |
| Tropical Storm Andrea   | 6-Jun-2013       | 7-Jun to 8-Jun-2013   | 4-Jun to 10-Jun  | 2013 |
| Hurricane Arthur        | 4-Jul-2014       | 4-Jul-2014            | 2-Jul to 6-Jul   | 2014 |
| Tropical Storm Bill     | 13-Jun-2015      | 21-Jun to 22-Jun-2015 | 11-Jun to 24-Jun | 2015 |
| Tropical Storm Bonnie   | 29-May-2016      | 28-May-2016           | 27-May to 30-May | 2016 |
| Hurricane Matthew       | 8-Oct-2016       | 9-Oct to 10-Oct-2016  | 6-Oct to 12-Oct  | 2016 |
| Tropical Storm Cindy    | 22-Jun-2017      | 19-Jun-2017           | 18-Jun to 24-Jun | 2017 |
| Hurricane Gert          | -                | 18-Aug-2017           | 16-Aug to 20-Aug | 2017 |
| Tropical Storm Jose     | -                | 19-Sep to 20-Sep-2017 | 17-Sep to 22-Sep | 2017 |
| Hurricane Maria         | 20-Sep-2017      | 27-Sep-2017           | 18-Sep to 29-Sep | 2017 |
| Tropical Storm Philippe | 28-Oct-2017      | 28-Oct to 30-Oct-2017 | 26-Oct to 1-Nov  | 2017 |
| Tropical Storm Gordon   | 5-Sep-2018       | 8-Sep to 9-Sep-2018   | 3-Sep to 11-Sep  | 2018 |
| Hurricane Michael       | 10-Oct-2018      | 11-Oct to 12-Oct-2018 | 8-Oct to 14-Oct  | 2018 |
| Hurricane Dorian        | 5-Sep-2019       | 6-Sep to 7-Sep-2019   | 3-Sep to 9-Sep   | 2019 |
| Tropical Storm Ogla     | 26-Oct-2019      | 27-Oct-2019           | 24-Oct to 29-Oct | 2019 |

## Hydrologic Modeling using NextGen CFE Model

The National Water Center CFE (Conceptual Framework for Entity) model is a type of rainfall-runoff model. It's a conceptual model, meaning it's designed to represent complex hydrological processes using simplified, easy-to-understand concepts. The model is designed to simulate how rainfall gets converted into runoff, a key process in understanding how much water will flow into rivers and streams after a rain event. It's designed with an implementation of the Basic Model Interface, a standard set of functions and procedures designed to facilitate model coupling in integrated environmental modeling studies.

### Generate HydroFabrics Subsets for the 8 watersheds in New York City (NYC) area

Retrieved hydrofabric data, followed by the extraction of necessary infromation for creating the parameter configuration file. These files are created for running Conceptual Functional Equivalent (CFE) model and Simple Logical Tautology Handler (SLoTH) in the NGEN framework.

### Prepare Basin Averaged Forcing for NextGen CFE Model

Prepared basin averaged forcing input from for the NOAA Next Generation (NextGen) Water Resource Modeling Framework from AORC v1.0 kerchunk header files.

### Run CFE Model in NGEN Framework

To run the _ngen_ engine, the following command line positional arguments are supported:

- _catchment_data_path_ -- path to catchment data geojson input file.
- _catchment subset ids_ -- list of comma separated ids (NO SPACES!!!) to subset the catchment data, i.e. 'cat-0,cat-1', an empty string or "all" will use all catchments in the hydrofabric
- _nexus_data_path_ -- path to nexus data geojson input file
- _nexus subset ids_ -- list of comma separated ids (NO SPACES!!!) to subset the nexus data, i.e. 'nex-0,nex-1', an empty string or "all" will use all nexus points
- _realization_config_path_ -- path to json configuration file for realization/formulations associated with the hydrofabric inputs
- _partition_config_path_ -- path to the partition json config file, when using the driver with [distributed processing](doc/DISTRIBUTED_PROCESSING.md).
- `--subdivided-hydrofabric` -- an explicit, optional flag, when using the driver with [distributed processing](doc/DISTRIBUTED_PROCESSING.md), to indicate to the driver processes that they should operate on process-specific subdivided hydrofabric files.

```bash
ngen <catchment_data_path> <catchment subset ids> <nexus_data_path> <nexus subset ids> <realization_config_path>
```

To simulate every catchment in the input hydrofabric, leave the subset lists empty, or use "all" i.e.:

```bash
ngen ./data/catchment_data.geojson "" ./data/nexus_data.geojson "" ./data/refactored_example_realization_config.json

ngen ./data/catchment_data.geojson "all" ./data/nexus_data.geojson "all" ./data/refactored_example_realization_config.json
```

## Hydrodynamic Modeling using GeoClaw Model

GeoClaw is one of the models available in [Geopack](https://github.com/clawpack/clawpack). GeoClaw is a coastal model that uses variable resolution to optimise model run times. Additional information on the GeoClaw coastal model can be found at [http://www.clawpack.org/](http://www.clawpack.org/).

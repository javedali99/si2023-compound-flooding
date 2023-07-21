<p align="center">
    <img src="https://github.com/javedali99/si2023-compound-flooding/assets/15319503/f2a06762-adfa-44e2-a9c0-67504b982e1b" alt="disaster" width="150" height="150">
  </a>
  <h1 align="center">Analyzing Contributions of Storm Drivers to Compound Flooding Using Coupled Modeling and Machine Learning Approaches</h1>
</p>

<br>

# Introduction :book:

This repository, [si2023-compound-flooding](https://github.com/javedali99/si2023-compound-flooding), is dedicated to an in-depth analysis of the contributions of various flood drivers to compound flooding in New York City (NYC). Compound flooding is a complex phenomenon involving the interplay of various factors such as storm surges, heavy rainfall, and river discharge. These factors interact in complex ways, making it difficult to isolate their individual contributions to overall flooding. Understanding and quantifying the contributions of these factors is essential for effective flood risk management, infrastructure planning, and climate change adaptation strategies.

### Background 🌍

New York City is one of the most flood-prone areas in the United States, with a coastline that stretches for over 500 miles. As a hub of economic activity and population density, it is imperative to protect the city against the adverse impacts of flooding. The city has experienced several major flooding events in the past, including Hurricane Sandy in 2012, which caused over $19 billion in damages and claimed 43 lives. The city is also vulnerable to future flooding events, with sea levels projected to rise by 11 to 30 inches by the 2050s and 18 to 60 inches by the 2080s. The city is also expected to experience more frequent and intense precipitation events in the future, which will further exacerbate the risk of flooding. In this context, understanding the drivers of compound flooding and their interactions becomes even more important. This project aims to address this need by analyzing the contributions of various flood drivers to compound flooding in NYC.

# Objectives :dart:

The primary objective of this study is to understand and quantify the contributions of various flood drivers to compound flooding in different parts of NYC under various storm and flooding scenarios. The project uses a combination of coupled modeling and machine learning approaches to quantify the contributions of various flood drivers to compound flooding in NYC. This knowledge will help in prioritizing simulation scenarios, optimizing the allocation of modeling resources, and devising more effective flood risk mitigation strategies.

# Data and Methodology :bar_chart: :hammer_and_wrench:

The methodology adopted in this research involves the coupling of hydrologic and hydrodynamic models, followed by the application of various machine learning techniques to analyze and understand the key drivers contributing to compound flooding.

## Study Area 📍

The figure below shows, (a) Study area: Manhattan, New York City, and (b) eight catchments used in the study area.

<p align="center">
    <img src="figures/Maps/study_area_nyc.png" alt="study-area-nyc" width="750">
  </a>

## Data 📊

This study uses a variety of data to perform the analysis. The data used in this study are listed below:

### Hydrologic and Hydrodynamic Data 🌊

- Hydrologic and hydrodynamic graphs based on the National Hydrologic Geospatial (Hydrofabric) data which includes catchments, nexus, and flowlines.
- Model domain parameters represented as configuration files.
  - The configuration files encompass model default parameters, formulations, input and output paths, simulation time step, initial conditions, and other relevant settings.
- Meteorological forcing data
- Storm track characteristics
- Topobathy
- Boundary Conditions
- Precipitation
- River discharge
- Storm surge

### Storms ⛈️

The analysis of storm drivers requires comprehensive historical data of storm events that have impacted NYC. This data includes information about storms, such as names, dates of landfall, dates of impact on NYC, and storm attributes. This information is critical for understanding the role of storm surges and extreme precipitation events in compound flooding.

| Storms                  | Date of Landfall | Date of Impact in NYC | Hour of Landfall | ATCF data | CFE Time Bounds  |
| ----------------------- | ---------------- | --------------------- | ---------------- | --------- | ---------------- |
| Tropical Storm Barry    | 2-Jun-2007       | 5-Jun-2007            | 02:00            | AL022007  | 31-May to 6-Jun  |
| Hurricane Hannah        | 6-Sep-2008       | 6-Sep-2008            | 07:20            | AL082008  | 4-Sep to 8-Sep   |
| Hurricane Irene         | 28-Aug-2011      | 28-Aug-2011           | 13:00            | AL092011  | 26-Aug to 30-Aug |
| Hurricane Sandy         | 29-Oct-2012      | 29-Oct-2012           | 23:30            | AL182012  | 26-Oct to 31-Oct |
| Hurricane Arthur        | 4-Jul-2014       | 4-Jul-2014            | 08:00            | AL012014  | 2-Jul to 6-Jul   |
| Tropical Storm Jose     | 19-Sep-2017      | 20-Sep-2017           | 00:00            | AL122017  | 17-Sep to 22-Sep |
| Tropical Storm Philippe | 28-Oct-2017      | 30-Oct-2017           | 22:00            | AL182017  | 26-Oct to 1-Nov  |
| Hurricane Dorian        | 6-Sep-2019       | 7-Sep-2019            | 12:30            | AL052019  | 3-Sep to 9-Sep   |
| Hurricane Ogla          | 27-Oct-2019      | 27-Oct-2019           | 03:00            | AL172019  | 24-Oct to 29-Oct |

## Coupled Modeling ⚙️

To analyze the drivers of compound flooding, we employ a coupled modeling approach that integrates hydrologic and hydrodynamic models. This allows for the simultaneous representation of different processes that contribute to flooding.

### Hydrologic Modeling using NextGen CFE Model 💧

---

The [National Water Center's Conceptual Functional Equivalent (CFE) model](https://github.com/NOAA-OWP/cfe) is a type of rainfall-runoff model. It's a conceptual model, meaning it's designed to represent complex hydrological processes using simplified, easy-to-understand concepts. The model is designed to simulate how rainfall gets converted into runoff, a key process in understanding how much water will flow into rivers and streams after a rain event. It's designed with an implementation of the Basic Model Interface, a standard set of functions and procedures designed to facilitate model coupling in integrated environmental modeling studies.

Steps:

1. Hydrofabrics: Generate hydroFabrics subsets for your area of interest.
2. CFE Forcing: Prepare basin averaged forcing for nextgen cfe model
3. Configuration: Define model parameters.
4. Model Execution: Run the CFE model.
5. Output Analysis: Analyze runoff and other hydrologic outputs for flood events.

#### Generate HydroFabrics Subsets for the 8 watersheds in New York City (NYC) area

Retrieve hydrofabric data, followed by the extraction of necessary infromation for creating the parameter configuration file. These files are created for running Conceptual Functional Equivalent (CFE) model and Simple Logical Tautology Handler (SLoTH) in the NGEN framework.

_**Watersheds:** ['wb-694856', 'wb-694725', 'wb-694855', 'wb-694724', 'wb-694854', 'wb-694723', 'wb-698891', 'wb-694722']_

#### Prepare Basin Averaged Forcing for NextGen CFE Model

Prepare basin averaged forcing input from for the NOAA Next Generation (NextGen) Water Resource Modeling Framework from AORC v1.0 kerchunk header files.

#### Run CFE Model in NGEN Framework

To run the _ngen_ engine, the following command line positional arguments are supported:

- _catchment_data_path_ -- path to catchment data geojson input file.
- _catchment subset ids_ -- list of comma separated ids (NO SPACES!!!) to subset the catchment data, i.e. 'cat-0,cat-1', an empty string or "all" will use all catchments in the hydrofabric
- _nexus_data_path_ -- path to nexus data geojson input file
- _nexus subset ids_ -- list of comma separated ids (NO SPACES!!!) to subset the nexus data, i.e. 'nex-0,nex-1', an empty string or "all" will use all nexus points
- _realization_config_path_ -- path to json configuration file for realization/formulations associated with the hydrofabric inputs
- _partition_config_path_ -- path to the partition json config file, when using the driver with [distributed processing](https://github.com/NOAA-OWP/ngen/blob/master/doc/DISTRIBUTED_PROCESSING.md).
- `--subdivided-hydrofabric` -- an explicit, optional flag, when using the driver with [distributed processing](https://github.com/NOAA-OWP/ngen/blob/master/doc/DISTRIBUTED_PROCESSING.md), to indicate to the driver processes that they should operate on process-specific subdivided hydrofabric files.

**Command to run the CFE model in NGEN framework:**

```bash
ngen config/catchments.geojson "" config/nexus.geojson "" config/realization.json ""
```

```bash
ngen <catchment_data_path> <catchment subset ids> <nexus_data_path> <nexus subset ids> <realization_config_path>
```

To simulate every catchment in the input hydrofabric, leave the subset lists empty, or use "all" i.e.:

```bash
ngen ./data/catchment_data.geojson "" ./data/nexus_data.geojson "" ./data/refactored_example_realization_config.json

ngen ./data/catchment_data.geojson "all" ./data/nexus_data.geojson "all" ./data/refactored_example_realization_config.json
```

### Results of CFE Model for Hurricane Irene

<p align="center">
    <img src="https://github.com/javedali99/si2023-compound-flooding/assets/15319503/fd879b76-8c23-4e09-a483-28a4ad25b218" width="750">
  </a>
</p>

|                      | Count | Mean  | Std Dev | Min   | 25th Percentile | Median | 75th Percentile | Max    |
| -------------------- | ----- | ----- | ------- | ----- | --------------- | ------ | --------------- | ------ |
| cat-694853-discharge | 121   | 35116 | 7759    | 13545 | 30303           | 36759  | 41286           | 45851  |
| cat-694852-discharge | 121   | 91612 | 20169   | 37608 | 78792           | 94914  | 108394          | 116500 |
| cat-694856-discharge | 121   | 14726 | 2420    | 12682 | 13323           | 13827  | 14890           | 23480  |
| cat-694725-discharge | 121   | 38087 | 1849    | 35030 | 36493           | 38032  | 39653           | 41361  |
| cat-694855-discharge | 121   | 12833 | 623     | 11803 | 12296           | 12815  | 13361           | 13936  |
| cat-694724-discharge | 121   | 5307  | 258     | 4881  | 5084            | 5299   | 5525            | 5763   |
| cat-694854-discharge | 121   | 20797 | 4108    | 12597 | 17201           | 21171  | 24727           | 26278  |
| cat-694723-discharge | 121   | 5535  | 269     | 5091  | 5304            | 5527   | 5763            | 6011   |
| cat-694722-discharge | 121   | 4426  | 215     | 4071  | 4241            | 4419   | 4608            | 4806   |

All values are rounded to the nearest whole number. The columns represent the following statistics:

- **Count**: The number of hourly discharge measurements for each catchment.
- **Mean**: The average discharge over the given time period.
- **Std Dev**: The standard deviation of the discharge, a measure of the variation or dispersion of the values.
- **Min**: The minimum discharge observed.
- **25th Percentile**: 25% of the discharge values were below this value (also known as the first quartile).
- **Median**: The middle value when the discharge values are arranged in ascending order (also known as the second quartile or the 50th percentile).
- **75th Percentile**: 75% of the discharge values were below this value (also known as the third quartile).
- **Max**: The maximum discharge observed.

### Hydrodynamic Modeling using GeoClaw Model 🌊

---

The [GeoClaw model](https://www.clawpack.org/geoclaw.html) specializes in modeling geophysical flows like storm surges and tsunamis. It’s particularly effective at capturing the dynamics of storm surges, which is critical for understanding compound flooding in coastal areas. GeoClaw is one of the models available in [Geopack](https://github.com/clawpack/clawpack). GeoClaw is a coastal model that uses variable resolution to optimise model run times.

This study aims to use GeoClaw to model flood drivers’ influence in New York City. The model solves the three equations of the two-dimensional nonlinear shallow water equations using high-resolution finite-volume methods. There are a total of seven auxiliary variables initialized in the set run script of the model; three are related to the shallow water equations, one to friction, and the remaining three to storm fields. A large computational domain in Geoclaw was defined using longitude and latitude coordinates. The model had a spatial coverage of - 88° to -55° W and 15° to 45° N. Geophysical parameters specified for the simulation included gravity, coordinate system, Earth radius, the density of water and air, ambient pressure, Coriolis forcing, friction forcing, friction depth, sea level, and dry tolerance. Also, gauge locations for monitoring specific points in the domain during the simulation are defined. The degree factor was set to 4, which is used to calculate the number of grid cells in each dimension. First, the time of the model simulation was converted from days to seconds. For the validation of Hurricane Sandy, the initial time was set to start three days before landfall. We set up a checkpoint file for the model in case of a restart. The output style was set to 1, indicating that output frames should be written at equally spaced time steps up to the final time. The number of output times was calculated based on the difference between the final and initial time, the recurrence, and the number of days. The initial time step was 0.010 days.

The time steps are based on the desired Courant–Friedrichs–Lewy (CFL) number. The model can also allow for very large time steps that are controlled by the CFL desired (0.75) and maximum number (1.0) function initialized in the set run script. The order accuracy was set to 2, which follows the Lax-Wendroff Flux limiter method. The dimension was left as unsplit as this is the only option currently allowed for AMRClaw. The transverse waves are also set to 2, which enables corner transport of second-order corrections. The number of waves was set to 3, indicating the number of waves in the Riemann solution. The Monotonized Central (MC) limiter was used for each wave family. The source split function was set up to advance the solution by solving the source term equations. Godunov (1st order) splitting was used, which is more accurate and can properly set ghost cells for boundary conditions, unlike Strang (2nd order) splitting. For the boundary conditions, we chose to extrapolate the values from the interior cells to the ghost cells.
Adaptive mesh refinement (AMR) parameters were used, and the maximum number of refinement levels was set to 8. The refinement ratios are set between successive levels in the x, and y directions, and time, respectively. Regions of refinement for the simulation were defined. Each region was specified by a list containing the minimum level, maximum level, start time, end time, lower x-coordinate, upper x-coordinate, lower y-coordinate, and upper y-coordinate. Also, the gauge locations for monitoring specific points in the domain during the simulation are defined. Each gauge is specified by a list containing the gauge number, longitude, latitude, start time, and end time. The gauges are appended to have a list of the gauges. The scratch directory in the $CLAW in-built folder is where the topography and storm files are stored and where they were accessed during the model run. The files are converted from ATCF to GeoClaw format during the model run. The model ran in Python but some of its scripts are written in Fortran.

#### Incorporating river discharge

The subroutine “src2” script, written in Fortran, was used to integrate the river discharge into the model. It is defined with several parameters specifying the number of equations, the size of the 2D grid on the x and y dimensions respectively, the number of boundary cells, the auxiliary variables, the current time, and the time step relative to the simulation. There are arrays that contain the water levels and velocities at each grid cell for each time step and auxiliary data needed for the computations. The subroutine then imports several modules, including GeoClaw and storm modules, which provide functionalities related to geophysical computations and storm simulations respectively. Constants and functions from these modules are used in the code. Several local variables are then defined to assist with computations inside the subroutine. The river source conditions simulating a river's discharge into the system being modeled are defined. It sets certain geographical bounds for the river source, computes the river's discharge in cubic meters per second, and adds this to the q array (which represents the water level at each grid cell) for cells that fall within the river source area. Tidal forcing can be incorporated as a source term based on the desired eta and can be handled based on a list of tide times and associated tide heights. Eta is computed based on the sine function, representing some oscillatory behavior, like tides in an ocean. Also, multiple rivers’ conditions, each with its own geographical bounds and discharge rate can be incorporated.

Steps:

1. Configuration: Set up model parameters in the setrun script.

   Setting up intial and final time -- 2 days before and 3 days after

   ```bash
    clawdata.t0 =  days2seconds(-2)
    clawdata.tfinal = days2seconds(3)
   ```

   Setting up time steps -- every 0.016 days

   ```bash
    clawdata.dt_initial = 0.016
   ```

   Setting up the landfall -- (yyyy, mm, dd, hh, mm)

   ```bash
   maria.time_offset = datetime.datetime(2017, 9, 20, 10, 15)
   ```

2. Storm and topo-bathy Data: Input storm track data and meteorological forcing.

   Data was retrieved from the National Oceanic and Atmospheric Administration archive (https://ftp.nhc.noaa.gov/)

3. Model Execution: Run the GeoClaw model.

   To generate model simulation for storm surge and water depth.

   ```bash
   make .output
   ```

   To generate plots that make a comparison between actual and model data.

   ```bash
   make .plots
   ```

4. Output Analysis: Analyze storm surge levels at each station and observation points while also incorporating bias correction.

## Machine Learning Approaches 🤖

Various machine learning models are employed to analyze the data obtained from the coupled modeling to understand and quantify the contributions of various flood drivers to compound flooding under various storm and flooding scenarios in NYC. These algorithms are selected for their ability to handle high-dimensionality, capture non-linear relationships, and model temporal sequences.

- **Random Forest (RF)**: A versatile and powerful algorithm, RF is employed to handle the nonlinear relationships between the flood drivers and the resulting flooding. By offering feature importance scores, RF helps to identify the most influential drivers, quantifying their individual contributions.

- **Support Vector Regression (SVR)**: SVR is an implementation of Support Vector Machine (SVM) for regression problems. It is designed to find the best fit line in a high or infinite dimensional space, which is defined by a set of predictors. In this study, we use SVR to predict the flood levels in different scenarios based on the corresponding drivers. This helps us to understand the effects of the flood drivers on the severity of compound flooding.

- **Multi-Layer Perceptron (MLP)**: MLP, a type of artificial neural network, is effective in capturing complex patterns in the dataset and modeling non-linear relationships. By employing MLP, we can model the intricate interactions between various flood drivers and their collective impact on compound flooding.

- **Long Short-Term Memory (LSTM)**: LSTM networks are a subtype of recurrent neural networks designed to learn patterns in time-series data. This makes them particularly suited for our study, where we are interested in understanding the temporal aspects of flood events, including the progression and interaction of various flood drivers over time.

<!---
- **Principal Component Analysis (PCA)**: PCA reduces the dimensionality of the dataset by transforming it into a set of orthogonal components that capture the most variance. By using PCA, we can simplify the complex multidimensional relationships between flood drivers, making it easier to visualize and understand the key drivers.
--->

Each of these machine learning methods contributes to a more comprehensive understanding of the dynamics of compound flooding in NYC, thereby helping to achieve our study's main objective.

# Contributing :handshake:

Contributions are welcome and highly appreciated. You can contribute by:

- Reporting Bugs
- Suggesting Enhancements
- Sending Pull Requests

# License :page_with_curl:

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

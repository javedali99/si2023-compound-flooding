from __future__ import print_function
from __future__ import absolute_import
from six.moves import range

import warnings
import sys
import os
import argparse
import datetime

# Added a few packages 
import numpy
import netCDF4

import clawpack.geoclaw.units as units
from clawpack.geoclaw.surge.storm import Storm 
import clawpack.clawutil.data


def load_emanuel_storms(path, mask_distance=None, mask_coordinate=(0.0, 0.0),
                               mask_category=None, categorization="NHC"):
    r"""Load storms from a Matlab file containing storms

    This format is based on the format Prof. Emmanuel uses to generate storms.

    :Input:
     - *path* (string) Path to the file to be read in
     - *mask_distance* (float) Distance from *mask_coordinate* at which a storm
       needs to in order to be returned in the list of storms.  If
       *mask_distance* is *None* then no masking is used.  Default is to
       use no *mask_distance*.
     - *mask_coordinate* (tuple) Longitude and latitude coordinates to measure
       the distance from.  Default is *(0.0, 0.0)*.
     - *mask_category* (int) Category or highter a storm needs to be to be
       included in the returned list of storms.  If *mask_category* is *None*
       then no masking occurs.  The categorization used is controlled by
       *categorization*.  Default is to use no *mask_category*.
     - *categorization* (string) Categorization to be used for the
       *mask_category* filter.  Default is "NHC".

    :Output:
     - (list) List of Storm objects that have been read in and were not
       filtered out.
    """


    # Load the mat file and extract pertinent data
    import scipy.io
    mat = scipy.io.loadmat(path)

    lon = mat['longstore']
    lat = mat['latstore']
    hour = mat['hourstore']
    day = mat['daystore']
    month = mat['monthstore']
    year = mat['yearstore']
    max_wind_radius = mat['rmstore']
    max_wind_speed = mat['vstore']
    central_pressure = mat['pstore']

    # Convert into storms and truncate zeros
    storms = []
    for n in range(lon.shape[0]):
        m = len(lon[n].nonzero()[0])


        storm = Storm()
        storm.ID = n 
        
        storm.t = [datetime.datetime(int(year[0, n]),
                                     int(month[n, i]),
                                     int(day[n, i]),
                                     int(hour[n, i])) for i in range(m)]

        storm.time_offset = storm.t[0]

        storm.eye_location = numpy.empty((m, 2))
        storm.max_wind_speed = numpy.empty(m)
        storm.max_wind_radius = numpy.empty(m)
        storm.central_pressure = numpy.empty(m)

        storm.eye_location[:, 0] = lon[n, :m]-360
        storm.eye_location[:, 1] = lat[n, :m]
        storm.max_wind_speed = max_wind_speed[n, :m]
        storm.max_wind_speed = units.convert(max_wind_speed[n, :m], 'knots',
'm/s') 
        storm.max_wind_radius = units.convert(max_wind_radius[n, :m], 'km', 'm')
        storm.central_pressure = units.convert(central_pressure[n, :m], 'hPa',
'Pa')
        storm.storm_radius = numpy.ones(m) * 300e3

        include_storm = True
        if mask_distance is not None:
            distance = numpy.sqrt((storm.eye_location[:, 0] - \
                         mask_coordinate[0])**2 + (storm.eye_location[:, 1] - \
                         mask_coordinate[1])**2)
            inlcude_storm = numpy.any(distance < mask_distance)
        if mask_category is not None:
            category = storm.category(categorization=categorization)
            include_storm = numpy.any(category > mask_category)

        if include_storm:
            storms.append(storm)
    print(storms[0])
    #print("Length of storms:", len(storms))
    storms_write_to_file(storms)
    #print(storms[0].max_wind_speed)
    return storms


def storms_write_to_file(storms):
    for s in storms:
     s.write(str(s.ID + 1)+'.dat', file_format="geoclaw")
        #myFile = open(str(s.ID)+'.dat', 'w')
        #myFile.write(str(s.ID))
        #myFile.write('\n')
        #myFile.write(str(s.t[0]))
        #myFile.write('\n')
        #for theIndex in range(len(s.t)):
        #    myFile.write(str(0)); myFile.write('\t');
        #    myFile.write(str(s.eye_location[theIndex,0] - 360)); myFile.write('\t'); 
        #    myFile.write(str(s.eye_location[theIndex,1])); myFile.write('\t');
        #   myFile.write(str(s.max_wind_speed[theIndex])); myFile.write('\t');     
        #   myFile.write(str(s.max_wind_radius[theIndex])); myFile.write('\t');
        #   myFile.write(str(s.central_pressure[theIndex])); myFile.write('\t');
        #   myFile.write(str(s.storm_radius[theIndex])); myFile.write('\t');
        #   myFile.write('\n') 
## Ensmeble Storm Formats
def load_chaz_storms(path, mask_distance=None, mask_coordinate=(0.0, 0.0),
                              mask_category=None, categorization="NHC"):
   r"""Load storms from a Matlab file containing storms

   This format is based on the format Prof. Emmanuel uses to generate storms.

   :Input:
    - *path* (string) Path to the file to be read in
    - *mask_distance* (float) Distance from *mask_coordinate* at which a storm
      needs to in order to be returned in the list of storms.  If
      *mask_distance* is *None* then no masking is used.  Default is to
      use no *mask_distance*.
    - *mask_coordinate* (tuple) Longitude and latitude coordinates to measure
      the distance from.  Default is *(0.0, 0.0)*.
    - *mask_category* (int) Category or highter a storm needs to be to be
      included in the returned list of storms.  If *mask_category* is *None*
      then no masking occurs.  The categorization used is controlled by
      *categorization*.  Default is to use no *mask_category*.
    - *categorization* (string) Categorization to be used for the
      *mask_category* filter.  Default is "NHC".

   :Output:
    - (list) List of Storm objects that have been read in and were not
      filtered out.
   """


   # Load the mat file and extract pertinent data
   data = netCDF4.Dataset(path)
   storms = []

   time_length = data['Mwspd'].shape[0]
   num_tracks = data['Mwspd'].shape[1]
   num_intensities = data['Mwspd'].shape[2]


   count = 0 

   for i in range(num_tracks):

       # Extract initial data ranges
       for n in range(num_intensities):

           # Use intensity to find non-nans and extract correct arrays
           max_wind_speed = numpy.array(data.variables['Mwspd'][:, i, n])
           index_set = (numpy.isnan(max_wind_speed) - 1).nonzero()[0]

           index = len(index_set)
           t = numpy.array(data.variables['time'][0:index, i])
           x = numpy.array(data.variables['longitude'][0:index, i])
           y = numpy.array(data.variables['latitude'][0:index, i])


           # Filter out nan values
           index_x = (numpy.isnan(x) - 1).nonzero()[0]
           index_y = (numpy.isnan(y) - 1).nonzero()[0]
           
           indicies = [index_x, index_y, index_set]
           index_set = min(indicies, key=len)

           x = x[index_set]
           y = y[index_set]
           t = t[index_set]
           max_wind_speed = max_wind_speed[index_set]
       
            
           # Remove zero-length intensities
           if len(index_set) > 0:
               # Create storm object
               storm = clawpack.geoclaw.surge.storm.Storm()
               storm.ID = i * num_intensities + n

               # Initialize the date set

               storm.t = [datetime.datetime(2012, 10, 30, 0) + \
                          datetime.timedelta(hours=6) * i
                          for i in range(len(index_set))]
  
               storm.eye_location = numpy.empty((len(index_set), 2))
               x = x - 360.0 * numpy.ones(len(index_set))
               
               storm.eye_location[:, 0] = x
               storm.eye_location[:, 1] = y
               
               # Get the storm within the domain for the first time step
           
               # The domain of the run in a list
               # x = [lower bound, upper bound] 
               # x is long
               # y is lat
               
                
               # Radius of the earth in km  
               R = 6373.0

               # Domain of storm 
               x_domain = numpy.abs([-55, -88])
               y_domain = numpy.abs([15, 45]) 
                                
               # Default time offset
               storm.time_offset = (storm.t[0], 0)  

               # Start the storm in a domain contained 
               # within the given boundaries. 
               # This domain is 5 degrees from either boundary 
               # of the latitude
               #and of the longitude. For example if the boundaries specified that
               #the domain of the entire storm was [-50, -95] for the latitude
               #and [10, 45] for the longitude then the actual domain in which we 
               #START the storm running would be [-55, -90] for lat and [15, 40] for long
               # than the boundaries. We find the region for this. 
               # Note here 5 degrees is roughly 550 km. Thus the center of the
               # storm is 550 km away from either boundary.
               for b in range(0, len(x)): 
                   if numpy.abs(x[b]) >= (x_domain[0]) and numpy.abs(x[b]) <= (x_domain[1]): 
                       if numpy.abs(y[b]) >= (y_domain[0]) and numpy.abs(y[b]) <= (y_domain[1]): 
                           #storm.time_offset = (storm.t[b],b)
                           storm.time_offset = storm.t[b]
                           break 

               # TODO: Convert from knots
               storm.max_wind_speed = numpy.array(max_wind_speed)


               # Calculate Radius of Max Wind
               C0 = 218.3784 * numpy.ones(len(index_set))
               storm.max_wind_radius = C0 - 1.2014 * storm.max_wind_speed + \
                                       (storm.max_wind_speed / 10.9884)**2 - \
                                       (storm.max_wind_speed / 35.3052)**3 - \
                                       145.5090 * \
                                       numpy.cos(storm.eye_location[:, 1] * 0.0174533)


               # From Kossin, J. P. WAF 2015
               a = -0.0025
               b = -0.36
               c = 1021.36
               storm.central_pressure = (  a * storm.max_wind_speed**2
                                         + b * storm.max_wind_speed
                                         + c)

               # Extent of storm set to 300 km                 
               storm.storm_radius = 500 * numpy.ones(len(index_set))
               storm.storm_radius = units.convert(storm.storm_radius, 
                                                           'km', 'm')
               storm.max_wind_radius = units.convert(storm.max_wind_radius, 'nmi', 'm')
               storm.max_wind_speed = units.convert(storm.max_wind_speed,
                                                    'knots', 'm/s')
               
               storm.central_pressure = units.convert(storm.central_pressure, 'hPa','Pa')
               #print(storm.central_pressure) 

               include_storm = True
               include_storm_md = True
               include_storm_mc = True 
               if mask_distance is not None:
                   distance = numpy.sqrt((storm.eye_location[:, 0] -
                                          mask_coordinate[0])**2 +
                                         (storm.eye_location[:, 1] -
                                          mask_coordinate[1])**2)
                   include_storm_md = numpy.any(distance <= mask_distance)

               if mask_category is not None:
                   category = storm.category(categorization=categorization)
                   include_storm_mc = numpy.any(category > mask_category)

               if include_storm_md and include_storm_mc:
                   storms.append(storm) 
   
   return storms
#
load_emanuel_storms("/home/asarhadi/scratch/NYC_1_AL_cesm2_20thcal/Ali_NYC_1_AL_cesm2_20thcal.mat")
#

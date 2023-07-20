
from __future__ import absolute_import
from __future__ import print_function

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

import clawpack.visclaw.colormaps as colormap
import clawpack.visclaw.gaugetools as gaugetools
import clawpack.clawutil.data as clawutil
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata
import clawpack.geoclaw.surge.plot as surgeplot
import csv
from clawpack.geoclaw.util import fetch_noaa_tide_data
from datetime import datetime, timedelta

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

df_storm = pd.read_csv(r'/opt/src/clawpack_src/clawpack-v5-9-0/geoclaw/scratch/1006.storm', delimiter='     ', skiprows=3, header = None)
df_landfall = pd.read_csv(r'/opt/src/clawpack_src/clawpack-v5-9-0/geoclaw/scratch/1006.storm' ,nrows = 2, header = None)
landfall = df_landfall.iloc[1,0]
landfall_time2 = pd.to_datetime(landfall)
landfall_index = int(df_landfall.iloc[0,0])-3

#df_storm.iloc[landfall_index,0]/(3600*24)
t_final = df_storm.iloc[-1,0]/(3600*24)
t_after = t_final-df_storm.iloc[landfall_index,0]/(3600*24)
start_time = landfall_time2 - timedelta(days=df_storm.iloc[landfall_index,0]/(3600*24))
end_time = landfall_time2 + timedelta(days=t_after)  
    
    
def setplot(plotdata=None):
    """"""

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    # clear any old figures,axes,items data
    plotdata.clearfigures()
    plotdata.format = 'ascii'

    # Load data from output
    clawdata = clawutil.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir, 'claw.data'))
    physics = geodata.GeoClawData()
    physics.read(os.path.join(plotdata.outdir, 'geoclaw.data'))
    surge_data = geodata.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir, 'surge.data'))
    friction_data = geodata.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir, 'friction.data'))

    # Load storm track
    track = surgeplot.track_data(os.path.join(plotdata.outdir, 'fort.track'))

    # Set afteraxes function
    def surge_afteraxes(cd):
        surgeplot.surge_afteraxes(cd, track, plot_direction=True,
                                             kwargs={"markersize": 4})
    def plot_coastline(cd):
        """Load fine coastline for plotting around NYC"""
        try:
            # Assumes that at path theres a fine topography file in NetCDF file format
            path = "/Users/mandli/Dropbox/research/data/topography/atlantic/sandy_bathy/ny_area.nc"
            topo_file = topotools.Topography(path, topo_type=4)
            topo_file.read(nc_params={"x_var":"lon", 
                                      "y_var":"lat", 
                                      "z_var": "Band1"})

            axes = plt.gca()
            axes.contour(topo_file.X, topo_file.Y, topo_file.Z, 
                         levels=[-0.001, 0.001], 
                         colors='k', linestyles='-')
        except:
            pass

        surge_afteraxes(cd)

    # Color limits
    surface_limits = [-5.0, 5.0]
    speed_limits = [0.0, 3.0]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    friction_bounds = [0.01, 0.04]

    def friction_after_axes(cd):
        plt.title(r"Manning's $n$ Coefficient")

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    regions = {'Full Domain': {"xlimits": [clawdata.lower[0], clawdata.upper[0]],
                               "ylimits": [clawdata.lower[1], clawdata.upper[1]],
                               "shrink": 1.0,
                               "figsize": [6.4, 4.8]},
               'Tri-State Region': {"xlimits": [-74.5,-71.0],
                                    "ylimits": [40.0,41.5],
                                    "shrink": 1.0,
                                    "figsize": [6.4, 4.8]},
                'NYC': {"xlimits": [-74.2,-73.7],
                        "ylimits": [40.4,40.85],
                        "shrink": 1.0,
                        "figsize": [6.4, 4.8]}
               }
    for (name, region_dict) in regions.items():

        # Surface Figure
        plotfigure = plotdata.new_plotfigure(name="Surface - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Surface"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = plot_coastline
        # plotaxes.afteraxes = surge_afteraxes

        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
        surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

        # Speed Figure
        plotfigure = plotdata.new_plotfigure(name="Currents - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Currents"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = plot_coastline
        # plotaxes.afteraxes = surge_afteraxes

        surgeplot.add_speed(plotaxes, bounds=speed_limits)
        surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10
    #
    # Friction field
    #
    plotfigure = plotdata.new_plotfigure(name='Friction')
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Manning's N Coefficient"
    plotaxes.afteraxes = friction_after_axes
    plotaxes.scaled = True

    surgeplot.add_friction(plotaxes, bounds=friction_bounds, shrink=0.9)
    plotaxes.plotitem_dict['friction'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['friction'].colorbar_label = "$n$"

    #
    #  Hurricane Forcing fields
    #
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure')
    plotfigure.show = surge_data.pressure_forcing and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_pressure(plotaxes, bounds=pressure_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_wind(plotaxes, bounds=wind_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Gauge Surfaces', figno=300,
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True
    
    stations = [ ('Gauge 1'), ('Gauge 2'), ('Gauge 3'),
            ('Gauge 4'), ('Gauge 5'), ('Gauge 6'),
            ('Gauge 7'), ('Gauge 8'), ('Gauge 9'),
            ('Gauge 10'), ('Gauge 11'), ('Gauge 12'),
            ('Gauge 13'), ('Gauge 14'), ('Gauge 15'),
            ('Gauge 16'), ('Gauge 17'), ('Gauge 18'),
            ('Gauge 19'), ('Gauge 20'), ('Gauge 21'),  
            ('Gauge 22'), ('Gauge 23')]

    # landfall_time = datetime.datetime(2012, 10, 29, 23, 30)
    
    landfall_time = np.datetime64(landfall)
    begin_date = start_time
    end_date = end_time
    
    

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [0,5]
    # plotaxes.xlabel = "Days from landfall"
    # plotaxes.ylabel = "Surface (m)"
    plotaxes.ylimits = [-1, 5]
    plotaxes.title = 'Surface'

    def gauge_afteraxes(cd):

        axes = plt.gca()
        surgeplot.plot_landfall_gauge(cd.gaugesoln, axes)

        # Fix up plot - in particular fix time labels
        axes.set_title('Station %s' % cd.gaugeno)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim([0,5])
        axes.set_ylim([-1, 5])
        axes.set_xticks([0,1,2,3,4,5])
        #axes.set_xticklabels([r"$-2$", r"$-1$", r"$0$", r"$1$"])
        axes.grid(True)
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 3
    # plotitem.plotstyle = 'b-'

    #
    #  Gauge Location Plot
    #
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos='all',
                                        format_string='ko', add_labels=True)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations'
    plotaxes.scaled = True
    plotaxes.xlimits = [-74.5, -71.6]
    plotaxes.ylimits = [40.5, 41.5]
    plotaxes.afteraxes = gauge_location_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10



    

    



    # -----------------------------------------
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'   # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # parallel plotting

    return plotdata
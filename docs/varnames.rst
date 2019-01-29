Variable naming for different versions of GLDAS NOAH
====================================================
 
For GLDAS Noah 1.0 parameters are called using their PDS IDs from the table below.
A full list of PDS IDs can be found in the `GLDAS 1.0 README <https://hydro1.gesdisc.eosdis.nasa.gov/data/GLDAS_V1/README.GLDAS.pdf>`_
        
For GLDAS Noah 2.0 and GLDAS Noah 2.1 parameters are called using Variable Names from the table below.
A full list of variable names can be found in the `GLDAS 2.x README <https://hydro1.gesdisc.eosdis.nasa.gov/data/GLDAS/README_GLDAS2.pdf>`_

+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| Short name  | Long variable name    | Parameter                        | Resolution | Depth/Height Interval [m] | Units      |
+=============+=======================+==================================+============+===========================+============+
| SFMC        | water_surface_layer                   | Soil moisture                    | 0.5°x0.625°| 0.00 - 0.05               | [m-3 m-3]  |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| RZMC        | water_root_zone                       | Soil moisture                    | 0.5°x0.625°| 0.10 - 1.00               | [m-3 m-3]  |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| GWETTOP     | surface_soil_wetness                  | Soil moisture                    | 0.5°x0.625°| 0.00 - 0.05               | [%]        |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| GWETROOT    | root_zone_soil_wetness                | Soil moisture                    | 0.5°x0.625°| 0.10 - 1.00               | [%]        |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| GWETPROF    | ave_prof_soil_moisture                | Soil moisture                    | 0.5°x0.625°| 1.34 - 8.53               | [%]        |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| PRECTOTLAND | Total_precipitation_land              | Rain precipitation rate        | 0.5°x0.625°| 0                         | [kg m-2 s-1]|
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| PRECSNOLAND | snowfall_land                         | Snow precipitation rate          | 0.5°x0.625°| 0                         | [kg m-2 s-1]|
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| SNOMAS      | Total_snow_storage_land               | Total snow storage land               | 0.5°x0.625°| 0                         | [kg m-2]   |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSOIL1      | soil_temperatures_layer_1             | Soil temperatures layer 1 | 0.5°x0.625°| X                         | [kg/m^2]   |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSOIL2      | soil_temperatures_layer_2             | Soil temperatures layer 2 | 0.5°x0.625°| X                         | [K]        |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSOIL3      | soil_temperatures_layer_3             | Soil temperatures layer 3 | 0.5°x0.625°| X                         | [kg/m^2/s] |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSOIL4      | soil_temperatures_layer_4             | Soil temperatures layer 4 | 0.5°x0.625°| X                         | [kg/m^2/s] |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSOIL5      | soil_temperatures_layer_5             | Soil temperatures layer 5 | 0.5°x0.625°| X                         | [kg/m^2/s] |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSOIL6      | soil_temperatures_layer_6             | Soil temperatures layer 6 | 0.5°x0.625°| X                         | [kg/m^2/s] |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+
| TSURF       | surface_temperature_of_land_incl_snow | Surface temperature  | 0.5°x0.625°| X                         | [kg/m^2/s] |
+-------------+-----------------------+----------------------------------+------------+---------------------------+------------+


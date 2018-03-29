#!/usr/bin/env python
 
import placentagen as pg
import numpy as np
 
#Number of seed points targeted for growing tree
n_seed=32000
#Number of chorionic seed points targeted
n_chorion=32
#volume of placenta
volume=427.0*1000 #mm^3
#thickness of placenta (z-axis dimension)
thickness=24.8 #mm
#ellipticity of placenta - ratio of y to x axis dimensions
ellipticity=1.00 #no units
#x and y coordinates of cord insertion point
cord_insertion_x=0.0
cord_insertion_y=0.0
#distance between the two umbilical arteries
umb_artery_distance=20.0 #mm
umb_artery_length=20.0
 
 
angle_max =  90 * np.pi /180
angle_min = 5 * np.pi /180
fraction_chorion =   0.5
min_length =  5.0 #mm
point_limit =  1
 
sv_length = 2.0
 
 
#datapoints_villi=pg.equispaced_data_in_ellipsoid(n_seed,volume,thickness,ellipticity)
 
datapoints_chorion=pg.uniform_data_on_ellipsoid(n_chorion,volume,thickness,ellipticity,0)
pg.export_ex_coords(datapoints_chorion,'chorion','chorion_data','exdata')
 
seed_geom=pg.umbilical_seed_geometry(volume,thickness,ellipticity,cord_insertion_x,cord_insertion_y,umb_artery_distance,umb_artery_length,datapoints_chorion)
pg.export_ex_coords(seed_geom['umb_nodes'],'umb','umb_nodes','exnode')
pg.export_exelem_1d(seed_geom['umb_elems'],'umb','umb_elems')
 
chorion_geom=pg.grow_chorionic_surface(angle_max, angle_min, fraction_chorion, min_length, point_limit,volume, thickness, ellipticity, datapoints_chorion, seed_geom,'surface')
 
 
pg.export_ex_coords(chorion_geom['nodes'],'chorion','chorion_nodes','exnode')
pg.export_exelem_1d(chorion_geom['elems'],'chorion','chorion_elems')

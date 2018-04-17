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

angle_max_ft =  180 * np.pi /180
angle_min_ft = 0 * np.pi /180
fraction_ft =   0.4
min_length_ft =  0.0 #mm
point_limit_ft =  1
 

datapoints_chorion=pg.uniform_data_on_ellipsoid(n_chorion,volume,thickness,ellipticity,0)
pg.export_ex_coords(datapoints_chorion,'chorion','chorion_data','exdata')
 
seed_geom=pg.umbilical_seed_geometry(volume,thickness,ellipticity,cord_insertion_x,cord_insertion_y,umb_artery_distance,umb_artery_length,datapoints_chorion)
pg.export_ex_coords(seed_geom['umb_nodes'],'umb','umb_nodes','exnode')
pg.export_exelem_1d(seed_geom['umb_elems'],'umb','umb_elems')
 
chorion_geom=pg.grow_chorionic_surface(angle_max, angle_min, fraction_chorion, min_length, point_limit,volume, thickness, ellipticity, datapoints_chorion, seed_geom,'surface')
 
 
pg.export_ex_coords(chorion_geom['nodes'],'chorion','chorion_nodes','exnode')
pg.export_exelem_1d(chorion_geom['elems'],'chorion','chorion_elems')

#Refine once from defined element number 
from_elem=5
refined_geom=pg.refine_1D(chorion_geom,from_elem)

pg.export_ex_coords(refined_geom['nodes'],'chorion','chorion_refined','exnode')
pg.export_exelem_1d(refined_geom['elems'],'chorion','chorion_refined')

#Add stem villi
chorion_and_stem = pg.add_stem_villi(refined_geom,from_elem,sv_length)

pg.export_ex_coords(chorion_and_stem['nodes'],'chorion','chorion_plus_stem','exnode')
pg.export_exelem_1d(chorion_and_stem['elems'],'chorion','chorion_plus_stem')

datapoints_villi=pg.equispaced_data_in_ellipsoid(n_seed,volume,thickness,ellipticity)
pg.export_ex_coords(datapoints_villi,'villous','villous_data','exdata')


full_geom=pg.grow_large_tree(angle_max_ft, angle_min_ft, fraction_ft, min_length_ft, point_limit_ft,volume, thickness, ellipticity, datapoints_villi, chorion_and_stem)


pg.export_ex_coords(full_geom['nodes'],'placenta','full_tree','exnode')
pg.export_exelem_1d(full_geom['elems'],'placenta','full_tree')



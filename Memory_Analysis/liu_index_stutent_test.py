import matplotlib.pyplot as plt
from scipy.stats import stats
import math
import numpy as np
import sys
print '~!!This is made by Steven Slaughter!!~'
list = sys.argv[1]

def distribution_method(coordinate_x, coordinate_y, center_x, center_y):
    point_count=0# count point that in position 3 and 9 in the paper
    for i in range(len(coordinate_x)):
        if coordinate_y[i] <= center_y:
           if coordinate_x[i] != center_x and coordinate_y[i] != center_y:
              vector_x = coordinate_x[i] - center_x
              vector_y = coordinate_y[i] - center_y
              dot_product = vector_x*1
              length_vector = math.sqrt(vector_x**2+vector_y**2)
              angle = math.degrees(math.acos(dot_product/length_vector))
              if 0 <= angle <= 15:
                 point_count = point_count+1
              elif 165 < angle <= 180:
           	     point_count = point_count+1
        elif coordinate_y[i] > center_y:
            if coordinate_x[i] != center_x and coordinate_y[i] != center_y:
              vector_x = coordinate_x[i] - center_x
              vector_y = coordinate_y[i] - center_y
              dot_product = vector_x*1
              length_vector = math.sqrt(vector_x**2+vector_y**2)
              angle = math.degrees(math.acos(dot_product/length_vector))
              if 0 <= angle <= 15:
                 point_count = point_count+1
              elif 165 < angle <= 180:
           	     point_count = point_count+1
    fixation_index = point_count/float(len(coordinate_x))
    return fixation_index

#-------------------read list--------------------------
id=[]
data3 = open(list,'rU')
for i in data3:
    name = map(int,i.strip().split())
    id.append(name)
#print len(id)
fixation_index_phase1=[]
fixation_index_phase2=[]
fixation_index_phase3=[]
for i in range(len(id)):
    number = id[i][0]

#-------------------read data--------------------------
    #coordinate data input
    data1 = open("%d.tsv"%(number),'rU')
    prevx=None
    prevy=None
    presit=None
    pre_time=None
    coordinate_x_phase1=[]
    coordinate_y_phase1=[]
    coordinate_x_phase2=[]
    coordinate_y_phase2=[]
    coordinate_x_phase3=[]
    coordinate_y_phase3=[]
    for line in data1:
        index,t,x_pos,y_pos,inter,sit = map(float,line.strip().split())    
        if sit==0:
           coordinate_x_phase1.append(x_pos)
           coordinate_y_phase1.append(y_pos)
        elif sit==1:
           coordinate_x_phase2.append(x_pos)
           coordinate_y_phase2.append(y_pos)
        elif sit==2:
           coordinate_x_phase3.append(x_pos)
           coordinate_y_phase3.append(y_pos)
    #arena data input
    data2 = open("%d.cfg"%(number),'rU')
    diameter,center_x,center_y,radius,lstripex,lstripey,rstripex,rstripey = [int(l.split('=')[1]) for l in data2 if len(l.split('='))>1]

#------------------Calculate over all fixation index-----------------
    fixation_index_phase1.append(distribution_method(coordinate_x_phase1,coordinate_y_phase1,center_x,center_y))
    fixation_index_phase2.append(distribution_method(coordinate_x_phase2,coordinate_y_phase2,center_x,center_y))
    fixation_index_phase3.append(distribution_method(coordinate_x_phase3,coordinate_y_phase3,center_x,center_y))

#------------------Student T test-----------------
t_static1,p_value1 = stats.ttest_rel(fixation_index_phase1,fixation_index_phase2)
t_static2,p_value2 = stats.ttest_rel(fixation_index_phase1,fixation_index_phase3)
print "p-value of phase 1 & 2 is %s" % p_value1
print "p-value of phase 1 & 3 is %s" % p_value2







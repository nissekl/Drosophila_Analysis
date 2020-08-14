import matplotlib.pyplot as plt
from scipy.stats import stats
import math
import numpy as np
import sys
print '~!!This is made by Steven Slaughter!!~'
list = sys.argv[1]

def bar_position_rotation(radius,center_x,center_y,degree):
    newl_x = center_x - math.cos(math.radians(degree))*radius
    newl_y = center_y + math.sin(math.radians(degree))*radius
    newr_x = center_x + math.cos(math.radians(degree))*radius
    newr_y = center_y - math.sin(math.radians(degree))*radius
    return newl_x,newl_y,newr_x ,newr_y


def angle_calculation(position_x,position_y,left_bar_x,left_bar_y,right_bar_x,right_bar_y):
    angle=[]
    for i in range(len(position_x)-1):
    	if math.sqrt((position_x[i+1]-position_x[i])**2 + (position_y[i+1]-position_y[i])**2)!=0:
           vector_p2p_x = position_x[i+1]-position_x[i]
           vector_p2p_y = position_y[i+1]-position_y[i]
           vector_p2l_x = left_bar_x-position_x[i]
           vector_p2l_y = left_bar_y-position_y[i]
           vector_p2r_x = right_bar_x-position_x[i]
           vector_p2r_y = right_bar_y-position_y[i]
           dot_p2p_and_p2l = (vector_p2p_x*vector_p2l_x) + (vector_p2p_y*vector_p2l_y)
           dot_p2p_and_p2r = (vector_p2p_x*vector_p2r_x) + (vector_p2p_y*vector_p2r_y)
           length_p2p = math.sqrt(vector_p2p_x**2+vector_p2p_y**2)
           length_p2l = math.sqrt(vector_p2l_x**2+vector_p2l_y**2)
           length_p2r = math.sqrt(vector_p2r_x**2+vector_p2r_y**2)
           multiply_p2p_and_p2l = length_p2p*length_p2l
           multiply_p2p_and_p2r = length_p2p*length_p2r
           angle_alpha = math.degrees(math.acos(dot_p2p_and_p2l/multiply_p2p_and_p2l))
           angle_beta  = math.degrees(math.acos(dot_p2p_and_p2r/multiply_p2p_and_p2r))
           cross_alpha = np.cross([vector_p2l_x,vector_p2l_y],[vector_p2p_x,vector_p2p_y])
           cross_beta  = np.cross([vector_p2r_x,vector_p2r_y],[vector_p2p_x,vector_p2p_y])
           if angle_alpha <= angle_beta:
                 if cross_alpha >= 0:
                    angle.append(angle_alpha)
                 else:
                    angle.append(angle_alpha*-1)
           else:
                 if cross_beta  >= 0:
                    angle.append(angle_beta)
                 else:
                    angle.append(angle_beta*-1)
    return angle


def movingaverage_degree(angle, window):
    in_degree_situation=[]
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(angle, weights, 'valid').tolist()
    for i in range(len(sma)):
          if -30<= sma[i] <= 30:
             in_degree_situation.append(1)
          else:
             in_degree_situation.append(0)    	
    return in_degree_situation


def fixation_index_calculation(in_degree_situation_0,in_degree_situation_90):
    percentage_degree_under30_0bar = np.sum(in_degree_situation_0)/float(len(in_degree_situation_0))
    percentage_degree_under30_90bar = np.sum(in_degree_situation_90)/float(len(in_degree_situation_90))
    fixation_index = percentage_degree_under30_0bar - percentage_degree_under30_90bar
    return fixation_index


#-------------------read list--------------------------
id=[]
data3 = open(list,'rU')
for i in data3:
    name = map(int,i.strip().split())
    id.append(name)
fixation_index_phase1=[]
fixation_index_phase2=[]
fixation_index_phase3=[]
#print len(id)
for i in range(len(id)):
    number = id[i][0]
    #print number


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
        if sit == 0:
           coordinate_x_phase1.append(x_pos)
           coordinate_y_phase1.append(y_pos)
        elif sit == 1:
           coordinate_x_phase2.append(x_pos)
           coordinate_y_phase2.append(y_pos)
        elif sit == 2:
           coordinate_x_phase3.append(x_pos)
           coordinate_y_phase3.append(y_pos)
    #arena data input
    data2 = open("%d.cfg"%(number),'rU')
    diameter,center_x,center_y,radius,lstripex,lstripey,rstripex,rstripey = [int(l.split('=')[1]) for l in data2 if len(l.split('='))>1]
    rate = (radius*2/diameter)*125
    conversion_rate = (diameter/float(radius*2))
    #set bar at 0 degree and 90 degree
    lstripex_0, lstripey_0, rstripex_0, rstripey_0 = bar_position_rotation(rate,center_x,center_y,0)
    lstripex_90, lstripey_90, rstripex_90, rstripey_90 =  bar_position_rotation(rate,center_x,center_y,90)


#-------------Calculate fixation index --------- 
    #calcualte angel with two bars
    angle_bar_0_phase1 = angle_calculation(coordinate_x_phase1, coordinate_y_phase1, lstripex_0, lstripey_0, rstripex_0, rstripey_0) 
    angle_bar_90_phase1 = angle_calculation(coordinate_x_phase1, coordinate_y_phase1, lstripex_90, lstripey_90, rstripex_90, rstripey_90)
    angle_bar_0_phase2 = angle_calculation(coordinate_x_phase2, coordinate_y_phase2, lstripex_0, lstripey_0, rstripex_0, rstripey_0) 
    angle_bar_90_phase2 = angle_calculation(coordinate_x_phase2, coordinate_y_phase2, lstripex_90, lstripey_90, rstripex_90, rstripey_90)
    angle_bar_0_phase3 = angle_calculation(coordinate_x_phase3, coordinate_y_phase3, lstripex_0, lstripey_0, rstripex_0, rstripey_0) 
    angle_bar_90_phase3 = angle_calculation(coordinate_x_phase3, coordinate_y_phase3, lstripex_90, lstripey_90, rstripex_90, rstripey_90)    
    #use sma and calculate ratio of in 30 degree
    under30_sit_bar_0_phase1 = movingaverage_degree(angle_bar_0_phase1,20)
    under30_sit_bar_90_phase1 = movingaverage_degree(angle_bar_90_phase1,20)
    under30_sit_bar_0_phase2 = movingaverage_degree(angle_bar_0_phase2,20)
    under30_sit_bar_90_phase2 = movingaverage_degree(angle_bar_90_phase2,20)
    under30_sit_bar_0_phase3 = movingaverage_degree(angle_bar_0_phase3,20)
    under30_sit_bar_90_phase3 = movingaverage_degree(angle_bar_90_phase3,20)
    #fixation index calculation
    fixation_index_phase1.append(fixation_index_calculation(under30_sit_bar_0_phase1,under30_sit_bar_90_phase1))
    fixation_index_phase2.append(fixation_index_calculation(under30_sit_bar_0_phase2,under30_sit_bar_90_phase2))
    fixation_index_phase3.append(fixation_index_calculation(under30_sit_bar_0_phase3,under30_sit_bar_90_phase3))

#------------------Student T test-----------------
t_static1,p_value1 = stats.ttest_rel(fixation_index_phase1,fixation_index_phase2)
t_static2,p_value2 = stats.ttest_rel(fixation_index_phase1,fixation_index_phase3)
print "p-value of phase 1 & 2 is %s" % p_value1
print "p-value of phase 1 & 3 is %s" % p_value2
    





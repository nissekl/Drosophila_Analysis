import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import stats
import math
import numpy as np
import sys
print '~!!This is made by Steven Slaughter!!~'
list = sys.argv[1]#condition list name
graph_name = sys.argv[2]#out put file name

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


def variation_graph(y_value, std, point_number, graph_name):
    x_value=[]
    y_upper=[]
    y_lower=[]
    plt.figure(figsize=(16,12),dpi=600)
    matplotlib.rcParams['axes.linewidth'] = 3
    word_size=40
    boundary_width=4
    font = {'family' : 'normal','weight' : 'normal','size'   : 35}
    matplotlib.rc('font', **font)
    for i in range(point_number):
        x_value.append(i*10+10)
    for i in range(len(y_value)):
        y_upper.append(y_value[i]+std[i])
        y_lower.append(y_value[i]-std[i])
    plt.fill_between(x_value,y_upper,y_lower,color='b', alpha=0.3)
    plt.plot(x_value, y_value, linewidth=5, color='b')
    plt.ylim(-0.2,0.5)
    plt.xlabel('Time (second)',size =word_size)
    plt.ylabel('Fixation index',size =word_size)
    plt.tick_params(axis='y',direction='in',length=0,width=0, colors='#000000')    
    #plt.axhline(y=-0.2, linewidth=4, color="#000000")        # inc. width of x-axis and color it green
    #plt.axvline(linewidth=4, color="#000000")        # inc. width of y-axis and color it red
    plt.savefig(graph_name) 


#-------------------read list--------------------------
id=[]
data3 = open(list,'rU')
for i in data3:
    name = map(int,i.strip().split())
    id.append(name)
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
    coordinate_x=[]
    coordinate_y=[]
    time=[]
    for line in data1:
        index,t,x_pos,y_pos,inter,sit = map(float,line.strip().split())    
        time.append(t)
        coordinate_x.append(x_pos)
        coordinate_y.append(y_pos)
    #check old and new data
    coordinate_x_checked=[]
    coordinate_y_checked=[]
    time_checked=[]
    if time[-1] > 300:
       for j in range(len(time)):
           if time[j]<=90:
              coordinate_x_checked.append(coordinate_x[j])
              coordinate_y_checked.append(coordinate_y[j])
              time_checked.append(time[j])
           elif 120< time[j]<=210:
              coordinate_x_checked.append(coordinate_x[j])
              coordinate_y_checked.append(coordinate_y[j])
              time_checked.append(time[j]-30)
           elif 240< time[j]<=330:
              coordinate_x_checked.append(coordinate_x[j])
              coordinate_y_checked.append(coordinate_y[j])
              time_checked.append(time[j]-60)
    else:
          coordinate_x_checked.extend(coordinate_x)
          coordinate_y_checked.extend(coordinate_y)
          time_checked.extend(time)
    #delete stop point
    non_stop_time=[]
    for k in range(len(time_checked)-1):
        if math.sqrt((coordinate_x_checked[k+1]-coordinate_x_checked[k])**2 + (coordinate_y_checked[k+1]-coordinate_y_checked[k])**2)!=0:
           non_stop_time.append(time_checked[k])
    #arena data input
    data2 = open("%d.cfg"%(number),'rU')
    diameter,center_x,center_y,radius,lstripex,lstripey,rstripex,rstripey = [int(l.split('=')[1]) for l in data2 if len(l.split('='))>1]
    rate = (radius*2/diameter)*125
    conversion_rate = (diameter/float(radius*2))
    #set bar at 0 degree and 90 degree
    lstripex_0, lstripey_0, rstripex_0, rstripey_0 = bar_position_rotation(rate,center_x,center_y,0)
    lstripex_90, lstripey_90, rstripex_90, rstripey_90 =  bar_position_rotation(rate,center_x,center_y,90)


#-------------Calculate angle and fixation index in part then add to array--------- 
    #calcualte angel with two bars
    angle_bar_0 = angle_calculation(coordinate_x_checked, coordinate_y_checked, lstripex_0, lstripey_0, rstripex_0, rstripey_0) 
    angle_bar_90 = angle_calculation(coordinate_x_checked, coordinate_y_checked, lstripex_90, lstripey_90, rstripex_90, rstripey_90)
    #use sma and calculate ratio of in 30 degree
    under30_sit_bar_0 = movingaverage_degree(angle_bar_0,20)
    under30_sit_bar_90 = movingaverage_degree(angle_bar_90,20)
    #scope time
    fixation_index_scope=[]
    for m in range(26):
        under30_sit_bar_0_scope=[]
        under30_sit_bar_90_scope=[]
        for n in range(len(non_stop_time)-19):
            if m*10< non_stop_time[n]<=m*10+20:
               under30_sit_bar_0_scope.append(under30_sit_bar_0[n])
               under30_sit_bar_90_scope.append(under30_sit_bar_90[n])
        if len(under30_sit_bar_0_scope) == 0:    
           fixation_index_scope.append(0)
        else:
           fixation_index_scope.append(fixation_index_calculation(under30_sit_bar_0_scope, under30_sit_bar_90_scope))
    if i == 0:
       fixation_variation = np.array([fixation_index_scope]) 
    else:
       fixation_variation = np.vstack((fixation_variation, fixation_index_scope))


#-------------Calculate overall fixation index---------  
fixation_index_average=np.mean(fixation_variation, axis=0)
fixation_index_std=stats.sem(fixation_variation, axis=0)
#print len(fixation_index_average)
#print len(fixation_index_std)


#-------------draw graph-------------------------------
variation_graph(fixation_index_average,fixation_index_std,26,graph_name)






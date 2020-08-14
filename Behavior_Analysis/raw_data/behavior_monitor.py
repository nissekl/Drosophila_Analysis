import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import stats
import math
import numpy as np
import sys
print '~!!This is made by Steven Slaughter!!~'
positiondata = sys.argv[1]
bardata= sys.argv[2]
input_second = int(sys.argv[3]) # time interval before and after the bars disappeared, for example 30 means 30 seconds before and after the bars disappear
perspective = int(sys.argv[4])#type=0 means observer's perspective, type=1 mens drosophila's perspective 
plot = int(sys.argv[5]) #graph type 0 means distance resolution, 1 means time resolution
graph_name = sys.argv[6]#out put file name


def axis_correction(stripevectorx,stripevectory,rstripex,rstripey):
    upper_dot = 1*stripevectorx
    stripevector_squareroot = math.sqrt(stripevectorx**2 + stripevectory**2)
    lower_multiply = 1*stripevector_squareroot
    axis_angle_cos_value = upper_dot/lower_multiply 
    axisangleround = math.acos(axis_angle_cos_value)
    if rstripey > lstripey :
       newrstripex = math.cos(-axisangleround)*rstripex - math.sin(-axisangleround)*rstripey
       newrstripey = math.sin(-axisangleround)*rstripex + math.cos(-axisangleround)*rstripey
       newlstripex = math.cos(-axisangleround)*lstripex - math.sin(-axisangleround)*lstripey
       newlstripey = math.sin(-axisangleround)*lstripex + math.cos(-axisangleround)*lstripey
    elif rstripey < lstripey :
       newrstripex = math.cos(axisangleround)*rstripex - math.sin(axisangleround)*rstripey
       newrstripey = math.sin(axisangleround)*rstripex + math.cos(axisangleround)*rstripey
       newlstripex = math.cos(axisangleround)*lstripex - math.sin(axisangleround)*lstripey
       newlstripey = math.sin(axisangleround)*lstripex + math.cos(axisangleround)*lstripey
    else :
       newrstripex = math.cos(axisangleround)*rstripex - math.sin(axisangleround)*rstripey
       newrstripey = math.sin(axisangleround)*rstripex + math.cos(axisangleround)*rstripey
       newlstripex = math.cos(axisangleround)*lstripex - math.sin(axisangleround)*lstripey
       newlstripey = math.sin(axisangleround)*lstripex + math.cos(axisangleround)*lstripey
    return newlstripex,newlstripey,newrstripex,newrstripey



def data_scope(position_x,position_y,time,bar_switch,arena_scope,interest_range,conversion_rate):
    distance=[]
    in_out_scope=[]
    scoped_arena_scope=[]
    scoped_in_out_scope=[]
    scoped_distance=[]
    scoped_coordinate_x=[]
    scoped_coordinate_y=[]
    scoped_time=[]
    scoped_bar_switch=[]
    for i in bar_switch:
        if i != 0:
           check_index = i 
           bar_offset_time = time[bar_switch.index(check_index)]   
           break
    for i in range(len(position_x)):
    	  if i == 0:    	   
    	     distance.append(0)
    	  else:   
           delta_x = position_x[i]-position_x[i-1]
           delta_y = position_y[i]-position_y[i-1]
           length = (math.sqrt(delta_x**2+delta_y**2))*conversion_rate
           distance.append(distance[-1]+length)    
    bar_offset_distance = distance[bar_switch.index(check_index)] 
    for i in range(len(time)):
    	if math.fabs(time[i]-bar_offset_time) <= interest_range:
    	   scoped_coordinate_x.append(position_x[i])
    	   scoped_coordinate_y.append(position_y[i])
    	   scoped_time.append(time[i])
    	   scoped_arena_scope.append(arena_scope[i])
    	   scoped_bar_switch.append(bar_switch[i])
    	   scoped_distance.append(distance[i])
    for i in range(len(scoped_arena_scope)-1):
        if scoped_arena_scope[i] == 1 and scoped_arena_scope[i+1] ==1:
           scoped_in_out_scope.append(1)
        else:
           scoped_in_out_scope.append(0)
    return scoped_coordinate_x, scoped_coordinate_y, scoped_time, scoped_distance, scoped_bar_switch, scoped_in_out_scope, bar_offset_time, bar_offset_distance


 
def angle_calculation_observer_perspective(position_x,position_y,left_bar_x,left_bar_y,right_bar_x,right_bar_y):
    angle=[]
    stop_move_situation=[]
    for i in range(len(position_x)-1):
      if position_x[i+1] == position_x[i] and position_y[i+1] == position_y[i]:
           angle.append(0)
           stop_move_situation.append(0)#Drosophila doesn't move
      else:
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
                 if position_y[i+1] >= right_bar_y:
                    angle.append(angle_alpha)
                 else:
                    angle.append(angle_alpha*-1)
           else:
                 if position_y[i+1] >= right_bar_y:
                    angle.append(angle_beta)
                 else:
                    angle.append(angle_beta*-1)
           stop_move_situation.append(1)#Drosophila moves
    return angle, stop_move_situation



def angle_calculation_drosophila_perspective(position_x,position_y,left_bar_x,left_bar_y,right_bar_x,right_bar_y):
    angle=[]
    stop_move_situation=[]
    for i in range(len(position_x)-1):
      if position_x[i+1] == position_x[i] and position_y[i+1] == position_y[i]:
           angle.append(0)
           stop_move_situation.append(0)#Drosophila doesn't move
      else:
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
           stop_move_situation.append(1)#Drosophila moves
    return angle, stop_move_situation



def movingaverage(angle, stop_move_situation, window, type):#type=0 means distance resolution type=1 mens time resolution 
    non_stop_angle=[]
    in_degree_situation=[]#0 means not in degree of 30. 1 means in degree of 30
    sma_time_resolution=[]
    in_point_count=0 #to calculate the sma point start point in time resolution
    for i in range(len(stop_move_situation)):
    	if stop_move_situation[i] == 1:
    	   non_stop_angle.append(angle[i])
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(non_stop_angle, weights, 'valid').tolist()
    if type == 0:
       for i in range(len(sma)):
           if -30<= sma[i] <= 30:
              in_degree_situation.append(1)
           else:
              in_degree_situation.append(0)    	
       return sma, in_degree_situation
    elif type == 1:
       for i in range(len(stop_move_situation)):
           if stop_move_situation[i] == 1:
              in_point_count=in_point_count+1
           if in_point_count >= 20:
              if stop_move_situation[i] == 1:
                 sma_time_resolution.append(sma[0])
                 if -30<= sma[0] <= 30:
                    in_degree_situation.append(1)
                 else:
                    in_degree_situation.append(0)         
                 del sma[0]
              elif stop_move_situation[i] == 0:
                 sma_time_resolution.append(0)
                 in_degree_situation.append(0)
       return sma_time_resolution, in_degree_situation


  
def drawing(angle, distance, time, in_out_scope, stop_move_situation, in_degree_situation, bar_offset_distance, bar_offset_time, window,type,graph_name):#type=0 means distance resolution type=1 mens time resolution 
    if type == 0:
       non_stop_arena_scope=[]
       non_stop_distance=[]
       plt.figure(figsize=(17,13),dpi=600)
       matplotlib.rcParams['axes.linewidth'] = 3
       word_size=40
       boundary_width=4
       font = {'family' : 'normal','weight' : 'normal','size'   : 35}
       matplotlib.rc('font', **font)
       for i in range(len(in_out_scope)):
       	   if stop_move_situation[i] == 1:
       	   	  non_stop_arena_scope.append(in_out_scope[i])
       	   	  non_stop_distance.append(distance[i+1])
       plt.axvline(x=bar_offset_distance,color='m',linewidth=6.0)
       for i in range(len(in_degree_situation)-1):
       	   if non_stop_arena_scope[i+window-1] ==1:
       	   	  if in_degree_situation[i] == 1 and in_degree_situation[i+1] == 1:
       	   	  	 color_curve = 'r'
       	   	  	 color_bout = '#000000'
       	   	  else:
       	   	  	 color_curve = 'g'
       	   	  	 color_bout ='#FFFFFF'
       	   elif non_stop_arena_scope[i+window-1] == 0:
       	   	  color_curve = '#DDDDDD'
       	   	  color_bout = '#FFFFFF'
           plt.plot(non_stop_distance[i+window-1:i+window+1],angle[i:i+2],'-',mfc='red',linewidth=6.0,color = color_curve)
           plt.plot(non_stop_distance[i+window-1:i+window+1],[140,140],color = color_bout,linewidth=8.0)
       plt.tick_params(direction='in',length=0,width=0, colors='#000000') 
       plt.xlabel('Walking Distance (mm)',size =word_size)
       plt.ylabel('Angle (degree)',size =word_size)
       plt.savefig(graph_name)
    elif type == 1:
       for i in range(len(stop_move_situation)-len(angle)):
           del stop_move_situation[0]
           del time[0]
           del in_out_scope[0]
       del time[0]
       plt.figure(figsize=(17,13),dpi=600)
       matplotlib.rcParams['axes.linewidth'] = 3
       word_size=40
       boundary_width=4
       font = {'family' : 'normal','weight' : 'normal','size'   : 35}
       matplotlib.rc('font', **font)
       plt.axvline(x=bar_offset_time,color='m',linewidth=6.0)
       for i in range(len(stop_move_situation)-1):
       	   if stop_move_situation[i] == 1 and stop_move_situation[i+1]:
              if in_out_scope[i] == 1:
              	 if in_degree_situation[i] == 1 and  in_degree_situation[i+1] == 1:
              	 	  color_curve = 'r'
              	 	  color_bout = '#000000'
                 else:
                    color_curve ='g'
                    color_bout = '#FFFFFF'
              elif in_out_scope[i] == 0:
              	 color_curve = '#DDDDDD'
              	 color_bout = '#FFFFFF'
       	   else:
       	   	 color_curve='#FFFFFF'
       	   	 color_bout='#FFFFFF'
           plt.plot(time[i:i+2],angle[i:i+2],'-',mfc='red',linewidth=6.0,color = color_curve)
           plt.plot(time[i:i+2],[140,140],color = color_bout,linewidth=8.0)  
       plt.tick_params(direction='in',length=0,width=0, colors='#000000') 
       plt.xlabel('Time (Second)', size =word_size)
       plt.ylabel('Angle (degree)', size =word_size)
       plt.savefig(graph_name)


#-------------------------------------------


coordinate_x=[]
coordinate_y=[]
bar_switch=[]
arena_scope=[]
time=[]


#------------Bar Data Input------------------


#bar position data
data2 = open(bardata,'rU')
diameter,center_x,center_y,radius,lstripex,lstripey,rstripex,rstripey = [int(i.split('=')[1]) for i in data2 if len(i.split('='))>1]
rate = (radius*2/diameter)*125
conversion_rate = (diameter/float(radius*2))
stripevectorx =  (rstripex+rate) - (lstripex-rate)
stripevectory =  rstripey - lstripey

#---------Axis Correction-------------------
lstripex_corrected, lstripey_corrected, rstripex_corrected, rstripey_corrected = axis_correction(stripevectorx,stripevectory,rstripex,rstripey)


#---------Coordinate Data Input-------------

#coordinate data input
data1 = open(positiondata,'rU')
prevx=None
prevy=None
presit=None
pre_time=None
for line in data1:
    index,t,x_pos,y_pos,inter,sit = map(float,line.strip().split())    
    coordinate_x.append(x_pos)
    coordinate_y.append(y_pos)
    bar_switch.append(sit)#0 means that bars are showed
    time.append(t)
    if (x_pos - center_x)**2+(y_pos - center_y)**2 <= (radius*0.9)**2:
    	arena_scope.append(1)#in arena 
    else:
    	arena_scope.append(0)#out arena

#---------------Scope Data-----------------
scoped_coordinate_x, scoped_coordinate_y, scoped_time, scoped_distance, scoped_bar_switch, scoped_in_out_scope, bar_offset_time, bar_offset_distance = data_scope(coordinate_x,coordinate_y,time,bar_switch,arena_scope,input_second,conversion_rate)


#------------Angle Calculate---------------
if perspective == 0:
   scoped_angle, scoped_stop_move_situation = angle_calculation_observer_perspective(scoped_coordinate_x, scoped_coordinate_y, lstripex_corrected, lstripey_corrected, rstripex_corrected, rstripey_corrected)
elif perspective == 1:
   scoped_angle, scoped_stop_move_situation = angle_calculation_drosophila_perspective(scoped_coordinate_x, scoped_coordinate_y, lstripex_corrected, lstripey_corrected, rstripex_corrected, rstripey_corrected)   


#----------Simple Moving Average-----------
angle_sma, in_degree_situation = movingaverage(scoped_angle, scoped_stop_move_situation, 20, plot)


#-------------Drawing Graph----------------
drawing(angle_sma, scoped_distance, scoped_time, scoped_in_out_scope, scoped_stop_move_situation, in_degree_situation, bar_offset_distance, bar_offset_time, 20, plot,graph_name)

  

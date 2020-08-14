import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import stats
import math
import numpy as np
import sys
print '~!!This is made by Steven Slaughter!!~'
positiondata = sys.argv[1]
bardata= sys.argv[2]
calculation_method = int(sys.argv[3]) # 0 means our method, 1 means strauss method
graph_name = sys.argv[4] #out put file name



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

 

def angle_calculation(position_x,position_y,left_bar_x,left_bar_y,right_bar_x,right_bar_y):
    angle=[]
    for i in range(len(position_x)-1):
      if position_x[i+1] != position_x[i] or position_y[i+1] != position_y[i]:
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
           if angle_alpha < angle_beta:
                 if cross_alpha >= 0:
                    angle.append(angle_alpha)
                 else:
                    angle.append(angle_alpha*-1)
           elif angle_alpha > angle_beta:
                 if cross_beta  >= 0:
                    angle.append(angle_beta)
                 else:
                    angle.append(angle_beta*-1)
           elif angle_alpha == angle_beta:
                angle.append(angle_beta*-1)
    return angle  

def angle_calculation_strausssmethod(position_x,position_y,left_bar_x,left_bar_y,right_bar_x,right_bar_y):
    angle=[]
    for i in range(len(position_x)-1):
      if position_x[i+1] != position_x[i] or position_y[i+1] != position_y[i]:
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
    return angle 

def distance_calculation(position_x,position_y):
    distance=[]
    for i in range(len(position_x)-1):
        if position_x[i+1] != position_x[i] or position_y[i+1] != position_y[i]:
           if i == 0:
              delta_x = position_x[i]-position_x[i-1]
              delta_y = position_y[i]-position_y[i-1]        
              length = (math.sqrt(delta_x**2+delta_y**2))*conversion_rate
              distance.append(length)    
           else:   
              delta_x = position_x[i]-position_x[i-1]
              delta_y = position_y[i]-position_y[i-1]
              length = (math.sqrt(delta_x**2+delta_y**2))*conversion_rate
              distance.append(distance[-1]+length)    
    return distance

def movingaverage(angle, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(angle, weights, 'valid').tolist()
    return sma

def drawing_variation(angle,distance,window):
    del distance[0]
    boundary_width=4
    word_size=40
    font = {'family' : 'normal','weight' : 'normal','size'   : 35}
    matplotlib.rc('font', **font)
    plt.plot(distance[window-1:],angle,linewidth=4.0,color = 'g')
    plt.xlabel('R. Strauss and J. Pichler, 1998. method',size =word_size)
    plt.ylabel('Angle (degree)',size =word_size)
    plt.title('R. Strauss and J. Pichler, 1998. method',size =word_size)
    plt.axhline(y=100,linewidth=boundary_width,color='#000000')
    plt.axhline(y=-100,linewidth=boundary_width, color='#000000')
    plt.axvline(x=0,linewidth=boundary_width, color='#000000')
    plt.axvline(x=80,linewidth=boundary_width, color='#000000')
    plt.tick_params(direction='in',length=7,width=3, colors='#000000')  
    plt.ylim(-100,100)
    plt.show()

def drawing_subplot(coordinate_x,coordinate_y,center_x,center_y,angle,distance):
    plt.subplot(211)
    del distance[0]
    plt.plot(distance[19:],angle,linewidth=3.0,color = 'g')
    plt.ylim(-100,100)
    plt.subplot(212)
    plt.plot(coordinate_x,coordinate_y)
    circle=plt.Circle((center_x,center_y),radius,fill = False)
    fig = plt.gcf()
    #fig.gca().add_artist(circle)
    ax = fig.add_subplot()
    plt.xlim(50,600)
    plt.ylim(50,450)
    plt.show()

def draw_static(data,graph_name):
    plt.figure(figsize=(13,11),dpi=600)
    matplotlib.rcParams['axes.linewidth'] = 3
    word_size=40
    font = {'family' : 'normal','weight' : 'normal','size'   : 35}
    matplotlib.rc('font', **font)
    plt.hist(data,facecolor='green', bins=15,linewidth=7.0)
    plt.xlabel('Angle (degree)',size =word_size)
    plt.ylabel('Frequency',size =word_size)
    plt.tick_params(direction='in',length=0,width=0, colors='#000000')  
    plt.xlim(-100,100)
    plt.savefig(graph_name)
    #plt.show()
#-------------------------------------------


coordinate_x=[]
coordinate_y=[]
coordinate_x2=[]
coordinate_y2=[]
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
    time.append(t)


#------------Angle Calculate---------------
if calculation_method == 0:
   angle = angle_calculation(coordinate_x, coordinate_y, lstripex, lstripey, rstripex, rstripey)
elif calculation_method == 1:
   angle = angle_calculation_strausssmethod(coordinate_x, coordinate_y, lstripex, lstripey, rstripex, rstripey)

#sma = movingaverage(angle,20)

#-------------Drawing Graph----------------
#drawing_variation(sma,time,20)
draw_static(angle,graph_name)
  

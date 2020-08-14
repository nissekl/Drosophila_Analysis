import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import stats
import math
import numpy as np
import sys
print '~!!This is made by Steven Slaughter!!~'
list = sys.argv[1]#condition list name
graph_name = sys.argv[2]#out put file name
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
    plt.plot(x_value, y_value, linewidth=3, color='b')
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
    #arena data input
    data2 = open("%d.cfg"%(number),'rU')
    diameter,center_x,center_y,radius,lstripex,lstripey,rstripex,rstripey = [int(l.split('=')[1]) for l in data2 if len(l.split('='))>1]

#-------------Calculate fixation index in part and add to array---------       
    fixation_index_scope=[]
    for j in range(26):
        coordinate_x_scope=[]
        coordinate_y_scope=[]
        for k in range(len(time_checked)):
            if j*10<time_checked[k]<=j*10+20:
               coordinate_x_scope.append(coordinate_x_checked[k])
               coordinate_y_scope.append(coordinate_y_checked[k])        
        fixation_index_scope.append(distribution_method(coordinate_x_scope,coordinate_y_scope,center_x, center_y))   
    if i == 0:
       fixation_variation = np.array([fixation_index_scope]) 
    else:
       fixation_variation = np.vstack((fixation_variation, fixation_index_scope))


#-------------Calculate overall fixation index---------  
fixation_index_average=np.mean(fixation_variation, axis=0)
fixation_index_std=stats.sem(fixation_variation, axis=0)


#-------------draw graph-------------------------------
variation_graph(fixation_index_average,fixation_index_std,26,graph_name)



    




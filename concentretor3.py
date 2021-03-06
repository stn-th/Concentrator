import csv
import utm
import math
from math import radians, sin, cos, acos
from pulp import *
import matplotlib.pyplot as plt
import time
import random
from unicodedata import name
from folium import IFrame
import folium
from folium.plugins import MarkerCluster


start_time = time.time()
#initialization
# N = 11   #number of nodes
# roi_x = 10; #region of interest (wide)
# roi_y = 10; #region of interest (high)
beta = 400 #cost of establishing node i as a concentrator
K = 8     #concentrator capacity
i=1
#P = {1:(x_EN,y_EN),2:(x_LAW,y_LAW),3:(x_AR,y_AR),4:(x_PS,y_PS),5:(x_NU,y_NU),6:(x_AG,y_AG),7:(x_BS,y_BS),8:(x_POL,y_POL),9:(x_LA,y_LA),10:(x_SC,y_SC),11:(x_PH,y_PH)}
P = {1.:(0.0,0.0),2:(0.0,0.0),3:(0.0,0.0),4:(0.0,0.0),5:(0.0,0.0),6:(0.0,0.0),7:(0.0,0.0),8:(0.0,0.0),9:(0.0,0.0),10:(0.0,0.0),11:(0.0,0.0)}
with open('lat_lon_ubu.csv') as csvfile:
    reader = csv.reader(csvfile)
    print(reader)
    for row in reader:
        #print(row[2])
        a = float(row[1])
        b = float(row[2])
        x, y,z,ut= utm.from_latlon(a,b)
        print( x, y)
        P.update({i:(x,y)})
        print(P[i])
        i = i+1
Np = [i for i in P.keys()]  #set of all nodes
D = {}  #D will be a dictionary whose keys are links and whose
        #values are distances, i.e. alpha ij
B = {}  #A will be a dictionary whose keys are nodes and whose
        #values are establishing costs, i.e. beta i
for i in Np:
    B[i] = beta
    for j in Np:
        tmp = math.sqrt(pow(P[i][0] - P[j][0],2) + \
                        pow(P[i][1] - P[j][1],2))
        D[(i,j)] = tmp #node separation distance
prob = LpProblem('location_problem', LpMinimize)
x = LpVariable.dicts('x', (Np, Np), 0, 1, LpInteger)
y = LpVariable.dicts('y', (Np), 0, 1, LpInteger)
#objective function
prob += lpSum(D[(i,j)]*x[i][j] for i in Np for j in Np) + \
    lpSum(B[i]*y[i] for i in Np) 
#constraints
for i in Np:
    prob += lpSum(x[i][j] for j in Np) == 1
for j in Np:
    prob += lpSum(x[i][j] for i in Np) <= K*y[j]
prob.writeLP('location_problem.lp')
prob.solve()
print ('Status:', LpStatus[prob.status])
print ('Optimal cost:', '%.2f' % value(prob.objective))
#print (value(prob.objective))
Ans = value(prob.objective)
for v in prob.variables():
    print(v.name, "=", v.varValue)


#display network layout

for i in Np:

    if y[i].varValue == 1:
        plt.plot(P[i][0],P[i][1], 'ro') #concentrater
        

    else:
        plt.plot(P[i][0],P[i][1], 'bo') #node ????????????
        plt.text(P[i][0], P[i][1]+0.1, '%d' % i)
    for j in Np:
        if x[i][j].varValue == 1:
            x_values = [P[i][0], P[j][0]]
            y_values = [P[i][1], P[j][1]]
            plt.plot(x_values, y_values, 'g--') #????????????
            
plt.axis('off')            
plt.title('Map concentretor\nBata = 400, K = 8 ' )
plt.xlabel('x position [m]')
plt.ylabel('y position [m]')
plt.show()
plt.grid(True)


#Add another network display here!!!
#runtime
print("\n** Runtime: %.2f sec **" % (time.time() - start_time))



#Map 
#????????????Map
m = folium.Map(location=[15.11710,104.90690],name='ubu_map',zoom_start = 17)

with open('node.csv') as csvfile:
    reader = csv.reader(csvfile)
    print(reader)
    for row in reader: 
        a = str(row[0])
        b =  [float(s) for s in row[1].split(",")]
        folium.Marker(location= b,popup = a,tooltip= b,icon = folium.Icon(color='blue')).add_to(m)
        #print(a)
with open('concentrater.csv') as csvfile:
    reader = csv.reader(csvfile)
    print(reader)
    for row in reader: 
        c = str(row[0])
        d =  [float(s) for s in row[1].split(",")]
        folium.Marker(location= d,popup = c,tooltip= d,icon = folium.Icon(color='red')).add_to(m)      

position1 =[[15.11829,104.90558],[15.12032 ,104.90462],[15.12053,104.90608],]
position2 =[[15.11947,104.90315],[15.12032 ,104.90462],[15.12255,104.90651]]
position3 =[[15.11706,104.90882],[15.11559,104.90653],[15.11548,104.90527]]
position4 =[[15.11943,104.91039],[15.12049,104.91065],[15.12221,104.90878]]

N = position1,position2,position3,position4 
#??????????????????????????????

folium.PolyLine(N, color="Green", weight=2.5, opacity=1).add_to(m)

#??????????????????????????????????????????
m.save('Mapubu.html')
# Concentrator
import math
from math import radians, sin, cos, acos
from pulp import *
import math
import matplotlib.pyplot as plt
import time
import random


#lat lon to x,y
R = 6371.01
# คณะวิศวกรรมศาตสร์ 
lat1 = 15.12032 
lon1 = 104.90462
x_EN = R*cos(lat1)*cos(lon1)
print("x_EN =", x_EN)
y_EN= R*cos(lat1)*sin(lon1)
print("y_EN =",y_EN) 

#คณะนิติศาตสร์
lat2 = 15.12053
lon2 =104.90608
x_LAW = R*cos(lat2)*cos(lon2)
print("x_LAW =", x_LAW)
y_LAW= R*cos(lat2)*sin(lon2)
print("y_LAW =",y_LAW) 

#คณะศิลปประยุกต์และสถาปัตยกรรมศาสตร์   
lat3 = 15.11829
lon3 =104.90558
x_AR = R*cos(lat3)*cos(lon3)
print("x_AR =", x_AR)
y_AR= R*cos(lat3)*sin(lon3)
print("y_AR =",y_AR) 

#คณะเภสัช
lat4 = 15.11943
lon4 =104.91039
x_PS = R*cos(lat4)*cos(lon4)
print("x_PS =", x_PS)
y_PS= R*cos(lat4)*sin(lon4)
print("y_PS =",y_PS) 

# คณะพยาบาลศาสตร์
lat5 = 15.11559
lon5 =104.90653
x_NU = R*cos(lat5)*cos(lon5)
print("x_NU =", x_NU)
y_NU= R*cos(lat2)*sin(lon2)
print("y_NU =",y_NU) 

# คณะเกษตรศาสตร์
lat6 = 15.11217
lon6 =104.90886
x_AG = R*cos(lat6)*cos(lon6)
print("x_AG =", x_AG)
y_AG= R*cos(lat6)*sin(lon6)
print("y_AG =",y_AG) 

#คณะบริหารศาตสร์
lat7 = 15.11947
lon7 =104.90315
x_BS = R*cos(lat7)*cos(lon7)
print("x_BS =", x_BS)
y_BS= R*cos(lat7)*sin(lon7)
print("y_BS =",y_BS) 

#คณะรัฐศาสตร์
lat8 = 15.12049
lon8 =104.91065
x_POL = R*cos(lat8)*cos(lon8)
print("x_POL=", x_POL)
y_POL= R*cos(lat8)*sin(lon8)
print("y_POL =",y_POL) 

#คณะศิลปกรรมศาสตร์
lat9 = 15.11706
lon9 =104.90882
x_FA = R*cos(lat9)*cos(lon9)
print("x_FA=", x_FA)
y_FA= R*cos(lat9)*sin(lon9)
print("y_FA =",y_FA) 

#คณะวิทยาศาสตร์
lat10 = 15.12255
lon10 =104.90651
x_SC = R*cos(lat10)*cos(lon10)
print("x_SC=", x_SC)
y_SC= R*cos(lat10)*sin(lon10)
print("y_SC =",y_SC) 

#วิทยาลัยแพทย์ศาสตร์
lat11 = 15.11548
lon11 =104.90527
x_PH = R*cos(lat11)*cos(lon11)
print("x_PH =", x_PH)
y_PH= R*cos(lat11)*sin(lon11)
print("y_PH =",y_PH) 

start_time = time.time()
#initialization
# N = 11   #number of nodes
# roi_x = 10; #region of interest (wide)
# roi_y = 10; #region of interest (high)
beta = 27 #cost of establishing node i as a concentrator
K = 5     #concentrator capacity
P = {}
#Add (lat, long) to (x, y) here!!!
#option 1 node generation (fixed positions)
P = {1:(x_EN,y_EN),2:(x_LAW,y_LAW),3:(x_AR,y_AR),4:(x_PS,y_PS),5:(x_NU,y_NU),6:(x_AG,y_AG),7:(x_BS,y_BS),8:(x_POL,y_POL),9:(x_FA,y_FA),10:(x_SC,y_SC),11:(x_PH,y_PH)}
#option 2 random node generation
# for i in range(0,N):
#     x = random.randint(0, roi_x)
#     y = random.randint(0, roi_y) 
#     P[i] = (x,y) 
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
for v in prob.variables():
    print(v.name, "=", v.varValue)
#display network layout
for i in Np:
    if y[i].varValue == 1:
        plt.plot(P[i][0],P[i][1], 'ro')
    else:
        plt.plot(P[i][0],P[i][1], 'bo')
    plt.text(P[i][0], P[i][1]+0.1, '%d' % i)
    for j in Np:
        if x[i][j].varValue == 1:
            x_values = [P[i][0], P[j][0]]
            y_values = [P[i][1], P[j][1]]
            plt.plot(x_values, y_values, 'g--')
plt.grid(True)
plt.show()

#Add another network display here!!!
#runtime
print("\n** Runtime: %.2f sec **" % (time.time() - start_time))

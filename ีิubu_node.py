import math
from pulp import *
import matplotlib.pyplot as plt
import time
import random
from unicodedata import name
from folium import IFrame
import folium
from folium.plugins import MarkerCluster
import utm

#lat lon to x,y
# คณะวิศวกรรมศาตสร์ 
lon1 = 104.90462
lat1 = 15.12032
x_EN, y_EN ,z_EN,ut_EN= utm.from_latlon(lat1, lon1)
print("x_EN=",x_EN )
print("y_EN",y_EN )
 
#คณะนิติศาตสร์
lat2 = 15.12053
lon2 =104.90608
x_LAW, y_LAW,z_LAW,ut_LAW= utm.from_latlon(lat2, lon2)
print("x_LAW=",x_LAW )
print("y_LAW",y_LAW )
 
#คณะศิลปประยุกต์และสถาปัตยกรรมศาสตร์   
lat3 = 15.11829
lon3 =104.90558
x_AR, y_AR,z_AR,ut_AR= utm.from_latlon(lat3, lon3)
print("x_AR=",x_AR )
print("y_AR",y_AR)

#คณะเภสัชศาสตร์
lat4 = 15.11943
lon4 =104.91039
x_PS, y_PS,z_PS,ut_PS= utm.from_latlon(lat4, lon4)
print("x_PS=",x_PS )
print("y_PS",y_PS)

# คณะพยาบาลศาสตร์
lat5 = 15.11559
lon5 =104.90653
x_NU, y_NU,z_NU,ut_NU= utm.from_latlon(lat5, lon5)
print("x_NU=",x_NU )
print("y_NU",y_NU)

# คณะเกษตรศาสตร์
lat6 = 15.122201
lon6 =104.908782
x_AG, y_AG,z_AG,ut_AG= utm.from_latlon(lat6, lon6)
print("x_AG=",x_AG )
print("y_AG",y_AG)

#คณะบริหารศาตสร์
lat7 = 15.11947
lon7 =104.90315
x_BS, y_BS,z_BS,ut_BS= utm.from_latlon(lat7, lon7)
print("x_BS=",x_BS )
print("y_BS",y_BS)

#คณะรัฐศาสตร์
lat8 = 15.12049
lon8 =104.91065
x_POL, y_POL,z_POL,ut_POL= utm.from_latlon(lat8, lon8)
print("x_POL=",x_POL )
print("y_POL",y_POL)

#คณะศิลปกรรมศาสตร์
lat9 = 15.11706
lon9 =104.90882
x_LA, y_LA,z_LA,ut_LA= utm.from_latlon(lat9, lon9)
print("x_LA=",x_LA )
print("y_LA",y_LA)

#คณะวิทยาศาสตร์
lat10 = 15.12255
lon10 =104.90651
x_SC, y_SC,z_SC,ut_SC= utm.from_latlon(lat10, lon10)
print("x_SC=",x_SC )
print("y_SC",y_SC)

#วิทยาลัยแพทย์ศาสตร์
lat11 = 15.11548
lon11 =104.90527
x_PH, y_PH,z_PH,ut_PH= utm.from_latlon(lat11, lon11)
print("x_PH=",x_PH )
print("y_PH",y_PH)

start_time = time.time()
#initialization
# N = 11   #number of nodes
# roi_x = 10; #region of interest (wide)
# roi_y = 10; #region of interest (high)
beta = 400 #cost of establishing node i as a concentrator
K = 8   #concentrator capacity
P = {}
#Add (lat, long) to (x, y) here!!!
#option 1 node generation (fixed positions)
P = {1:(x_EN,y_EN),2:(x_LAW,y_LAW),3:(x_AR,y_AR),4:(x_PS,y_PS),5:(x_NU,y_NU),6:(x_AG,y_AG),7:(x_BS,y_BS),8:(x_POL,y_POL),9:(x_LA,y_LA),10:(x_SC,y_SC),11:(x_PH,y_PH)}
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


#Map 
#แสดงMap
concentrator1 =[[15.11829,104.90558],[15.12032 ,104.90462],[15.12053,104.90608]]
concentrator2 =[[15.11947,104.90315],[15.12032 ,104.90462],[15.12255,104.90651]]
concentrator3 =[[15.11706,104.90882],[15.11559,104.90653],[15.11548,104.90527]]
concentrator4 =[[15.11943,104.91039],[15.12049,104.91065],[15.12221,104.90878]]


m = folium.Map(location=[15.11710,104.90690],name='ubu_map',zoom_start = 17)
html = '<img src="data:image/png;base64,{}">'.format

#concentrator
tooltip1 = "concentrator1 is Faculty of Engineering'"
folium.Marker(location=[15.12032,104.90462],popup ='Engineering' ,tooltip=tooltip1,icon = folium.Icon(color='red')).add_to(m)

tooltip3 = " concentrator2 is Faculty of Political Science"
folium.Marker(location=[15.12049,104.91065],popup='Political Science',tooltip=tooltip3,icon = folium.Icon(color='red')).add_to(m)

tooltip2 = " concentrator3 is   Faculty of Nursing"
folium.Marker(location=[15.11559,104.90653],popup='Faculty of Nursing',tooltip=tooltip2,icon = folium.Icon(color='red')).add_to(m)


#node
tooltip4 = " Faculty Of College of Medicine and Public Health"
folium.Marker(location=[15.11548,104.90527],popup='College of Medicine and Public Health',tooltip=tooltip4 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip5 = " Faculty of Law"
folium.Marker(location=[15.12053,104.90608],popup='Law' ,tooltip=tooltip5 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip6 = "  Faculty of Agriculture"
folium.Marker(location=[15.122201,104.90878],popup='  Agriculture' , tooltip=tooltip6 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip7 = " Faculty of Pharmaceutical Sciences"
folium.Marker(location=[15.11943,104.91039],popup='  Pharmaceutical Sciences' ,tooltip=tooltip7 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip8 = " Faculty of Management Science"
folium.Marker(location=[15.11947,104.90315],popup=' Management Science',tooltip=tooltip8 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip9 = " Faculty Of Applied Art & Architecture"
folium.Marker(location=[15.11829,104.90558],popup=' Applied Art & Architecture' , tooltip=tooltip9 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip10 = "Faculty of Liberal Arts"
folium.Marker(location=[15.11706,104.90882],popup=' Liberal Arts' ,tooltip=tooltip10 ,icon = folium.Icon(color='blue')).add_to(m)
tooltip11 = " Faculty of Science"
folium.Marker(location=[15.12255,104.90651],popup=' Science' , tooltip=tooltip11 ,icon = folium.Icon(color='blue')).add_to(m)

#เส้นเชื่อม
folium.PolyLine(concentrator1, color="Green", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(concentrator2, color="Green", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(concentrator3, color="orange", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(concentrator4, color="brown ", weight=2.5, opacity=1).add_to(m)

#บันทึกไฟล์แสดง
m.save('Mapubu.html')

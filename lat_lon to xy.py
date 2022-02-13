import utm
input_lon = 104.90462
input_lat = 15.12032
x, y, zone, ut = utm.from_latlon(input_lat, input_lon)
print(x, y, zone, ut )

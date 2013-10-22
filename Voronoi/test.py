import subprocess

tmp='400,500,404,472,404,528,420,440\n1,5,1,0,0,2,500,500'
p = subprocess.Popen([".\Voronoi.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
output = p.communicate(tmp)[0]
print output

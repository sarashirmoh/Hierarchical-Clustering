
# coding: utf-8

# In[408]:

import sys
import os
import heapq
import math

k = int(sys.argv[-1])
fn = sys.argv[-2]
# In[409]:

indx = 0
inp_points = []
clusters = {}
f = open (fn)
for line in f:
    if len(line) > 1:
        points = {}
        p = line.strip().split(",")
        #points.append((indx,((float(p[0]),float(p[1]),float(p[2]),float(p[3])),p[4])))
        points["index"] = indx
        points["#"] = p[0:4]
        points["category"] = p[4]
        inp_points.append(points)
        clusters[str([indx])] = {}
        clusters[str([indx])]["points"]=[indx]
        clusters[str([indx])]["centroid"]= p[0:4]
        indx+=1
# In[411]:

processed = []
lst = []
for a in range(len(inp_points)-1):   
    for b in range(a+1, len(inp_points)): 
        dd = 0.0
        for c in range(0,4):
            dd += (float(inp_points[a]["#"][c])-float(inp_points[b]["#"][c]))**2
        dd = math.sqrt(dd)
        lst.append((dd, [dd, [[a], [b]]]))
euc_lst = lst

heapq.heapify(euc_lst)
while len(clusters) > k:
    merge = {}
    min_heap = heapq.heappop(euc_lst)
    euc_distance = min_heap[0]
    part = min_heap[1]
    duplicates = False
    for b in processed:
        if b in part[1]:
            duplicates = True
    if duplicates == True:
        continue
    c = [0.0]*4
    merge_p = sum(part[1], [])
    for s in merge_p:
        for q in range(0,4):
            c[q] += float(inp_points[s]["#"][q])
    ll = len(merge_p)
    merge["centroid"]=tuple (i/ll for i in c)
    merge_p.sort()
    merge["points"] = merge_p
    for pr in part[1]:
        processed.append(pr)
        del clusters[str(pr)]
    for crnt in clusters.values():
        upd_lst = []
        #euc_distance = euclidean_distance(crnt["centroid"], merge["centroid"])
        
        euc_distance = 0.0
        for c in range(0,4):
            euc_distance += (float(crnt["centroid"][c])-float(merge["centroid"][c]))**2
        euc_distance = math.sqrt(euc_distance)
        
        upd_lst.append(euc_distance)
        upd_lst.append([merge["points"], crnt["points"]])
        heapq.heappush(euc_lst, (euc_distance, upd_lst))
    clusters[str(merge_p)] = merge
ccc=0
wrongs = 0
g = open ("clustering_output.txt",'w')
for key in clusters:
    
    ccc = 0
    fl_dct = {}
    fl_dct['Iris-virginica'] = 0
    fl_dct['Iris-versicolor'] = 0
    fl_dct['Iris-setosa'] = 0
    m = key[1:-1].split(",")
    for j in m:
        if inp_points[int(j)]["category"] == 'Iris-virginica':
            fl_dct['Iris-virginica'] +=1
        elif inp_points[int(j)]["category"] == 'Iris-versicolor':
            fl_dct['Iris-versicolor'] +=1
        elif inp_points[int(j)]["category"] =='Iris-setosa':
            fl_dct['Iris-setosa'] +=1
    c_name = max(fl_dct, key=fl_dct.get) 
    g.write("cluster:%s\n" %c_name)
    #print n_virginica
    #print "category:"
    l = []
    l = key[1:-1].split(",")
    for i in l:
        g.write("[%.1f, %.1f, %.1f, %.1f, '%s']\n" %(float(inp_points[int(i)]["#"][0]),float(inp_points[int(i)]["#"][1]),float(inp_points[int(i)]["#"][2]),float(inp_points[int(i)]["#"][3]),inp_points[int(i)]["category"]))
        if inp_points[int(i)]["category"] != c_name:
            wrongs += 1
        ccc+=1
    g.write( "Number of points in this cluster:%d\n\n" %ccc)
g.write( "Number of points wrongly assigned:%d" %wrongs)


# In[ ]:





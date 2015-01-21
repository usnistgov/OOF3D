import string
from numarray import *
import numarray.linear_algebra as la

def tet_volume(tet, points):
    p1 = points[tet[0]]
    p2 = points[tet[1]]
    p3 = points[tet[2]]
    p4 = points[tet[3]]

    a = [[p2[0]-p1[0], p3[0]-p1[0], p4[0]-p1[0]],
         [p2[1]-p1[1], p3[1]-p1[1], p4[1]-p1[1]],
         [p2[2]-p1[2], p3[2]-p1[2], p4[2]-p1[2]]]

    det = la.determinant(a)
    return det/6.0
    

bad = open("badrationalizationrule2.txt","r")
lines = bad.readlines()

points = {}
initial = []
final = []
begin_new = False
begin_old = False
current_tet = []

for line in lines:
    tokens = string.splitfields(line)

    if len(tokens) == 0:
        continue

    if tokens[0] == "old:":
        begin_old = True;

    if tokens[0] == "new:":
        begin_new = True;

    if tokens[0].isdigit():
        i = int(tokens[0])
        try:
            x = points[i]
        except KeyError:
            x = [float(tokens[2][1:-1]), float(tokens[3][:-1]), float(tokens[4][:-1])]
            points[i] = x

        current_tet.append(i)

        if len(current_tet) == 4:
        
            if begin_old and not begin_new:
                initial.append(current_tet)

            if begin_new:
                final.append(current_tet)

            current_tet = []
            

total_initial_volume = 0
total_final_volume = 0

faces = [(0,1,3),(1,2,3),(0,2,3),(0,1,2)]
initial_outer_faces = []
final_outer_faces = []

print "num initial tets", len(initial)
for tet in initial:
    v = tet_volume(tet,points)
    total_initial_volume += v
    for face in faces:
        f = [tet[face[0]],tet[face[1]],tet[face[2]]]
        f.sort()
        try:
            initial_outer_faces.remove(f)
        except ValueError:
            initial_outer_faces.append(f)

print "total initial volume", total_initial_volume
print "initial outer faces", initial_outer_faces

print "num final tets", len(final)
for tet in final:
    v = tet_volume(tet,points)
    total_final_volume += v
    for face in faces:
        f = [tet[face[0]],tet[face[1]],tet[face[2]]]
        f.sort()
        try:
            final_outer_faces.remove(f)
        except ValueError:
            final_outer_faces.append(f)

print "total final volume", total_final_volume
print "final outer faces", final_outer_faces

for face in initial_outer_faces:
    if face not in final_outer_faces:
        print face, "is not in final faces"

print "\n\n"

for face in final_outer_faces:
    if face not in initial_outer_faces:
        print face, "is not in initial faces"


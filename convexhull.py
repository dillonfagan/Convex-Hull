import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c.
Note that this area will be negative
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0

'''
Given three points a,b,c,
returns True if and only if
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON

'''
Given three points a,b,c,
returns True if and only if
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON

'''
Given three points a,b,c,
returns True if and only if
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)

'''
Brute force convex hull construction.
'''
def brute(points):
	ch = []
	for p in points:
		for q in points:
			if q == p:
				continue
			print("PAIR: " + str(p) + " and " + str(q))
			# Invariants: either above or below must be zero in order for a pair of
			#	points to be added to the convex hull
			above = 0
			below = 0
			for r in points:
				if r == p or r == q:
					continue
				if cw(p, q, r):
					above += 1
				elif ccw(p, q, r):
					below += 1
			if above == 0 or below == 0:
				if not p in ch:
					ch.append(p)
				if not q in ch:
					ch.append(q)

	clockwiseSort(ch)
	print(ch)
	return ch

'''
Returns a merger of two convex hulls.
'''
def mergeHulls(a, b): # FIXME
	ch = []
	l_anchor = a[len(a) - 1] # rightmost point on the left hull
	r_anchor = b[0] # leftmost point on the right hull

	print("INIT LA: " + str(l_anchor))
	print("INIT RA: " + str(r_anchor))

	# find upper bridge right side
	for (ri, r) in b:
		np = b[(ri + 1) % (len(b) - 1)] # next point on hull
		if np[1] > r_anchor[1]:
			r_anchor = np
	ch.append(r_anchor)

	# upper bridge left side
	for (li, l) in a:
		np = a[(li + 1) % (len(a) - 1)]
		if np[1] > l_anchor[1]:
			l_anchor = np
	ch.append(l_anchor)

	# find lower bridge
	for (ri, r) in b:
		np = a[(li + 1) % (len(b) - 1)]
		if np[1] < r_anchor[1]:
			r_anchor = np
	ch.append(r_anchor)

	for (li, l) in a:
		np = a[(li + 1) % (len(a) - 1)]
		if np[1] < l_anchor[1]:
			l_anchor = np
	ch.append(l_anchor)

	clockwiseSort(ch)
	print(ch)
	return ch

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm.
'''
def computeHull(points):
	# simple case
	if len(points) <= 3:
		clockwiseSort(points)
		return points

	# sort points by their x coordinates
	points.sort(key = lambda p: p[0])
	print(points)

	def hull(points):
		# base case(s) -> compute hull with brute force
		if len(points) <= 3:
			print("SIMPLE TRIPLE")
			clockwiseSort(points)
			return points
		if len(points) < 6:
			print("BRUTE FORCE")
			return brute(points)

		# midpoint index of the points list
		m = int(math.floor(len(points) / 2))
		# left half
		a = points[:m]
		# right half
		b = points[(m + 1):]

		return mergeHulls(hull(a), hull(b))

	return hull(points)

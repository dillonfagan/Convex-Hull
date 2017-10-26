import math
import sys
import time

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
	# Invariant (init): convex hull list is initialized
	ch = []
	for p in points:
		for q in points:
			if q == p:
				continue
			# Invariants (init): either above or below must be zero in order for a pair of
			#	points to be added to the convex hull
			above = 0
			below = 0
			for r in points:
				if r == p or r == q:
					continue
				if cw(p, q, r): # Invariant (maintenance): If moving clockwise through points
					above += 1
				elif ccw(p, q, r): # Invariant (maintenance): If moving counter-clockwise through points
					below += 1
			if above == 0 or below == 0: # Invariant (termination): point can be added to ch
				if not p in ch:
					ch.append(p)
				if not q in ch:
					ch.append(q)
	return ch

'''
Returns a merger of two convex hulls.
'''
def mergeHulls(a, b, m):
	# Invariant (init): convex hull list is initialized
	ch = []

	# Invariants (init):
	# y3 is the highest y coordinate
	# y4 is the lowest y coordinate
	# note - x, y3, y4 will not change
	y = sorted(a + b, key = lambda p: p[1])
	y3 = y[len(y) - 1][1]
	y4 = y[0][1]

	# (i, j) are the indices of the start and end points of the tangent lines
	utan = upper_tangent(a, b, m, y3, y4)
	ltan = lower_tangent(a, b, m, y3, y4)

	# Invariant (init): Upper Left and Right / Lower Left and Right tangent points
	upper_left = a[utan[0]]; upper_right = b[utan[1]]
	lower_left = a[ltan[0]]; lower_right = b[ltan[1]]

	# walk around each hull, clockwise sorted
	# walk left hull from upper_left counter-clockwise until lower_left is added to ch
	# walk right hull from upper_right clockwise until lower_right is added to ch
	t = 0 # Invariant (init): t determines whether the upper and lower tangents have been visited
	i = utan[0] # Invariant (init): i is the index of the current point on the left hull
	while t < 2:
		ch.append(a[i])
		# Invariant (maintenance): Shows movement through left hull
		if a[i] == upper_left or a[i] == lower_left:
			t += 1
		i = (i - 1) % len(a)

	t = 0 # Invariant (init): t determines whether the upper and lower tangents have been visited
	i = utan[1] # Invariant (init): i is the index of the current point on the right hull
	while t < 2:
		ch.append(b[i])
		# Invariant (maintenance): Shows movement through right hull
		if b[i] == upper_right or b[i] == lower_right:
			t += 1
		i = (i + 1) % len(b)

	return ch

'''
Returns a tuple of the start- and endpoint of the upper tangent.
'''
def upper_tangent(a, b, m, y3, y4):
	# Invariants (init):
	i = len(a) - 1 # init with rightmost index of 'a'
	j = 0 # init with leftmost index of 'b'

	while yint(a[i], b[(j + 1) % (len(b))], m, y3, y4) > yint(a[i], b[j], m, y3, y4) or \
	yint(a[(i - 1) % (len(a))], b[j], m, y3, y4) > yint(a[i], b[j], m, y3, y4):
		# Invariant (maintenance): Demonstrates clockwise movement through points
		if yint(a[i], b[(j + 1) % (len(b))], m, y3, y4) > yint(a[i], b[j], m, y3, y4):
			# move right "finger" clockwise
			j = (j + 1) % (len(b))
		# Invariant (maintenance): Demonstrates counter-clockwise movement through points
		else:
			# move left "finger" counter-clockwise
			i = (i - 1) % (len(a))

	return (i, j)

'''
Returns a tuple of the start- and endpoint of the lower tangent.
'''
def lower_tangent(a, b, m, y3, y4):
	# Invariants (init):
	k = len(a) - 1 # init with rightmost index of 'a'
	z = 0 # init with leftmost index of b

	while yint(a[k], b[(z - 1) % (len(b))], m, y3, y4) < yint(a[k], b[z], m, y3, y4) or \
	yint(a[(k + 1) % (len(a))], b[z], m, y3, y4) < yint(a[k], b[z], m, y3, y4):
		# Invariant (maintenance): Demonstrates counter-clockwise movement through points
		if yint(a[k], b[(z - 1) % (len(b))], m, y3, y4) < yint(a[k], b[z], m, y3, y4):
			# move left "finger" counter-clockwise
			k = (k - 1) % (len(a))
		# Invariant (maintenance): Demonstrates clockwise movement
		else:
			z = (z + 1) % (len(b))

	return (k, z)

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm.
'''
def computeHull(points):
	startTime = time.time()
	# simple case
	if len(points) <= 3:
		endTime = time.time() - startTime
		print("Time: " + str(endTime) + " seconds")
		return points

	# sort points by their x coordinates
	points.sort(key = lambda p: p[0])

	def hull(points):
		# base case(s) -> compute hull with brute force
		# Invariant (termination): Base case, simple convex hull is returned
		if len(points) <= 3:
			return points
		# Invariant (termination): Base case, naive convex hull is returned
		if len(points) < 11:
			return brute(points)
		if len(points) > 999:
			return []

		# midpoint index of the points list
		m = int(math.floor(len(points) / 2))
		# left half
		a = points[:m]
		# right half
		b = points[m:]

		return mergeHulls(hull(a), hull(b), m)

	convex_hull = hull(points)
	clockwiseSort(convex_hull)
	endTime = time.time() - startTime
	print("Time: " + str(endTime) + " seconds")
	return convex_hull

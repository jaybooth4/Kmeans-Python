dimensions = input('Please Enter Dimensions: ')
clusters = input('Please Enter Number of Clusters: ')
iterations = input('Please Enter Number of Iterations: ')

import random
import collections
import numpy
import matplotlib.pylab as plt

def ReadIn():
	points = []
	with open("input2D.txt", "r") as f:
		for line in f:
			points.append(line.replace("\n", "").split(" "))
	for i in range(len(points)):	
		points[i] = map(int, points[i])
	return points
	
def AssignCenters(points):
	centers = []
	rand_numbers = random.sample(range(0, len(points)), clusters)
	for center in rand_numbers:
		centers.append(points[center])
	return centers
	
def GetAssignments(centers, points):
	distances = []
	closest_centers = []
	distance = 0
	for point in range(len(points)):
		for center in range(len(centers)):
			for dim in range(dimensions):
				distance += abs(centers[center][dim] - points[point][dim])
			distances.append(distance)
			distance = 0
		assignment = distances.index(min(distances))
		closest_centers.append(assignment)
 		distances = []
	return closest_centers

def AdjustPoints(assignments, points):
	num_points_per_cluster = [0] * clusters
	sums = [[0.0] * dimensions for i in range(clusters)]
	centers = [[0.0] * dimensions for i in range(clusters)]
	for cluster_id in range(clusters):
		for point in range(len(assignments)):
			if assignments[point] == cluster_id:
				num_points_per_cluster[cluster_id] += 1
				for dim in range(dimensions):
					sums[cluster_id][dim] += points[point][dim]
	for center in range(len(sums)):
		for dim in range(dimensions):
			centers[center][dim] = (sums[center][dim]/num_points_per_cluster[center])
	return centers
	
def Visualize(points, centers, assignments):
	x_points = numpy.array([coord[0] for coord in points])
	y_points = numpy.array([coord[1] for coord in points])
	center_x_points = numpy.array([coord[0] for coord in centers])
	center_y_points = numpy.array([coord[1] for coord in centers])
	plt.figure(1)
	plt.scatter(x_points,y_points,c=assignments,edgecolor='k',s=45)
	plt.hold(True)
	plt.scatter(center_x_points,center_y_points,marker='*',color='r',edgecolor='b',s=500,label='Centroids')
	plt.grid(True)
	plt.title('K-Means Clustering',fontsize=30)
	plt.xlabel('X-axis',fontsize=25)
	plt.ylabel('Y-axis',fontsize=25)
	#plt.yticks([0,50,100,150,200,250,300,350], fontsize = 21)
	#plt.xticks([200,250,300,350,400,450], fontsize = 21)
	plt.legend(prop={'size':25})
	plt.hold(False)
	plt.show()

def main():
	points = []
	points = ReadIn()
	centers = AssignCenters(points)
	iteration = 0
	assignments = []
	new_centers = []
	while(iteration < iterations and not centers == new_centers):
		if iteration == 0:
			assignments = GetAssignments(centers, points)
			new_centers = AdjustPoints(assignments, points)
			iteration += 1
		else:
			centers = new_centers
			assignments = GetAssignments(centers, points)
			new_centers = AdjustPoints(assignments, points)	
			iteration += 1	
	print "Done! Assignments: ", assignments
	if dimensions == 2:
		Visualize(points, centers, assignments) 
main()

#	for i in range(len(points)):
#		print points[i]
#	for i in range(len(centers)):
#		print centers[i]

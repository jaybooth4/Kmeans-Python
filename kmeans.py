dimensions = input('Please Enter Dimensions: ')
clusters = input('Please Enter Number of Clusters: ')
iterations = input('Please Enter Number of Iterations: ')

import random #For random numbers
import numpy #Science library for numpy arrays
import matplotlib.pylab as plt #For displaying results

def ReadIn(): # Reads in points
	points = []
	with open("input2D.txt", "r") as f:
		for line in f: #Each line
			points.append(line.replace("\n", "").split(" ")) 
			#Get rid of \n, break at " " and add to list
	for i in range(len(points)):	
		points[i] = map(int, points[i]) #Convert into a list
	return points
	
def AssignCenters(points): #Assign initial centers
	centers = []
	rand_numbers = random.sample(range(0, len(points)), clusters) 
	#Random initial centers
	for center in rand_numbers:
		centers.append(points[center])
	return centers
	
def GetAssignments(centers, points): #Closest centers to each point
	distances = []
	closest_centers = []
	distance = 0
	for point in range(len(points)): #Each point
		for center in range(len(centers)): #Each center
			for dim in range(dimensions): #Each dimension 
				distance += abs(centers[center][dim] - points[point][dim])
			distances.append(distance) #List of distances
			distance = 0 #Reset
		assignment = distances.index(min(distances)) #Assign to min
		closest_centers.append(assignment)
 		distances = []
	return closest_centers

def AdjustPoints(assignments, points): #Recalculate centers
	num_points_per_cluster = [0] * clusters #List of specific length
	sums = [[0.0] * dimensions for i in range(clusters)] #Float list
	centers = [[0.0] * dimensions for i in range(clusters)]
	for cluster_id in range(clusters): #For each cluster
		for point in range(len(assignments)): #For each point
			if assignments[point] == cluster_id: 
				#If assigned to specific cluster
				num_points_per_cluster[cluster_id] += 1
				for dim in range(dimensions): #Calculate sum
					sums[cluster_id][dim] += points[point][dim]
	for center in range(len(sums)):
		for dim in range(dimensions):
			#Assign new centers to average
			centers[center][dim] = (sums[center][dim]/num_points_per_cluster[center])
	return centers
	
def Visualize(points, centers, assignments): #Create Kmeans visual
	x_points = numpy.array([coord[0] for coord in points]) #Numpy array
	y_points = numpy.array([coord[1] for coord in points])
	center_x_points = numpy.array([coord[0] for coord in centers])
	center_y_points = numpy.array([coord[1] for coord in centers])
	plt.figure(1)
	plt.scatter(x_points,y_points,c=assignments,edgecolor='k',s=45) #Plot points
	plt.hold(True)
	#plot centroids
	plt.scatter(center_x_points,center_y_points,marker='*',color='r',edgecolor='b',s=500,label='Centroids')
	plt.grid(True)
	plt.title('K-Means Clustering',fontsize=30)
	plt.xlabel('X-axis',fontsize=25)
	plt.ylabel('Y-axis',fontsize=25)
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
	#While loop: When under max iterations and unique centers produced
	while(iteration < iterations and not centers == new_centers):
		if iteration == 0: #First iteration case
			assignments = GetAssignments(centers, points)
			new_centers = AdjustPoints(assignments, points)
			iteration += 1
		else:
			centers = new_centers
			assignments = GetAssignments(centers, points)
			new_centers = AdjustPoints(assignments, points)	
			iteration += 1	
	print "Done! Assignments: ", assignments
	if dimensions == 2: #Can only visualize 2D
		Visualize(points, centers, assignments) 
main()


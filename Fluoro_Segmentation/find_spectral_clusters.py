from sklearn.cluster import SpectralClustering 
import matplotlib.pyplot as plt


# from sklearn.preprocessing import StandardScaler
#did not work well, most likely because clusters don't have similar density 
def find_spectral_clusters(maximas, min_sample, y = 1024, x =1280 ):
	spectral= SpectralClustering(n_clusters=min_sample, eigen_solver='arpack',
								 affinity="nearest_neighbors")
	spectral.fit(maximas)
	labels = spectral.labels_
	centroids = [] # spectral.cluster_centers_
	"""
	print('labels are ', labels)
	
	plt.scatter(maximas[:, 1], maximas[:, 0], c=labels, cmap='viridis')
	plt.title('find_spectral_clusters')
	plt.xlim(0,x)
	plt.ylim(y,0)
	plt.xlabel(r'$x$')
	plt.ylabel(r'$y$')
	plt.show()
	"""
	return centroids, labels
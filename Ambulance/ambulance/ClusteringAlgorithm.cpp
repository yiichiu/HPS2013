#include "ClusteringAlgorithm.h"
#include <math.h>
#include <iostream>

ClusteringAlgorithm::ClusteringAlgorithm(Hospitals *hosps, Persons *psons)
{
	_hosps = hosps;
	_psons = psons;
	
	_numClusters = hosps->getCount();
	_numDimensions = 2;
	_numPoints = psons->getCount();

	for (long ptc = 0; ptc < _numPoints; ++ptc)
		_pointsToClusters.push_back(0);

	ClusterId i = 0;
	for (; i < _numClusters; i++) {
		SetPoints set_of_points;

		// init clusterId -> set of points
		_clustersToPoints.push_back(set_of_points);
	}
}


ClusteringAlgorithm::~ClusteringAlgorithm(void)
{
}

// obsolete
void
ClusteringAlgorithm::cluster(Hospitals *hosps, Persons *psons) {

	//init(hosps, psons);



/*	long personsCount = psons->getCount();
	long hospCount = hosps->getCount();
	int i, x, y;
	long step = personsCount / hospCount;
	for (i=0; i<hospCount; ++i) {
		Person p = psons->getPerson(i * step);
		x = p._x;
		y = p._y;
		hosps->setHospitalCoordinates(i, x, y);
	}
*/
}

long
ClusteringAlgorithm::distance(const Person &p1, const Person &p2) {
	// no need to do square root because all calculations will be proportional
	return pow(p1._x - p2._x, 2) + pow(p1._y - p2._y, 2);
}

long
ClusteringAlgorithm::distance(const Hospital &h, const Person &p) {
	// no need to do square root because all calculations will be proportional
	return pow(h._x - p._x, 2) + pow(h._y - p._y, 2);
}

//
// Compute Centroids
//
void ClusteringAlgorithm::compute_centroids() {

	///*Dimensions*/ unsigned int i;	// number of dimensions, should be two
    ClusterId cid = 0;	// id of the cluster
    PointId numPointsInCluster;	// id of this point
    // For each centroid
    for (cid=0; cid<_hosps->getCount(); ++cid) {

		numPointsInCluster = 0;
		Hospital h = _hosps->getHospital(cid);
		int x = h._x, y = h._y;
		// For earch PointId in this set
		SetPoints &ctp = _clustersToPoints[cid];
		for (SetPoints::iterator iter=ctp.begin(); iter!=ctp.end(); ++iter) {
			Person p = _psons->getPerson((*iter));
			x += p._x;
			y += p._y;	
			++numPointsInCluster;
		}
		//
		// if no point in the clusters, this goes to inf (correct!)
		//
		_hosps->setHospitalCoordinates(cid, x/numPointsInCluster, y/numPointsInCluster);
	}
}

//
// Initial partition points among available clusters
//
void ClusteringAlgorithm::initial_partition_points() {
    
	ClusterId cid;

	for (long pid = 0; pid < _psons->getCount(); ++pid) {
		cid = pid % _numClusters;
		_pointsToClusters[pid] = cid;
		_clustersToPoints[cid].insert(pid);
	}
}

//
// k-means
//
void ClusteringAlgorithm::k_means() {

	bool move;
	bool some_point_is_moving = true;
	unsigned int num_iterations = 0;
	PointId pid;
	ClusterId cid, to_cluster;
	Distance d, min;

	//
	// Initial partition of points
	//
	initial_partition_points();

	//
	// Until not converge
	//
	while (some_point_is_moving) {

		std::cout << std::endl << "*** Num Iterations " 
			<< num_iterations  << std::endl << std::endl ;;

		some_point_is_moving = false;

		compute_centroids();
		//      std::cout << "Centroids" << std::endl << centroids__;      

		//
		// for each point
		//
		for (pid=0; pid<_numPoints; pid++) {
			// distance from current cluster
			Hospital h = _hosps->getHospital(_pointsToClusters[pid]);
			Person p = _psons->getPerson(pid);
			min = ClusteringAlgorithm::distance(h, p);

			std::cout << "pid[" << pid << "] in cluster=" 
				<< _pointsToClusters[pid] 
				<< " with distance=" << min << std::endl;

			//
			// foreach centroid
			//
			cid = 0; 
			move = false;
			for (long c = 0; c<_numClusters; ++c) {
				Hospital h1 = _hosps->getHospital(c);
				Person p1 = _psons->getPerson(pid);
				d = ClusteringAlgorithm::distance(h1, p1);
				if (d < min) {
					min = d;
					move = true;
					to_cluster = cid;
					// remove from current cluster
					_clustersToPoints[_pointsToClusters[pid]].erase(pid);

					some_point_is_moving = true;
					std::cout << "\tcluster=" << cid 
						<< " closer, dist=" << d << std::endl;	    
				}
				cid++;
			}
	
			//
			// move towards a closer centroid 
			//
			if (move) {
				// insert
				_pointsToClusters[pid] = to_cluster;
				_clustersToPoints[to_cluster].insert(pid);
				std::cout << "\t\tmove to cluster=" << to_cluster << std::endl;
			}
		}      

		num_iterations++;
	} // end while (some_point_is_moving)

	//std::cout << std::endl << "Final clusters" << std::endl;
	//std::cout << clusters_to_points__;
}

void ClusteringAlgorithm::zero_centroids() {
	// nothing to do here, all the points should already be zero

	/*BOOST_FOREACH(Centroids::value_type& centroid, centroids__) {
		BOOST_FOREACH(Point::value_type& d, centroid) {
			d = 0.0;
		}
	}*/
}
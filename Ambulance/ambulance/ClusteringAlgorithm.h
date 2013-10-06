#ifndef _CLUSTERING_ALGO_H_
#define _CLUSTERING_ALGO_H_

#include "Hospitals.h"
#include "Persons.h"
#include <set>

typedef unsigned int ClusterId;  // the id of this cluster
typedef long Distance;			 // distance
typedef unsigned int PointId;    // the id of this point
typedef std::vector<Person> Centroids;
// PointId -> ClusterId
typedef std::vector<ClusterId> PointsToClusters;

typedef std::set<PointId> SetPoints; // set of points
  
// ClusterId -> (PointId, PointId, PointId, .... )
typedef std::vector<SetPoints> ClustersToPoints;

class ClusteringAlgorithm
{
public:
	ClusteringAlgorithm(Hospitals *hosps, Persons *psons);
	virtual ~ClusteringAlgorithm(void);

	void cluster(Hospitals *h, Persons *p);
	void k_means();
	static long distance(const Person &p1, const Person &p2);
	static long distance(const Hospital &h, const Person &p);

private:
	void compute_centroids();
	void initial_partition_points();
	void zero_centroids();
	//void init(Hospitals *hosps, Persons *psons);

	//Centroids _centroids; // our centroids are hospitals!
	ClustersToPoints _clustersToPoints;
	PointsToClusters _pointsToClusters;

	long _numClusters;
	int _numDimensions;
	long _numPoints;
	Hospitals *_hosps;
	Persons *_psons;
};

#endif // _CLUSTERING_ALGO_H_
#ifndef _CLUSTERING_ALGO_H_
#define _CLUSTERING_ALGO_H_

#include "Hospitals.h"
#include "Persons.h"

class ClusteringAlgorithm
{
public:
	ClusteringAlgorithm(void);
	virtual ~ClusteringAlgorithm(void);

	void cluster(Hospitals *h, Persons *p);
};

#endif // _CLUSTERING_ALGO_H_
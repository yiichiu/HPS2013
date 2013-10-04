#include "ClusteringAlgorithm.h"


ClusteringAlgorithm::ClusteringAlgorithm(void)
{
}


ClusteringAlgorithm::~ClusteringAlgorithm(void)
{
}

void
ClusteringAlgorithm::cluster(Hospitals *hosps, Persons *psons) {
	long personsCount = psons->getCount();
	long hospCount = hosps->getCount();
	int i, x, y;
	long step = personsCount / hospCount;
	for (i=0; i<hospCount; ++i) {
		Person p = psons->getPerson(i * step);
		x = p._x;
		y = p._y;
		hosps->setHospitalCoordinates(i, x, y);
	}
}
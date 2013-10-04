#include "SimpleAlgorithm.h"


SimpleAlgorithm::SimpleAlgorithm(void)
{
}


SimpleAlgorithm::~SimpleAlgorithm(void)
{
}

void
SimpleAlgorithm::runAlgorithm(const Hospitals *h, const Persons *p) {
	int hospitalCount = h->getCount();

	Hospital hosp = h->getHospital(0);
	int ambulanceNum = hosp._ambulanceCount;

}

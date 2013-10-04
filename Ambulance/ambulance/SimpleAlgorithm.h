#pragma once

#include "Hospitals.h"
#include "Persons.h"

class SimpleAlgorithm
{
public:
	SimpleAlgorithm(void);
	virtual ~SimpleAlgorithm(void);

	void runAlgorithm(const Hospitals *hospitals, const Persons *persons);
};


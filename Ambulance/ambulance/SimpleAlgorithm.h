#ifndef _SIMPLE_ALGORITHM_H_
#define _SIMPLE_ALGORITHM_H_

#include "Hospitals.h"
#include "Persons.h"
#include "Ambulances.h"
#include <set>

class SimpleAlgorithm
{
public:
	SimpleAlgorithm(void);
	virtual ~SimpleAlgorithm(void);
	
	void initAmbulances(const Hospitals *hosps);

	void runAlgorithm(const Hospitals *hospitals, const Persons *persons);

private:
	void runAmbulance(Ambulance &amb);
	void initUnsavedPersons();
	bool canSavePerson(int currTime, Ambulance amb, long pIndex);
	int savePerson(Ambulance &amb, long pIndex);
	Ambulances _ambulances;
	const Persons *_psons;
	const Hospitals *_hosps;
	std::set<long> _unsaved;

};

#endif // _SIMPLE_ALGORITHM_H_
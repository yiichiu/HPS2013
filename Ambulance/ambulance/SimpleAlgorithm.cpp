#include "SimpleAlgorithm.h"
#include <iostream>


SimpleAlgorithm::SimpleAlgorithm(void)
{
}


SimpleAlgorithm::~SimpleAlgorithm(void)
{
}

void
SimpleAlgorithm::initAmbulances(const Hospitals *hosps) {

	for (long i=0; i<hosps->getCount(); ++i) {
		Hospital h = hosps->getHospital(i);
		_ambulances.addAmbulances(h);
	}
}

long getDistance(const Hospital &h, const Person &p) {
	return abs(h._x - p._x) + abs(h._y - p._y);
}

bool
SimpleAlgorithm::canSavePerson(int currTime, Ambulance amb, long pIndex) {
	Person p = _psons->getPerson(pIndex);
	long distance = getDistance(amb._h, p);
	long timeToSave = distance * 2 + 1 + 1;
	if (timeToSave + currTime <= p._rescuetime)
		return true;

	return false;
}

int
SimpleAlgorithm::savePerson(Ambulance &amb, long pIndex)
{
	Person p = _psons->getPerson(pIndex);
	long distance = getDistance(amb._h, p);
	long timeToSave = distance * 2 + 1 + 1;
	std::cout << "Saved person " << pIndex << " by ambulance " << amb._id << std::endl;
	return timeToSave;
}

void
SimpleAlgorithm::runAmbulance(Ambulance &amb)
{
	int time=0;
	for (std::set<long>::iterator iter=_unsaved.begin(); iter != _unsaved.end();)
	{
		long pIndex = (*iter);
		if (canSavePerson(time, amb, pIndex))
		{
			time += savePerson(amb, pIndex);
			std::set<long>::iterator itertmp = iter;
			iter++;
			_unsaved.erase(itertmp);
		}
		else
		{
			iter++;
		}
	}
}

void
SimpleAlgorithm::initUnsavedPersons()
{
	for (long i=0; i<_psons->getCount(); ++i)
	{
		_unsaved.insert(i);
	}
}

void
SimpleAlgorithm::runAlgorithm(const Hospitals *h, const Persons *p) {

	_psons = p;
	_hosps = h;
	initUnsavedPersons();
	initAmbulances(h);
	for (long a=0; a<_ambulances.getCount(); ++a)
	{
		Ambulance amb = _ambulances.getAmbulance(a);
		runAmbulance(amb);
	}

}

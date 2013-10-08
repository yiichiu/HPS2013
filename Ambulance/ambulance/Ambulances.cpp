#include "Ambulances.h"


Ambulances::Ambulances(void)
{
}


Ambulances::~Ambulances(void)
{
}

void
Ambulances::addAmbulances(Hospital h) {
	for (int i=0; i<h._ambulanceCount; ++i) {
		Ambulance a(h);
		a._h = h;
		a._id = _ambulances.size();
		_ambulances.push_back(a);
	}
}

long
Ambulances::getCount() const {
	return _ambulances.size();
}

Ambulance
Ambulances::getAmbulance(long i) const {
	return _ambulances[i];
}



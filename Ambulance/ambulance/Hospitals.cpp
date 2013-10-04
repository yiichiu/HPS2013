#include "Hospitals.h"


Hospitals::Hospitals(void)
{
}


Hospitals::~Hospitals(void)
{
}

// TODO: clustering algorithm here
void
Hospitals::placeHospitals() {
	for (long i=0; i<_hospitals.size(); ++i) {
		_hospitals[i]._x = i;
		_hospitals[i]._y = i;
	}
}
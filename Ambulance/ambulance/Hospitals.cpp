#include "Hospitals.h"
#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string.h>

Hospitals::Hospitals(void)
{
}


Hospitals::~Hospitals(void)
{
}

void
Hospitals::setHospitalCoordinates(int hnum, int x, int y)
{
	Hospital &h = _hospitals[hnum];
	h._x = x;
	h._y = y;
}

void
Hospitals::printHospitals() {
	for (long i=0; i<_hospitals.size(); ++i) {
		std::cout << _hospitals[i]._x << " " << _hospitals[i]._y << " " << _hospitals[i]._ambulanceCount << std::endl;
	}
}

void
Hospitals::outputHospitals(const char *fileName) const {

	std::ofstream f;
	f.open(fileName);
	for (long i=0; i<_hospitals.size(); ++i) {
		f << _hospitals[i]._x << " " << _hospitals[i]._y << std::endl;
	}

	f.close();
}
#ifndef _HOSPITALS_H_
#define _HOSPITALS_H_

#include <vector>
#include "Hospital.h"
#include <string.h>

class Hospitals
{
public:
	Hospitals();
	virtual ~Hospitals();
	void outputHospitals(const char *fileName) const;
	void addHospital(Hospital h) {
		_hospitals.push_back(h);
	}

	long getCount() const {
		return _hospitals.size();
	}

	Hospital getHospital(int i) const {
		return _hospitals[i];
	}

	void setHospitalCoordinates(int hnum, int x, int y);

	void printHospitals();

private:
	std::vector<Hospital> _hospitals;
};

#endif // _HOSPITALS_H_
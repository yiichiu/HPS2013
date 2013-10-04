#pragma once

#include <vector>
#include "Hospital.h"

class Hospitals
{
public:
	Hospitals(void);
	virtual ~Hospitals(void);

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


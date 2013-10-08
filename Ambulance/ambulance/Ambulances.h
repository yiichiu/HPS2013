#ifndef _AMBULANCES_H_
#define _AMBULANCES_H_

#include "Hospitals.h"
#include <vector>

class Ambulance {
public:
	Ambulance(Hospital h) : _h(Hospital(h._x, h._y, h._ambulanceCount)) {}
	Hospital _h;
	int _id;
};

class Ambulances
{
public:
	Ambulances(void);
	virtual ~Ambulances(void);
	void addAmbulances(Hospital h);
	long getCount() const;
	Ambulance getAmbulance(long i) const;

private:
	std::vector<Ambulance> _ambulances;
};

#endif // _AMBULANCES_H_
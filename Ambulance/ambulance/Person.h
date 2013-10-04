#ifndef _PERSON_H_
#define _PERSON_H_

#include <cstdlib>
#include "Hospital.h"

class Person
{
public:
	Person(void);
	Person(int x, int y, int rescuetime);
	virtual ~Person(void);

	int _x, _y, _rescuetime;

	bool canBeRescuedByHospital(const Hospital &h);
	bool canBeRescuedInTime(int x, int y) {
		return _rescuetime >= abs(x - _x) + abs(y - _y);
	}
};

#endif	// _PERSON_H_
#include "Person.h"


Person::Person(void)
{
}

Person::Person(int x, int y, int rescuetime) : _x(x), _y(y), _rescuetime(rescuetime) {
}

Person::~Person(void)
{
}

bool
Person::canBeRescuedByHospital(const Hospital &h) {
	int rescueTime = 2 * (abs(h._x - _x) + abs(h._y	- _y)) + 1;

	return rescueTime <= _rescuetime;
}

#pragma once

#include <vector>
#include "Person.h"

class Persons
{
public:
	Persons(void);
	virtual ~Persons(void);
	void addPerson(Person p) {
		_persons.push_back(p);
	}

	long getCount() const {
		return _persons.size();
	}

private:
	std::vector<Person> _persons;
};


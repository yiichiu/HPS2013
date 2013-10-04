#ifndef _FILE_READER_H_
#define _FILE_READER_H_

#include "Persons.h"
#include "Hospitals.h"
#include <string>

class FileReader
{
public:
	FileReader(void);
	void readFile(const char *fileName, Persons *persons, Hospitals *hospitals);
	virtual ~FileReader(void);

private:
	void addPerson(Persons *persons, const std::string &line) const;
	void addHospital(Hospitals *hospitals, const std::string &line) const;
};


#endif // _FILE_READER_H_


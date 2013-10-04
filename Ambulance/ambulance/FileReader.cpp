#include "FileReader.h"
#include <fstream>
#include <string.h>
#include <vector>

FileReader::FileReader(void)
{
}


FileReader::~FileReader(void)
{
}

void
FileReader::addHospital(Hospitals *hospitals, const std::string &line) const {
	int ambNum = atoi(line.c_str());
	if (ambNum > 0) {
		hospitals->addHospital(Hospital(0, 0, ambNum));
	}
}

void
FileReader::addPerson(Persons *persons, const std::string &line) const {
	char *str = new char[line.size() + 1];
	strcpy(str, line.c_str());
	char * pch = strtok (str,", \t");
	std::vector<int> vec;
	while (pch != NULL)
	{
		vec.push_back(atoi(pch));
		pch = strtok (NULL, ", \t");
	}
	if (vec.size() == 3) {
		persons->addPerson(Person(vec[0], vec[1], vec[2]));
	}
	delete [] str;
}

void
FileReader::readFile(const char *fileName, Persons *persons, Hospitals *hospitals) {
	bool personMode = false;
	bool hospMode = false;
	std::string line;
	std::ifstream input(fileName);
	while (std::getline(input, line)) {
		if (strncmp(line.c_str(), "person", 6) == 0) {
			personMode = true;
			hospMode = false;
		}
		else if (strncmp(line.c_str(), "hospital", 8) == 0) {
			personMode = false;
			hospMode = true;
		}
		else {
			if (personMode) {
				addPerson(persons, line);
			}
			if (hospMode) {
				addHospital(hospitals, line);
			}
		}
	}
	input.close();
}

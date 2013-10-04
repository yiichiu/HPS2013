// UnitTester.cpp : Defines the entry point for the console application.
//

#include "..\ambulance\Person.h"
#include "..\ambulance\FileReader.h"

#include <stdio.h>

void runTestFileReader() {
	printf("runTestFileReader\n");
	FileReader fr;
	Persons p;
	Hospitals h;
	fr.readFile("ambusamp2010", &p, &h);
	if (p.getCount() != 300)
		printf("test failed\n");
	else
		printf("test succeeded\n");
	
	if (h.getCount() != 5)
		printf("test failed\n");
	else
		printf("test succeeded\n");

}

void runTestPerson() {
	printf("runTestPerson\n");
	Person p(1, 1, 3);
	if (p.canBeRescuedInTime(1, 1))
		printf("test successful\n");
	else
		printf("test unsuccessful\n");

	if (p.canBeRescuedInTime(2, 2))
		printf("test successful\n");
	else
		printf("test unsuccessful\n");

	if (p.canBeRescuedInTime(3, 2))
		printf("test successful\n");
	else
		printf("test unsuccessful\n");

	if (!p.canBeRescuedInTime(3, 3))
		printf("test successful\n");
	else
		printf("test unsuccessful\n");

}

int main(int argc, char* argv[])
{
	runTestPerson();
	runTestFileReader();
	return 0;
}


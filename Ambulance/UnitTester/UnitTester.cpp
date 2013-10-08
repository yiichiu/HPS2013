// UnitTester.cpp : Defines the entry point for the console application.
//

#include "..\ambulance\Person.h"
#include "..\ambulance\FileReader.h"
#include "..\ambulance\ClusteringAlgorithm.h"
#include "..\ambulance\Ambulances.h"
#include "..\ambulance\SimpleAlgorithm.h"

#include "GridPrinter.h"

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

void printGrid() {
	FileReader fr;
	Persons p;
	Hospitals h;
	fr.readFile("ambusamp2010.txt", &p, &h);

	ClusteringAlgorithm cl(&h, &p);
	cl.k_means();
	GridPrinter grp;
	grp.printGrid("grid.txt", &h, &p);
	grp.printHospitals(&h);
}

void test2Persons1Hosp() {
	FileReader fr;
	Persons p;
	Hospitals h;
	fr.readFile("test2persons.txt", &p, &h);
	ClusteringAlgorithm cl(&h, &p);
	cl.k_means();
	GridPrinter grp;
	grp.printGrid("grid2persons.txt", &h, &p);
}

void runTestAmbulances() {
	printf("runTestAmbulances\n----------------\n");
	FileReader fr;
	Persons p;
	Hospitals h;
	fr.readFile("ambusamp2010.txt", &p, &h);

	Ambulances ambs;
	for (long i=0; i < h.getCount(); ++i) {
		ambs.addAmbulances(h.getHospital(i));
	}
	if (ambs.getCount() == 41)
		printf("success\n");
	else
		printf("test failed\n");
	
}

void test3Persons2Hosp() {
	FileReader fr;
	Persons p;
	Hospitals h;
	fr.readFile("test3persons.txt", &p, &h);
	ClusteringAlgorithm cl(&h, &p);
	cl.k_means();
	GridPrinter grp;
	grp.printGrid("grid3persons.txt", &h, &p);
}

void testSimpleAlgorithm() {
	printf("testSimpleAlgorith\n-------------------\n");
	FileReader fr;
	Persons p;
	Hospitals h;
	fr.readFile("test3persons.txt", &p, &h);
	ClusteringAlgorithm cl(&h, &p);
	cl.k_means();
	SimpleAlgorithm algo;
	algo.runAlgorithm(&h, &p);
}

int main(int argc, char* argv[])
{
	//runTestPerson();
	//runTestFileReader();
	//printGrid();
	//runTestAmbulances();
	testSimpleAlgorithm();

	return 0;
}


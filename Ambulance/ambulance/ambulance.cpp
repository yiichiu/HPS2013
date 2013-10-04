// ambulance.cpp : Defines the entry point for the console application.
//
#include "Person.h"
#include <stdlib.h>
#include <iostream>
#include "FileReader.h"
#include "SimpleAlgorithm.h"

int main(int argc, char* argv[])
{
	Hospitals h;
	Persons p;

	FileReader fr;
	fr.readFile("ambusamp2010", &p, &h);

	//ClusteringAlgorithm cl;
	//cl.cluster(&h);

	SimpleAlgorithm algo;
	algo.runAlgorithm(&h, &p);

	// value
	// reference
	// pointer
	Hospital h1(5, 6, 7);
	h1._ambulanceCount;

	Hospital *h2 = NULL;
	h2 = new Hospital(6, 6, 6);
	delete(h2);

	h2 = &h1;

	return 0;
}


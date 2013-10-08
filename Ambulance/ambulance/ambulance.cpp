// ambulance.cpp : Defines the entry point for the console application.
//
#include "Person.h"
#include <stdlib.h>
#include <iostream>
#include "FileReader.h"
#include "SimpleAlgorithm.h"
#include "ClusteringAlgorithm.h"

int main(int argc, char* argv[])
{
	Hospitals h;
	Persons p;

	FileReader fr;
	fr.readFile("input", &p, &h);

	ClusteringAlgorithm cl(&h, &p);
	cl.k_means();

	h.outputHospitals("hospitals.txt");

	return 0;
}


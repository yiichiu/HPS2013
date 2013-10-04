// ambulance.cpp : Defines the entry point for the console application.
//
#include "Person.h"
#include <stdlib.h>
#include <iostream>
#include "FileReader.h"

int main(int argc, char* argv[])
{
	Hospital h(5, 5, 5);
	Person p(0, 0, 21);

	printf("can be rescued: %d\n", p.canBeRescuedByHospital(h));
	return 0;
}


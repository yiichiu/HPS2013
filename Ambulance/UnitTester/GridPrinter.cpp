#include "GridPrinter.h"
#include <fstream>

GridPrinter::GridPrinter(void)
{
}


GridPrinter::~GridPrinter(void)
{
}

void
GridPrinter::printGrid(const std::string &fileName, const Hospitals *hosps, const Persons *psons) const {
	char arr[100][100];
	std::ofstream f;
	f.open(fileName.c_str());

	for (int x=0; x<100; ++x) {
		for (int y=0; y<100; ++y) {
			arr[x][y] = ' ';
		}
	}

	for (long i=0; i<psons->getCount(); ++i) {
		Person p = psons->getPerson(i);
		arr[p._x-1][p._y-1] = '.';
	}

	for (long j=0; j<hosps->getCount(); ++j) {
		Hospital h = hosps->getHospital(j);
		arr[h._x-1][h._y-1] = 'H';

	}

	for (int x=0; x<100; ++x) {
		for (int y=0; y<100; ++y) {
			f << arr[x][y];
		}
		f << std::endl;
	}
	f.close();
}
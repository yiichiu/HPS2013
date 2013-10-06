#ifndef _GRID_PRINTER_H_
#define _GRID_PRINTER_H_

#include "..\ambulance\Hospitals.h"
#include "..\ambulance\Persons.h"

class GridPrinter
{
public:
	GridPrinter(void);
	virtual ~GridPrinter(void);

	void printGrid(const std::string &fileName, const Hospitals *h, const Persons *p) const;
};


#endif // _GRID_PRINTER_H_

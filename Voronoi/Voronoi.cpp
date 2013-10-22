// Voronoi.cpp : Defines the entry point for the console application.
//
#include <vector>
#include <iostream>
#include <istream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <math.h>
#include <stdio.h>
#include <string.h>

#define IS_ZERO(x) (x > -0.000001 && x < 0.000001)
#define PI 3.14159265

struct Move {
	int playerNum;
	int x;
	int y;
};

typedef std::vector<Move> MovesType;

MovesType moves, testMoves;
int player1Score = 0;
int player2Score = 0;
int currPlayer = 0;
int outX = 0;
int outY = 0;
std::string outputString;

void outputFile(const char *fileName)
{
	//std::ofstream f;
	//f.open(fileName);
	std::cout << outputString;

	//f.close();
}

void parseTestMoves(std::string &line)
{

	char *str = new char[line.length() + 1];
	strcpy(str, line.c_str());
	char *pch = strtok(str, ",");
	while (pch != NULL)
	{
		int x = atoi(pch);
		pch = strtok(NULL, ",");
		int y = atoi(pch);
		Move m;
		m.playerNum = currPlayer;
		m.x = x;
		m.y = y;
		testMoves.push_back(m);
		pch = strtok(NULL, ",");
	}
}

void parseMoves(std::string &line)
{
	char *str = new char[line.length() + 1];
	strcpy(str, line.c_str());
	char *pch = strtok(str, ",");
	currPlayer = atoi(pch);
	pch = strtok (NULL, ",");
	int numberOfMoves = atoi(pch);
	
	pch = strtok (NULL, ",");
	while (pch != NULL)
	{
		Move m;
		m.playerNum = atoi(pch);
		pch = strtok (NULL, ",");
		m.x = atoi(pch);
		pch = strtok (NULL, ",");
		m.y = atoi(pch);
		moves.push_back(m);
		pch = strtok (NULL, ",");
	}
}

void parseFile(const char *fileName)
{
	//std::ifstream input(fileName);
	std::string line1, line2;

	std::getline(std::cin, line1);
	std::getline(std::cin, line2);
	//input.close();
	
	parseMoves(line2);
	parseTestMoves(line1);

}

double distance(int x1, int y1, int x2, int y2)
{
	double d = sqrt(pow((double)(x1 - x2), 2) + pow((double)(y1 - y2), 2));
	return d;
}

void calculatePullForPoint(int x, int y)
{
	double pull, pull1 = 0.0, pull2 = 0.0;
	long deltaX, deltaY;
	for (int i=0; i<moves.size(); ++i)
	{
		deltaX = moves[i].x - x;
		deltaX = deltaX * deltaX;
		deltaY = moves[i].y - y;
		deltaY = deltaY * deltaY;
		if (deltaX > 0 || deltaY > 0)
		{
			pull = 1.0 / (deltaX + deltaY);
		}
		else
		{
			pull = 1000000;	// infinity approximation
		}
		if (moves[i].playerNum == 1)
		{
			pull1 += pull;
		}
		else
		{
			pull2 += pull;
		}
	}
	if (pull1 > pull2)
		player1Score += 1;
	else if (pull2 > pull1)
		player2Score += 1;
}

void calculatePull()
{
	for (int x=0; x<1000; ++x)
	{
		for (int y=0; y<1000; ++y)
		{
			calculatePullForPoint(x, y);
		}
	}
}

bool isValidMove(int x, int y)
{
	for (int i=0; i<moves.size(); ++i)
	{
		if (moves[i].x == x && moves[i].y == y)
			return false;
	}
	return true;
}

/*
void testRandom()
{
	int bestp1score = 0; int bestp2score = 0;
	int xtest, ytest;
	for (int i=0; i<10; ++i)
	{
		player1Score = 0;
		player2Score = 0;
		xtest = rand() % 1000;
		ytest = rand() % 1000;
		if (isValidMove(xtest, ytest))
		{
			std::cout << xtest << " " << ytest << std::endl;
			Move m;
			m.playerNum = currPlayer;
			m.x = xtest;
			m.y = ytest;
			moves.push_back(m);
			calculatePull();
			if (currPlayer == 1 && player1Score > bestp1score)
			{
				bestp1score = player1Score;
				outX = xtest;
				outY = ytest;
			}
			else if (currPlayer == 2 && player2Score > bestp2score)
			{
				bestp2score = player2Score;
				outX = xtest;
				outY = ytest;
			}
			std::cout << "p1 score is " << player1Score << " p2 score is " << player2Score << std::endl;
			moves.pop_back();
		}
	}
}
*/

void testCircleStrategy()
{
	int bestp1score = 0; int bestp2score = 0;
	int xtest, ytest;
	for (double deg=0.0; deg < 360.0; deg+= 36.0)
	{
		player1Score = 0;
		player2Score = 0;
		double x = 300 * cos(deg * PI / 180.0);
		double y = 300 * sin(deg * PI / 180.0);
		xtest = 500 + (int)x;
		ytest = 500 + (int)y;
		if (isValidMove(xtest, ytest))
		{
			Move m;
			m.playerNum = currPlayer;
			m.x = xtest;
			m.y = ytest;
			moves.push_back(m);
			calculatePull();
			if (currPlayer == 1 && player1Score > bestp1score)
			{
				bestp1score = player1Score;
				outX = xtest;
				outY = ytest;
			}
			else if (currPlayer == 2 && player2Score > bestp2score)
			{
				bestp2score = player2Score;
				outX = xtest;
				outY = ytest;
			}
			//std::cout << "p1 score is " << player1Score << " p2 score is " << player2Score << std::endl;
			moves.pop_back();
		}
	}
}

void goToCenter()
{
	int x = 500, y = 500;
	if (isValidMove(x, y))
	{
		outX = x;
		outY = y;
		return;
	}
	x = 501;
	y = 501;
	if (isValidMove(x, y))
	{
		outX = x;
		outY = y;
		return;
	}
	outX = 499;
	outY = 499;
}

void runTestMoves()
{
	int bestp1score = 0; int bestp2score = 0;
	
	char tmpstr[100];
	for (int i=0; i<testMoves.size(); ++i)
	{
		player1Score = 0;
		player2Score = 0;
		moves.push_back(testMoves[i]);
		calculatePull();
		if (!outputString.empty())
			outputString += ",";

		sprintf(tmpstr, "%d,%d,%d,%d", testMoves[i].x, testMoves[i].y, player1Score, player2Score);
		outputString += tmpstr;

		moves.pop_back();
	}
}

int main(int argc, char* argv[])
{
	parseFile("input.txt");
	runTestMoves();
	outputFile("output.txt");
	//std::cout << "p1 score is " << player1Score << " p2 score is " << player2Score << std::endl;
	return 0;
}


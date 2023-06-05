//
// Created by Shrekulka on 31.05.2023.
//

#pragma once

#include "pch.h"

#ifndef MATRIXCOPY_ROW_H
#define MATRIXCOPY_ROW_H


class Row
{
protected:
	double* _row;
	unsigned _size;

public:
	Row();

	Row(unsigned, double = 0.0);

	Row(const Row&);

	~Row();

	unsigned size() const;

	void resize(unsigned = 1, double = 0.0);

	double& operator[](unsigned);

	const double& operator[](unsigned) const;

	friend std::istream& operator>>(std::istream&, Row&);

	friend std::ostream& operator<<(std::ostream&, const Row&);

	bool operator==(const Row&) const;

	bool operator!=(const Row&) const;

	const Row& operator=(const Row&);
};


#endif //MATRIXCOPY_ROW_H

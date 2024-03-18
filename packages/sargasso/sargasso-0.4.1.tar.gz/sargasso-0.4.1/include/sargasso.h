#ifndef _SARGASSO_H
#define _SARGASSO_H

#include <iostream>
#include "cblas.h"

namespace sargasso {

template <typename T>
T add(T a, T b);

float sdot(int n, const float* x, const float* y);

} // end namespace sargasso

#endif

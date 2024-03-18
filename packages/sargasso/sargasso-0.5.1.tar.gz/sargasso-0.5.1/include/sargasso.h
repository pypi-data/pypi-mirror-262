#ifndef _SARGASSO_H
#define _SARGASSO_H

#include <iostream>
#include <vector>
#include <string>

namespace sargasso {

template <typename T>
T add(T a, T b);

// Compute dot product of two single precision vectors
// of length *n*.
float sdot(
    int n,
    const float* x,
    const float* y
);

// Compute the eigenvalues of a real symmetric single-
// precision matrix, using the values in the upper
// diagonal
void get_eigvals(
    const int order,
    float* matrix,
    float* eigvals
);

} // end namespace sargasso

#endif

#include <sargasso.h>

// For compatibility of lapack.h (OpenBLAS) with the
// Microsoft Visual Studio compiler, which requires a
// custom definition of complex types.
#ifdef _MSC_VER
#include <complex.h>
#define LAPACK_COMPLEX_CUSTOM
#define lapack_complex_float _Fcomplex
#define lapack_complex_double _Dcomplex
#endif

#include "cblas.h"
#include "lapacke.h"

namespace sargasso {

template <typename T>
T add(T a, T b) {
    return a + b;
}
template int add<int>(int, int);
template float add<float>(float, float);

float sdot(const int n, const float* x, const float* y)
{
    float result = cblas_sdot(n, x, 1, y, 1);
    return result;
}

void get_eigvals(
    const int order,
    float* matrix,
    float* eigvals
){
    lapack_int out = LAPACKE_ssyev(
        LAPACK_ROW_MAJOR, // matrix_layout
        'N',              // jobz ('N': eigvals only)
        'U',              // uplo ('U': upper triangular)
        order,            // n (matrix order)
        matrix,           // a (matrix)
        order,            // lda
        eigvals           // output
    );
    if(out!=0){
        throw std::runtime_error(
            std::string("got nonzero return value ") + std::to_string(out)
        );
    }
}

} // end namespace sargasso

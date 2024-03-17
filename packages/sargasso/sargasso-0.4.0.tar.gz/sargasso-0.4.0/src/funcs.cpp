#include <sargasso.h>

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

} // end namespace sargasso

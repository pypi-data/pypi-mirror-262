#include <sargasso.h>
#include <cassert>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

float sdot(
    const py::array_t<float, py::array::c_style | py::array::forcecast>& x,
    const py::array_t<float, py::array::c_style | py::array::forcecast>& y
){
    py::buffer_info bx = x.request();
    py::buffer_info by = y.request();
    if((bx.ndim!=1)||(by.ndim!=1)){
        throw std::runtime_error("input arrays must be 1D");
    }
    if(bx.shape[0]!=by.shape[0]){
        throw std::runtime_error("input arrays must be the same length");
    }
    const float* ptr_x = static_cast<const float*>(bx.ptr);
    const float* ptr_y = static_cast<const float*>(by.ptr);
    return sargasso::sdot(bx.shape[0], ptr_x, ptr_y);
}

PYBIND11_MODULE(_sargasso, m) {
    m.def("add", &sargasso::add<int>);
    m.def("sdot", &sdot);
}

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

py::array_t<float> get_eigvals(
    const py::array_t<float, py::array::c_style | py::array::forcecast>& x
){
    py::buffer_info bx = x.request();
    if((bx.ndim!=2)||(bx.shape[0]!=bx.shape[1])){
        throw std::runtime_error(
            "input must be square 2D array"
        );
    }
    const int order = static_cast<const int>(bx.shape[0]);
    std::vector<float> matrix(order*order);
    const float* ptrx = static_cast<const float*>(bx.ptr);
    std::memcpy(matrix.data(), ptrx, sizeof(float)*order*order);
    py::array_t<float> eigvals(order);
    sargasso::get_eigvals(order, matrix.data(), eigvals.mutable_data());
    return eigvals;
}

PYBIND11_MODULE(_sargasso, m) {
    m.def("add", &sargasso::add<int>);
    m.def("sdot", &sdot);
    m.def("get_eigvals", &get_eigvals);
}

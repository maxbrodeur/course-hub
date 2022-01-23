#include <Python.h>
#include "caller.h"

int
main()
{
    PyImport_AppendInittab("caller", PyInit_caller);
    Py_Initialize();
    PyImport_ImportModule("caller");
    PyImport_ImportModule("encodings");
    call_quack();
    Py_Finalize();
    return 0;
}
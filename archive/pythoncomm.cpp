//
// Created by Theo Fabi on 2022-01-22.
//




//int pyTest2(){
//    CPyInstance hInstance;
//
//    CPyObject pName = PyUnicode_FromString("test_thing");
////    CPyObject pName = Py_BuildValue("s#", "test_thing", 10);
////    std::cout << pName << std::endl;
//    PyRun_SimpleString("import sys");
//    PyRun_SimpleString("sys.path.append(\".\")");
//    CPyObject pModule = PyImport_ImportModule("test_thing");
//    PyErr_Print();
//
//    if(pModule)
//    {
//        auto val = call_int_function("get_zero", pModule);
//        cout << val << endl;
//        auto val_2 = call_int_function("long_time", pModule);
//        cout << val << endl;
//    }
//    else
//    {
//        printf("ERROR: Module not imported\n");
//    }
//    return 0;
//
//}
//
//int pyTest(){
//    CPyInstance pyobj;
////    PyRun_SimpleString("print('Hello!')");
////    PyRun_SimpleString("import test_thing");
//    return 0;
//}
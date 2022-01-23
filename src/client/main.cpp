#include "pyhelper.h"
#include <Python.h>

#include <QApplication>
#include <QPushButton>
#include <QVBoxLayout>
#include <QTabWidget>
#include "MainWidget.h"
#include "MainTabs.h"
#include <QTabBar>
#include <iostream>

using std::cout;
using std::endl;

long call_int_function(const char *func, CPyObject &module){
    CPyInstance hInstance;
    CPyObject pFunc = PyObject_GetAttrString(module, "get_zero");
    if(pFunc && PyCallable_Check(pFunc)) {
        CPyObject returnVal = PyObject_CallObject(pFunc, nullptr);
        auto return_C = PyLong_AsLong(returnVal);
        return return_C;
    } else {
        PyErr_Print();
        return -1;
    }

}

int pyTest2(){
    CPyInstance hInstance;

    CPyObject pName = PyUnicode_FromString("test_thing");
//    CPyObject pName = Py_BuildValue("s#", "test_thing", 10);
//    std::cout << pName << std::endl;
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(\".\")");
    CPyObject pModule = PyImport_ImportModule("test_thing");
//    CPyObject pModule = PyImport_Import(pName);
    PyErr_Print();

//    cout << PyUnicode_AsUTF8(
//            PyDict_GetItemString(
//                    PyImport_ImportModule("test_thing"),
//                    "__version__"
//            )
//    ) << endl;

    if(pModule)
    {
//        CPyObject pFunc = PyObject_GetAttrString(pModule, "get_zero");
//        if(pFunc && PyCallable_Check(pFunc))
//        {
//            CPyObject pValue = PyObject_CallObject(pFunc, NULL);
//            printf("C: get_zero() = %ld\n", PyLong_AsLong(pValue));
//            CPyObject pFun2 = PyObject_GetAttrString(pModule, "get_another_number");
//            CPyObject Value_2 = PyObject_CallObject(pFun2, NULL);
//            printf("another num: %d", PyLong_AsLong(Value_2));
//        }
//        else
//        {
//            printf("ERROR: function get_zero()\n");
//        }
        auto val = call_int_function("get_zero", pModule);
        cout << val << endl;
        auto val_2 = call_int_function("long_time", pModule);
        cout << val << endl;
    }
    else
    {
        printf("ERROR: Module not imported\n");
    }
    return 0;

}

int pyTest(){
    CPyInstance pyobj;
//    PyRun_SimpleString("print('Hello!')");
//    PyRun_SimpleString("import test_thing");
    return 0;
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    pyTest();
    pyTest2();

    app.setStyleSheet(
//            "QWidget { background-color: white; }"
            "QTabWidget {"
            "background-color: white;"
            "}"
//            "QTabWidget::pane {"
//            "margin-top: -1px;"
//            "margin-bottom: 50px;"
//            "left: -1px;"
//            "}"
            "QDialog {"
            "background: white;"
            "}"
//            "QTabWidget::left-corner {"
//            "height: 10px;"
//            "width: 100px;"
//            "bottom: -1px;"
//            "margin-left: 100px;"
//            "padding: 50px;"
//            "top: 1px;"
//            "}"
//            "QTabWidget::tab-bar:left {"
//            "left: 1 px;"
//            "background: light gray;"
//            "}"
            "QTabBar::tab {"
            "border: none; "
//            "background: gray;"
            "margin-left: 2px; "
            "margin-right: 2px; "
            "font-size: 1px;"
            "}"
//            "QTabBar::tab:selected {"
//            "background: red;"
//            "}"
            );
//    QWidget main;
//    main.setStyleSheet(" background-color: white; ");
//    QVBoxLayout mainLayout;
//
//    QIcon logo;
//    logo.addFile("icons/temp-logo.png", QSize(250,100));
//    auto *logoWidget = new QLabel();
////    logoWidget->setMinimumSize(250, 100);
////    QSizePolicy sizer(QSizePolicy::Expanding, QSizePolicy::Expanding);
////    logoWidget->setSizePolicy(sizer);
//    logoWidget->setPixmap(logo.pixmap(QSize(120,60)));
//    mainLayout.addWidget(logoWidget);

    MainTabs tabs;
    QTabBar bar;
    bar.addTab("hi");
    bar.addTab("hello");
    QPushButton btn("test button");
//    tabs.setStyleSheet("tab::selected { color: red; }");
    tabs.addTab(&btn, "test");
//    mainLayout.addWidget(&tabs);

//    main.setLayout(&mainLayout);
//    main.show();
    tabs.show();
    return app.exec();
}

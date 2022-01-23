#include "pyhelper.h"
//#include <Python.h>
#include <iostream>


//#include "pythoncomm.cpp"
#include <QApplication>
#include <QPushButton>
#include <QVBoxLayout>
#include <QTabWidget>
#include "MainWidget.h"
#include "MainTabs.h"
#include <QTabBar>
//#include <iostream>




using std::cout;
using std::endl;


long call_int_function(const char *func, CPyObject &module){
//    CPyInstance hInstance;
    CPyObject pFunc = PyObject_GetAttrString(module, func);
    if(pFunc && PyCallable_Check(pFunc)) {
        CPyObject returnVal = PyObject_CallObject(pFunc, nullptr);
        auto return_C = PyLong_AsLong(returnVal);
        return return_C;
    } else {
        PyErr_Print();
        return -1;
    }
}

CPyObject* load_module(const char* name){
//    auto inst = new CPyInstance();
    PyRun_SimpleString("import sys; sys.path.append(\".\")");
    auto *pyModule = PyImport_ImportModule(name);
//    module = CPyObject(*PyImport_ImportModule(name));
//    CPyObject pModule = PyImport_ImportModule(name);
    if(!pyModule){
        printf("ERROR: Module not imported\n");
        PyErr_Print();
        return nullptr;
    } else {
        auto *module = new CPyObject(pyModule);
        return module;
    }
}


int py_main_test(){
    CPyInstance hInstance;
    CPyObject *module = load_module("test_thing");
    auto ret = call_int_function("get_zero", *module);
    printf("%d", static_cast<int>(ret));
    delete module;
    return 0;
}






int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    py_main_test();
//    pyTest();
//    pyTest2();

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
//            "QTableWidget::item:selected {"
//            "border: 1 px;"
//            " border-radius: 5px; "
//            "}"
//            "QTableView::item {"
//            " border: 1 px solid #d21919; "
//            " border-radius: 10px; "
//            " }"
//            "QTableWidget {"
//            " gridline-color: gray;"
//            " }"
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
    tabs.calendarTab->schedule->addClass("COMP 360", 2, 7, 3);

//    main.setLayout(&mainLayout);
//    main.show();
    tabs.show();
    tabs.resize(1280,720);
    return app.exec();
}

#include <QApplication>
#include <QPushButton>
#include <QVBoxLayout>
#include <QTabWidget>
#include "MainWidget.h"
#include "MainTabs.h"
#include <QTabBar>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    app.setStyleSheet(
//            "QWidget { background-color: white; }"
            "QTabWidget {"
            "background-color: white;"
            "}"
            "QTabWidget::pane {"
            "margin-top: 10px;"
            "margin-bottom: 50px;"
//            "left: -1px;"
            "}"
            "QDialog {"
            "background: white;"
            "}"
            "QTabWidget::left-corner {"
            "height: 1px;"
            "width: 100px;"
            "bottom: -1px;"
//            "top: 1px;"
            "}"
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
    QWidget main;
    main.setStyleSheet(" background-color: white; ");
    QVBoxLayout mainLayout;

    QIcon logo;
    logo.addFile("icons/temp-logo.png", QSize(250,100));
    auto *logoWidget = new QLabel();
//    logoWidget->setMinimumSize(250, 100);
//    QSizePolicy sizer(QSizePolicy::Expanding, QSizePolicy::Expanding);
//    logoWidget->setSizePolicy(sizer);
    logoWidget->setPixmap(logo.pixmap(QSize(120,60)));
    mainLayout.addWidget(logoWidget);

    MainTabs tabs;
    QTabBar bar;
    bar.addTab("hi");
    bar.addTab("hello");
    QPushButton btn("test button");
//    tabs.setStyleSheet("tab::selected { color: red; }");
    tabs.addTab(&btn, "test");
    mainLayout.addWidget(&tabs);

    main.setLayout(&mainLayout);
    main.show();
//    tabs.show();
    return app.exec();
}

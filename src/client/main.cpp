#include <QApplication>
#include <QPushButton>
#include <QVBoxLayout>
#include <QTabWidget>
#include "MainWidget.h"
#include "MainTabs.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    app.setStyleSheet(
            "QTabWidget {"
            "background-color: white;"
            "}"
            "QTabWidget::pane {"
//            "border: none;"
            "margin-top: 10px;"
            "left: -1px;"
            "}"
//            "top: -1px; }"
            "QDialog {"
            "background: white;"
            "}"
            "QTabWidget::tab-bar:left {"
            "left: 1 px;"
            "background: light gray;"
            "}"
            "QTabBar::tab {"
            "border: none; "
//            "background: gray;"
            "margin-left: 10px; "
            "margin-right: 10px; }"
            "QTabBar::tab:selected {"
//            "background: red;"
            "}"
            );

    MainTabs tabs;
    QPushButton btn("test button");
//    tabs.setStyleSheet("tab::selected { color: red; }");
    tabs.addTab(&btn, "test");
    tabs.show();
    return app.exec();
}

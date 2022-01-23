//
// Created by Theo Fabi on 2022-01-21.
//

#ifndef CORE_UI_MAINWIDGET_H
#define CORE_UI_MAINWIDGET_H

#include <QWidget>
#include <QPushButton>
#include <QVBoxLayout>


class MainWidget : public QWidget {
public:
    explicit MainWidget(QWidget *master = 0);
    virtual ~MainWidget() noexcept;
private:
};


#endif //CORE_UI_MAINWIDGET_H

//
// Created by Theo Fabi on 2022-01-21.
//

#include "MainWidget.h"


MainWidget::MainWidget(QWidget *master) :
    QWidget(master){
//    setFixedSize(100,100);
    auto *btn = new QPushButton("Test", this);
    auto *layout = new QVBoxLayout();
    layout->addWidget(btn);
    setLayout(layout);
}

MainWidget::~MainWidget() noexcept = default;
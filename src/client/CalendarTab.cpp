//
// Created by Theo Fabi on 2022-01-22.
//

#include "CalendarTab.h"
#include "Schedule.h"
#include <QWidget>
#include <QHeaderView>
#include <QPushButton>
#include <QGroupBox>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QDialog>
#include <QObject>

CalendarTab::CalendarTab(QWidget *master) : QWidget(master){
    auto *btns = new QGroupBox("Edit schedule");
    addCourse = new QPushButton("Add course");
    addTutorial = new QPushButton("Add tutorial");
    addTask = new QPushButton("Add task");

    auto *leftBtnLayout = new QVBoxLayout();
    leftBtnLayout->addWidget(addCourse);
    leftBtnLayout->addWidget(addTutorial);
    leftBtnLayout->addWidget(addTask);
    btns->setLayout(leftBtnLayout);

    QObject::connect(addCourse, &QPushButton::clicked, this, &CalendarTab::showAddDialog);

    schedule = new Schedule();

    QHeaderView *hHeader = schedule->horizontalHeader();
    QHeaderView *vHeader = schedule->verticalHeader();
    hHeader->setSectionResizeMode(QHeaderView::Stretch);
    hHeader->setMinimumSectionSize(60);
    vHeader->setSectionResizeMode(QHeaderView::Stretch);
    vHeader->setMinimumSectionSize(20);

    auto *mainLayout = new QHBoxLayout();
    mainLayout->addWidget(btns);
    mainLayout->addWidget(schedule);

    setLayout(mainLayout);
}

CalendarTab::~CalendarTab() noexcept = default;


void CalendarTab::showAddDialog() {
    QDialog dialog(this);
    QVBoxLayout lyt;
    QPushButton btn("hi");
    lyt.addWidget(&btn);
    dialog.setLayout(&lyt);
    dialog.exec();
}

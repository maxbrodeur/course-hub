//
// Created by Theo Fabi on 2022-01-22.
//

#include "MainTabs.h"
#include "CalendarTab.h"
#include <QTabWidget>
#include <QHBoxLayout>
#include <QLabel>
#include <Qt>
#include <QTabBar>
#include <QSplitter>
#include "Schedule.h"
#include <QHeaderView>
#include <QPushButton>
#include <QGroupBox>

MainTabs::MainTabs(QWidget *master) : QTabWidget(master){
//    auto *calendarLayout = new QHBoxLayout();
//    auto *cal = new Schedule();
//    QHeaderView *hHeader = cal->horizontalHeader();
//    QHeaderView *vHeader = cal->verticalHeader();
//    hHeader->setSectionResizeMode(QHeaderView::Stretch);
//    hHeader->setMinimumSectionSize(60);
//    vHeader->setSectionResizeMode(QHeaderView::Stretch);
//    vHeader->setMinimumSectionSize(20);
//
//    auto *btns = new QGroupBox("Edit schedule");
//    auto *addCourse = new QPushButton("Add course");
//    auto *addTutorial = new QPushButton("Add tutorial");
//    auto *addTask = new QPushButton("Add task");
//
//    auto *leftBtnLayout = new QVBoxLayout();
//    leftBtnLayout->addWidget(addCourse);
//    leftBtnLayout->addWidget(addTutorial);
//    leftBtnLayout->addWidget(addTask);
//    btns->setLayout(leftBtnLayout);
//
//    auto *bar = tabBar();
//
//
//    calendarLayout->addWidget(btns);
//    calendarLayout->addWidget(cal);
//
//    calendarTab = new QWidget();
//    calendarTab->setLayout(calendarLayout);
    calendarTab = new CalendarTab();






    auto *assLayout = new QHBoxLayout(master);
    auto *ah = new QLabel("Assignments are here");
    assLayout->addWidget(ah);
    assignmentsTab = new QWidget();
    assignmentsTab->setLayout(assLayout);

    addTab(calendarTab, "Schedule");
    addTab(assignmentsTab, "Assignments");


    setTabShape(QTabWidget::Triangular);

}


MainTabs::~MainTabs() noexcept = default;
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
#include <QIcon>
#include <iostream>
#include <QSizePolicy>

MainTabs::MainTabs(QWidget *master) : QTabWidget(master){
    calendarTab = new CalendarTab();

    auto *assLayout = new QHBoxLayout(master);
    auto *ah = new QLabel("Assignments are here");
    assLayout->addWidget(ah);
    assignmentsTab = new QWidget();
    assignmentsTab->setLayout(assLayout);

    QIcon calIcon;
    calIcon.addFile("icons/calendar_grayed.png", QSize(40, 40), QIcon::Normal, QIcon::Off);
    calIcon.addFile("icons/calendar_subtle_glow.png", QSize(40, 40), QIcon::Normal, QIcon::On);
//    setTabIcon(0, *calIcon);

    QIcon taskIcon;
    taskIcon.addFile("icons/tasks_unselected.png", QSize(10, 10), QIcon::Normal, QIcon::Off);
    taskIcon.addFile("icons/tasks_subtle_glow.png", QSize(10, 10), QIcon::Normal, QIcon::On);

    addTab(calendarTab, calIcon, "");
    addTab(assignmentsTab, taskIcon, "");

//    QIcon logo;
//    logo.addFile("icons/temp-logo.png", QSize(250,100));
//    auto *logoWidget = new QLabel();
//    logoWidget->setMinimumSize(250, 100);
//    QSizePolicy sizer(QSizePolicy::Expanding, QSizePolicy::Expanding);
////    sizer.setControlType(QSizePolicy::Expanding);
//    logoWidget->setSizePolicy(sizer);
//    logoWidget->setPixmap(logo.pixmap(QSize(250,100)));
//    setCornerWidget(logoWidget, Qt::TopLeftCorner);

    auto *bar = tabBar();
    bar->setIconSize(QSize(80,80));

    setTabEnabled(0, true);
    for(int i=1; i<count(); i++){
        setTabEnabled(i-1, false);
        setTabEnabled(i, true);
    }
    setTabEnabled(0, true);






//    bar->setStyleSheet(" tab { "
//                       "border: none;"
//                       "margin-left: 10px;"
//                       "margin-right: 10px;"
//                       "font-size:0pt;"
//                       "} ");

}


MainTabs::~MainTabs() noexcept = default;
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
#include <QLabel>
#include <QDialog>
#include <QObject>
#include <QLineEdit>
#include <QSpinBox>
#include <Qt>
#include <QtGlobal>
#include <QTableWidgetItem>
#include "CalendarEntryDialog.h"


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

    schedule = new Schedule();

    QObject::connect(addCourse, &QPushButton::clicked, this,
                     [&](){ CalendarEntryDialog("New course", schedule).exec(); });



    QHeaderView *hHeader = schedule->horizontalHeader();
    QHeaderView *vHeader = schedule->verticalHeader();
    hHeader->setSectionResizeMode(QHeaderView::Stretch);
    hHeader->setMinimumSectionSize(60);
    vHeader->setSectionResizeMode(QHeaderView::Stretch);
    vHeader->setMinimumSectionSize(20);

    auto *mainLayout = new QHBoxLayout();
    mainLayout->addWidget(btns);
    mainLayout->addWidget(schedule);

    int x = 0;

//    auto *course = new QTableWidgetItem("MATH 340");
////    course->setFlags(Qt::Item
//    schedule->setItem(7, 3, course);
//    schedule->setSpan(7, 3, 3, 1);

    setLayout(mainLayout);
}

CalendarTab::~CalendarTab() noexcept = default;





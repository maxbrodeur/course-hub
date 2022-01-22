//
// Created by Theo Fabi on 2022-01-22.
//

#include <array>
#include <string>
#include "CalendarEntryDialog.h"
#include <QDialog>
#include <QLabel>
#include <QSpinBox>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QObject>
#include <QtGlobal>
#include <QPushButton>
#include <Qt>
#include <QComboBox>
#include <algorithm>

using std::array;
using std::string;
using std::for_each;

CalendarEntryDialog::CalendarEntryDialog(const QString &s, QWidget *master): QDialog(master) {
    sw = true;
    auto *lyt = new QVBoxLayout();
//    QSpinBox start;
//    start.setRange(-1, 13);
//    start.setValue(8);
//    start.setSuffix(" am");

    setWindowTitle(s);

    auto *name = new QLineEdit();
    name->setPlaceholderText("Class name");

    auto *startLabel = new QLabel("Start time ");
    start = new QSpinBox();
    start->setRange(-1, 13);
    start->setValue(0);
    start->setSuffix(" am");
    QObject::connect(start, qOverload<int>(&QSpinBox::valueChanged), this,
                     &CalendarEntryDialog::formatTime, Qt::QueuedConnection);
    auto *timeLayout = new QHBoxLayout();
    timeLayout->addWidget(startLabel);
    timeLayout->addWidget(start);

    auto *dayCombo = new QComboBox();
    array<string, 7> days{"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
//    for(const auto &d: days){
//        day->addItem(d.c_str());
//    }
    for_each(days.begin(), days.end(),
             [dayCombo](const string &s) mutable { dayCombo->addItem(s.c_str());});

    QObject::connect(dayCombo, &QComboBox::currentTextChanged, this,
                     &CalendarEntryDialog::setDay);

    auto *durLabel = new QLabel("Duration ");
    length = new QSpinBox();
    length->setRange(0, 10);
    length->setValue(1);
    length->setSuffix("");
    auto *durLayout = new QHBoxLayout();
    durLayout->addWidget(durLabel);
    durLayout->addWidget(length);

    lyt->addLayout(timeLayout);
    auto *btn = new QPushButton("Add");
    lyt->addLayout(durLayout);
    lyt->addWidget(name);
    lyt->addWidget(dayCombo);
    lyt->addWidget(btn);
    setLayout(lyt);
}

CalendarEntryDialog::~CalendarEntryDialog() noexcept = default;

void CalendarEntryDialog::setDay(const QString &s){ this->day = s.toStdString();}

void CalendarEntryDialog::formatTime(int i) {
    findChild<QLineEdit*>()->deselect();
    if(start->value() < 0){
        start->setValue(12);
        if(sw) {
            start->setSuffix(" pm");
            sw = false;
        } else {
            start->setSuffix(" am");
            sw = true;
        }
    }
    else if (start->value() > 12){
        start->setValue(0);
        if(sw) {
            start->setSuffix(" pm");
            sw = false;
        } else {
            start->setSuffix(" am");
            sw = true;
        }
    }
}
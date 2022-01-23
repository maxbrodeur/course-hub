//
// Created by Theo Fabi on 2022-01-22.
//

#include "Schedule.h"
#include <QStringList>
#include <string>
#include <QAbstractItemView>
#include "CalendarEntry.cpp"
#include <QBrush>
#include <QColor>
#include <Qt>


using std::string;

Schedule::Schedule(QWidget *master) : QTableWidget(master) {
    setColumnCount(7);
    setRowCount(24);
    QStringList days;
    days << "Sunday" << "Monday" << "Tuesday" << "Wednesday" << "Thursday" << "Friday" \
    << "Saturday";
//    setStyleSheet(
//            "QTableWidget::item:selected {"
//            "border: 1 px;"
//            " border-radius: 5px; "
//            "}"
//            );
    setStyleSheet(" gridline-color: #FFF9F9 ");


//    setShowGrid(false);
    QStringList hours;
    string curr;
    hours << "12 AM";
    for(int i=1; i<12; i++) {
        curr = std::to_string(i) + " AM";
        hours << curr.c_str();
    }
    hours << "12 PM";
    for(int i=1; i<12; i++){
        curr = std::to_string(i) + " PM";
        hours << curr.c_str();
    }
    setEditTriggers(QAbstractItemView::NoEditTriggers);

    setHorizontalHeaderLabels(days);
    setVerticalHeaderLabels(hours);
}

Schedule::~Schedule() noexcept = default;

void Schedule::addClass(const char *name, int day, int start, int duration) {
    auto *course = new CalendarEntry(
            start, duration, EntryType::COURSE
            );
    course->setText(name);
    setItem(start, day, course);
    setSpan(start, day, duration, 1);
//    QBrush courseBrush(QColor(220, 70, 70));
    course->setBackgroundColor(QColor(220, 70, 70));
    course->setTextAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    course->setTextColor(QColor("white"));
//    course->setTextAlignment(Qt::AlignVCenter);
//    dc4646
// 220, 70, 70
}
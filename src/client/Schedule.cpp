//
// Created by Theo Fabi on 2022-01-22.
//

#include "Schedule.h"
#include <QStringList>
#include <string>

using std::string;

Schedule::Schedule(QWidget *master) : QTableWidget(master) {
    setColumnCount(7);
    setRowCount(24);
    QStringList days;
    days << "Sunday" << "Monday" << "Tuesday" << "Wednesday" << "Thursday" << "Friday" \
    << "Saturday";
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

    setHorizontalHeaderLabels(days);
    setVerticalHeaderLabels(hours);
}

Schedule::~Schedule() noexcept = default;
//
// Created by Theo Fabi on 2022-01-22.
//

#ifndef CORE_UI_CALENDARTAB_H
#define CORE_UI_CALENDARTAB_H

#include <QWidget>
#include <QPushButton>
#include "Schedule.h"

class CalendarTab: public QWidget {
public:
    explicit CalendarTab(QWidget* master = nullptr);
    virtual ~CalendarTab() noexcept;
    Schedule *schedule;
private:
    QPushButton *addCourse;
    QPushButton *addTutorial;
    QPushButton *addTask;
public slots:
    void showAddDialog();
};


#endif //CORE_UI_CALENDARTAB_H

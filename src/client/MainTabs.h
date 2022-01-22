//
// Created by Theo Fabi on 2022-01-22.
//

#ifndef CORE_UI_MAINTABS_H
#define CORE_UI_MAINTABS_H

#include <QTabWidget>
#include <QLabel>
#include <QVBoxLayout>
#include "CalendarTab.h"


class MainTabs: public QTabWidget {
public:
    explicit MainTabs(QWidget *master = nullptr);
    virtual ~MainTabs() noexcept;
    CalendarTab *calendarTab;
    QWidget *assignmentsTab;
};


#endif //CORE_UI_MAINTABS_H

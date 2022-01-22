//
// Created by Theo Fabi on 2022-01-22.
//

#ifndef CORE_UI_SCHEDULE_H
#define CORE_UI_SCHEDULE_H

#include <QTableWidget>
#include <QTableWidgetItem>

class Schedule: public QTableWidget {
public:
    explicit Schedule(QWidget *master = nullptr);
    void addClass(const char* name, int day, int start, int end);
    virtual ~Schedule() noexcept;
};


#endif //CORE_UI_SCHEDULE_H

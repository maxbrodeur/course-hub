//
// Created by Theo Fabi on 2022-01-22.
//

#ifndef CORE_UI_CALENDARENTRYDIALOG_H
#define CORE_UI_CALENDARENTRYDIALOG_H

#include <QDialog>
#include <QLabel>
#include <QSpinBox>
#include <string>

using std::string;


class CalendarEntryDialog: public QDialog {
public:
    explicit CalendarEntryDialog(const QString &s, QWidget *master = nullptr);
    virtual ~CalendarEntryDialog() noexcept;
    QSpinBox *start;
    QSpinBox *length;
    string day;
    string name;

private:
    bool sw;
    void formatTime(int i);
    void checkLength(int i);
    void setDay(const QString &s);
};


#endif //CORE_UI_CALENDARENTRYDIALOG_H

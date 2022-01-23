//
// Created by Theo Fabi on 2022-01-22.
//

#ifndef CORE_UI_CALENDARENTRYDIALOG_H
#define CORE_UI_CALENDARENTRYDIALOG_H

#include <QDialog>
#include <QLabel>
#include <QSpinBox>
#include <string>
#include <QTableWidget>

using std::string;


class CalendarEntryDialog: public QDialog {
public:
    explicit CalendarEntryDialog(const QString &s, QTableWidget *table,
                                 QWidget *master = nullptr);
    virtual ~CalendarEntryDialog() noexcept;
    QTableWidget *cal;
    QSpinBox *start;
    QSpinBox *length;
//    QComboBox *day;
    string day;
    string name;

private:
    bool sw;
    void formatTime(int i);
    void checkLength(int i);
    void setDay(const QString &s);
    void addSignal();
};


#endif //CORE_UI_CALENDARENTRYDIALOG_H

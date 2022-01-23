//
// Created by Theo Fabi on 2022-01-22.
//

#include <QTableWidgetItem>

enum EntryType { COURSE, TUTORIAL, TASK };
class CalendarEntry : public QTableWidgetItem {
public:
    int start, length;
    EntryType type;
    CalendarEntry(int s, int e, EntryType type = EntryType::COURSE) :
            QTableWidgetItem() {
        start = s;
        length = e;
        this->type = type;
    }

    ~CalendarEntry() override = default;
};
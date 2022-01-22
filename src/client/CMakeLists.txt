cmake_minimum_required(VERSION 3.21)
project(core_ui)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

#set(PQXX /usr/local/include/pqxx)
#find_library(PQXX_LIB pqxx)
#find_library(PQ_LIB pq)
find_package(Qt5 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)

#find_package(PostgreSQL REQUIRED)

set_property(SOURCE CalendarTab.cpp PROPERTY SKIP_AUTOMOC ON)

add_executable(core_ui main.cpp MainWidget.cpp MainWidget.h MainTabs.cpp MainTabs.h Schedule.cpp Schedule.h CalendarTab.cpp CalendarTab.h CalendarEntryDialog.cpp CalendarEntryDialog.h CalendarEntry.cpp)
target_link_libraries(core_ui
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        )


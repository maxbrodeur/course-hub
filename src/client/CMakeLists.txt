cmake_minimum_required(VERSION 3.21)
project(core_ui)

set(CMAKE_CXX_STANDARD 14)
#set(CMAKE_AUTOMOC ON)
#set(CMAKE_AUTORCC ON)
#set(CMAKE_AUTOUIC ON)

#set(PQXX /usr/local/include/pqxx)
#find_library(PQXX_LIB pqxx)
#find_library(PQ_LIB pq)
find_package(Qt5 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)
execute_process(
        COMMAND bash "python3.9-config --embed --ldflags --include --libs --cflags"
        OUTPUT_VARIABLE PYEMBED
)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 ${PYEMBED}")
find_package(Python 3.9 COMPONENTS Interpreter Development)
##########find_package(PythonInterp 3.9 REQUIRED)
find_package(PythonLibs 3.9 REQUIRED)
#message(STATUS ${PYTHON_INCLUDE_DIRS})
#message(STATUS ${PYTHON_LIBRARIES})
include_directories(${PYTHON_INCLUDE_DIRS})
#message(STATUS ${Python_INCLUDE_DIR})

macro(print_all_variables)
    message(STATUS "print_all_variables------------------------------------------{")
    get_cmake_property(_variableNames VARIABLES)
    foreach (_variableName ${_variableNames})
        message(STATUS "${_variableName}=${${_variableName}}")
    endforeach()
    message(STATUS "print_all_variables------------------------------------------}")
endmacro()

print_all_variables()

#find_package(PostgreSQL REQUIRED)

#set_property(SOURCE CalendarTab.cpp PROPERTY SKIP_AUTOMOC ON)

add_executable(core_ui main.cpp MainWidget.cpp MainWidget.h MainTabs.cpp
        MainTabs.h Schedule.cpp Schedule.h CalendarTab.cpp CalendarTab.h
        CalendarEntryDialog.cpp CalendarEntryDialog.h CalendarEntry.cpp
        pytest.cpp pyhelper.h)
target_link_libraries(core_ui
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        Python
        ${PYTHON_LIBRARIES}
        )


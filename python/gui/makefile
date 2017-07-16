

SRCS = main_window.ui

OBJS = ${SRCS:.ui=.py}

.SUFFIXES:
.SUFFIXES: .ui .py

all:$(OBJS)

.ui.py:
		pyuic5 $< -o $@

clean:
		rm -rf *.pyc *_ui.py

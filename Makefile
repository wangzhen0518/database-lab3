.PHONY: all scripts clean

UI := ./ui

SCRIPTS = \
	$(UI)/account.ui \
	$(UI)/customer.ui \
	$(UI)/loan.ui \
	$(UI)/login.ui \
	$(UI)/MainWindow.ui \
	$(UI)/statistic.ui \
	$(UI)/searchRes.ui

PYSCRIPTS := $(SCRIPTS:$(UI)/%.ui=$(UI)/Ui_%.py)
PYSCRIPTS += $(UI)/res_rc.py

all: scripts

scripts: $(PYSCRIPTS)

$(UI)/res_rc.py: $(UI)/res.qrc
	pyrcc5 -o $(UI)/res_rc.py $(UI)/res.qrc

Ui_%.py: %.ui
	pyuic5 -o $@ $<

clean:
	rm  $(SCRIPTS)
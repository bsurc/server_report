
install:
	mkdir -p ~/.server_report/server_report
	cp *.py ~/.server_report/server_report/.
	cp report ~/.server_report/.
	echo 'export PYTHONPATH=~/.server_report:$$PYTHONPATH' >> ~/.bashrc
	echo 'export PATH=~/.server_report:$$PATH' >> ~/.bashrc

default: install

# server_report
This project is a python library and application intended to provide easy 
access to statistics of a Globus Endpoint. The Globus service already has
tools to do this, but this application will provide simple output for system
administration purposes. This project utilizes and requires as a dependency 
the [globus_python_sdk](https://github.com/globus/globus-sdk-python) as well 
as sqlite3.

Installation:  
```bash
pip install globus_sdk sqlite3  
make install
```

This will install the scripts into ~/.server_report as well as edit the PYTHONPATH variable in your .bashrc.

This project is licensed under the Apache 2.0 license, included in the 
LICENSE file.

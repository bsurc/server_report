# server_report
This project is a python library and application intended to provide easy 
access to statistics of a Globus Endpoint. The Globus service already has
tools to do this, but this application will provide simple output for system
administration purposes. This project utilizes and requires as a dependency 
the [globus_python_sdk](https://github.com/globus/globus-sdk-python) as well 
as sqlite3.

This application was developed for, and is only tested against, Python 3. 
This software is currently in the alpha stage and features are likely to 
change or be removed at any time. However, I do my best to ensure the current
master branch is stable if somewhat limited.

Installation:  
```bash
pip install globus_sdk sqlite3  
make install
```

This will install the scripts into ~/.server_report as well as edit the PYTHONPATH variable in your .bashrc.

This project is licensed under the Apache 2.0 license, included in the 
LICENSE file.

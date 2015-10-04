Scrapie Backend
===============

This is a project made during Hack Upstate 6; a 24 hour hackathon.

Scrapie is designed to make the process of mining a webpage for data simple and user friendly. Using Scrapie, users with little technical background can gather the data they need to do data analysis.

Architecture
------------

Scrapie is composed of three parts: the Chrome extension, the job processing back-end, and the data visualization front-end. The processing back-end and a very basic visualization front-end are provided in this repository.

The configurations for the back-end are stored in `config.py`. This defines which directory contains the python scripts and which directories should hold the jobs and data created by Scrapie.

There are two important script files in this repository: `tcp_client.py` and `process_job.py`.

`tcp_client.py` listens on a network port for new jobs. Once the user has created a job, with the help of the Chrome extension, this job is sent as a json object to the TCP server. The TCP server then takes this json object, saves it as a job in the jobs directory, and schedules it in cron for execution on a user defined interval.

When the cron job executes, `process_job.py` is started with the name of the job to be executed as its sole argument. `process_job.py` parses this job and performs the appropriate scraping and then appends this data to the appropriate file in the data directory.

Finally, the user visits the visualization front-end, `visual_server.py`, where they can see all the jobs on the server. They can then select a particular job to see the data for it.

Configuration
-------------

Since this back-end uses cron for job scheduling, Scrapie has to be deployed on a Linux or UNIX system. Scrapie is also designed for Python 2.7. `requirements.txt` contains the libraries Scrapie depends on. `tcp_client.py` and `visual_server.py` should be configured to run on start-up.

Debugging
---------

`test_data.py` contains an example job which can be used for debugging purposes.
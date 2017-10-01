# SQL Log Analyzer project for Udacity
This is a simple Python script that will connect to a local PostgreSQL database, analyze it and return the following information to the console:

1. TOP 3 most viewed articles
2. Most popular authors by articles' views
3. Days in which the HTTP invalid request where more that 1% of the daily total

The script will automatically create any of the needed SQL views.

## Usage

1. Install [Python 3.x](https://www.python.org/).
2. Place the script file on the server/instance where your database is located.
3. On Windows from the command prompt run:
 `C:\path-to-python3-binary\python.exe C:\path-to-project-folder\log_analyzer.py`
On Mac OSX or Linux from the terminal run:
`chmod +x /path-to-project-folder/log_analyzer.py`
`python /path-to-project-folder/log_analyzer.py`

# SQL Log Analyzer project for Udacity
This is a simple Python script that will connect to a local PostgreSQL database, analyze it and return the following information to the console:

1. TOP 3 most viewed articles
2. Most popular authors by articles' views
3. Days in which the HTTP invalid request where more that 1% of the daily total


## Usage

1. Install [Python 3.x](https://www.python.org/).
2. Place the script file on the server/instance where your database is located.
3. Access the database from the terminal with psql -d news and create the following views:

1. `create view invalid_requests as select date_trunc('day', time), status, count(*) as num from log where status like '%404%' group by status, date_trunc('day', time) order by date_trunc('day', time);`

2. `create view total_requests as select date_trunc('day', time), count(*) as num from log group by date_trunc('day', time) order by date_trunc('day', time);`

3. `create view invalid_req_perc as select round((CAST (a.num/b.num::float*100 as numeric)), 2) as percentage, a.date_trunc from invalid_requests as a, total_requests as b where a.date_trunc = b.date_trunc;`

4. `create view hits_by_article as select path, count(*) as num from log where path like '/article/%' group by path order by num desc;`

5. `create view hits_by_title as select title, author, num from hits_by_article, articles where hits_by_article.path like '%'||articles.slug order by num desc;`

4. On Windows from the command prompt run:
`C:\path-to-python3-binary\python.exe C:\path-to-project-folder\log_analyzer.py`
On Mac OSX or Linux from the terminal run:
`chmod +x /path-to-project-folder/log_analyzer.py`
`python /path-to-project-folder/log_analyzer.py`

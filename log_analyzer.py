#!/usr/bin/python3
import psycopg2

"""Create the SQL views needed by this script to succesfully query
the database"""


def create_views():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select to_regclass('public.invalid_requests')")
    if (str(c.fetchall()[0][0]) == "None"):
        c.execute("create view invalid_requests as select date_trunc('day', \
            time), status, count(*) as num from log where status like '%404%'\
             group by status, date_trunc('day', time) order by \
             date_trunc('day', time);")
    c.execute("select to_regclass('public.total_requests');")
    if (str(c.fetchall()[0][0]) == "None"):
        c.execute("create view total_requests as select date_trunc('day', \
            time), count(*) as num from log group by date_trunc('day', time) \
            order by date_trunc('day', time);")
    c.execute("select to_regclass('public.invalid_req_perc');")
    if (str(c.fetchall()[0][0]) == "None"):
        c.execute("create view invalid_req_perc as select round((CAST \
            (a.num/b.num::float*100 as numeric)), 2) as percentage, \
            a.date_trunc from invalid_requests as a, total_requests as b \
            where a.date_trunc = b.date_trunc;")
    c.execute("select to_regclass('public.hits_by_article');")
    if (str(c.fetchall()[0][0]) == "None"):
        c.execute("create view hits_by_article as select path, count(*) as \
            num from log where path like '/article/%' group by path order by \
            num desc;")
    c.execute("select to_regclass('public.hits_by_title');")
    if (str(c.fetchall()[0][0]) == "None"):
        c.execute("create view hits_by_title as select title, author, num \
            from hits_by_article, articles where hits_by_article.path like \
            '%'||articles.slug order by num desc;")
    db.commit()
    db.close()


"""Get from the database and print to the terminal the days in which
the invalid requests (e.g. HTTP 404) percentage has been more than 1%
of the total daily requests"""


def get_errors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        "select date(date_trunc), percentage from invalid_req_perc as \
        percentages where percentage > 1;")
    print("List of days on which more than 1% of requests led to errors:\n")
    data = c.fetchall()
    print(str(data[0][0]) + " -- " + str(data[0][1]) + "% errors")
    db.close()


"""Get from the database and print to the terminal the 3 most popular
articles' title by number of views"""


def get_hits_by_article():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select * from hits_by_title limit 3")
    data = c.fetchall()
    print("TOP 3 of the most popular articles of all time:\n")
    for i in range(0, len(data)):
        print(str(data[i][0]) + " -- " + str(data[i][2]) + " views")
    db.close()


"""Get form the datanase and print to the terminal the total
articles' views for each author"""


def get_hits_by_author():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("select name, sum(num) from hits_by_title left join authors on \
        hits_by_title.author = authors.id group by name order by sum(num) \
        desc;")
    data = c.fetchall()
    print("Authors popularity by articles views:\n")
    for i in range(0, len(data)):
        print(str(data[i][0]) + " -- " + str(data[i][1]) + " views")
    db.close()


create_views()
get_hits_by_article()
print("\n")
get_hits_by_author()
print("\n")
get_errors()

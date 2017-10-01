#!/usr/bin/python3
import psycopg2


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


get_hits_by_article()
print("\n")
get_hits_by_author()
print("\n")
get_errors()

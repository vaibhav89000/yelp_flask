import subprocess
import sqlite3
import pandas as pd
from flask import Flask,request,render_template,redirect
import os
# import requests
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('http://127.0.0.1:5000/home')

@app.route('/')
def home():
    return redirect('http://127.0.0.1:5000/home')

@app.route('/home')
def my_form():
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def my_form_post():
    country = request.form['input1']
    city = request.form['input2']
    keyword = request.form['input3']

    if (os.stat('country.txt').st_size != 0):
        with open('country.txt', 'a') as f:
            f.write('')
    if(os.stat('city.txt').st_size != 0):
        with open('city.txt', 'a') as f:
            f.write('')
    if (os.stat('keyword.txt').st_size != 0):
        with open('keyword.txt', 'a') as f:
            f.write('')
    new_country=''
    new_city=''
    new_keyword=''

    for b in country:
        if(b=='\n'):
            new_country+=''
        else:
            new_country+=b

    for b in city:
        if(b=='\n'):
            new_city+=''
        else:
            new_city+=b

    for b in keyword:
        if(b=='\n'):
            new_keyword += ''
        else:
            new_keyword += b

    if request.method == 'POST':
        if country!='' and city!='' and keyword!='':
           with open('country.txt', 'a') as f:
                f.write(str(new_country))
           with open('city.txt', 'a') as f:
               f.write(str(new_city))
           with open('keyword.txt', 'a') as f:
               f.write(str(new_keyword))
    # return render_template('home.html', find=find,near=near)
    return redirect('http://127.0.0.1:5000/home')


# @app.route('/run')
# def run():
#     """
#     Run spider in another process and store items in file. Simply issue command:
#
#     > scrapy crawl dmoz -o "output.json"
#
#     wait for  this command to finish, and read output.json to client.
#     """
#
#     # p = subprocess.Popen(...)
#     # """
#     # A None value indicates that the process hasn't terminated yet.
#     # """
#     # poll = p.poll()
#     # if poll == None:
#     spider_name = "search"
#     subprocess.check_output(['scrapy', 'crawl', spider_name])
#
#     return redirect('http://127.0.0.1:5000/view')
    # with open("output.json") as items_file:
    #     return items_file.read()



@app.route("/view")
def view_get():
    con = sqlite3.connect("searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")
    rows = cur.fetchall()

    return render_template("index.html", rows=rows)

@app.route("/delete")
def delete_all():
    con = sqlite3.connect("searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")

    cur.execute('DELETE FROM detail;', )
    # rows = cur.fetchall()
    con.commit()

    return render_template("home.html")


@app.route("/csv")
def csv():
    con = sqlite3.connect("searchdetail.db")
    con.row_factory = sqlite3.Row

    df = pd.read_sql_query("SELECT * FROM detail", con)
    print(df)
    print(type(df))
    df.to_csv('details.csv', index=False)

    return render_template("home.html")


@app.route("/deletebysearch", methods=['POST'])
def deletebysearch():
    key = request.form['del']
    print(key)
    print(type(key))
    sqliteConnection = sqlite3.connect('searchdetail.db')
    cursor = sqliteConnection.cursor()

    # sql_delete_query = "SELECT * FROM detail WHERE keyword LIKE '%Dentist%'"
    # query = str("DELETE FROM detail WHERE keyword LIKE"+ " %{".format(key))
    query = "DELETE FROM detail WHERE keyword LIKE '%{}%'".format(key)
    sql_delete_query = query
    cursor.execute(sql_delete_query)
    sqliteConnection.commit()

    return render_template("home.html")


@app.route("/view", methods=['POST'])
def view():
    con = sqlite3.connect("searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()



    # if request.method == 'POST':
    country = request.form['input1']
    city = request.form['input2']
    keyword = request.form['input3']

    if(country!='' and city!='' and keyword!=''):
        # cur.execute("select * from detail where country")
        cur.execute("SELECT * FROM detail WHERE country=? and city=? and keyword=?", (country,city,keyword,))
        rows = cur.fetchall()
        if(len(rows)==0):
            cur.execute("select * from detail")
            rows = cur.fetchall()
    else:
        cur.execute("select * from detail")
        rows = cur.fetchall()
    return render_template("index.html",rows = rows)

if __name__ == '__main__':
    app.run(debug=True)
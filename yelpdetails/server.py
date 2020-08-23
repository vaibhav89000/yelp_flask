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
    find = request.form['input1']
    near = request.form['input2']


    if (os.stat('option.txt').st_size != 0):
        with open('option.txt', 'a') as f:
            f.write('')
    if(os.stat('location.txt').st_size != 0):
        with open('location.txt', 'a') as f:
            f.write('')

    new_find=''
    new_near=''


    for b in find:
        if(b=='\n'):
            new_find+=''
        else:
            new_find+=b

    for b in near:
        if(b=='\n'):
            new_near+=''
        else:
            new_near+=b


    if request.method == 'POST':
        if find!='' and near!='' :
           with open('option.txt', 'a') as f:
                f.write(str(new_find))
           with open('location.txt', 'a') as f:
               f.write(str(new_near))

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
    con = sqlite3.connect("yelpdetails.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")
    rows = cur.fetchall()

    return render_template("index.html", rows=rows)

@app.route("/delete")
def delete_all():
    con = sqlite3.connect("yelpdetails.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")

    cur.execute('DELETE FROM detail;', )
    # rows = cur.fetchall()
    con.commit()

    return render_template("home.html")


@app.route("/csv")
def csv():
    con = sqlite3.connect("yelpdetails.db")
    con.row_factory = sqlite3.Row

    df = pd.read_sql_query("SELECT * FROM detail", con)
    print(df)
    print(type(df))
    df.to_csv('details.csv', index=False)

    return redirect('http://127.0.0.1:5000/home')


@app.route("/deletebysearch", methods=['POST'])
def deletebysearch():
    key = request.form['del']
    print(key)
    print(type(key))
    sqliteConnection = sqlite3.connect('yelpdetails.db')
    cursor = sqliteConnection.cursor()

    # sql_delete_query = "SELECT * FROM detail WHERE keyword LIKE '%Dentist%'"
    # query = str("DELETE FROM detail WHERE keyword LIKE"+ " %{".format(key))
    query = "DELETE FROM detail WHERE find LIKE '%{}%'".format(key)
    sql_delete_query = query
    cursor.execute(sql_delete_query)
    sqliteConnection.commit()

    return render_template("home.html")


@app.route("/view", methods=['POST'])
def view():
    con = sqlite3.connect("yelpdetails.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    find = request.form['input1']
    near = request.form['input2']

    if(find!='' and near!=''):
        # cur.execute("select * from detail where country")
        cur.execute("SELECT * FROM detail WHERE find=? and near=? ", (find,near,))
        rows = cur.fetchall()
        if(len(rows)==0):
            cur.execute("select * from detail")
            rows = cur.fetchall()
    else:
        cur.execute("select * from detail")
        rows = cur.fetchall()
    return render_template("index.html",rows = rows)


@app.route('/submittwo', methods=['POST'])
def onsubmittwo():
    find = request.form['input1']
    near = request.form['input2']

    if (os.stat('optiontwo.txt').st_size != 0):
        with open('optiontwo.txt', 'a') as f:
            f.write('')
    if (os.stat('locationtwo.txt').st_size != 0):
        with open('locationtwo.txt', 'a') as f:
            f.write('')

    new_find = ''
    new_near = ''

    for b in find:
        if (b == '\n'):
            new_find += ''
        else:
            new_find += b

    for b in near:
        if (b == '\n'):
            new_near += ''
        else:
            new_near += b

    if request.method == 'POST':
        if find != '' and near != '':
            with open('optiontwo.txt', 'a') as f:
                f.write(str(new_find))
            with open('locationtwo.txt', 'a') as f:
                f.write(str(new_near))

    return redirect('http://127.0.0.1:5000/home')


@app.route('/submitthree', methods=['POST'])
def onsubmitthree():
    find = request.form['input1']
    near = request.form['input2']

    if (os.stat('optionthree.txt').st_size != 0):
        with open('optionthree.txt', 'a') as f:
            f.write('')
    if (os.stat('locationthree.txt').st_size != 0):
        with open('locationthree.txt', 'a') as f:
            f.write('')

    new_find = ''
    new_near = ''

    for b in find:
        if (b == '\n'):
            new_find += ''
        else:
            new_find += b

    for b in near:
        if (b == '\n'):
            new_near += ''
        else:
            new_near += b

    if request.method == 'POST':
        if find != '' and near != '':
            with open('optionthree.txt', 'a') as f:
                f.write(str(new_find))
            with open('locationthree.txt', 'a') as f:
                f.write(str(new_near))

    return redirect('http://127.0.0.1:5000/home')


@app.route('/submitfour', methods=['POST'])
def onsubmitfour():
    find = request.form['input1']
    near = request.form['input2']

    if (os.stat('optionfour.txt').st_size != 0):
        with open('optionfour.txt', 'a') as f:
            f.write('')
    if (os.stat('locationfour.txt').st_size != 0):
        with open('location.txt', 'a') as f:
            f.write('')

    new_find = ''
    new_near = ''

    for b in find:
        if (b == '\n'):
            new_find += ''
        else:
            new_find += b

    for b in near:
        if (b == '\n'):
            new_near += ''
        else:
            new_near += b

    if request.method == 'POST':
        if find != '' and near != '':
            with open('optionfour.txt', 'a') as f:
                f.write(str(new_find))
            with open('locationfour.txt', 'a') as f:
                f.write(str(new_near))

    return redirect('http://127.0.0.1:5000/home')


if __name__ == '__main__':
    app.run(debug=True)
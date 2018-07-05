#!/usr/bin/env python
#coding:utf-8
import os 
import pymysql
from flask import Flask,request,session,redirect,url_for,abort,render_template,flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

def get_db(sql):
	"""
		连接数据库
		在独立进程下,原数据库连接已经关闭,所以需要重新连接
	"""
	config = {'host':'localhost','user':'root','password':'','db':'devdb','charset':'utf8mb4'}
	connection = pymysql.connect(**config)
	cur = connection.cursor()
	try:
		cur.execute(sql)
	except:
		connection.rollback()
	connection.commit()
	cur.close()
	connection.close()
	

def create_entries():
	sql = "create table entries(id int not null auto_increment,title varchar(64) not null,text varchar(64) not null,primary key (id))"
	get_db(sql)
create_entries()

@app.route('/') 
def show_entries():
	sql = "select title,text from entries order by id desc"
	config = {'host':'localhost','user':'root','password':'','database':'devdb','charset':'utf8mb4'}
	connection = pymysql.connect(**config)
	cur = connection.cursor()
	cur.execute(sql)
	entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	cur.close()
	connection.close()
	return render_template('show_entries.html',entries=entries)

@app.route('/data',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	sql = "insert into entries(title,text) values ('{0}','{1}')" .format(request.form['title'],request.form['text'])
	config = {'host':'localhost','user':'root','password':'','database':'devdb','charset':'utf8mb4'}
	connection = pymysql.connect(**config)
	cur = connection.cursor()
	cur.execute(sql)
	connection.commit()
	cur.close()
	connection.close()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))
@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'wuxiangyu':
			error = 'Invalid username'
		elif request.form['password'] != 'yicai127':
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were Logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)
@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')	
	return redirect(url_for('show_entries'))	
app.debug = True
if __name__ == '__main__':
	app.run('10.10.8.7')

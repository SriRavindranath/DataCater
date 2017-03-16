from flask_wtf import *
from wtforms import *
from flask import *
from flask_admin.form import DatePickerWidget
from flaskext.mysql import MySQL
import csv
import xlsxwriter
from xlsxwriter.workbook import Workbook
import os
import datetime

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

start_date=" "
end_date=" "

@app.route('/')
    
def home():
        return render_template('login.html')
                
    
@app.route('/login', methods = ['GET','POST'])
    
def login_name():
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.get_db().cursor()

        cursor.execute("select * from login where name='" + username + "' and password='" + password + "'")

        data = cursor.fetchall()

        if data:
                return "<label>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Hi " +username+ "</label>" +home1()
        else:
                error="Invalid Username or Password!!!"
           	return render_template("login.html",error = error)

        return home()


def home1():
        return render_template('date_input1.html')


@app.route("/login1", methods = ['GET', 'POST'])

def index():
        if request.method == 'POST':
              
		start_date1 = request.form['start_date']
		end_date1 = request.form['end_date']
		if start_date1 != "" and end_date1 != "":
			f = '%d/%m/%Y'
	
			start_date = datetime.datetime.strptime(start_date1, f)
			end_date = datetime.datetime.strptime(end_date1, f)

                	if start_date != "" and end_date != "" and start_date < end_date:
				error=""                        			
                        	return options(start_date,end_date,error)
			else:
				error="Enter valid start date and end date"
                        	return render_template("date_input1.html",error = error)

                else:
                        error="Enter valid start date and end date"                        
			return render_template("date_input1.html",error = error)


def options(start_date,end_date,error):

        return render_template('dummy2.html',date = start_date, date1 = end_date,error=error)


def home2(start_date,end_date):

        return render_template('wallet_input.html',date = start_date, date1 = end_date)

@app.route("/date", methods = ['GET','POST'])

def index111():
        start_date=request.form['date']
        end_date=request.form['date1']

        cursor = mysql.get_db().cursor()

        row_count=cursor.execute("select 'wallet_id','name','product','startdate','enddate' union all select * from wallet_info where startdate >= '" + start_date + "'and enddate <= '" + end_date + "'")

        if row_count > 1:

                row = cursor.fetchall()
                workbook =xlsxwriter.Workbook('output.xlsx')
                sheet = workbook.add_worksheet()
                for r, row1 in enumerate(row):
                        for c, col in enumerate(row1):
                                sheet.write(r, c, col)

                return '<html> <body> Data copied to XLSX file <a href = "/downloadCSV"> Click here to download. </a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <a href="/logout"><b>Logout</b></a></body> </html>'

        else:
		error=""
                return options(start_date,end_date,error)



@app.route("/parameter", methods = ['GET','POST'])

def index1111():
	wallet_id=request.form['wallet_id']
        product = request.form['product']

        start_date=request.form['date']
        end_date=request.form['date1']

        cursor = mysql.get_db().cursor()
	
	if request.form.get("wallet_op", False) and request.form.get("product_op", False):
        	row_count=cursor.execute("select 'wallet_id','name','product','startdate','enddate' union all select * from wallet_info where wallet_id='" +wallet_id+ "'and product='" + product + "'and startdate >= '" + start_date + "'and enddate <= '" + end_date + "'")
	
	elif request.form.get("wallet_op", False) and not request.form.get("product_op", False):
		row_count=cursor.execute("select 'wallet_id','name','product','startdate','enddate' union all select * from wallet_info where wallet_id='" + wallet_id + "'and startdate >= '" + start_date + "'and enddate <= '" + end_date + "'")
	
	elif request.form.get("product_op", False):
                row_count=cursor.execute("select 'wallet_id','name','product','startdate','enddate' union all select * from wallet_info where product='" + product + "'and startdate >= '" + start_date + "'and enddate <= '" + end_date + "'")
	else:
		error="Please input information!!!!!"
		return options(start_date,end_date,error)
	
        
	if row_count > 1:

                row = cursor.fetchall()
                workbook =xlsxwriter.Workbook('output.xlsx')
                sheet = workbook.add_worksheet()
                for r, row1 in enumerate(row):
                        for c, col in enumerate(row1):
                                sheet.write(r, c, col)

                return '<html> <body> Data copied to XLSX file <a href = "/downloadCSV"> Click here to download. </a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <a href="/logout"><b>Logout</b></a></body> </html>'

        else:
		error="No transaction found!!!"
                return options(start_date,end_date,error)

@app.route("/downloadCSV")

def getPlotExcel():
    excelDownload = open("output.xlsx",'rb').read()
    return Response(
        excelDownload,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-disposition":
                 "attachment; filename=output.xlsx"})


@app.route("/logout")

def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
        app.secret_key = os.urandom(12)
        app.run(debug = True)


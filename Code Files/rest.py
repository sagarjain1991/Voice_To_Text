from flask import Flask, render_template, request, jsonify
import os
import sys
from time import time
import psycopg2
import mysql.connector

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')



#mysql
@app.route('/mysql', methods=['GET', 'POST'])
def call_mysql():
    print('call mysql')
    start_time = time()
    if request.method == 'POST':
        data = request.get_json()
    query = data['query'] + ';'
    print(query)

    mysqlcon =  mysql.connector.connect(host="db.cbmuwzdg0zjd.us-east-2.rds.amazonaws.com",user="admin",passwd = "password",database="instacartdatabase")
    mycursor = mysqlcon.cursor()
    mycursor.execute(query)
    result = mycursor.fetchall()
    columns = mycursor.column_names

    query_result = '<table border="1"  width="100%"> <tr>'
    for head in columns:
        query_result += '<th>'+str(head)+'</th>'
    query_result += '</tr>'
    for rows in result:
        query_result += '<tr>'
        for cols in rows:
            query_result += '<td><center>'+str(cols)+'</center></td>'
        query_result += '</tr>'
    query_result += '</table>'
    end_time = time() - start_time
    query_result += '<h4>Time Elapsed: '+str(round(end_time,3))+' sec</h4>'
    print(query_result)
    data = {'result' : query_result}

    return jsonify(data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], ssl_context='adhoc', debug=True)

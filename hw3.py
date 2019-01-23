import pandas as pd
import numpy as np
import sqlite3,os
from datetime import datetime, date, timedelta

'''
Class: ISTA131
Author: YongBaek Cho
Date: 09/20 2018
Description: This program call the One SQL DB file(class_redacted) and One sun_frame csv file. Then, analyze two files.
'''
def student_report(file_name, stud_id):
	# This function takes an SQLite db filename and a student id.   
    conn = sqlite3.connect(file_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT name FROM sqlite_master WHERE type = 'table';"

    class_list = c.execute(query).fetchall()
    transcript = ""
    for i in range(len(class_list)):
        query2 = 'SELECT last, first, grade FROM ' + (''.join(class_list[i][0])) + ' WHERE id = ' + stud_id + ';'
        name = c.execute(query2).fetchone()
        if name:
            if not transcript:
                transcript += name['last'] + ', ' + name['first'] + ', ' + stud_id + '\n'
                transcript += '-' * (len(transcript) - 1) + '\n'
            clss = class_list[i][0].split('_')
            transcript += ' '.join(clss) + ': ' + name['grade'] + '\n'
    return transcript

    conn.close()
def A_students(conn,tbl_name="ISTA_131_F17",clss=None,mx_num=10):
	# This function takes a connection object, a table name with default value "ISTA_131_F17", a class standing string with default value None, and a maximum number of results to return with default value 10. 
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    name_list = []
    
    if not clss == None:
        query2 = "SELECT last,first FROM " + tbl_name + " WHERE grade = 'A' AND level LIKE \'" + clss+ "\' ORDER BY last LIMIT "+str(mx_num)+";"
        name = c.execute(query2).fetchall()
        for i in range(len(name)):
            name_list.append(name[i][0] + ', ' + name[i][1])

    else:
        query3 = "SELECT last,first FROM " + tbl_name + " WHERE grade ='A' ORDER BY last LIMIT "+ str(mx_num) +";"
        name = c.execute(query3).fetchall()
        for i in range(len(name)):
            name_list.append(name[i][0] + ', ' + name[i][1])
    return name_list
	
def class_performance(conn,tbl_name="ISTA_131_F17"):
	#This function takes a connection object and a table name with default value "ISTA_131_F17" and returns a dictionary that maps the grades (capitalized) to their 1-decimal point precision percentages of the class that got that grade. 
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    dic = {}
    string = []

    query1 = "SELECT COUNT(*) FROM " +tbl_name +";"
    total = c.execute(query1).fetchone()[0]
    
    query2 = "SELECT UPPER(grade), COUNT(*) FROM " + tbl_name + " GROUP BY grade;"
    grade = c.execute(query2).fetchall()
    for i in range(len(grade)):
        dic[grade[i][0]] = round((grade[i][1] / total) * 100,1)

    return dic
def read_frame():
	# read a csv file 
	col_names = ['Jan_r', 'Jan_s', 'Feb_r', 'Feb_s', 'Mar_r', 'Mar_s', 'Apr_r',
        'Apr_s', 'May_r', 'May_s', 'Jun_r', 'Jun_s', 'Jul_r', 'Jul_s', 'Aug_r',
        'Aug_s', 'Sep_r', 'Sep_s', 'Oct_r', 'Oct_s', 'Nov_r', 'Nov_s', 'Dec_r',
        'Dec_s']
	sun_frame = pd.read_csv('sunrise_sunset.csv', header = None, names = col_names, index_col = 0, dtype ='str')
	return sun_frame
    

def get_series(sun_frame):
	# This function takes a sun DataFrame as created by the previous function and returns two Series, one for sunrise data, one for sunset data. 
	col_names = sun_frame.columns
	sunrise = pd.concat(map(sun_frame.get, col_names[::2]))
	sunrise.dropna(inplace=True)
	sunset = pd.concat(map(sun_frame.get, col_names[1::2]))
	sunset.dropna(inplace=True)
	new_index = pd.date_range(start = '2018-01-01', end = '2018-12-31')
	sunrise.index = new_index
	sunset.index = new_index
	rise = pd.Series(data = sunrise)
	set = pd.Series(data = sunset)
	
	return rise, set
def longest_day(rise, set):
	#This function takes sunrise and sunset Series and returns the timestamp of the longest day and an hour-minute string that represents the length of that day (just like the strings in the Series).
	sunrise1 = rise.apply(lambda x: int (x[:-2:]) * 60 + int(x[-2::]))
	sunset1 = set.apply(lambda x: int(x[:-2:]) * 60 + int(x[-2::]))
	daylength = sunset1 - sunrise1
	s = pd.Series(data = daylength)
	abc = s.idxmax()
	set1 = set.astype(int)
	rise1 = rise.astype(int)
	s = set1 - rise1
	s1 = s.max()
	return abc, str(s1)
	
def sunrise_dif(rise, abc):
	#This function takes a sunrise Series and a timestamp.  It returns the difference in minutes between the sunrise time 90 days before the timestamp and 90 days after. 
	days_before = (abc - timedelta(days=90))
	days_after = (abc + timedelta(days=90))
	rise_days_before = pd.Series(rise, index = [days_before])
	rise_a = rise_days_before.apply(lambda x: int (x[:-2:]) * 60 + int(x[-2::]))
	rise_days_after = pd.Series(rise, index = [days_after])
	rise_b = rise_days_after.apply(lambda x: int (x[:-2:]) * 60 + int(x[-2::]))
	absol_rdb = int(rise_a)
	absol_rda = int(rise_b)
	return absol_rdb - absol_rda
	
	
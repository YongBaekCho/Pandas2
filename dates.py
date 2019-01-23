#=================================================================================================
#   Assignment: Long assignment 7 dates.py
#       Author: Feiran Yang 
#
#       Course:  CS 120
#   Instructor:  Saumya Debray
#
#  Description:  This file include 2 class and a main program. This program readin a file which 
#				 contians lines of date in specific form. after read in this file, the program
#				 will then create a DateSet object and map tranfered date data into DateSet dict
#				 with event.
#				 if a line start with R, print event has same date with that line.
#=================================================================================================
MDICT = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr': 4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9,
		 'Oct':10, 'Nov':11, 'Dec':12}
#=================================================================================================
# 	 Class Name:    Date
#       Purpose:    init a Date object, set date and event than transfer date to a specific form.
#=================================================================================================
class Date:
	def __init__(self, date, event):
		self._date = date
		self._event = event

	# return date in specific form
	def get_date(self):
	    date_str = self._date
	    if '-' in date_str:
	    	date = date_str.split('-')
	    	dd = date[2]
	    	yyyy = date[0]
	    	mm = date[1]
	    elif '/' in date_str:
	    	date = date_str.split('/')
	    	yyyy = date[2]
	    	mm = date[0]
	    	dd = date[1]
	    else:
	    	date = date_str.split()
	    	yyyy = date[2]
	    	# if mm is a str and cant cover to int, mark it as a tuple
	    	mm = (date[0],)
	    	dd = date[1]

	    # if mm is a tuple
	    if type(mm) == tuple:
	        # get the first element
	    	month = mm[0]
	    	assert month in MDICT
	    	# for each month, lookup month dictionary to fget digital ver
	    	mm = MDICT[month]
	    # assert, try if mm and dd is in right form.
	    try:
	    	int(mm)
	    	int(dd)
	    except ValueError:
	    	assert False
	    # assert, see if mm and dd in in right range
	    assert 1<=int(mm)<=13 and 1<=int(dd)<=31 
	    self._date_conversed = ("{:d}-{:d}-{:d}".format( int(yyyy), int(mm), int(dd)))
	    return self._date_conversed

	# return event
	def get_event(self):
		return self._event
	# return conversed date and event in right form
	def __str__(self):
		return ("{}: {}".format(self._date_conversed, self._event)) 
	# for debuging
	def __repr__(self):
		return ("{}: {}".format(self._date_conversed, self._event))

#=================================================================================================
# 	 Class Name:    DateSet
#       Purpose:    init a DateSet object, mapping every date to date object
#=================================================================================================
class DateSet:
	def __init__(self):
		self._date_dict = {}

	# get date from date object and map date object to date
	def mapping(self, date):
		# if date not in dict
		if not date.get_date() in self._date_dict:
			self._date_dict[date.get_date()] = [date]
		# if in dict
		else:
			self._date_dict[date.get_date()].append(date)

	# return event in dict has that date
	def get_events(self, date):
		try:
			return self._date_dict[date]
		# if date is not exist in dict
		except KeyError:
			# return a empty list
			return []

	# for debugging
	def __repr__(self):
		return str(self._date_dict)


def main():
	lines = input_file()
	process_data(lines)

#=================================================================================================
# Function Name:    input_file()
#       Purpose:    aks user for a input file name. exit if there is error with file. and process
#					data into a list
#    Parameters:    N/A
#       Returns:    lines
#=================================================================================================
def input_file():
	file_name = input()
	# try to open the file
	try:
		lines = open(file_name).readlines()
	# if file could not be found, exit the program
	except IOError:
		print('ERROR: could not open file ')
		exit(1)
	# return useless data from every lines
	for i in range(0, len(lines)):
		# assert to see if lines is not in right form
		assert 'R' in lines[i] or ':' in lines[i]
		if lines[i][0] == 'I':
			lines[i] = lines[i].strip('I \n').split(':')
			for j in range(0, len(lines[i])):
				lines[i][j] = lines[i][j].strip(' ')
		else:
			# add R after lines start with R to search
			lines[i] = [lines[i].strip('R \n'), 'R']

	return lines
#=================================================================================================
# Function Name:    process_data()
#       Purpose:    take lines from main. create a DateSet object. loop trough every lines and
#					create Date object based on info in every lines. if the secend element is 'R',
#					search in the DateSet object and print returned info out.
#    Parameters:    lines
#       Returns:    N/A
#=================================================================================================
def process_data(lines):
	# create a DateSet object.
	date_dict = DateSet()
	# looping trough lines list
	for i in range(0, len(lines)):
		# create a new Date object for each lines
		this_data = Date(lines[i][0], lines[i][1])
		# if a line list end with 'R'
		if lines[i][1] == 'R':
			# get date
			key = this_data.get_date()
			# get events with the key
			events = date_dict.get_events(key)
			# loop trough every element in events list and print them out.
			for j in range(0, len(events)):
				print(events[j])
		# or just mapping date object in to DateSet object
		else:
			date_dict.mapping(this_data)


main()
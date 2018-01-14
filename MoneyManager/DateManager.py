import datetime, calendar

def getDelta(amount):
	return datetime.timedelta(days=amount)

def getDays():
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	num_days = calendar.monthrange(year, month)[1]
	days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
	return days

def getNow():
	return toDate(str(datetime.datetime.now()).split(".")[0])

def toDate(data):
	date = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
	return date

def toDateOnly(data):
	date = datetime.datetime.strptime(data, '%Y-%m-%d')
	return date

from datetime import date, datetime
year = datetime.now().year

# Calendar constructed rowwise for easy iterations
calendar_rowwise = []
for month in range(1,13,1):
    new_month=[]
    for day in range(1,31,1):
        try:
            day_name = date(year=year,month=month,day=day).strftime('%A')
        except:
            day_name = ''
        new_month.append(day_name)
        month_name = date(year=year,month=month,day=1).strftime('%B')
    month_obj = {
        'month_name':month_name,
        'month_days':new_month
    }
    calendar_rowwise.append(month_obj)

# Calendar constructed column-wise for use with a table
#calendar_columwise =[]
# for day in range(1,31,1):
#     new_day =[]
#     for month in range(1,13,1):
#         try:
#             day_name = date(year=year,month=month,day=day).strftime('%A')
#         except:
#             day_name = ''
#         month_name = date(year=year,month=month,day=1).strftime('%B')
#         new_day.append({'month_name':month_name,'day_name':day_name})
#     calendar_columwise.append(new_day)


day_rows = dict()
for day in range(1,31,1):
    new_day = []
    for month in range(1,13,1):
        try:
            day_name = date(year=year,month=month,day=day).strftime('%A')
        except:
            day_name = ''
        new_day.append(day_name)
    day_rows[day] = new_day
month_names = [date(year=year,month=month,day=1).strftime('%B') for month in range(1,13,1)]
day_num = [day for day in range(1,31,1)]

calendar_columwise_dict = {
    'day_rows':day_rows,
    'month_names':month_names,
    'day_num':day_num
}

month_dict = {idx+1:month for idx, month in enumerate('Januar Februar März April Mai Juni Juli August September Oktober November Dezember'.split(' '))}
weekday_dict = {idx:day for idx, day in enumerate('Montag Dienstag Mittwoch Donnerstag Freitag Samstag Sonntag'.split(' '))}

def objectify(name,_class):
    return {'class':str(_class),'name':str(name)}

calendar_columwise = [[objectify('','empty')]+[objectify(month_dict[month],'month') for month in range(1,13,1)]]
for day in range(1,32,1):
    new_day = [objectify(str(day),'day-col')]
    for month in range(1,13,1):
        try:
            this_day = date(year=year,month=month,day=day)
            day_name = weekday_dict[this_day.weekday()]
            day_class = day_name
        except:
            day_name = ''
            day_class = 'empty'
        new_day.append(objectify(day_name,day_class))
    calendar_columwise.append(new_day)

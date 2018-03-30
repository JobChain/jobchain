from datetime import date
import calendar

def educationStartDate(year):
    if year is None:
        return 
    return date(int(year), 9, 1)

def educationEndDate(year):
    if year is None:
        return None
    return date(int(year), 6, 1)

def parseDate(dateRange):
    dates = list(filter(None, dateRange.split(' ')))
    length = len(dates)
    start = None
    end = None
    if length == 2:
        if dates[1] == 'Present':
            start = date(int(dates[0]), 1, 1)
        else:
            start = date(int(dates[0]), 1, 1)
            if dates[0] == dates[1]:
                end = date(int(dates[1]), 12, 31)
            else:
                end = date(int(dates[1]), 1, 1)
    elif length == 3:
        if dates[0].isdigit():
            start = date(int(dates[0]), 1, 1)
            month = list(calendar.month_abbr).index(dates[1])
            day = calendar.monthrange(int(dates[2]), month)[1]
            end = date(int(dates[2]), month, day)
        elif dates[2] == 'Present':
            month = list(calendar.month_abbr).index(dates[0])
            start = date(int(dates[1]), month, 1)
        else:
            month = list(calendar.month_abbr).index(dates[0])
            start = date(int(dates[1]), month, 1)
            if dates[0] == dates[2]:
                end = date(int(dates[2]), 12, 31)
            else:
                end = date(int(dates[2]), 1, 1)
    elif length == 4:
        start_month = list(calendar.month_abbr).index(dates[0])
        start = date(int(dates[1]), start_month, 1)
        if dates[0] == dates[2] and dates[1] == dates[3]:
            end_day = calendar.monthrange(int(dates[3]), end_month)[1]
        else:
            end_day = 1
        end_month = list(calendar.month_abbr).index(dates[2])
        end = date(int(dates[3]), end_month, end_day)
    return (start, end)

# Work in progress
def parseDateRange(dateRange):
    dict((v,k) for k,v in enumerate(calendar.month_abbr))
    if dateRange is None:
        return None
    dates = dateRange.split('  ')
    begin = None
    end = None
    if len(dates) == 2:
        begin = dates[0]
        end = dates[1]
    beginDay = " 1 "
    begin = begin.split(" ")
    begin = beginDay.join(begin)
    end.split(" ")
    endYear = int(end[1])
    endMonth = list(calendar.month_abbr).index(end[0])
    endDay = calendar.monthrange(endYear, endMonth)
    joinStr = " " + endDay + " "
    end = joinStr.join(end)
    return (begin, end)
    

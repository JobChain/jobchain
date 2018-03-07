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
    

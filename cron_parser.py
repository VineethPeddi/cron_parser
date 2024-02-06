#!/usr/bin/env python3
import sys
import logging

dayMap={
    "SUN" : "0",
    "MON" : "1",
    "TUE" : "2",
    "WED" : "3",
    "THU" : "4",
    "FRI" : "5",
    "SAT" : "6"
}

def get_value(timeUnit,minLimit,maxLimit):
    if timeUnit=="?":
        return list()   
    ans=[]
    for str in timeUnit.split(','):
        if "/" in str:
            numerator=str.split('/')[0]
            start=0
            if numerator!="*":
                start=int(numerator)
            increment=int(str.split('/')[1])
            ans.extend(list(range(start, maxLimit+1,increment)))
        elif "-" in str:
            start=int(str.split('-')[0])
            end=int(str.split('-')[1])
            ans.extend(list(range(start, end+1)))
        elif "*" in str:
            ans.extend(list(range(minLimit,maxLimit+1)))
        else:
            ans.append(int(str))

    return sorted(set(ans))


def get_minutes(minsStr,minValue,maxValue):
    return get_value(minsStr,minValue,maxValue)


def get_hours(hoursStr,minValue,maxValue):
    return get_value(hoursStr,minValue,maxValue)


def get_months(monthsStr,minValue,maxValue):
    return get_value(monthsStr,minValue,maxValue)


def get_dates_in_month(datesStr,minValue,maxValue):
    if "L" in datesStr:
        b=0
        if "-" in datesStr:
            b=int(datesStr.split('-')[1])
        return [30-b]
    return get_value(datesStr,minValue,maxValue)

def get_days_of_all_weeks(dayStr,minValue,maxValue):
    ans=[]
    for _ in range(4):
        ans.append([])
    if dayStr=="?":
        return ans
    if dayStr=="L":
        ans[3].append(maxValue)
        return ans
    for key,value in dayMap.items():
        dayStr=dayStr.replace(key,value)
    
    if "L" in dayStr:
        weekDay=dayStr.split('L')[0]
        ans[3].append(int(weekDay))
        return ans
    if "#" in dayStr:
        day=int(dayStr.split('#')[0])-1
        weekIdx=int(dayStr.split('#')[1])-1
        ans[weekIdx].append(day)
        return ans
    
    daysList= get_value(dayStr,minValue,maxValue)
    for i in range(4):
        ans[i]=daysList        
    return ans

def validate_cron_values(cron_values):
    if len(cron_values)!=6:
        raise ValueError("cron_string must be of length 6")
    if cron_values[2] == "?" and cron_values[4] == "?":
        raise ValueError("Both day of month and day of week cannot have ? in a cron expression")
    for cron_val in cron_values:
        for csv in cron_val.split(','):
            if (csv=="*" or csv=="L") and len(cron_val)>1:
                raise ValueError("Multiple "+ csv + " are not allowed in a cron value")
    

def expand_cron_string(cron_str):
    cron_str=cron_str.upper()
    cron_values = cron_str.split()
    try:
        validate_cron_values(cron_values)
    except ValueError as error:
        logging.error(error)
        raise
    else:
        print('minute ' + ' '.join(map(str, get_minutes(cron_values[0],0,59))))
        print('hour ' + ' '.join(map(str, get_hours(cron_values[1],0,23))))
        print('day of month ' + ' '.join(map(str, get_dates_in_month(cron_values[2],1,30))))
        print('month '+ ' '.join(map(str, get_months(cron_values[3],1,12))))
        daysInAllWeeks=get_days_of_all_weeks(cron_values[4],0,6)
        for i in range (4):
            print('day of week '+ str(i+1)+ '   '+ ' '.join(map(str, daysInAllWeeks[i])))
        print('command ',cron_values[5])

def main():
    if len(sys.argv) != 2:
        print('Usage: {} <cron_string>'.format(sys.argv[0]))
        sys.exit(1)

    cron_str = sys.argv[1]
    expand_cron_string(cron_str)
    
if __name__ == "__main__":
    main()

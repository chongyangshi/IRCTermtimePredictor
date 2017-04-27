import json
import datetime
from collections import OrderedDict

TERM_DATES = [('2013-09-30', '2013-12-06'), ('2014-01-06', '2014-03-14'),
  ('2014-04-22', '2014-06-27'), ('2014-09-29', '2014-12-05'),
  ('2015-01-05', '2015-03-13'), ('2015-04-13', '2015-06-19'),
  ('2015-09-28', '2015-12-04'), ('2016-01-04', '2016-03-11'),
  ('2016-04-11', '2016-06-17'), ('2016-09-26', '2016-12-02'),
  ('2017-01-09', '2017-03-17'), ('2017-04-18', '2017-06-23')]

def check_date_string(date):
    """ Return True if the input string is a valid YYYY-MM-DD date, False
        otherwise. """

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False

    return True


def get_next_day(date, last_day):
    """ Get the next day of a date in YYYY-MM-DD form, unless date beyond
        last_day. """

    if not check_date_string:
        return False

    last_day = datetime.datetime.strptime(last_day, '%Y-%m-%d')
    this_day = datetime.datetime.strptime(date, '%Y-%m-%d')
    next_day = this_day + datetime.timedelta(days=1)

    if this_day > last_day:
        return False

    return datetime.datetime.strftime(next_day, '%Y-%m-%d')


def is_term_time(date):
    """ Check whether date in YYYY-MM-DD is in term time. """

    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    for terms in TERM_DATES:
        start = datetime.datetime.strptime(terms[0], '%Y-%m-%d')
        end = datetime.datetime.strptime(terms[1], '%Y-%m-%d')
        if start <= date <= end:
            return True

    return False


with open('cs-york.json', 'r') as json_file:
    json_content = json.load(json_file)

# Find out the top ten who have been undergraduate students most of the time.
top_twenty = [i[0] for i in sorted(json_content['messages_all_time'].items(), key=lambda x:x[1], reverse=True)[:20]]
input_users = ['LordAro', '_46', 'Taneb', 'bjs', 'icydoge', 'liamfraser', 'Speed`', 'sdhand', 'ddm', 'nitia'] # Manually done.

# Tally by day.
messages_by_day = json_content['messages_by_day']
message_counts = {}
for day in messages_by_day:
    if not check_date_string(day):
        continue
    messages_of_the_day = messages_by_day[day]
    messages_by_user = {i:0 for i in input_users}
    for user in input_users:
        if user in messages_of_the_day:
            messages_by_user[user] = messages_of_the_day[user]
    message_counts[day] = messages_by_user

days = sorted(message_counts.keys())
last_day = days[-1]

# Write CSV
output_csv = 'date, ' + ', '.join(input_users) + ', is_term_time'
this_day = json_content['earliest_date']
while True:
    if not get_next_day(this_day, last_day):
        break

    if this_day not in message_counts:
        this_day = get_next_day(this_day, last_day)
        continue

    day_count = message_counts[this_day]
    day_line = this_day + ', '
    for user in input_users:
        day_line += str(day_count[user]) + ', '

    if is_term_time(this_day):
        day_line += '1'
    else:
        day_line += '0'

    output_csv += '\n' + day_line
    this_day = get_next_day(this_day, last_day)

with open('messages_by_day.csv', 'w') as csv:
    csv.write(output_csv)

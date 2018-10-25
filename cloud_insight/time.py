import datetime


def format_time(time_to_format):
    formatted_time = '{}Z'.format(time_to_format.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    return formatted_time


def time_ago(days=0, hours=0, minutes=0, seconds=0):
    current_time = datetime.datetime.utcnow()
    past_time = current_time - datetime.timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )
    print('Will be searching events between {} & {}'.format(current_time, past_time))
    return past_time

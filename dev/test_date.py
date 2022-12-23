from datetime import datetime, timedelta

def get_end_date_str(start_date, days_after=10):
    # Date string format: yyyy-mm-dd
    date_object = datetime.strptime(start_date, '%Y-%m-%d').date()
    td = timedelta(days=days_after)
    return str(date_object+td)

print(get_end_date_str('1980-12-12'))
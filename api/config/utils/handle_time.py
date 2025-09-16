from django.utils.timezone import localtime
from pytz import timezone

def format_time_to_est(passed_date_time):
    est = timezone('America/New_York')
    local_time = localtime(passed_date_time, est)
    return local_time.strftime('%b %d, %Y') 
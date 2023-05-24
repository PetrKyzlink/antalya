from datetime import datetime

def opening_hours(timezone):
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    
    if weekday == 0 and 7 <= hour < 24:
        return True
    elif weekday == 1 and 7 <= hour < 23:
        return True
    elif weekday == 2 and 7 <= hour < 23:
        return True
    elif weekday == 3 and 7 <= hour < 23:
        return True
    elif weekday == 4 and 6 <= hour < 23:
        return True
    elif weekday == 5 and (7 <= hour <= 23 or 0 <= hour < 1):
        return True
    elif weekday == 6 and 7 <= hour < 22:
        return True
    else:
        return False

from datetime import datetime, timedelta
import holidays


def holidays_count(start_date, end_date):
    uae_holidays = holidays.UnitedArabEmirates(years=datetime.now().year)

    count = 0

    while start_date <= end_date:
        if start_date in uae_holidays:
            count += 1
        elif start_date.weekday() in (5, 6):
            count += 1
        start_date += timedelta(days=1)

    return count


def delivery_date(delivery_day, zone=None):
    order_time = datetime.now()
    work_time = datetime.strptime("17:00", '%H:%M')

    if order_time.time() > work_time.time():
        delivery_time = datetime.now() + timedelta(days=delivery_day + 1)
    else:
        delivery_time = datetime.now() + timedelta(days=delivery_day)

    # if zone != 'Dubai':
    #     delivery_time += timedelta(days=holidays_count(order_time, delivery_time))
    delivery_time += timedelta(days=holidays_count(order_time, delivery_time))

    return delivery_time.strftime('%Y-%m-%d')
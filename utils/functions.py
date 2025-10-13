def categorize_time_of_day(hour: int) -> int:
    """
    Categorizes the hour of the day into four segments:
    0: Morning (5 AM to 11:59 AM)
    1: Afternoon (12 PM to 4:59 PM)
    2: Evening (5 PM to 8:59 PM)
    3: Night (9 PM to 4:59 AM)
    :param hour: Hour of the day (0-23)
    :return: Integer representing the time of day segment
    """
    if 5 <= hour < 12:
        return 0  # Morning
    elif 12 <= hour < 17:
        return 1  # Afternoon
    elif 17 <= hour < 21:
        return 2  # Evening
    else:
        return 3  # Night

def get_timestamp(item):
    for key in ['taken_at_timestamp', 'created_time', 'taken_at', 'date']:

        timestamp = item.get(key, 0)

        try:
            timestamp = int(timestamp)

            if timestamp > 1:  # >1 to ignore any boolean casts
                return timestamp
        except (ValueError, TypeError):
            pass

    return 0

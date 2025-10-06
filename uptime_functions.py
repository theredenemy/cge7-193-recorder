def get_uptime_days():
    import psutil
    import datetime

    pc_uptime = psutil.boot_time()

    uptime_timestamp = datetime.datetime.fromtimestamp(pc_uptime)

    the_time = datetime.datetime.now()

    delta = the_time - uptime_timestamp

    return delta.days
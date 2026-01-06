def new_session():
    return {
        "active": False,
        "start_time": None,
        "end_time": None,
        "initial_honey": None,
        "hourly_reports": 0,
        "last_hourly_image": None,
    }


def reset_session(session, start_time):
    session["active"] = True
    session["start_time"] = start_time
    session["end_time"] = None
    session["initial_honey"] = None
    session["hourly_reports"] = 0
    session["last_hourly_image"] = None


def end_session(session, end_time):
    session["active"] = False
    session["end_time"] = end_time

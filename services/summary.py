def build_summary(session):
    return (
        "🧾 **Macro Session Summary**\n"
        f"⏱️ Macro Start: {session['start_time']}\n"
        f"⏱️ Macro End: {session['end_time']}\n"
        f"🍯 Initial Honey: {session['initial_honey'] or 'Unknown'}\n"
        f"📊 Hourly Reports: {session['hourly_reports']}\n"
    )

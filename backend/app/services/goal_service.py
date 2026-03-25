from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import Activity, Goal


def compute_goal_progress(goal):
    now = datetime.utcnow().date()

    query = Activity.query.filter(
        Activity.user_id == goal.user_id,
        Activity.date >= goal.start_date,
        Activity.date <= now
    )

    if goal.category:
        query = query.filter(Activity.category == goal.category)

    result = query.with_entities(func.sum(Activity.co2_kg)).scalar()
    goal.current_co2_kg = round(result or 0.0, 3)

    if goal.end_date and now > goal.end_date:
        if goal.current_co2_kg <= goal.target_co2_kg:
            goal.status = 'achieved'
        else:
            goal.status = 'missed'

    return goal

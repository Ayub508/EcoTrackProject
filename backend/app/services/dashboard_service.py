from datetime import datetime, timedelta
from sqlalchemy import func
from app.extensions import db
from app.models import Activity


def get_summary(user_id, period='week'):
    now = datetime.utcnow().date()
    if period == 'week':
        start = now - timedelta(days=now.weekday())
    elif period == 'month':
        start = now.replace(day=1)
    elif period == 'year':
        start = now.replace(month=1, day=1)
    else:
        start = now - timedelta(days=7)

    results = db.session.query(
        Activity.category,
        func.sum(Activity.co2_kg).label('total_co2'),
        func.count(Activity.id).label('count')
    ).filter(
        Activity.user_id == user_id,
        Activity.date >= start,
        Activity.date <= now
    ).group_by(Activity.category).all()

    categories = {}
    total = 0
    for row in results:
        categories[row.category] = {
            'total_co2_kg': round(row.total_co2, 3),
            'activity_count': row.count
        }
        total += row.total_co2

    return {
        'period': period,
        'start_date': start.isoformat(),
        'end_date': now.isoformat(),
        'total_co2_kg': round(total, 3),
        'categories': categories
    }


def get_trend(user_id, weeks=12):
    now = datetime.utcnow().date()
    start = now - timedelta(weeks=weeks)

    results = db.session.query(
        func.strftime('%Y-%W', Activity.date).label('week'),
        Activity.category,
        func.sum(Activity.co2_kg).label('total_co2')
    ).filter(
        Activity.user_id == user_id,
        Activity.date >= start
    ).group_by('week', Activity.category).order_by('week').all()

    trend = {}
    for row in results:
        week_str = row.week.strftime('%Y-%m-%d') if hasattr(row.week, 'strftime') else str(row.week)
        if week_str not in trend:
            trend[week_str] = {'week': week_str, 'transport': 0, 'energy': 0, 'diet': 0, 'consumption': 0, 'total': 0}
        trend[week_str][row.category] = round(row.total_co2, 3)
        trend[week_str]['total'] += round(row.total_co2, 3)

    return sorted(trend.values(), key=lambda x: x['week'])

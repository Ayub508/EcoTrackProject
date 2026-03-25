from app.models import EmissionFactor


def lookup_emission_factor(category, sub_category):
    factor = EmissionFactor.query.filter_by(
        category=category,
        sub_category=sub_category
    ).first()
    return factor


def compute_co2(quantity, factor_value):
    return round(quantity * factor_value, 3)


def calculate_activity_co2(category, sub_category, quantity, emission_factor_id=None):
    if emission_factor_id:
        factor = EmissionFactor.query.get(emission_factor_id)
    else:
        factor = lookup_emission_factor(category, sub_category)

    if factor:
        co2_kg = compute_co2(quantity, factor.factor_value)
        return co2_kg, factor.id
    return 0.0, None

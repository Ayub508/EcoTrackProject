import numpy as np
import pandas as pd
import os


def generate_synthetic_data(n_users=1000, n_weeks=52, seed=42):
    np.random.seed(seed)

    records = []

    behaviour_profiles = {
        'high_transport': {'transport': (30, 15), 'energy': (8, 4), 'diet': (10, 5), 'consumption': (5, 3)},
        'high_energy': {'transport': (10, 5), 'energy': (25, 12), 'diet': (10, 5), 'consumption': (5, 3)},
        'high_diet': {'transport': (8, 4), 'energy': (8, 4), 'diet': (25, 10), 'consumption': (5, 3)},
        'balanced_high': {'transport': (18, 8), 'energy': (18, 8), 'diet': (18, 8), 'consumption': (12, 6)},
        'improving': {'transport': (12, 6), 'energy': (10, 5), 'diet': (10, 5), 'consumption': (5, 3)},
    }

    profile_names = list(behaviour_profiles.keys())
    countries = ['GB', 'US', 'DE', 'FR', 'IN', 'AU', 'CA']

    for user_id in range(1, n_users + 1):
        profile_name = np.random.choice(profile_names)
        profile = behaviour_profiles[profile_name]
        country = np.random.choice(countries)

        improving = profile_name == 'improving'

        for week in range(n_weeks):
            decay = 1.0 - (week / n_weeks * 0.3) if improving else 1.0
            month = (week % 52) // 4 + 1

            seasonal_factor = 1.0 + 0.15 * np.sin(2 * np.pi * (month - 1) / 12)

            transport_co2 = max(0, np.random.normal(profile['transport'][0], profile['transport'][1]) * decay * seasonal_factor)
            energy_co2 = max(0, np.random.normal(profile['energy'][0], profile['energy'][1]) * decay * seasonal_factor)
            diet_co2 = max(0, np.random.normal(profile['diet'][0], profile['diet'][1]) * decay)
            consumption_co2 = max(0, np.random.normal(profile['consumption'][0], profile['consumption'][1]) * decay)

            total_co2 = transport_co2 + energy_co2 + diet_co2 + consumption_co2

            records.append({
                'user_id': user_id,
                'week': week,
                'month': month,
                'country': country,
                'transport_co2': round(transport_co2, 2),
                'energy_co2': round(energy_co2, 2),
                'diet_co2': round(diet_co2, 2),
                'consumption_co2': round(consumption_co2, 2),
                'total_co2': round(total_co2, 2),
                'behaviour_class': profile_name,
            })

    df = pd.DataFrame(records)
    return df


def create_prediction_features(df):
    features = []

    for user_id in df['user_id'].unique():
        user_data = df[df['user_id'] == user_id].sort_values('week')

        for i in range(4, len(user_data)):
            window = user_data.iloc[i - 4:i]
            current = user_data.iloc[i]

            row = {
                'transport_avg_4w': window['transport_co2'].mean(),
                'energy_avg_4w': window['energy_co2'].mean(),
                'diet_avg_4w': window['diet_co2'].mean(),
                'consumption_avg_4w': window['consumption_co2'].mean(),
                'total_avg_4w': window['total_co2'].mean(),
                'transport_change': (window['transport_co2'].iloc[-1] - window['transport_co2'].iloc[0]) / max(window['transport_co2'].iloc[0], 0.1),
                'energy_change': (window['energy_co2'].iloc[-1] - window['energy_co2'].iloc[0]) / max(window['energy_co2'].iloc[0], 0.1),
                'diet_change': (window['diet_co2'].iloc[-1] - window['diet_co2'].iloc[0]) / max(window['diet_co2'].iloc[0], 0.1),
                'consumption_change': (window['consumption_co2'].iloc[-1] - window['consumption_co2'].iloc[0]) / max(window['consumption_co2'].iloc[0], 0.1),
                'total_change': (window['total_co2'].iloc[-1] - window['total_co2'].iloc[0]) / max(window['total_co2'].iloc[0], 0.1),
                'month': current['month'],
                'activity_frequency': 4,
                'target_co2': current['total_co2'],
            }
            features.append(row)

    return pd.DataFrame(features)


def create_classification_features(df):
    features = []

    for user_id in df['user_id'].unique():
        user_data = df[df['user_id'] == user_id].sort_values('week')

        for i in range(4, len(user_data)):
            window = user_data.iloc[i - 4:i]
            current = user_data.iloc[i]
            total = window['total_co2'].mean()
            if total == 0:
                total = 0.01

            row = {
                'transport_pct': window['transport_co2'].mean() / total,
                'energy_pct': window['energy_co2'].mean() / total,
                'diet_pct': window['diet_co2'].mean() / total,
                'consumption_pct': window['consumption_co2'].mean() / total,
                'transport_trend': 1 if window['transport_co2'].iloc[-1] > window['transport_co2'].iloc[0] else -1,
                'energy_trend': 1 if window['energy_co2'].iloc[-1] > window['energy_co2'].iloc[0] else -1,
                'diet_trend': 1 if window['diet_co2'].iloc[-1] > window['diet_co2'].iloc[0] else -1,
                'total_vs_avg_ratio': total / 50.0,
                'behaviour_class': current['behaviour_class'],
            }
            features.append(row)

    return pd.DataFrame(features)


if __name__ == '__main__':
    output_dir = os.path.join(os.path.dirname(__file__))
    df = generate_synthetic_data()
    df.to_csv(os.path.join(output_dir, 'synthetic_data.csv'), index=False)
    print(f"Generated {len(df)} records for {df['user_id'].nunique()} users")

    pred_features = create_prediction_features(df)
    pred_features.to_csv(os.path.join(output_dir, 'prediction_features.csv'), index=False)
    print(f"Created {len(pred_features)} prediction feature rows")

    class_features = create_classification_features(df)
    class_features.to_csv(os.path.join(output_dir, 'classification_features.csv'), index=False)
    print(f"Created {len(class_features)} classification feature rows")

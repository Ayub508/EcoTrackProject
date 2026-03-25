import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def train_all():
    print("=" * 50)
    print("Step 1: Generating synthetic training data...")
    print("=" * 50)
    from ml.data.synthetic_training import generate_synthetic_data, create_prediction_features, create_classification_features

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    df = generate_synthetic_data()
    df.to_csv(os.path.join(data_dir, 'synthetic_data.csv'), index=False)
    print(f"Generated {len(df)} records")

    pred_features = create_prediction_features(df)
    pred_features.to_csv(os.path.join(data_dir, 'prediction_features.csv'), index=False)
    print(f"Created {len(pred_features)} prediction features")

    class_features = create_classification_features(df)
    class_features.to_csv(os.path.join(data_dir, 'classification_features.csv'), index=False)
    print(f"Created {len(class_features)} classification features")

    print("\n" + "=" * 50)
    print("Step 2: Training Carbon Predictor...")
    print("=" * 50)
    from ml.carbon_predictor import train as train_predictor
    train_predictor()

    print("\n" + "=" * 50)
    print("Step 3: Training Behaviour Classifier...")
    print("=" * 50)
    from ml.behaviour_classifier import train as train_classifier
    train_classifier()

    print("\n" + "=" * 50)
    print("All models trained successfully!")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description='Train EcoTrack ML models')
    parser.add_argument('--model', choices=['all', 'predictor', 'classifier'],
                        default='all', help='Which model to train')
    args = parser.parse_args()

    if args.model == 'all':
        train_all()
    elif args.model == 'predictor':
        from ml.data.synthetic_training import generate_synthetic_data, create_prediction_features
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        df = generate_synthetic_data()
        pred_features = create_prediction_features(df)
        pred_features.to_csv(os.path.join(data_dir, 'prediction_features.csv'), index=False)
        from ml.carbon_predictor import train as train_predictor
        train_predictor()
    elif args.model == 'classifier':
        from ml.data.synthetic_training import generate_synthetic_data, create_classification_features
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        df = generate_synthetic_data()
        class_features = create_classification_features(df)
        class_features.to_csv(os.path.join(data_dir, 'classification_features.csv'), index=False)
        from ml.behaviour_classifier import train as train_classifier
        train_classifier()


if __name__ == '__main__':
    main()

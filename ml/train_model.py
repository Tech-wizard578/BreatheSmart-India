import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.ml_models import AQIPredictionModel
from datetime import datetime, timedelta

def generate_synthetic_training_data(n_samples=10000, sequence_length=24):
    """Generate synthetic training data for model training"""
    print(f"Generating {n_samples} synthetic training samples...")
    
    X = []
    y = []
    
    for i in range(n_samples):
        # Generate a realistic AQI sequence
        base_aqi = np.random.randint(80, 300)
        trend = np.random.uniform(-2, 2)
        noise = np.random.normal(0, 20, sequence_length)
        
        # Time-based patterns
        hour_effect = 30 * np.sin(np.linspace(0, 2*np.pi, sequence_length))
        
        # Create sequence
        aqi_sequence = base_aqi + trend * np.arange(sequence_length) + noise + hour_effect
        aqi_sequence = np.clip(aqi_sequence, 50, 450)
        
        # Create multi-feature sequence
        sequence = []
        for aqi in aqi_sequence:
            features = [
                aqi,                          # AQI
                aqi * 0.6 + np.random.normal(0, 5),   # PM2.5
                aqi * 0.8 + np.random.normal(0, 8),   # PM10
                aqi * 0.15 + np.random.normal(0, 3),  # NO2
                aqi * 0.08 + np.random.normal(0, 2),  # SO2
                aqi * 0.01 + np.random.normal(0, 0.2), # CO
                aqi * 0.12 + np.random.normal(0, 3),  # O3
                np.random.uniform(15, 35),     # Temperature
                np.random.uniform(30, 80),     # Humidity
                np.random.uniform(5, 20)       # Wind Speed
            ]
            sequence.append(features)
        
        # Target is next hour's AQI
        next_aqi = aqi_sequence[-1] + trend + np.random.normal(0, 15)
        next_aqi = np.clip(next_aqi, 50, 450)
        
        X.append(sequence)
        y.append(next_aqi)
    
    return np.array(X), np.array(y)

def load_real_data_if_available(data_path="data/historical_aqi.csv"):
    """Load real historical data if available"""
    try:
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} real data samples")
        # Process real data into sequences
        # Implementation depends on your data format
        return None, None  # Replace with actual processing
    except FileNotFoundError:
        print("No real data found, using synthetic data")
        return None, None

def prepare_training_data(sequence_length=24):
    """Prepare training, validation, and test sets"""
    
    # Try to load real data first
    X_real, y_real = load_real_data_if_available()
    
    if X_real is None:
        # Use synthetic data
        X, y = generate_synthetic_training_data(n_samples=15000, sequence_length=sequence_length)
    else:
        X, y = X_real, y_real
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Validation set: {len(X_val)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    # Reshape for ensemble models
    X_test_flat = X_test.reshape(X_test.shape[0], -1)
    
    # LSTM predictions
    lstm_preds = model.lstm_model.predict(X_test, verbose=0).flatten()
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, lstm_preds)
    mse = mean_squared_error(y_test, lstm_preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, lstm_preds)
    
    # Calculate accuracy (within 20% tolerance)
    tolerance = 0.2
    accurate_predictions = np.abs(lstm_preds - y_test) <= (y_test * tolerance)
    accuracy = np.mean(accurate_predictions) * 100
    
    print("\n" + "="*50)
    print("MODEL EVALUATION RESULTS")
    print("="*50)
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"Accuracy (±20% tolerance): {accuracy:.2f}%")
    print("="*50 + "\n")
    
    return {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'accuracy': accuracy
    }

def main():
    """Main training function"""
    print("="*50)
    print("AQI PREDICTION MODEL TRAINING")
    print("="*50 + "\n")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Initialize model
    print("Initializing AQI Prediction Model...")
    model = AQIPredictionModel(model_path='models/')
    
    # Prepare data
    print("\nPreparing training data...")
    X_train, X_val, X_test, y_train, y_val, y_test = prepare_training_data()
    
    # Train model
    print("\nStarting model training...")
    print("This may take several minutes...\n")
    
    history = model.train(
        X_train, y_train,
        X_val, y_val,
        epochs=50
    )
    
    # Evaluate model
    print("\nEvaluating model performance...")
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save metrics
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv('models/training_metrics.csv', index=False)
    
    print("\nTraining completed successfully!")
    print(f"Models saved to: models/")
    print(f"Metrics saved to: models/training_metrics.csv")

if __name__ == "__main__":
    main()
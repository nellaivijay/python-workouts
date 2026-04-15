"""
Machine Learning - Scikit-learn Basics
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import make_classification, load_iris
import warnings
warnings.filterwarnings('ignore')


def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    # Generate synthetic classification dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=3,
        random_state=42
    )
    
    # Convert to DataFrame for better visualization
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    return df


def preprocess_data(df, target_column='target'):
    """
    Data preprocessing pipeline
    """
    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Handle missing values (if any)
    X = X.fillna(X.mean())
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, scaler


def split_data(X, y, test_size=0.2, random_state=42):
    """Split data into training and testing sets"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def train_random_forest(X_train, y_train):
    """Train a Random Forest classifier"""
    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    return rf_model


def train_logistic_regression(X_train, y_train):
    """Train a Logistic Regression classifier"""
    lr_model = LogisticRegression(
        random_state=42,
        max_iter=1000
    )
    lr_model.fit(X_train, y_train)
    return lr_model


def train_svm(X_train, y_train):
    """Train a Support Vector Machine classifier"""
    svm_model = SVC(
        kernel='rbf',
        random_state=42
    )
    svm_model.fit(X_train, y_train)
    return svm_model


def evaluate_model(model, X_test, y_test, model_name):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    print(f"\n{model_name} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Confusion Matrix:\n{conf_matrix}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix,
        'predictions': y_pred
    }


def feature_importance(model, feature_names):
    """Get feature importance from tree-based models"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        return feature_importance_df
    return None


def iris_dataset_example():
    """Example using the classic Iris dataset"""
    print("\n" + "=" * 50)
    print("Iris Dataset Example")
    print("=" * 50)
    
    # Load Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    
    print(f"Dataset shape: {X.shape}")
    print(f"Number of classes: {len(np.unique(y))}")
    print(f"Feature names: {feature_names}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    print("\nTraining Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)
    
    # Evaluate models
    rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test_scaled))
    lr_accuracy = accuracy_score(y_test, lr_model.predict(X_test_scaled))
    
    print(f"\nRandom Forest Accuracy: {rf_accuracy:.4f}")
    print(f"Logistic Regression Accuracy: {lr_accuracy:.4f}")
    
    # Feature importance
    importance_df = feature_importance(rf_model, feature_names)
    if importance_df is not None:
        print("\nFeature Importance:")
        print(importance_df)


def main():
    """Main function to demonstrate ML workflow"""
    print("Machine Learning with Scikit-learn")
    print("=" * 50)
    
    # Create sample dataset
    print("\n1. Creating Sample Dataset:")
    df = create_sample_dataset()
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution:\n{df['target'].value_counts()}")
    
    # Preprocess data
    print("\n2. Data Preprocessing:")
    X, y, scaler = preprocess_data(df)
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Split data
    print("\n3. Train-Test Split:")
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train models
    print("\n4. Training Models:")
    
    print("   Training Random Forest...")
    rf_model = train_random_forest(X_train, y_train)
    
    print("   Training Logistic Regression...")
    lr_model = train_logistic_regression(X_train, y_train)
    
    print("   Training SVM...")
    svm_model = train_svm(X_train, y_train)
    
    # Evaluate models
    print("\n5. Model Evaluation:")
    
    rf_results = evaluate_model(rf_model, X_test, y_test, "Random Forest")
    lr_results = evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    svm_results = evaluate_model(svm_model, X_test, y_test, "SVM")
    
    # Feature importance
    print("\n6. Feature Importance (Random Forest):")
    feature_names = [col for col in df.columns if col != 'target']
    importance_df = feature_importance(rf_model, feature_names)
    if importance_df is not None:
        print(importance_df.head(10))
    
    # Model comparison
    print("\n7. Model Comparison:")
    comparison = pd.DataFrame({
        'Model': ['Random Forest', 'Logistic Regression', 'SVM'],
        'Accuracy': [rf_results['accuracy'], lr_results['accuracy'], svm_results['accuracy']]
    }).sort_values('Accuracy', ascending=False)
    
    print(comparison)
    
    # Iris dataset example
    iris_dataset_example()
    
    print("\n" + "=" * 50)
    print("Machine Learning Key Concepts:")
    print("✓ Data preprocessing and feature scaling")
    print("✓ Train-test splitting for model evaluation")
    print("✓ Multiple algorithm comparison")
    print("✓ Model evaluation metrics")
    print("✓ Feature importance analysis")
    print("✓ Working with real datasets")
    print("\nTo run this script:")
    print("pip install scikit-learn pandas numpy")


if __name__ == "__main__":
    main()
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
try:
    from imblearn.over_sampling import SMOTE
except ImportError:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "imbalanced-learn"])
    from imblearn.over_sampling import SMOTE

def preprocess_data(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Fill missing values before encoding
    num_cols = X.select_dtypes(include=[np.number]).columns
    cat_cols = X.select_dtypes(include=['object', 'category']).columns
    
    for col in num_cols:
        X[col] = X[col].fillna(X[col].mean())
    for col in cat_cols:
        if not X[col].mode().empty:
            X[col] = X[col].fillna(X[col].mode()[0])
            
    # Dummy encoding for any remaining categorical columns
    if len(cat_cols) > 0:
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
    
    # Scale ALL features that are now numeric
    final_features = X.columns
    scaler = StandardScaler()
    if len(final_features) > 0:
        X[final_features] = scaler.fit_transform(X[final_features])
    
    # Encode target if necessary
    if y.dtype == 'object' or y.name == 'category':
        le = LabelEncoder()
        y = le.fit_transform(y)
        
    y = y.astype(int)
    return X, y, scaler

def train_and_evaluate(filepath, target_col, save_path, binarize_target=False, sep=','):
    print(f"\n{'='*50}")
    print(f"Executing Pipeline for {filepath}")
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return
        
    df = pd.read_csv(filepath, sep=sep)
    print(f"Loaded records: {df.shape}")
    
    # DROP 'id' and 'dataset' if they exist to prevent feature mismatch
    for col_to_drop in ['id', 'ID', 'dataset', 'Dataset']:
        if col_to_drop in df.columns:
            print(f"Dropping non-feature column: {col_to_drop}")
            df = df.drop(columns=[col_to_drop])

    # Special handling for heart disease categorical mapping
    if "heart_disease.csv" in filepath:
        print("Applying robust manual encoding for heart disease categorical columns...")
        # Lowercase and strip for robust matching
        for col_name in ['sex', 'cp', 'restecg', 'slope', 'thal', 'fbs', 'exang']:
            if col_name in df.columns:
                df[col_name] = df[col_name].astype(str).str.lower().str.strip()

        # sex: male->1, female->0
        if 'sex' in df.columns:
            df['sex'] = df['sex'].map({'male': 1, 'female': 0, '1': 1, '0': 0}).fillna(1).astype(int)
        # fbs: true->1, false->0
        if 'fbs' in df.columns:
            df['fbs'] = df['fbs'].map({'true': 1, 'false': 0, 'nan': 0, '1': 1, '0': 0}).fillna(0).astype(int)
        # exang: true->1, false->0
        if 'exang' in df.columns:
            df['exang'] = df['exang'].map({'true': 1, 'false': 0, 'nan': 0, '1': 1, '0': 0}).fillna(0).astype(int)
        # cp
        cp_map = {'typical angina': 1, 'atypical angina': 2, 'non-anginal': 3, 'asymptomatic': 4}
        if 'cp' in df.columns:
            df['cp'] = df['cp'].map(cp_map).fillna(4).astype(int)
        # restecg
        restecg_map = {'normal': 0, 'st-t abnormality': 1, 'lv hypertrophy': 2}
        if 'restecg' in df.columns:
            df['restecg'] = df['restecg'].map(restecg_map).fillna(0).astype(int)
        # slope
        slope_map = {'upsloping': 1, 'flat': 2, 'downsloping': 3}
        if 'slope' in df.columns:
            df['slope'] = df['slope'].map(slope_map).fillna(1).astype(int)
        # thal
        thal_map = {'normal': 3, 'fixed defect': 6, 'reversable defect': 7}
        if 'thal' in df.columns:
            df['thal'] = df['thal'].map(thal_map).fillna(3).astype(int)

    if target_col not in df.columns:
        print(f"Configured target column '{target_col}' not found. Available: {list(df.columns)}")
        return
        
    X, y, scaler = preprocess_data(df, target_col)
    
    # Binarize if requested
    if binarize_target:
        y = (y > 0).astype(int)
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    print("Executing SMOTE for class imbalance...")
    min_class = np.min(np.bincount(y_train))
    k_neighbors = min(5, max(1, min_class - 1))
    
    try:
        smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    except Exception as e:
        print(f"SMOTE Warning: {e}. Falling back to original class balance.")
        X_train_res, y_train_res = X_train, y_train
        
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }
    
    best_model = None
    best_f1 = -1
    best_name = ""
    best_metrics = {}
    
    print("Training classifiers...")
    for name, model in models.items():
        try:
            model.fit(X_train_res, y_train_res)
            y_pred = model.predict(X_test)
            
            try:
                y_proba = model.predict_proba(X_test)
                if len(np.unique(y_test)) == 2:
                    roc = roc_auc_score(y_test, y_proba[:, 1])
                else:
                    roc = roc_auc_score(y_test, y_proba, multi_class='ovr')
            except Exception:
                roc = 0.0

            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            if f1 > best_f1:
                best_f1 = f1
                best_model = model
                best_name = name
                best_metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                    'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                    'f1': f1,
                    'roc_auc': roc,
                    'classification_report': classification_report(y_test, y_pred, zero_division=0),
                    'confusion_matrix': confusion_matrix(y_test, y_pred)
                }
        except Exception as err:
            print(f"Failed to train {name}: {err}")
            
    print(f">>> Best Selected Model: {best_name} (F1 Score: {best_f1:.4f}, ROC_AUC: {best_metrics['roc_auc']:.4f})")
    print(best_metrics['classification_report'])
    print(f"Confusion Matrix:\n{best_metrics['confusion_matrix']}")
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    # Save both model and scaler. Prediction service uses scaler first.
    joblib.dump({'model': best_model, 'scaler': scaler}, save_path)
    print(f"Exported artifact to {save_path}")

def main():
    datasets_base = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    models_base = os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'models')
    
    # Config definition
    configs = [
        {
            "filepath": os.path.join(datasets_base, "heart_disease.csv"),
            "target": "target",
            "save_path": os.path.join(models_base, "heart_model.pkl"),
            "binarize": True,
            "sep": ","
        },
        {
            "filepath": os.path.join(datasets_base, "diabetes.csv"),
            "target": "Outcome",
            "save_path": os.path.join(models_base, "diabetes_model.pkl"),
            "binarize": False,
            "sep": ","
        },
        {
            "filepath": os.path.join(datasets_base, "cardiovascular.csv"),
            "target": "cardio",
            "save_path": os.path.join(models_base, "cardio_model.pkl"),
            "binarize": False,
            "sep": ";"
        },
        {
            "filepath": os.path.join(datasets_base, "health_indicators.csv"),
            "target": "Diabetes_012",
            "save_path": os.path.join(models_base, "health_indicators_model.pkl"),
            "binarize": True,
            "sep": ","
        }
    ]
    
    for cfg in configs:
        # Resolve target aliases
        try:
            df_temp = pd.read_csv(cfg['filepath'], sep=cfg['sep'], nrows=1)
            # Find target if it's 'num' instead of 'target'
            if cfg['target'] not in df_temp.columns:
                if 'num' in df_temp.columns:
                    cfg['target'] = 'num'
                elif 'target' in df_temp.columns:
                    cfg['target'] = 'target'
        except Exception:
            pass
            
        train_and_evaluate(cfg['filepath'], cfg['target'], cfg['save_path'], cfg['binarize'], cfg['sep'])

if __name__ == "__main__":
    main()

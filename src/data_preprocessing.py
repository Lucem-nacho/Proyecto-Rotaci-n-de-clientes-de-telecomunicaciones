import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def load_and_preprocess_data(test_size=0.2, random_state=42):
    """
    Carga el dataset crudo, aplica limpieza, divide en Train/Test y 
    aplica las transformaciones evitando el Data Leakage.
    """
    # 1. Rutas dinámicas
    BASE_DIR = Path(__file__).resolve().parent.parent
    raw_path = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    
    # Carga de datos
    df = pd.read_csv(raw_path)
    
    # 2. Limpieza e Imputación Profesional
    df['TotalCharges'] = df['TotalCharges'].replace(" ", "0")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
    
    # Mapeo temprano de la variable objetivo
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # Eliminación de columnas sin valor predictivo
    df = df.drop(columns=['customerID'])
    
    # Separación de características y variable objetivo
    X = df.drop(columns=['Churn'])
    y = df['Churn']
    
    # 3. DIVISIÓN TRAIN/TEST (¡El paso clave del profesor!)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # 4. Pipeline de Preprocesamiento (Scikit-Learn)
    numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
        ],
        remainder='passthrough'
    )
    
    # 5. Transformación Diferenciada para evitar Data Leakage
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Reconstrucción de los DataFrames
    feature_names = [n.split('__')[-1] for n in preprocessor.get_feature_names_out()]
    
    X_train_df = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_processed, columns=feature_names)
    
    return X_train_df, X_test_df, y_train, y_test

# Bloque de prueba local
if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    print(f"Dataset procesado con éxito sin Data Leakage.")
    print(f"Dimensiones de X_train: {X_train.shape}")
    print(f"Dimensiones de X_test: {X_test.shape}")
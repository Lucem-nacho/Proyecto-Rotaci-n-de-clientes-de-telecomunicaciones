import pandas as pd
from pathlib import Path

def audit_data(file_path="data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"):
    """
    Realiza una auditoria tecnica del dataset para asegurar la integridad del pipeline.
    Verifica la existencia del archivo, que no este vacio y que contenga las columnas necesarias.
    """
    print(f"Iniciando auditoria de: {file_path}")
    path = Path(file_path)

    # 1. Verificar si el archivo existe en la ruta especificada
    if not path.exists():
        print(f"Error: El archivo no se encuentra en {file_path}")
        return False

    try:
        # Carga de una muestra para validacion estructural
        df_audit = pd.read_csv(path, nrows=100)
        
        # 2. Verificar si el archivo contiene registros
        if df_audit.empty:
            print("Error: El archivo CSV esta vacio.")
            return False

        # 3. Validar presencia de columnas criticas para la pregunta de negocio
        # Se requiere informacion de facturacion, contrato y la variable objetivo
        required_columns = ['MonthlyCharges', 'TotalCharges', 'Contract', 'Churn']
        missing_columns = [col for col in required_columns if col not in df_audit.columns]
        
        if missing_columns:
            print(f"Error: Faltan columnas criticas en el dataset: {missing_columns}")
            return False

        print("Auditoria completada: La estructura y disponibilidad de los datos es correcta.")
        return True

    except Exception as e:
        print(f"Error inesperado durante el proceso de auditoria: {e}")
        return False
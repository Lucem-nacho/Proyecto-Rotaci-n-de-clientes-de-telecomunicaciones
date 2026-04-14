import pandas as pd
import numpy as np

def clean_data(df):
    # Convierte TotalCharges a numérico y maneja espacios en blanco
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    # Elimina filas con nulos (los 11 clientes con tenure 0)
    df.dropna(inplace=True)
    return df

import pandas as pd
from pathlib import Path
from src.audit import audit_data
from src.transformers import clean_data

def main():
    """
    Script principal de orquestacion para el proyecto de prediccion de rotacion.
    Coordina la auditoria, carga, limpieza y guardado de datos.
    """
    print("--- Iniciando Pipeline de Preparacion de Datos: Telco Churn ---")

    try:
        # 1. Fase de Auditoria
        # Verifica integridad, existencia y columnas necesarias antes de procesar.
        raw_path = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
        if not audit_data(raw_path):
            print("Pipeline detenido: El archivo no supero las validaciones de auditoria.")
            return

        # 2. Carga de Datos
        print(f"Cargando datos desde: {raw_path}")
        df_raw = pd.read_csv(raw_path)

        # 3. Fase de Transformacion y Limpieza
        # Se aplican las correcciones de tipado y manejo de valores nulos.
        print("Aplicando transformaciones y limpieza de datos...")
        df_processed = clean_data(df_raw)

        # 4. Fase de Guardado
        # Se exporta el resultado final a la carpeta de datos procesados.
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        output_path = processed_dir / "processed_data.csv"
        
        df_processed.to_csv(output_path, index=False)
        
        print(f"Resultado: El dataset procesado se ha guardado en {output_path}")
        print(f"Dimensiones finales: {df_processed.shape}")
        print("--- Pipeline finalizado exitosamente ---")

    except FileNotFoundError:
        print("Error critico: No se encontro el archivo en la ruta especificada.")
    except pd.errors.EmptyDataError:
        print("Error critico: El archivo CSV esta vacio.")
    except Exception as e:
        print(f"Error fatal: El pipeline fallo inesperadamente debido a: {e}")

if __name__ == "__main__":
    main()
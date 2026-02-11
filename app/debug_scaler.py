import joblib
from pathlib import Path


SCALER_PATH = Path("app/ml_models/scaler_xv2.pkl")

def inspect_scaler():
    if not SCALER_PATH.exists():
        print(f"Arquivo não encontrado: {SCALER_PATH}")
        return

    scaler = joblib.load(SCALER_PATH)

        

    if hasattr(scaler, 'n_features_in_'):
        print(f"\nTotal de features : {scaler.n_features_in_}")

if __name__ == "__main__":
    inspect_scaler()
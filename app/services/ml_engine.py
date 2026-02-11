import joblib
import numpy as np
import tensorflow as tf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_models" / "lstm_reservatorio_model.keras"
SCALER_X_PATH = BASE_DIR / "ml_models" / "scaler_xv2.pkl"
SCALER_Y_PATH = BASE_DIR / "ml_models" / "scaler_yv2.pkl"

class MLEngine:
    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)
        self.scaler_x = joblib.load(SCALER_X_PATH)
        self.scaler_y = joblib.load(SCALER_Y_PATH)

    def predict(self, feature_list: list):
    # 1. Garanta que o input tenha o shape correto (n_samples, n_features)
     X_input = np.array([feature_list], dtype=np.float32)
    
    # 2. Transformação
     X_scaled = self.scaler_x.transform(X_input)

    # 3. [DICA DE OURO] Clipar os valores
    # Se a entrada for maior que o treino, ele trava no limite do scaler
    # Isso evita que o modelo receba valores bizarros (ex: 1.5, 2.0)
     X_scaled = np.clip(X_scaled, 0, 1) 
    
    # 4. Reshape para LSTM (Batch, Timesteps, Features)
     X_3d = X_scaled.reshape((1, 1, 16))
    
    # 5. Predição
     y_pred_scaled = self.model.predict(X_3d, verbose=0)
    
    # 6. Inverse Transform
     y_final = self.scaler_y.inverse_transform(y_pred_scaled)
    
     return float(y_final[0][0])

engine = MLEngine()
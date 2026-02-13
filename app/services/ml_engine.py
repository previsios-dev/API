import joblib
import logging
import numpy as np
import tensorflow as tf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_models" / "lstm_reservatorio_model.keras"
SCALER_X_PATH = BASE_DIR / "ml_models" / "scaler_xv2.pkl"
SCALER_Y_PATH = BASE_DIR / "ml_models" / "scaler_yv2.pkl"
EXPECTED_FEATURES = 16

logger = logging.getLogger(__name__)


class MLEngine:
    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)
        self.scaler_x = joblib.load(SCALER_X_PATH)
        self.scaler_y = joblib.load(SCALER_Y_PATH)
        self.expected_features = getattr(self.scaler_x, "n_features_in_", EXPECTED_FEATURES)

    def predict(self, feature_list: list):
        # Garante shape (1, n_features) com todos os valores numéricos.
        x_input = np.asarray(feature_list, dtype=np.float32).reshape(1, -1)
        if x_input.shape[1] != self.expected_features:
            raise ValueError(
                f"Quantidade de features inválida: recebido={x_input.shape[1]}, "
                f"esperado={self.expected_features}"
            )
        if not np.isfinite(x_input).all():
            raise ValueError("Features contêm NaN ou infinito.")

        x_scaled = self.scaler_x.transform(x_input)
        out_of_range = int(((x_scaled < 0) | (x_scaled > 1)).sum())
        if out_of_range:
            logger.warning("Detectado drift em %s feature(s): valores fora do range do scaler.", out_of_range)

        # Mantém entrada dentro do intervalo esperado pelo modelo.
        x_scaled = np.clip(x_scaled, 0, 1)
        x_3d = x_scaled.reshape((1, 1, self.expected_features))

        y_pred_scaled = self.model.predict(x_3d, verbose=0)
        y_pred_scaled = np.clip(y_pred_scaled, 0, 1)
        y_final = self.scaler_y.inverse_transform(y_pred_scaled)

        return float(y_final[0][0])

engine = MLEngine()

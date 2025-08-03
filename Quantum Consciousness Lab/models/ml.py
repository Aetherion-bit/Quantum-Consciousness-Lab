from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from pennylane import qnn
import numpy as np
from models.eeg import analyze_eeg_band

def classify_eeg(eeg_data: np.ndarray, sfreq: float) -> dict:
    """
    Classifies EEG patterns using SVM.
    """
    features = analyze_eeg_band(eeg_data, sfreq)
    X = np.array([features["band_power"][band] for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']] + [features["connectivity_wpli"], features["entropy"]])
    
    model = SVC(probability=True)
    model.fit(X.reshape(1, -1), [0])  # Placeholder training
    prediction = model.predict(X.reshape(1, -1))
    return {"prediction": int(prediction[0]), "probabilities": model.predict_proba(X.reshape(1, -1)).tolist(), "classes": ["normal", "altered"]}

def classify_emotion(eeg_data: np.ndarray, sfreq: float) -> dict:
    """
    Classifies emotions using RandomForest.
    """
    features = analyze_eeg_band(eeg_data, sfreq)
    X = np.array([features["band_power"][band] for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']])
    model = RandomForestClassifier()
    model.fit(X.reshape(1, -1), [0])
    return {"emotion": model.predict(X.reshape(1, -1)).tolist(), "classes": ["happy", "sad", "neutral"]}

def hybrid_classifier(eeg_data: np.ndarray, sfreq: float) -> dict:
    """
    Combines QNN and XGBoost for hybrid classification.
    """
    features = analyze_eeg_band(eeg_data, sfreq)
    inputs = np.array([features["band_power"][band] for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']] + [features["connectivity_wpli"]])
    
    dev = qml.device("default.qubit", wires=4)
    @qml.qnode(dev)
    def qnn_circuit(inputs, weights):
        qml.AngleEmbedding(inputs[:4], wires=range(4))
        qml.StronglyEntanglingLayers(weights, wires=range(4))
        return [qml.expval(qml.PauliZ(i)) for i in range(4)]
    
    weight_shapes = {"weights": (3, 4, 3)}
    qnn_model = qnn.KerasLayer(qnn_circuit, weight_shapes, output_dim=4)
    qnn_pred = qnn_model(inputs)
    
    xgb_model = XGBClassifier()
    xgb_pred = xgb_model.predict_proba(inputs.reshape(1, -1))
    
    ensemble_pred = 0.5 * qnn_pred + 0.5 * xgb_pred[0]
    return {"prediction": np.argmax(ensemble_pred), "probabilities": ensemble_pred.tolist()}

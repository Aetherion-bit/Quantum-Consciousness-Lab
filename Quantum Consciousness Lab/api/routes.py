from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from models import consciousness, eeg, ml, optimization, connectivity, neuromorphic, multimodal
from services import collaboration, cloud, blockchain, ar_vr

router = APIRouter()

class ConsciousnessInput(BaseModel):
    density_matrix: list = Field(..., description="Quantum density matrix (flattened)")
    entanglement: float = Field(..., ge=0.0, le=1.0, description="Entanglement measure [0-1]")
    entropy: float = Field(..., ge=0.0, description="Von Neumann entropy")
    qft_noise: float = Field(..., ge=0.0, description="QFT noise")
    decoherence: float = Field(..., ge=0.0, description="Decoherence rate")

class EEGInput(BaseModel):
    eeg_data: list = Field(..., description="EEG data array")
    sfreq: float = Field(..., gt=0.0, description="Sampling frequency in Hz")

class MultimodalInput(BaseModel):
    fmri_file: str = Field(..., description="Path to fMRI file")
    eeg_data: list = Field(..., description="EEG data array")

class CollaborationInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    data: dict = Field(..., description="Session data")

class ProvenanceInput(BaseModel):
    data: dict = Field(..., description="Data to record")
    contract_address: str = Field(..., description="Blockchain contract address")

@router.post("/compute_consciousness")
async def calculate_consciousness(input: ConsciousnessInput):
    try:
        return consciousness.compute_consciousness(
            input.density_matrix, input.entanglement, input.entropy,
            input.qft_noise, input.decoherence
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compute_c_sigma")
async def calculate_c_sigma(input: EEGInput):
    try:
        return consciousness.compute_c_sigma(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze_eeg")
async def analyze_eeg(input: EEGInput):
    try:
        return eeg.analyze_eeg_band(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/classify_eeg")
async def classify_eeg_data(input: EEGInput):
    try:
        return ml.classify_eeg(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/classify_emotion")
async def classify_emotion_data(input: EEGInput):
    try:
        return ml.classify_emotion(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/hybrid_classifier")
async def hybrid_classify(input: EEGInput):
    try:
        return ml.hybrid_classifier(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize_frequencies")
async def optimize_f(input: EEGInput):
    try:
        return optimization.optimize_frequencies(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stabilize_coherence")
async def stabilize(input: EEGInput):
    try:
        return optimization.stabilize_coherence(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stabilize_coherence_dqn")
async def stabilize_dqn(input: EEGInput):
    try:
        return optimization.stabilize_coherence_dqn(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/qaoa_feedback")
async def qaoa(input: EEGInput):
    try:
        return optimization.qaoa_feedback(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gnn_connectivity")
async def gnn_connect(input: EEGInput):
    try:
        return connectivity.gnn_connectivity(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/neuromorphic_simulation")
async def neuromorphic_sim(input: EEGInput):
    try:
        return neuromorphic.neuromorphic_simulation(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/integrate_fmri")
async def integrate_fmri_data(input: MultimodalInput):
    try:
        return multimodal.integrate_fmri(input.fmri_file, np.array(input.eeg_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream_ar_vr")
async def stream_ar_vr(input: EEGInput):
    try:
        return ar_vr.stream_ar_vr_brain(np.array(input.eeg_data), input.sfreq)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create_collaboration_session")
async def create_session(input: CollaborationInput):
    try:
        return collaboration.create_collaboration_session(input.user_id, input.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream_to_aws")
async def stream_aws(data: dict):
    try:
        return cloud.stream_to_aws(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/record_provenance")
async def record_provenance(input: ProvenanceInput):
    try:
        return blockchain.record_data_provenance(input.data, input.contract_address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

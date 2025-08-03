# API Documentation

## Endpoints
- **POST /api/compute_consciousness**: Computes \(C(t)\).
  - Input: `{ "density_matrix": [...], "entanglement": 0.5, "entropy": 0.1, "qft_noise": 0.1, "decoherence": 0.1 }`
  - Output: `{ "C(t)": 0.123, "phi_qm": 0.25, ... }`
- **POST /api/compute_c_sigma**: Computes \(C_\Sigma(t)\).
- **POST /api/analyze_eeg**: Analyzes EEG with FFT, wavelet, Hilbert, tensor decomposition.
- **POST /api/classify_eeg**: Classifies EEG patterns.
- **POST /api/classify_emotion**: Classifies emotions.
- **POST /api/hybrid_classifier**: Hybrid QNN-XGBoost classification.
- **POST /api/optimize_frequencies**: Optimizes \(f_1\), \(f_2\).
- **POST /api/stabilize_coherence**: PPO-based coherence stabilization.
- **POST /api/stabilize_coherence_dqn**: DQN-based coherence stabilization.
- **POST /api/qaoa_feedback**: QAOA-based feedback.
- **POST /api/gnn_connectivity**: GNN-based connectivity analysis.
- **POST /api/neuromorphic_simulation**: Neuromorphic simulation.
- **POST /api/integrate_fmri**: Integrates fMRI with EEG.
- **POST /api/stream_ar_vr**: Streams to AR/VR.
- **POST /api/create_collaboration_session**: Creates multi-user session.
- **POST /api/stream_to_aws**: Streams to AWS S3.
- **POST /api/record_provenance**: Records data on blockchain.

## WebSocket
- **/ws/eeg_stream**: Real-time EEG streaming.
- **/ws/bci_stream**: Real-time BCI streaming.

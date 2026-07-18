# 🧠 MONCO — Brain Tumor Detection using Deep Learning

MONCO is an end-to-end deep learning application that classifies brain MRI scans into four categories — **glioma**, **meningioma**, **pituitary tumor**, or **no tumor** — using transfer learning on **VGG16**, and now generates a **natural language AI explanation** of each result. The project covers the full pipeline: data preprocessing, model training and evaluation, a **FastAPI** inference backend, and a modular **Streamlit** web interface for real-time predictions.

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white">
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00?logo=tensorflow&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="Plotly" src="https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-lightgrey">
</p>

---

## 📌 Overview

MRI-based brain tumor diagnosis is time-consuming and requires expert radiological review. MONCO assists this process by using a convolutional neural network built on top of **VGG16 (ImageNet weights)** to classify an uploaded MRI scan into one of four classes, along with a confidence score, a full class-probability breakdown, and an **AI-generated explanation** of what the prediction means — all served through a clean web dashboard.

> ⚠️ **Disclaimer:** MONCO is a research and educational project. It is **not** a certified medical device and should **never** be used as a substitute for professional diagnosis.

---

## 🎯 Key Features

- **Transfer learning** with a frozen VGG16 backbone plus a custom classification head
- Real-time image augmentation (brightness/contrast jitter) during training
- Batch-wise data generator to handle large MRI datasets without loading everything into memory
- **FastAPI** backend exposing a `/predict` REST endpoint that returns the prediction, confidence, full per-class probability distribution, and an AI-generated natural language explanation
- **Streamlit** dashboard, split into modular components, for uploading a scan and viewing:
  - The predicted class as a color-coded badge
  - A confidence score and progress bar
  - An interactive **Plotly** probability distribution chart across all four classes
  - An expandable **AI Explanation** panel rendered from the backend's Markdown output
- Friendly, non-crashing error handling for backend downtime, timeouts, and invalid responses
- Full evaluation suite — classification report, confusion matrix, and multi-class ROC/AUC curves

---

## 🧬 Model Architecture

| Component | Details |
|---|---|
| Base model | VGG16 (`include_top=False`, ImageNet weights) |
| Input size | 128 × 128 × 3 |
| Trainable layers | Base frozen; head layers trainable |
| Head | Flatten → Dropout(0.3) → Dense(128, ReLU) → Dropout(0.2) → Dense(4, Softmax) |
| Optimizer | Adam (lr = 0.0001) |
| Loss | Sparse Categorical Crossentropy |
| Metric | Sparse Categorical Accuracy |
| Epochs | 20 (batch size 20) |

**Classes:** `glioma`, `meningioma`, `pituitary`, `notumor`

---

## 📊 Results

**Training performance:** reached **94.82% training accuracy** with a final loss of **0.1388** after 20 epochs.

**Test set classification report (1,600 test images):**

| Class | Precision | Recall | F1-score | Support |
|---|---|---|---|---|
| glioma | 0.95 | 0.73 | 0.82 | 400 |
| pituitary | 0.98 | 0.95 | 0.96 | 400 |
| meningioma | 0.79 | 0.92 | 0.85 | 400 |
| notumor | 0.91 | 1.00 | 0.95 | 400 |
| **Accuracy** | | | **0.90** | 1600 |
| Macro avg | 0.91 | 0.90 | 0.90 | 1600 |
| Weighted avg | 0.91 | 0.90 | 0.90 | 1600 |

**ROC-AUC per class:**

| Class | AUC |
|---|---|
| glioma | 0.91 |
| pituitary | 1.00 |
| meningioma | 0.97 |
| notumor | 1.00 |

The confusion matrix and ROC curve are available in the training notebook (`main.ipynb`).

---

## 🗂️ Project Structure

```
MONCO/
├── .devcontainer/
│   └── devcontainer.json        # Dev container config for consistent environments
│
├── app/                         # FastAPI backend
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py           # App-wide settings (paths, model config, Ollama host/model)
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── prompt_builder.py     # Builds the prompt sent to the LLM for each prediction
│   │   └── service.py             # Calls Ollama (gemma3:4b) and returns the explanation
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   ├── loader.py              # Loads the trained Keras/VGG16 model
│   │   └── predictor.py           # Runs inference and returns class + probabilities
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── predict.py             # /predict route definition
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── prediction_service.py  # Orchestrates prediction + LLM explanation for a request
│   │
│   ├── __init__.py
│   ├── main.py                    # FastAPI entrypoint
│   ├── schemas.py                 # Pydantic request/response schemas
│   └── utils.py                   # Image preprocessing helpers
│
├── dataset/
│   └── data/
│       ├── Testing/               # Testing images, per-class folders
│       │   ├── glioma/
│       │   ├── meningioma/
│       │   ├── notumor/
│       │   └── pituitary/
│       └── Training/              # Training images, per-class folders
│           ├── glioma/
│           ├── meningioma/
│           ├── notumor/
│           └── pituitary/
│
├── model/
│   ├── classes.json               # Class label mapping
│   ├── monco.h5                    # Saved model (HDF5 format)
│   └── monco.keras                 # Saved model (Keras native format)
│
├── streamlit_app/
│   ├── assets/
│   ├── __init__.py
│   ├── app.py                     # Main entrypoint - orchestrates the modules below
│   ├── config.py                   # API URL, class labels, colors, emojis
│   ├── api_client.py                # Backend communication + error handling
│   ├── charts.py                     # Plotly probability distribution chart
│   └── ui_components.py               # Styling and reusable UI render functions
│
├── main.ipynb                     # Full training & evaluation notebook
├── .gitattributes
├── .gitignore
└── .python-version
```

---

## ⚙️ Tech Stack

- **Deep Learning:** TensorFlow, Keras, VGG16
- **Backend:** FastAPI
- **Explanation Generation:** [Ollama](https://ollama.com) running **gemma3:4b** locally for natural language prediction explanations
- **Frontend:** Streamlit, Plotly
- **Data & Evaluation:** NumPy, scikit-learn, Seaborn, Matplotlib
- **Image Processing:** Pillow (PIL)

---

## 🚀 Getting Started

### 0. Prerequisite: Ollama

The AI explanation feature calls a local **Ollama** instance running **gemma3:4b**. Install Ollama, then pull and serve the model:

```bash
ollama pull gemma3:4b
ollama serve
```

### 1. Clone the repository

```bash
git clone https://github.com/Manabendu-ai/MONCO.git
cd MONCO
```
> Replace with your actual repository URL if different.

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI backend

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 5. Run the Streamlit frontend

```bash
streamlit run streamlit_app/app.py
```

The web app will open at `http://localhost:8501`.

---

## 🔌 API Usage

**Endpoint:** `POST /predict`

**Request:** `multipart/form-data` with an image file field named `file`

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@sample_mri.jpg"
```

**Example response:**
```json
{
  "prediction": "glioma",
  "confidence": 99.89,
  "probabilities": {
    "glioma": 99.89,
    "pituitary": 0.03,
    "meningioma": 0.07,
    "notumor": 0.01
  },
  "explanation": "## Prediction\n\nThe classifier predicts that the brain MRI shows a high probability of glioma...\n\n## Important Disclaimer\n\nThis AI-generated explanation is for informational purposes only and should not be considered a medical diagnosis."
}
```

---

## 🧪 How Prediction Works

1. The uploaded image is resized to 128×128 and converted to a NumPy array.
2. The array is passed through the trained VGG16-based model.
3. The class with the highest softmax probability is selected as the prediction, alongside the full probability distribution across all four classes.
4. `prompt_builder.py` constructs a prompt from the prediction and confidence, which `llm/service.py` sends to a locally running **Ollama** instance (**gemma3:4b**). The model returns a Markdown-formatted natural language explanation covering what the prediction means, how confident the model is, and a disclaimer to consult a medical professional.
5. If the predicted class is `notumor`, the result is shown as **"No Tumor Detected"**; otherwise it's shown as **"Tumor: <class name>"**, along with the confidence percentage, probability chart, and AI explanation.

---

## 🔮 Future Improvements

- Fine-tune deeper VGG16 layers for improved glioma recall
- Add Grad-CAM visualizations to highlight tumor regions on the MRI
- Containerize the app with Docker for easier deployment
- Add authentication and request logging to the API
- Add prediction history and downloadable PDF reports
- Expand the dataset with more diverse MRI sources to improve generalization

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute with attribution.

---

## 👤 Project Owner

**Manabendu Karfa**

- Email: [technoriku@gmail.com](mailto:technoriku@gmail.com)
- GitHub: [github.com/Manabendu-ai](https://github.com/Manabendu-ai)
- LinkedIn: [linkedin.com/in/manabendu-karfa](https://linkedin.com/in/manabendu-karfa-890ba52a3/)

---

<p align="center"><i>Built with curiosity, VGG16, and a lot of epochs. 🧠</i></p>
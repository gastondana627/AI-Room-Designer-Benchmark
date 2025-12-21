# 🚀 AI-Room-Designer-Benchmark (Image-to-3D)

A professional benchmarking pipeline designed to evaluate the geometric fidelity, 
computational cost, and visual accuracy of modern Image-to-3D AI models (Trellis/FAL-AI).

## 📌 Project Origin
This project evolved from an **AI Room Designer** generator. The goal is to bridge the gap 
between 2D interior design concepts and 3D spatial reality by identifying the most 
efficient generation pipelines.

## 🛠️ Technical Stack
- **Engine:** Kaggle (Python 3.10)
- **3D Pipeline:** [FAL-AI / Trellis](https://fal.ai/models/fal-ai/trellis-image-to-3d)
- **Output Formats:** GLB (Binary glTF), Interactive HTML (Three.js Viewer)
- **Metrics:** Vertex Density, Face Count, API Overhead (USD), Complexity Ratio

## 📊 The Scoreboard (Current Status)
The project generates a dynamic `index.html` "Jumbotron" that allows stakeholders 
to view side-by-side comparisons of the original 2D input and the 3D output.

## 📂 Repository Structure
- `/notebooks`: Core execution engine (`.ipynb`)
- `/outputs`: Generated 3D models and interactive viewers
- `benchmark_manifest.csv`: The testing dataset (8 unique cases)

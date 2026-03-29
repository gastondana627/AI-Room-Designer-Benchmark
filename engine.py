# AI Room Designer Benchmark - Engine (Local Compatible)
# Extracted from engine_benchmark_v1.ipynb

import os
import pandas as pd
import trimesh
import numpy as np
import requests
import json
from io import BytesIO
import time
import base64
import tempfile
from PIL import Image

# Try to import optional dependencies
try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x, **kwargs: x

try:
    from fal_client import submit, upload_file
except ImportError:
    submit = None
    upload_file = None
    print("⚠️ fal-client not installed. Generation features will be disabled.")

try:
    from IPython.display import display, HTML, FileLink
except ImportError:
    display = print
    HTML = lambda x: x
    FileLink = lambda x: x

# --- Configuration & Paths ---
ENV_KEY_NAME = "FAL_KEY"
FAL_API_KEY = os.environ.get(ENV_KEY_NAME) or os.environ.get("FAL_API_KEY")

if FAL_API_KEY:
    os.environ[ENV_KEY_NAME] = FAL_API_KEY
    print(f"✅ FAL API Key loaded: {FAL_API_KEY[:8]}...")
else:
    print("⚠️ FAL_API_KEY not found in environment. Set it to enable generation.")

DATASET_ROOT = os.environ.get('DATASET_ROOT', '.')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', './results/')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_ID = "fal-ai/trellis"

def upload_image_to_fal(img, case_id):
    if not upload_file:
        raise ImportError("fal-client not installed")

    tmp_path = None
    try:
        MAX_SIZE = (512, 512)
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False, mode='wb') as tmp:
            img.save(tmp, format='JPEG', quality=95)
            tmp_path = tmp.name
        return upload_file(tmp_path)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

def run_fal_generation(row):
    case_id = row['case_id']
    print(f"\n🎯 Processing Case: {case_id}")

    image_path = os.path.join(DATASET_ROOT, row['image_file_path'])
    if not os.path.exists(image_path):
        print(f"  ⚠️ Image not found locally: {image_path}. Attempting to use provided preview URL if available.")
        uploaded_image_url = row.get('image_preview_url')
    else:
        try:
            img = Image.open(image_path).convert('RGB')
            uploaded_image_url = upload_image_to_fal(img, case_id)
        except Exception as e:
            print(f"  ❌ Upload/Load failed: {e}")
            return row

    if not uploaded_image_url:
        print(f"  ❌ No valid image URL to process.")
        return row

    inputs = {
        "image_url": uploaded_image_url,
        "seed": 42,
        "generate_model": True
    }

    try:
        job_handler = submit(MODEL_ID, arguments=inputs)
        result = job_handler.get()
        glb_url = result.get('model_mesh', {}).get('url')

        if glb_url:
            generated_3d_path = os.path.join(OUTPUT_DIR, f"{case_id}_FAL_GEN.glb")
            glb_response = requests.get(glb_url, timeout=60)
            with open(generated_3d_path, 'wb') as f:
                f.write(glb_response.content)

            row['fal_generated_3d_path'] = generated_3d_path
            row['fal_api_cost_usd'] = result.get('cost_usd', np.nan)

            # --- New Metric Calculation Logic ---
            try:
                mesh = trimesh.load(generated_3d_path)
                if isinstance(mesh, trimesh.Scene):
                    # Combine all meshes in the scene
                    row['vertex_count'] = sum(len(m.vertices) for m in mesh.geometry.values())
                    row['face_count'] = sum(len(m.faces) for m in mesh.geometry.values())
                else:
                    row['vertex_count'] = len(mesh.vertices)
                    row['face_count'] = len(mesh.faces)
                print(f"  ✅ Metrics calculated: {row['vertex_count']} vertices, {row['face_count']} faces.")
            except Exception as e:
                print(f"  ⚠️ Failed to calculate metrics: {e}")

    except Exception as e:
        print(f"  ❌ Generation failed: {e}")

    return row

def main():
    csv_path = os.path.join(DATASET_ROOT, 'data/benchmark_manifest.csv')
    if not os.path.exists(csv_path):
        print(f"❌ Manifest not found at {csv_path}.")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} cases.")

    # Process rows with tqdm progress bar
    print("🚀 Starting benchmark processing...")
    results = []
    for index, row in tqdm(df.iterrows(), total=len(df)):
        results.append(run_fal_generation(row))

    processed_df = pd.DataFrame(results)

    # Save back to manifest
    processed_df.to_csv(csv_path, index=False)
    print(f"✅ Manifest updated at {csv_path}")

if __name__ == "__main__":
    main()

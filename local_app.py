# Local Scoreboard Generator for AI-Room-Designer-Benchmark

import os
import pandas as pd

def generate_scoreboard():
    csv_path = "data/benchmark_manifest.csv"
    if not os.path.exists(csv_path):
        print(f"❌ Manifest not found at {csv_path}. Run engine.py or create it first.")
        return

    df = pd.read_csv(csv_path)
    all_evals = df.to_dict('records')

    # HTML Jumbotron Template
    jumbotron_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Room Designer Benchmark</title>
    <style>
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: #0f172a; color: white; padding: 40px; margin: 0; }}
        .jumbotron {{ background: linear-gradient(90deg, #1e293b, #334155); padding: 40px; border-radius: 15px; margin-bottom: 30px; text-align: center; border: 1px solid #475569; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; max-width: 1200px; margin: 0 auto; }}
        .card {{ background: #1e293b; border: 1px solid #334155; padding: 20px; border-radius: 12px; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-5px); border-color: #3b82f6; }}
        .card img {{ width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; }}
        .badge {{ background: #3b82f6; padding: 6px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.025em; margin-right: 5px; }}
        .quality {{ color: #fbbf24; font-weight: bold; margin: 10px 0; }}
        a.viewer-btn {{ display: inline-block; margin-top: 15px; color: #60a5fa; text-decoration: none; font-weight: 500; border-bottom: 1px solid transparent; }}
        a.viewer-btn:hover {{ border-bottom-color: #60a5fa; }}
        h1 {{ margin-top: 0; font-size: 2.5rem; }}
        p.subtitle {{ color: #94a3b8; font-size: 1.1rem; }}
        .status-badge {{ font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }}
        .status-success {{ background: #059669; }}
        .status-pending {{ background: #d97706; }}
    </style>
</head>
<body>
    <div class="jumbotron">
        <h1>🚀 3D Generation Scoreboard</h1>
        <p class="subtitle">Current Benchmark Progress: {len(df[df['fal_generated_3d_path'].notna()])} / {len(df)} Models Complete</p>
    </div>
    <div class="grid">
"""

    for eval in all_evals:
        is_complete = pd.notna(eval.get('fal_generated_3d_path')) and eval.get('fal_generated_3d_path') != ""
        status_text = "Success" if is_complete else "Pending"
        status_class = "status-success" if is_complete else "status-pending"

        cost = f"${eval.get('fal_api_cost_usd'):.2f}" if pd.notna(eval.get('fal_api_cost_usd')) else "N/A"
        verts = f"{int(eval.get('vertex_count', 0)):,}" if pd.notna(eval.get('vertex_count')) else "0"

        # Determine image to show
        image_url = eval.get('image_preview_url')
        if pd.isna(image_url) or image_url == "":
            image_url = 'https://via.placeholder.com/400x300?text=No+Preview'

        # Link to viewer
        viewer_link = eval.get('fal_generated_3d_path')
        if pd.isna(viewer_link) or viewer_link == "":
            viewer_link = "#"

        jumbotron_html += f"""
        <div class="card">
            <img src="{image_url}" alt="Case {eval['case_id']}">
            <h3 style="margin: 0 0 10px 0;">Case: {eval['case_id']} <span class="status-badge {status_class}">{status_text}</span></h3>
            <div style="margin-bottom: 15px;">
                <span class="badge">Cost: {cost}</span>
                <span class="badge">Verts: {verts}</span>
            </div>
            <p class="quality">Quality Score: {eval.get('quality_score', 'N/A')}</p>
            <a href="{viewer_link}" class="viewer-btn">{"Open 3D Model →" if is_complete else "Awaiting Generation..."}</a>
        </div>
    """

    jumbotron_html += """
    </div>
    <footer style="text-align: center; margin-top: 50px; color: #64748b; font-size: 0.9rem;">
        <p>AI-Room-Designer-Benchmark • Data-Driven View</p>
    </footer>
</body>
</html>
"""

    with open("index.html", "w", encoding='utf-8') as f:
        f.write(jumbotron_html)

    print("✅ Scoreboard (index.html) successfully updated from manifest.")

if __name__ == "__main__":
    generate_scoreboard()

# Local Scoreboard Generator for AI-Room-Designer-Benchmark

import os

def generate_scoreboard():
    # Mock data based on the notebook's sample
    all_evals = [
        {
            "case_id": "S02_001",
            "image_preview": "https://images.unsplash.com/photo-1616489953149-75517400eeba?auto=format&fit=crop&q=80&w=400",
            "cost": "$0.04",
            "vertices": "42,000",
            "quality_score": "9/10",
            "status": "Success",
            "viewer_link": "#"
        },
        {
            "case_id": "S02_002",
            "image_preview": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&q=80&w=400",
            "cost": "$0.05",
            "vertices": "38,500",
            "quality_score": "8/10",
            "status": "Success",
            "viewer_link": "#"
        },
        {
            "case_id": "S02_003",
            "image_preview": "https://images.unsplash.com/photo-1616137422495-1e9e46e2aa77?auto=format&fit=crop&q=80&w=400",
            "cost": "$0.04",
            "vertices": "45,200",
            "quality_score": "7/10",
            "status": "Success",
            "viewer_link": "#"
        }
    ]

    # HTML Jumbotron Template
    jumbotron_html = f"""
<html>
<head>
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
    </style>
</head>
<body>
    <div class="jumbotron">
        <h1>🚀 3D Generation Scoreboard</h1>
        <p class="subtitle">Current Benchmark Progress: {len(all_evals)} / 8 Models Complete</p>
    </div>
    <div class="grid">
"""

    for eval in all_evals:
        jumbotron_html += f"""
        <div class="card">
            <img src="{eval['image_preview']}" alt="Case {eval['case_id']}">
            <h3 style="margin: 0 0 10px 0;">Case: {eval['case_id']}</h3>
            <div style="margin-bottom: 15px;">
                <span class="badge">Cost: {eval['cost']}</span>
                <span class="badge">Verts: {eval['vertices']}</span>
            </div>
            <p class="quality">Quality: {eval['quality_score']}</p>
            <a href="{eval['viewer_link']}" class="viewer-btn">Open Interactive Viewer →</a>
        </div>
    """

    jumbotron_html += """
    </div>
    <footer style="text-align: center; margin-top: 50px; color: #64748b; font-size: 0.9rem;">
        <p>AI-Room-Designer-Benchmark • Local View</p>
    </footer>
</body>
</html>
"""

    with open("index.html", "w", encoding='utf-8') as f:
        f.write(jumbotron_html)

    print("✅ Local scoreboard (index.html) successfully generated.")

if __name__ == "__main__":
    generate_scoreboard()

from app.graphrag.graph import build_graph
from pathlib import Path
G = build_graph(str(Path(__file__).resolve().parents[1] / "data" / "graph" / "edges.csv"))
print(f"nodes={len(G.nodes())}, edges={len(G.edges())}")
import pandas as pd
import networkx as nx
from pathlib import Path
def build_graph(edge_csv: str) -> nx.DiGraph:
    df = pd.read_csv(edge_csv)
    G = nx.DiGraph()
    for _, r in df.iterrows():
        G.add_edge(r['src'], r['dst'], rel=r.get('rel', 'refers'))
    return G
def shortest_explain(G: nx.DiGraph, src: str, dst: str):
    try:
        return nx.shortest_path(G, src, dst)
    except Exception:
        return []

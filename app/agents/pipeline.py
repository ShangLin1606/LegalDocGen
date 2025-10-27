from dataclasses import dataclass
from typing import Dict, Any
from pathlib import Path
from app.rag.retriever import simple_keyword_retrieval
from app.graphrag.graph import build_graph, shortest_explain
from app.utils.render import render_template
from app.utils.logging import get_logger
from .llm import simple_local_generate
logger = get_logger()
@dataclass
class GenerationRequest:
    case_title: str
    principal: str
    facts: str
    demands: str
    query: str
    template_name: str = "lawyer_letter.md"
    legal_basis_hint: str = "民法第71條等（示例）"
    graph_src: str = "CivilCode71"
    graph_dst: str = "CivilCode73"
class LegalDocPipeline:
    def __init__(self, root: str):
        self.root = Path(root)
    def run(self, req: GenerationRequest) -> Dict[str, Any]:
        corpus_dir = self.root / "data" / "sample_corpus"
        retrieved = simple_keyword_retrieval(req.query, str(corpus_dir), top_k=3)
        logger.info(f"retrieved {len(retrieved)} chunks")
        G = build_graph(str(self.root / "data" / "graph" / "edges.csv"))
        path = shortest_explain(G, req.graph_src, req.graph_dst)
        prompt = f"""案件：{req.case_title}
當事人：{req.principal}
事實：{req.facts}
請求：{req.demands}
檢索到的參考：{retrieved}
可能的法規路徑：{path}
法律依據提示：{req.legal_basis_hint}
請草擬正式語氣之法律文件正文（條列化、具體期限、明確請求）。"""
        body = simple_local_generate(prompt)
        tpl_path = self.root / "app" / "templates" / "legal" / req.template_name
        md = render_template(str(tpl_path), {
            "case_title": req.case_title,
            "principal": req.principal,
            "date": "YYYY-MM-DD",
            "facts": req.facts,
            "legal_basis": req.legal_basis_hint,
            "demands": req.demands,
            "body": body,
            "doc_no": "LE-0001",
            "sender": "王小明 律師",
            "recipient": "安可股份有限公司",
            "attachments": ["授權書影本", "往來郵件截圖"],
        })
        return {"markdown": md, "retrieved": retrieved, "graph_path": path}

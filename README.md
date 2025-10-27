# LegalDocGen — AI Legal Document & Evidence Letter Generator

LegalDocGen 是一個以檔案檢索與圖譜推理為核心的法律文件自動化草擬平台，支援律師函、存證信函（附件版）等模板化文件的快速生成。系統採用簡化的多代理（Multi-Agent）流程、RAG 與 GraphRAG 方法，並提供 FastAPI 後端與 Streamlit 前端，讓使用者可在本地環境離線跑通最小可用版本（MVP），同時保留擴充至向量資料庫、真實 LLM、LoRA 微調與 MLflow 追蹤的彈性。

---

## 功能總覽

- 多代理管線（Retrieval → Graph Reasoning → Drafting → Review）示範實作  
- RAG：以檔案關鍵字檢索為基礎，可擴充為向量檢索（Chroma + Embeddings）  
- GraphRAG：以 NetworkX 建構簡易法規關聯圖，提供最短路徑與脈絡說明  
- 模板系統：支援 Jinja2 模板（律師函、存證信函附件版）  
- 產出格式：Markdown 預覽，另提供簡化 PDF 輸出程式  
- 服務化：FastAPI 提供文件生成與 PDF 匯出的 API  
- 介面：Streamlit 參數填寫與結果預覽  
- 設定管理：.env.template 提供 LLM、向量庫、MLflow 等環境變數

---

## 系統架構與流程

高階流程：
1. 使用者於前端填寫案件資訊與關鍵字。
2. 後端檢索樣本語料（RAG 簡化版）。
3. 讀取法規關聯圖，進行最短路徑推導（GraphRAG 示範）。
4. 起草代理根據檢索片段、圖譜脈絡與使用者輸入，生成草稿正文（MVP 以本地假模型替代）。
5. 以 Jinja2 模板合成 Markdown。
6. 選用 PDF 輸出器生成簡化 PDF（可替換為更高品質的 HTML→PDF）。

目錄結構：
```
app/
  agents/           # 多代理與生成流程
  backend/          # FastAPI 服務
  graphrag/         # 法規圖譜與路徑推導
  rag/              # 檢索（目前為關鍵字版）
  templates/legal/  # Jinja2 模板
  ui/               # Streamlit 前端
  utils/            # 設定、渲染、簡化 PDF
data/
  sample_corpus/    # 範例語料
  graph/            # 法規關聯圖（CSV）
scripts/
  ingest_data.py    # 向量化/Chroma 架設入口（預留）
  build_graph.py    # 從 CSV 建圖
tests/
  test_pipeline.py  # 管線測試
```

---

## 環境需求

- Python 3.10 以上
- 建議以虛擬環境管理套件
- 若要導入 GPU 或真實 LLM，額外需求視選定方案而定（如 CUDA、vLLM、Ollama 等）

---

## 安裝與啟動

### 1. 建立與啟用虛擬環境
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 2. 安裝套件
```bash
pip install -r requirements.txt
```

### 3. 啟動後端 API
```bash
uvicorn app.backend.main:app --reload --port 8001
```
API 服務啟動後，主要端點如下：
- POST /generate：生成 Markdown 草稿
- POST /export_pdf：將 Markdown 以簡化方式輸出為 PDF

### 4. 啟動前端介面
```bash
streamlit run app/ui/StreamlitApp.py
```
預設前端會連線至 http://localhost:8001 的後端服務。

---

## 設定檔與環境變數

將 `.env.template` 複製為 `.env`，並依需要填寫：
```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
LOCAL_TINYLLAMA_PATH=./models/tinyllama
CHROMA_PERSIST_DIR=./data/chroma
MLFLOW_TRACKING_URI=./mlruns
```

說明：
- 若使用本地假模型（內建簡化產文），可不填雲端金鑰。
- 如需導入向量資料庫，請設定 `CHROMA_PERSIST_DIR` 並實作 `scripts/ingest_data.py`。
- 如需紀錄實驗與模型微調，請設定 `MLFLOW_TRACKING_URI` 並整合訓練腳本。

---

## 前端使用說明

1. 在左側欄位填寫案件標題、當事人、事實、請求與檢索關鍵字，並選擇模板（律師函或存證信函）。
2. 點選「生成文件」後，右側會顯示 Markdown 結果。
3. 如需 PDF，可使用「匯出 PDF」按鈕，將 Markdown 以簡化方式輸出為 PDF。  
   備註：目前 PDF 為示範用途，若需正式版面，建議改為「Markdown→HTML→PDF」或直接使用 HTML 範本轉 PDF 的流程（如 WeasyPrint、wkhtmltopdf）。

---

## API 介面

### POST /generate
請求範例：
```json
{
  "case_title": "催告返還・侵權停止請求",
  "principal": "林ＯＯ",
  "facts": "對方未經授權擅用素材...",
  "demands": "七日內返還並停止侵權，逾期依法處理。",
  "query": "契約 無效 第71條",
  "template_name": "lawyer_letter.md"
}
```

回應欄位：
- markdown：合成後的 Markdown 內容
- retrieved：檢索到的片段（示範）
- graph_path：法規最短路徑（示範）

### POST /export_pdf
- 參數：`md_text`（string，Markdown 原文）
- 回傳：`{"pdf_path": "/tmp/..."}`（示範，實務上可改以串流下載）

---

## 模板與產出

- 模板位置：`app/templates/legal/`
  - lawyer_letter.md：律師函模板  
  - evidence_letter.md：存證信函（附件版）模板  
- 模板語法：Jinja2  
- 支援欄位：案件標題、當事人、日期、事實、法律依據、請求、正文章節、附件清單等  
- 建議做法：在模板內保留法條或事實的佔位符，透過檢索與推理階段動態填入

---

## RAG 與 GraphRAG

- 目前檢索為簡化的關鍵字比對（`app/rag/retriever.py`），可替換為以下方案：
  - 建立語料向量：`scripts/ingest_data.py`（預留）
  - ChromaDB 作為向量庫，持久化路徑使用 `CHROMA_PERSIST_DIR`
  - Embedding 模型可使用 `sentence-transformers` 或自行接入其他提供者
- GraphRAG：
  - 法規關聯圖 CSV：`data/graph/edges.csv`  
  - 使用 NetworkX 建構與查徑（`app/graphrag/graph.py`）
  - 可擴充為帶權重的路徑、解釋節點屬性、引用來源產出等

---

## 模型與微調（擴充方向）

- 內建以本地假模型取代 LLM 產文，確保專案不依賴雲端金鑰即可跑通。
- 若要切換至真實 LLM：
  - 在 `.env` 填入供應商金鑰，並改寫 `app/agents/llm.py`
  - 可接 OpenAI、Anthropic、Ollama、vLLM 等
- LoRA 微調：
  - 參考 `app/models/lora_config.yaml`，自訂基底模型、目標模組與超參數
  - 建議另建 `train_lora.py` 與 MLflow 整合，追蹤實驗與版本

---

## 測試與品質

執行基本測試：
```bash
pytest -q
```

建議補強項目：
- 型別檢查與靜態分析（mypy、ruff）
- 範例語料與模板的單元測試
- 前後端整合測試與契約測試

---

## 部署

### Docker（後端）
```bash
docker build -t legaldocgen:api .
docker run -p 8001:8001 legaldocgen:api
```

或使用 docker-compose：
```bash
docker-compose up --build
```

生產化建議：
- 反向代理（Nginx）與 HTTPS
- 記錄與監控（如 Prometheus/Grafana）
- 機敏資訊使用 Secret 管理（而非平文本地 .env）
- 長文本與 PDF 生成改為非同步工作（如 Celery、RQ）

---

## 安全與合規注意

- 法律文件內容涉及個資與敏感資訊，請確保儲存、傳輸與存取權限符合規範。
- 輸出內容僅為草稿，正式對外前必須由法律專業人員審閱。
- 若導入外部 LLM 或第三方 API，請留意資料外洩風險與提供者的使用條款。

---

## 發展藍圖

- 導入真實 LLM、token 成本控管與安全防護
- 完整的向量化管線與檢索重排（Reranking）
- GraphRAG 增加節點屬性、引用說明與路徑權重
- 高品質排版的 HTML→PDF 流程與文件樣式庫
- Docker Compose 整合前端、後端與 Chroma
- 更完善的審閱工作流程與批註機制

---

## 授權條款

本專案採用 MIT License。實務上引用之法規文本、案例與樣本資料，請依其授權條款與合規要求使用。

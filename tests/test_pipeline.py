from app.agents.pipeline import LegalDocPipeline, GenerationRequest
from pathlib import Path
def test_run_pipeline():
    pipe = LegalDocPipeline(str(Path(__file__).resolve().parents[1]))
    res = pipe.run(GenerationRequest(
        case_title='測試', principal='王ＯＯ', facts='甲與乙於...', demands='七日內返還...', query='契約 無效 第71條'
    ))
    assert 'markdown' in res and len(res['markdown']) > 0

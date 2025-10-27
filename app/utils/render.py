from jinja2 import Template
from pathlib import Path
def render_template(path: str, context: dict) -> str:
    tpl = Path(path).read_text(encoding="utf-8")
    return Template(tpl).render(**context)

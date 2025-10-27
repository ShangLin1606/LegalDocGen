def simple_local_generate(prompt: str) -> str:
    return ("""【AI Draft】以下為初稿（示範用）：
——
""" + prompt[:800] + "\n——\n(以上為示範輸出，請在 Review 階段調整用語與法條)") 

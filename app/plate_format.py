import re
from typing import Optional

PATTERN = re.compile(r"^[0-9]{3}[A-Z]{3}[0-9]{2}$")

def clean_ocr(text: str) -> str:
    text = (text or "").upper().replace(" ", "").replace("-", "").replace("_", "")
    return re.sub(r"[^A-ZА-Я0-9]", "", text)

def normalize_rk_plate(text: str) -> Optional[str]:
    s = clean_ocr(text)
    if len(s) < 8:
        return None
    if PATTERN.fullmatch(s):
        return s
    if len(s) == 8:
        chars=list(s); out=[]
        for i,ch in enumerate(chars):
            if i in {0,1,2,6,7}:
                out.append({"O":"0","Q":"0","D":"0","I":"1","L":"1","Z":"2","S":"5","B":"8"}.get(ch,ch))
            else:
                out.append({"0":"O","1":"I","2":"Z","4":"A","5":"S","6":"G","8":"B"}.get(ch,ch))
        candidate="".join(out)
        if PATTERN.fullmatch(candidate):
            return candidate
    for i in range(max(0,len(s)-7)):
        chunk=s[i:i+8]
        if len(chunk)==8:
            n=normalize_rk_plate(chunk)
            if n: return n
    return None

def is_valid_rk_plate(text: str) -> bool:
    return bool(PATTERN.fullmatch(text or ""))

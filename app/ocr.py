import re
import pytesseract
from dataclasses import dataclass
from .config import settings
from .plate_format import normalize_rk_plate
from .preprocess import enhance_variants

if settings.tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

@dataclass
class OCRResult:
    plate: str | None
    confidence: float
    raw: str

class TesseractPlateOCR:
    def recognize(self, crop):
        results=[]
        for img in enhance_variants(crop):
            for psm in (7,8,13):
                config=f'--oem 1 --psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                try: data=pytesseract.image_to_data(img,config=config,output_type=pytesseract.Output.DICT)
                except Exception: continue
                texts=[]; confs=[]
                for text,conf in zip(data.get('text',[]),data.get('conf',[])):
                    text=re.sub(r'[^A-Za-z0-9]','',text or '').upper()
                    try: c=float(conf)
                    except Exception: c=-1
                    if text and c>=0: texts.append(text); confs.append(c/100.0)
                plate=normalize_rk_plate(''.join(texts))
                if plate:
                    results.append(OCRResult(plate,max(0,min(1,sum(confs)/len(confs) if confs else 0)),''.join(texts)))
        return results

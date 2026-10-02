import cv2
import numpy as np
from dataclasses import dataclass
from .config import settings

@dataclass
class PlateCandidate:
    x:int; y:int; w:int; h:int; score:float

class OpenCVPlateDetector:
    def detect(self, frame: np.ndarray) -> list[PlateCandidate]:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray=cv2.bilateralFilter(gray,7,50,50)
        edges=cv2.Canny(gray,80,180)
        kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(17,5))
        closed=cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)
        closed=cv2.morphologyEx(closed,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(7,3)))
        contours,_=cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        candidates=[]
        for c in contours:
            x,y,w,h=cv2.boundingRect(c); area=w*h; ratio=w/max(h,1)
            if area<settings.plate_min_area or area>settings.plate_max_area: continue
            if not settings.plate_min_ratio<=ratio<=settings.plate_max_ratio: continue
            if w<70 or h<12: continue
            roi=edges[y:y+h,x:x+w]
            density=float(np.mean(roi>0))
            score=min(1.0,0.35+0.35*min(ratio/4,1)+0.30*min(density/0.22,1))
            candidates.append(PlateCandidate(x,y,w,h,score))
        candidates.sort(key=lambda c:c.score,reverse=True)
        return candidates[:settings.max_candidates]

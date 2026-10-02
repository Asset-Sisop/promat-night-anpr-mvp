import base64,time,cv2,numpy as np
from .detector import OpenCVPlateDetector
from .ocr import TesseractPlateOCR

class RecognitionService:
    def __init__(self): self.detector=OpenCVPlateDetector(); self.ocr=TesseractPlateOCR()
    def decode(self,data:bytes): return cv2.imdecode(np.frombuffer(data,dtype=np.uint8),cv2.IMREAD_COLOR)
    def encode_jpeg_b64(self,frame):
        ok,enc=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,90])
        return base64.b64encode(enc.tobytes()).decode('ascii') if ok else None
    def recognize_frame(self,frame):
        started=time.perf_counter(); candidates=self.detector.detect(frame); results=[]
        for c in candidates:
            crop=frame[c.y:c.y+c.h,c.x:c.x+c.w]
            if crop.size==0: continue
            for r in self.ocr.recognize(crop): results.append((r.plate,r.confidence,c))
        results.sort(key=lambda x:x[1],reverse=True); payload=None
        if results:
            plate,confidence,c=results[0]
            payload={'plate':plate,'confidence':round(min(1,confidence),4),'bbox':{'x':c.x,'y':c.y,'width':c.w,'height':c.h},'frame':self.encode_jpeg_b64(frame)}
        return payload,(time.perf_counter()-started)*1000,[x[0] for x in results[:8]]

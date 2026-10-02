from collections import Counter
from datetime import datetime,timedelta,timezone
from fastapi import FastAPI,UploadFile,File,HTTPException
from .service import RecognitionService
from .models import RecognitionResponse

app=FastAPI(title='Promat Night ANPR MVP',version='1.0.0')
service=RecognitionService(); KZ=timezone(timedelta(hours=5))

@app.get('/health')
def health(): return {'status':'ok','service':'promat-night-anpr-mvp'}

@app.post('/api/v1/recognize',response_model=RecognitionResponse)
async def recognize(file:UploadFile=File(...)):
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=415,detail='Only image files are supported')
    frame=service.decode(await file.read())
    if frame is None: raise HTTPException(status_code=400,detail='Invalid image')
    payload,elapsed,candidates=service.recognize_frame(frame); ts=datetime.now(KZ).isoformat()
    if not payload:
        return RecognitionResponse(plate=None,confidence=0,bbox=None,frame=None,timestamp=ts,processing_ms=round(elapsed,2),candidates=candidates,status='not_recognized',message='No valid RK plate found in the frame.')
    payload.update(timestamp=ts,processing_ms=round(elapsed,2),candidates=candidates,status='ok')
    return RecognitionResponse(**payload)

@app.post('/api/v1/recognize/sequence',response_model=RecognitionResponse)
async def recognize_sequence(files:list[UploadFile]=File(...)):
    if not files: raise HTTPException(status_code=400,detail='At least one frame is required')
    aggregate=[]; elapsed=0; candidates=[]
    for file in files:
        if not file.content_type or not file.content_type.startswith('image/'): continue
        frame=service.decode(await file.read())
        if frame is None: continue
        payload,e,c=service.recognize_frame(frame); elapsed+=e; candidates.extend(c)
        if payload: aggregate.append(payload)
    ts=datetime.now(KZ).isoformat()
    if not aggregate:
        return RecognitionResponse(plate=None,confidence=0,bbox=None,frame=None,timestamp=ts,processing_ms=round(elapsed,2),candidates=candidates[:8],status='not_recognized',message='No valid RK plate found in the sequence.')
    counts=Counter(p['plate'] for p in aggregate); aggregate.sort(key=lambda p:(counts[p['plate']],p['confidence']),reverse=True)
    best=aggregate[0]; best.update(timestamp=ts,processing_ms=round(elapsed,2),candidates=list(counts.keys())[:8],status='ok')
    return RecognitionResponse(**best)

# Promat Night ANPR MVP

Локальный MVP модуля ночного распознавания ГРНЗ Республики Казахстан для Promat Parking.

## Реализовано
- FastAPI HTTP API
- POST /api/v1/recognize
- POST /api/v1/recognize/sequence
- GET /health
- OpenCV baseline plate detector
- Ночная предобработка: CLAHE, подавление бликов, denoise, unsharp, adaptive threshold, Otsu
- Tesseract OCR с несколькими PSM
- Нормализация и валидация формата РК NNNABCNN
- Выбор лучшего результата из серии кадров
- Docker / docker-compose
- Unit tests
- RTSP adapter
- Документация API и пилотных испытаний

## Ограничение MVP
95% ночной точности нельзя гарантировать без реальной выборки ночных проездов объекта. После NDA выполняется калибровка на данных заказчика и, при необходимости, замена baseline detector/OCR на обученные модели.

## Быстрый запуск
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Swagger: http://127.0.0.1:8080/docs

Docker:
```bash
docker compose up --build
```

## API
```bash
curl -X POST "http://127.0.0.1:8080/api/v1/recognize" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@night_frame.jpg"
```

Ответ содержит plate, confidence, bbox, frame, timestamp, processing_ms и status.

## Production roadmap
1. NDA и ночная выборка.
2. Разметка plate bbox и ground truth.
3. Calibration / validation / test.
4. Настройка exposure/gain/WDR/HLC/BLC/IR.
5. Обученный detector + специализированный OCR при необходимости.
6. Двухнедельный пилот.

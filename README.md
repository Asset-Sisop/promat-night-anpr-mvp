# Promat Night ANPR MVP

Локальный MVP модуля устойчивого ночного распознавания государственных регистрационных номерных знаков Республики Казахстан для интеграции с Promat Parking.

## Назначение

Решение предназначено для сценария въезда на парковку, где используется обычная IP-камера видеонаблюдения. MVP выполняет цепочку: детекция области номера → ночная предобработка → OCR → нормализация формата → выдача результата через HTTP API.

## Что реализовано

- FastAPI REST API и Swagger/OpenAPI.
- `POST /api/v1/recognize` — распознавание одного изображения.
- `POST /api/v1/recognize/sequence` — обработка серии кадров одного проезда.
- `GET /health` — health-check.
- OpenCV baseline detector с геометрической фильтрацией кандидатов.
- Ночная предобработка: denoise, CLAHE, повышение резкости, adaptive threshold и Otsu.
- Tesseract OCR с несколькими режимами PSM.
- Нормализация целевого формата `NNNABCNN`.
- Confidence, bbox, timestamp и processing time в API-ответе.
- Dockerfile.
- Unit-тесты для формата номера и health endpoint.

## Архитектура

```text
IP Camera / RTSP
       ↓
Frame acquisition
       ↓
Plate detector
       ↓
Night preprocessing
       ↓
OCR
       ↓
RK plate validation
       ↓
Best result / sequence aggregation
       ↓
Promat Parking API
```

Модуль не принимает решение об открытии шлагбаума. Он возвращает результат распознавания, а проверка access list и бизнес-решение остаются в Promat Parking.

## Запуск локально

### Windows

```powershell
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Linux / Docker

```bash
docker build -t promat-night-anpr .
docker run --rm -p 8080:8080 promat-night-anpr
```

Swagger: `http://127.0.0.1:8080/docs`

## Пример API

```bash
curl -X POST "http://127.0.0.1:8080/api/v1/recognize" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@night_frame.jpg"
```

Пример ответа:

```json
{
  "plate": "123ABC01",
  "confidence": 0.93,
  "bbox": {"x": 1012, "y": 388, "width": 264, "height": 58},
  "frame": "<base64 JPEG>",
  "timestamp": "2026-10-02T23:19:20+05:00",
  "processing_ms": 214.3,
  "candidates": ["123ABC01"],
  "status": "ok"
}
```

## Критически важное ограничение

Этот репозиторий является MVP/baseline для пилотирования. Целевые показатели заказчика нельзя считать подтверждёнными только по исходному коду. Для подтверждения требований необходима реальная ночная выборка с объекта после NDA, эталонная разметка и двухнедельный пилот.

Калибруются отдельно: exposure, gain, WDR/HLC/BLC, Smart IR, угол/мощность ИК, пороги детектора и OCR. При необходимости baseline detector/OCR заменяется обученными ONNX/YOLO и специализированным OCR без изменения внешнего API.

## Следующий этап

1. Получить данные объекта после NDA.
2. Разметить номера и сформировать calibration / validation / test.
3. Измерить exact-match, false-read rate и latency.
4. Оптимизировать камеру и ИК-подсветку.
5. Провести двухнедельный пилот.
6. Оформить протокол испытаний и production deployment.

## Конфиденциальность

В репозитории отсутствуют реальные записи с камер, государственные номера автомобилей и иные персональные данные.

## Статус

**MVP / Pilot-ready baseline** — исходный код подготовлен для технической оценки и последующей калибровки на объекте заказчика.

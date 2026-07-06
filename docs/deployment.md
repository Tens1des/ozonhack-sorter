# Инструкция по развёртыванию и проверке

## Требования

| Компонент | Версия |
|-----------|--------|
| Python | 3.11+ |
| pip | актуальный |
| ffmpeg | для генерации `docs/demo.mp4` |
| Docker | 20+ (опционально) |

## Локальный запуск

```bash
git clone <repo-url>
cd OzonHack

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=.                # или: pip install -e ".[dev]"
```

## Полный прогон (рекомендуется)

```bash
./scripts/run_all.sh
# или: make all
```

Выполняет: расчёты → схемы → STL → симуляция → видео → S3-архив → верификация.

## Пошагово

### 1. Инженерные расчёты

```bash
python scripts/calculations.py
```

Результат: `simulation/results/engineering_calculations.json`

### 2. Симуляция

```bash
# Быстрая проверка (10 мин модельного времени)
python simulation/run.py --scenario baseline --duration 600

# Все 5 сценариев
python simulation/run.py --scenario all --duration 600
```

Результаты: `simulation/results/scenario_summary.csv`, `*.png`

### 3. WMS HTTP API

```bash
python control/wms_server.py --port 8080
curl http://localhost:8080/health
curl http://localhost:8080/route/OZ123456789
```

### 4. Видео и отчёт

```bash
make video                              # docs/demo.mp4
python scripts/generate_report_html.py  # docs/report.html
```

### 5. S3-пакет

```bash
./scripts/package_s3.sh
```

Создаёт `dist/ozonhack_s3_bundle.zip` — см. [s3_upload.md](s3_upload.md)

### 6. Верификация комплекта

```bash
python scripts/verify_submission.py
```

Ожидается: 28+ файлов ✓, тесты ✓

### 7. Тесты

```bash
PYTHONPATH=. pytest tests/ -q
```

## Docker

```bash
docker build -t ozonhack-sorter .
docker run --rm -v "$(pwd)/simulation/results:/app/simulation/results" ozonhack-sorter
```

## Карта материалов для эксперта

| Что проверить | Где |
|---------------|-----|
| Навигация | `README.md` |
| Отчёт | `docs/report.md`, `docs/report.html` |
| Симуляция | `simulation/run.py --scenario all --duration 600` |
| Презентация | `docs/slides.html` |
| Видео | `docs/demo.mp4` |
| 3D | `cad/models/*.stl` |
| Постановка | `docs/source/` |

## Устранение неполадок

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError` | `export PYTHONPATH=.` из корня репозитория |
| Нет `demo.mp4` | Установите ffmpeg, выполните `make video` |
| Долгая симуляция | `--duration 600` вместо 3600 |
| Нет графиков | `pip install matplotlib`, проверьте `simulation/results/` |

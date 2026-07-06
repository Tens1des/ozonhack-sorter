# OzonHack — Трек 2: Модульный кросс-белт сортировщик

Инженерно проработанный проект автоматизированного сортировщика для СЦ Ozon:  
**100 000 товаров/час**, **400 направлений**, размещение в **КТЯ**.

## Состав решения

| Раздел | Путь | Описание |
|--------|------|----------|
| Концепция | [docs/concept.md](docs/concept.md) | Принцип работы, узлы, процессы |
| Расчёты | [docs/calculations.md](docs/calculations.md) | Производительность, площадь, энергия |
| Отчёт | [docs/report.md](docs/report.md) | Итоговый инженерный отчёт |
| Алгоритмы | [docs/algorithms.md](docs/algorithms.md) | Маршрутизация, антизатор, КТЯ |
| Спецификации | [docs/specifications.md](docs/specifications.md) | Компоненты и параметры |
| Симуляция | [simulation/](simulation/) | SimPy-модель, 5 сценариев |
| Управление | [control/](control/) | WMS, маршрутизация, балансировщик |
| CAD | [cad/](cad/) | Схемы, STL-модели |
| Презентация | [docs/slides.html](docs/slides.html), [docs/presentation.pdf](docs/presentation.pdf) | Слайды 7 мин |
| Демо-видео | [docs/demo.mp4](docs/demo.mp4) | Автогенерируемое MP4 |
| Верификация | `python scripts/verify_submission.py` | Проверка комплекта |
| Видео-сценарий | [docs/video_script.md](docs/video_script.md) | Сценарий MP4 |
| Чеклист сдачи | [docs/checklist.md](docs/checklist.md) | Контроль перед отправкой |
| S3-загрузка | [docs/s3_upload.md](docs/s3_upload.md) | Инструкция и архив |
| Команда (шаблон) | [docs/team.md](docs/team.md) | Состав команды |
| Альтернативы | [docs/alternatives.md](docs/alternatives.md) | Обоснование выбора |
| Запуск | [docs/deployment.md](docs/deployment.md) | Инструкция для экспертов |
| Статус проекта | [docs/STATUS.md](docs/STATUS.md) | Готовность 97% |

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Полный прогон: расчёты + диаграммы + STL + симуляция
./scripts/run_all.sh

# Или через Make
make all
```

### Отдельные команды

```bash
make calc       # инженерные расчёты
make simulate   # 5 сценариев SimPy
make diagrams   # SVG-схемы
make stl        # 3D STL-модели
make test       # pytest
make wms        # HTTP WMS на :8080
make verify     # проверка комплекта сдачи
make video      # генерация docs/demo.mp4
```

### Docker

```bash
docker build -t ozonhack-sorter .
docker run --rm -v "$(pwd)/simulation/results:/app/simulation/results" ozonhack-sorter
```

## Архитектура

**4 параллельных кросс-белт модуля** × 100 направлений = 400 ячеек сброса.

```
Вход → Сканер → WMS → Индукция → Контур → Сброс → КТЯ
```

- Индукция: 4 линии на модуль (16 всего)
- КТЯ: автосмена 14 с, уплотнение, контроль заполнения
- Антизатор: перенаправление при перегрузке ячейки

## Результаты симуляции (600 с)

| Сценарий | Пропускная | Точность | Перенаправления |
|----------|------------|----------|-----------------|
| baseline | 99,8% | 99,45% | 0,54% |
| overload 125% | 125,8% | 99,05% | 0,93% |
| отказ ячеек | 99,7% | 98,48% | 1,50% |
| деградация модуля | 100,6% | 99,53% | 0,47% |
| hotspot | 100,1% | 96,52% | 3,46% |

Файлы: `simulation/results/scenario_summary.csv`, `scenario_summary.png`

## Ключевые показатели

| Параметр | Значение |
|----------|----------|
| Пропускная способность | 99 792 т/ч |
| Площадь | 9 737 м² (лимит 20 000) |
| Электромощность | 460 кВт |
| Направления | 400 |
| Модули | 4 × 100 ячеек |

## WMS API (имитатор)

```bash
python control/wms_server.py
curl http://localhost:8080/route/OZ123456789
```

| Артефакт | Локально | S3 URL |
|----------|----------|--------|
| Полный архив | `dist/ozonhack_s3_bundle.zip` | `https://s3.../ozonhack_s3_bundle.zip` |
| Видео | `docs/demo.mp4` | `https://s3.../demo.mp4` |
| 3D-модели | `cad/models/` | `https://s3.../models/` |

## Команда

| Участник | Роль | Вклад |
|----------|------|-------|
| Котов Роман | Тимлид / концепция | Архитектура, отчёт |

Подробнее: [docs/team.md](docs/team.md)

## Лицензия

Проект подготовлен для хакатона Ozon.

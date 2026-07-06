# CAD и компоновка

## Файлы в репозитории

| Файл | Описание |
|------|----------|
| `layout_top_view.svg` | Вид сверху — 4 модуля |
| `process_flow.svg` | Блок-схема потока обработки |
| `kinematic_scheme.svg` | Кинематическая схема модуля |
| `kty_station.svg` | Станция КТЯ — узел ячейки |
| `models/kty_box.stl` | КТЯ 600×400×300 мм |
| `models/module_footprint.stl` | Габарит модуля 58×26 м |
| `models/carriage.stl` | Тележка кросс-белта |
| `models/*.obj` | OBJ-версии для просмотрщиков |
| `layout.pdf` | Компоновка (PDF) |

## Генерация

```bash
python scripts/generate_layout.py
python scripts/generate_diagrams.py
python scripts/generate_stl.py
python scripts/generate_pdfs.py
```

## S3

| Файл | Локально |
|------|----------|
| 3D-модели | `cad/models/` |
| Компоновка PDF | `cad/layout.pdf` |
| Видео | `docs/demo.mp4` |
| Архив | `dist/ozonhack_s3_bundle.zip` |

## Размеры модуля

| Параметр | Значение |
|----------|----------|
| Овал | 58 × 26 м |
| Высота контура | 2,2 м |
| Ячеек сброса | 100 |
| Шаг ячеек | ~1,46 м по контуру |

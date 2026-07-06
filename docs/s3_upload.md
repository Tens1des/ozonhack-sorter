# Загрузка на S3

## Что загрузить

| Файл / папка | Локальный путь | Назначение |
|--------------|----------------|------------|
| Демо-видео | `docs/demo.mp4` | Обязательная видеодемонстрация |
| 3D STL | `cad/models/*.stl` | 3D-модели |
| Схемы SVG | `cad/*.svg` | Компоновка, кинематика, КТЯ |
| Графики | `simulation/results/*.png` | Результаты симуляции |

## Быстрая упаковка

```bash
./scripts/package_s3.sh
```

Создаёт `dist/ozonhack_s3_bundle.zip` — загрузите содержимое на S3.

## Ссылки для README

После загрузки замените в `README.md`:

```markdown
| Демо-видео | `docs/demo.mp4` | https://s3.../demo.mp4 |
| 3D STL | `cad/models/` | https://s3.../models/ |
| Графики | `simulation/results/` | https://s3.../results/ |
```

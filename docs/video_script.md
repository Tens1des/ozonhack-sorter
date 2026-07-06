# Сценарий видеодемонстрации (~5–7 мин)

## Блок 1. Вступление (45 с)

- Показать `README.md` и структуру репозитория
- Озвучить: 100k/ч, 400 направлений, кросс-белт 4×100

## Блок 2. Концепция (60 с)

- Открыть `cad/process_flow.svg` и `cad/layout_top_view.svg`
- Кратко: вход → сканер → WMS → индукция → сброс → КТЯ

## Блок 3. Запуск симуляции (90 с)

```bash
source .venv/bin/activate
./scripts/run_all.sh
```

- Показать вывод в терминале
- Открыть `simulation/results/scenario_summary.png`
- Комментировать: baseline 100%, hotspot — рост перенаправлений

## Блок 4. WMS API (45 с)

```bash
python control/wms_server.py &
curl http://localhost:8080/route/OZ123456789
```

- Показать JSON с destination

## Блок 5. Расчёты (45 с)

- Открыть `simulation/results/engineering_calculations.json`
- Площадь 9 737 м², мощность 460 кВт

## Блок 6. 3D и спецификации (45 с)

- Показать `cad/models/module_footprint.stl` в просмотрщике
- Ссылка на полные модели в S3 (если загружены)

## Блок 7. Итог (30 с)

- Таблица метрик из отчёта
- Ограничения и планы развития

## Технические требования

- Формат: MP4, 1080p
- Запись экрана: OBS / QuickTime
- Загрузить на S3, ссылку — в README

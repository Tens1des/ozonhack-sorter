.PHONY: install calc simulate diagrams stl video verify all test wms docker

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

calc:
	PYTHONPATH=. .venv/bin/python scripts/calculations.py

diagrams:
	PYTHONPATH=. .venv/bin/python scripts/generate_layout.py
	PYTHONPATH=. .venv/bin/python scripts/generate_diagrams.py

stl:
	PYTHONPATH=. .venv/bin/python scripts/generate_stl.py

simulate:
	PYTHONPATH=. .venv/bin/python simulation/run.py --scenario all --duration 600

video:
	PYTHONPATH=. .venv/bin/python scripts/generate_demo_video.py

verify:
	PYTHONPATH=. .venv/bin/python scripts/verify_submission.py

test:
	PYTHONPATH=. .venv/bin/python -m pytest tests/ -q

wms:
	PYTHONPATH=. .venv/bin/python control/wms_server.py

all:
	./scripts/run_all.sh

package:
	chmod +x scripts/package_s3.sh
	./scripts/package_s3.sh

docker:
	docker build -t ozonhack-sorter .
	docker run --rm -v "$$(pwd)/simulation/results:/app/simulation/results" ozonhack-sorter

.PHONY: install calc simulate diagrams stl video verify all test wms docker package

ifeq ($(wildcard .venv/bin/python),)
PY := python3
else
PY := .venv/bin/python
endif

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

calc:
	PYTHONPATH=. $(PY) scripts/calculations.py

diagrams:
	PYTHONPATH=. $(PY) scripts/generate_layout.py
	PYTHONPATH=. $(PY) scripts/generate_diagrams.py

stl:
	PYTHONPATH=. $(PY) scripts/generate_stl.py

simulate:
	PYTHONPATH=. $(PY) simulation/run.py --scenario all --duration 600

video:
	PYTHONPATH=. $(PY) scripts/generate_demo_video.py

verify:
	PYTHONPATH=. $(PY) scripts/verify_submission.py

test:
	PYTHONPATH=. $(PY) -m pytest tests/ -q

wms:
	PYTHONPATH=. $(PY) control/wms_server.py

all:
	./scripts/run_all.sh

package:
	chmod +x scripts/package_s3.sh
	./scripts/package_s3.sh

docker:
	docker build -t ozonhack-sorter .
	docker run --rm -v "$$(pwd)/simulation/results:/app/simulation/results" ozonhack-sorter

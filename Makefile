PY?=python3

.PHONY: snapshot validate serve clean

snapshot:
	$(PY) -m backend.jobs.mvp_snapshot --input data/sample.csv --out data/snapshots/v2025-08-15

validate:
	$(PY) -m backend.publish.manifest --validate data/snapshots/v2025-08-15

serve:
	$(PY) -m backend.devserver --root data

clean:
	rm -rf data/snapshots/v2025-08-15

set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]



dev:
	uv run litestar run -rd

run:
	uv run litestar run

test:
	uv run tests/fakes.py

buildcontainer:
	podman build -t erp:latest  --ignorefile=.gitignore .

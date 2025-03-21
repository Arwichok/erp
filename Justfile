set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]
set dotenv-load


dev:
	uv run litestar run -R app -rd --reload-exclude tests

run:
	uv run litestar run

test:
	uv run pytest .

buildcontainer:
	podman build -t erp:latest  --ignorefile=.gitignore .

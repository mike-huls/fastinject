uv run coverage run --omit="test/*" -m pytest -v --log-cli-level=DEBUG

uv run coverage run --omit="test/*" -m pytest -v -s "test/" --log-cli-level=DEBUG
uv run coverage report
uv run coverage html
start chrome %cd%/htmlcov/index.html

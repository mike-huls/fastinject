uv run coverage run --omit="test/*" -m pytest -v --log-cli-level=DEBUG

uv run coverage run --omit="test/*" -m pytest "test/" --log-cli-level=DEBUG -v -s
uv run coverage report
uv run coverage html
start chrome %cd%/htmlcov/index.html



uv run coverage run --omit="test/*" -m pytest "test/" --log-cli-level=DEBUG -v -s && uv run coverage report && uv run coverage html && start chrome %cd%/htmlcov/index.html

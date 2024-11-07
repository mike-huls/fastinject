uv run coverage run --omit="test/*" -m pytest -v \
&& uv run coverage report \
&& uv run coverage html \
&& start chrome %cd%/htmlcov/index.html

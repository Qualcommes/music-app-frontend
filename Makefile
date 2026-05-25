install:
	uv sync

run:
	uv run flet run --recursive --web main.py 

android:
	uv run flet run --recursive --android --web 

web:
	uv run flet run --web --recursive ./src/main.py

desctop:
	uv run flet run --recursive ./src/main.py

build:
	uv build

lint:
	uv run ruff 

tree:
	tree -I __pycache__ -I icon.png -I splash_android.png -I calculator.py -I hail.py -I messenger.py -I todo.py -I run_examples.py -I *.jpg:Zone.Identifier
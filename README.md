# 2D-Mario-style-platformer

## SETUP UBUNTU
- `python3 -m venv venv/2D-Mario-style-platformer`
- `source venv/2D-Mario-style-platformer/bin/activate`
- `pip install -r requirements.txt`

## SETUP WINDOWS
- `conda create --prefix ./venv python=3.10`
- `conda activate C:\workspaces\Repos\mario_style_platformer_tutorial\venv`
- `pip install -r requirements.txt`

# Build distributable (data files need to be zipped with .exe after build)
- `pyinstaller src\main.py --onefile --noconsole`

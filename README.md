# Pygame Tutorials

## SETUP
- `conda create --prefix ./venv python=3.10`
- `conda activate C:\workspaces\Repos\pygame_tutorials\venv`
- `pip install -r requirements.txt`

# Build distributable (data files need to be zipped with .exe after build)
- `pyinstaller src\main.py --onefile --noconsole`

# Run breakout
- `cd pygame_tutorials\breakout\src`
- `python main.py`

# Run mario
- `cd pygame_tutorials\mario\code`
- `python main.py`

# Run zelda
- `cd pygame_tutorials\zelda\src`
- `python main.py`

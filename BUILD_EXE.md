# Building Strivon Osu! Mania EXE

To convert the Python script into a standalone executable, follow these steps:

## 1. Install Python
Ensure you have Python 3.9+ installed from [python.org](https://www.python.org/).

## 2. Install Dependencies
Open your terminal (PowerShell or CMD) and run:
```bash
pip install keyboard pygame pyinstaller
```

## 3. Generate the EXE
Run the following command in the directory where `StrivonOsuMania.py` is located:

```bash
pyinstaller --onefile --noconsole --name "StrivonOsuMania" StrivonOsuMania.py
```

### Options Explained:
- `--onefile`: Packs everything into a single `.exe`.
- `--noconsole`: Hides the black terminal window when running the app.
- `--name`: Sets the output filename.

## 4. Find Your EXE
Go to the `dist` folder that was created in your directory. Your `StrivonOsuMania.exe` will be there.

---
**Note:** Some antivirus software might flag `keyboard` emulation as suspicious. You may need to whitelist the `.exe` or run it as Administrator for key presses to work inside of games.

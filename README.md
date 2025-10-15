# Shutdown Timer - Build & Distribution

This project is a small Windows utility to schedule shutdown/restart/logoff. Below are steps to build and package the app to share with friends.

Prerequisites
- Python 3.8+ (this project used 3.14 in the venv)
- Git (optional)
- pip
- (For installer) Inno Setup on Windows

Steps to create a distributable EXE

1. Create and activate virtualenv (recommended):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Generate icon files (PNG + ICO):

```powershell
python .\make_icon.py
```

4. Build single-file exe with PyInstaller (script provided):

```powershell
# default: onefile, no console
.\build.ps1

# show console window (useful for debugging)
.\build.ps1 -noconsole:$false
```

After a successful build the EXE will be in `dist\ShutdownTimer.exe`.

Create installer (optional)

Install Inno Setup (https://jrsoftware.org/isinfo.php) and then open `installer.iss` or run:

- Open Inno Setup, load `installer.iss` and compile.
- Or run `ISCC.exe installer.iss` from Inno Setup command line.

Notes & Safety
- The app executes Windows shutdown commands. When testing, avoid setting short timers or comment out `os.system` calls in `main.py`.
- If you want a "dry-run" mode, I can add a CLI flag that prevents executing shutdown commands and only logs actions.

If you want, I can also:
- Build a zip distribution (exe + README) and prepare an installer on this machine.
- Add a dry-run mode and a confirmation dialog before executing shutdown commands.
- Sign the executable (requires a code-signing certificate).

Quick build (one-liner)
-----------------------
If you just want to build the program quickly from PowerShell (uses the repo's venv and the provided build script), run this one-liner from the project root:

```powershell
& .\.venv\Scripts\Activate.ps1; .\build.ps1
```

After it finishes the built executable will be at `dist\ShutdownTimer.exe`.
=======
# ShutDownTimerTool
Shut Down Timer Tool

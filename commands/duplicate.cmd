if not defined path2go (set /p "path2go=Saisir chemin : ")

mkdir "%path2go%\commands"

if not exist "%path2go%\commands\activate.cmd" (copy "%~dp0\activate.cmd" "%path2go%\commands\activate.cmd")
if not exist "%path2go%\commands\venv.cmd" (copy "%~dp0\venv.cmd" "%path2go%\commands\venv.cmd")
if not exist "%path2go%\shell.cmd" (copy "%~dp0\..\shell.cmd" "%path2go%\shell.cmd")

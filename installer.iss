; Inno Setup script for Shutdown Timer
; Requires Inno Setup (https://jrsoftware.org/isinfo.php)

[Setup]
AppName=Shutdown Timer
AppVersion=1.0
DefaultDirName={autopf}\Shutdown Timer
DefaultGroupName=Shutdown Timer
DisableProgramGroupPage=yes
OutputBaseFilename=ShutdownTimerInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\ShutdownTimer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "shutdown_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Shutdown Timer"; Filename: "{app}\ShutdownTimer.exe"; IconFilename: "{app}\shutdown_icon.ico"
Name: "{commondesktop}\Shutdown Timer"; Filename: "{app}\ShutdownTimer.exe"; IconFilename: "{app}\shutdown_icon.ico"

[Run]
Filename: "{app}\ShutdownTimer.exe"; Description: "Launch Shutdown Timer"; Flags: nowait postinstall skipifsilent

; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{0A46DED6-C50C-4E8D-ACE1-387ADC7C10C4}
AppName=The Binding of Isaac
AppVersion=1.5
;AppVerName=The Binding of Isaac 1.5
AppPublisher=KPU
AppPublisherURL=http://www.kpu.ac.kr
AppSupportURL=http://www.kpu.ac.kr
AppUpdatesURL=http://www.kpu.ac.kr
DefaultDirName={pf}\The Binding of Isaac
DisableProgramGroupPage=yes
OutputDir=C:\Users\A35X\Desktop
OutputBaseFilename=issac_setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\github\2DGP\dist\mygame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\github\2DGP\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\The Binding of Isaac"; Filename: "{app}\mygame.exe"
Name: "{commondesktop}\The Binding of Isaac"; Filename: "{app}\mygame.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\mygame.exe"; Description: "{cm:LaunchProgram,The Binding of Isaac}"; Flags: nowait postinstall skipifsilent

#define MyAppName "GameLoop Smartkeys Reborn"
#define MyAppVersion "1.0"
#define MyAppPublisher "Skuny"
#define MyAppExeName "GameLoop Smartkeys Reborn.exe"

[Setup]
AppId={{8B8E7F52-5B5D-4D31-A4C8-6F7C6B7E91D2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

OutputDir={#SourcePath}\installer
OutputBaseFilename=GameLoop Smartkeys Reborn Setup

SetupIconFile={#SourcePath}\smartkeys.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible

VersionInfoVersion=1.0.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCopyright=Copyright © 2026 Skuny

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#SourcePath}\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Messages]
WelcomeLabel1=Welcome to {#MyAppName} Setup
WelcomeLabel2=Install {#MyAppName} {#MyAppVersion} by {#MyAppPublisher}.%n%nA lightweight keyboard sequence tool designed for GameLoop.%n%nClick Next to continue.

FinishedLabel=Installation of {#MyAppName} is complete.%n%nYou can launch the application using the desktop or Start Menu shortcut.

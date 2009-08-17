; Canta Install Script

; this script is not used since version 0.2 beta4
; so you have to modify it, if you want to get it working

!define exec "canta.exe"
!define icon "canta.ico"

!define licensefile "LICENSE.txt"
;!define notefile "README.txt"
!define prodname "Canta"
!define regkey "Software\${prodname}"
!define setup "dist/canta-${version}.exe"
;!define screenimage background.bmp
!define srcdir "build/win32-canta/"
!define startmenu "$SMPROGRAMS\${prodname}"
!define uninstaller "uninstall.exe"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\${prodname}"
;!define version "0.2-beta4"

SetCompress force
SetCompressor /SOLID lzma

XPStyle on

ShowInstDetails hide
ShowUninstDetails hide

Name "${prodname} ${version}"
Caption "${prodname} ${version}"
!ifdef icon
    Icon "${icon}"
!endif
OutFile "${setup}"

InstallDir "$PROGRAMFILES\${prodname}"
InstallDirRegKey HKLM "${regkey}" "installdir"

!ifdef licensefile
    LicenseText "License"
    LicenseData "${licensefile}"
!endif

;LoadLanguageFile "${NSISDIR}\Contrib\Language files\German.nlf"

!ifdef licensefile
    Page license
!endif
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

!ifdef screenimage
    Function .onGUIInit
        InitPluginsDir
        File /oname=$PLUGINSDIR\1.bmp "${screenimage}"
        BgImage::SetBg /NOUNLOAD /FILLSCREEN $PLUGINSDIR\1.bmp
        BgImage::Redraw /NOUNLOAD
    FunctionEnd

    Function .onGUIEnd
        BgImage::Destroy
    FunctionEnd
!endif

Section
    SetOutPath $INSTDIR
    File /r "${srcdir}"
    WriteUninstaller "$INSTDIR\${uninstaller}"
    WriteRegStr HKLM "SOFTWARE\${prodname}" "installdir" "$INSTDIR"

 
    CreateDirectory "$SMPROGRAMS\${prodname}"
    CreateShortCut "$SMPROGRAMS\${prodname}\${prodname}.lnk" "$INSTDIR\${exec} "" "$INSTDIR\${icon}"
    CreateShortCut "$SMPROGRAMS\${prodname}\Canta Song Generator.lnk" "$INSTDIR\csg.exe "" "$INSTDIR\csg.ico"
    CreateShortCut "$SMPROGRAMS\${prodname}\Uninstall ${prodname}.lnk" "$INSTDIR\${uninstaller}"
    CreateShortCut "$DESKTOP\${prodname}.lnk" "$OUTDIR\${exec} "" "$INSTDIR\${icon}"
SectionEnd

Section "un.Uninstall"
   RMDir /r $INSTDIR
   Delete "$SMPROGRAMS\${prodname}\${prodname}.lnk"
   Delete "$SMPROGRAMS\${prodname}\Canta Song Generator.lnk"
   Delete "$SMPROGRAMS\${prodname}\Uninstall ${prodname}.lnk"
   RMDir "$SMPROGRAMS\${prodname}"
   Delete "$DESKTOP\${prodname}.lnk"
SectionEnd


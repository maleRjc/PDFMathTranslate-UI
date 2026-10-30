Unicode true
ManifestDPIAware true
ManifestDPIAwareness PerMonitorV2

SetCompressor /SOLID lzma

!include "MUI2.nsh"
!include "FileFunc.nsh"

# General Definitions
!define PRODUCT_NAME "PDFMathTranslate"
!define PRODUCT_VERSION "1.9.12"
!define PRODUCT_VERSION_NUM "1.9.12.0"
!define PRODUCT_PUBLISHER "武汉矩阵力量科技有限公司"
!define PRODUCT_WEB_SITE "https://github.com/maleRjc/PDFMathTranslate-UI"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\PDFMathTranslate.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKCU"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "..\dist\release\PDFMathTranslate-v1.9.12-windows-x64-setup.exe"
InstallDir "$LOCALAPPDATA\Programs\PDFMathTranslate"
InstallDirRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "InstallLocation"
RequestExecutionLevel user

# Version Information
VIProductVersion "${PRODUCT_VERSION_NUM}"
VIAddVersionKey "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey "Comments" "基于 AI 的科研论文双语对照翻译工具"
VIAddVersionKey "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey "LegalCopyright" "Copyright (c) 2026 ${PRODUCT_PUBLISHER}"
VIAddVersionKey "FileDescription" "${PRODUCT_NAME} 安装程序"
VIAddVersionKey "FileVersion" "${PRODUCT_VERSION_NUM}"
VIAddVersionKey "ProductVersion" "${PRODUCT_VERSION_NUM}"

# MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\assets\app_icon.ico"
!define MUI_UNICON "..\assets\app_icon.ico"

# Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

# Finish page options
!define MUI_FINISHPAGE_RUN "$INSTDIR\PDFMathTranslate.exe"
!define MUI_FINISHPAGE_RUN_TEXT "立即运行 ${PRODUCT_NAME}"
!insertmacro MUI_PAGE_FINISH

# Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Languages
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on

  # Install all application files recursively
  File /r "PDFMathTranslate-v1.9.12-windows-x64\*"

  # Create Shortcuts
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\PDFMathTranslate.exe" "" "$INSTDIR\app_icon.ico" 0
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\卸载 ${PRODUCT_NAME}.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\app_icon.ico" 0
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\PDFMathTranslate.exe" "" "$INSTDIR\app_icon.ico" 0

  # Register Application
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\PDFMathTranslate.exe"

  # Write Uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  # Registry entries for Add/Remove Programs
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\app_icon.ico"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "NoRepair" 1
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "EstimatedSize" 1358000
SectionEnd

Section Uninstall
  # Remove Shortcuts
  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\卸载 ${PRODUCT_NAME}.lnk"
  RMDir "$SMPROGRAMS\${PRODUCT_NAME}"

  # Remove Files and Directories
  RMDir /r "$INSTDIR\runtime"
  RMDir /r "$INSTDIR\site-packages"
  Delete "$INSTDIR\pdf2zh.exe"
  Delete "$INSTDIR\pdf2zh.int"
  Delete "$INSTDIR\PDFMathTranslate.exe"
  Delete "$INSTDIR\PDFMathTranslate.int"
  Delete "$INSTDIR\_pystand_static.int"
  Delete "$INSTDIR\app_icon.ico"
  Delete "$INSTDIR\启动*.bat"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir /r "$INSTDIR"

  # Clean Registry
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd

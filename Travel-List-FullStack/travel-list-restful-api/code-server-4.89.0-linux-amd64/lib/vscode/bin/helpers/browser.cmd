@echo off
setlocal
set ROOT_DIR=%~dp0..\..\..\..
set VSROOT_DIR=%~dp0..\..
call "%ROOT_DIR%\node.exe" "%VSROOT_DIR%\out\server-cli.js" "code-server" "1.89.0" "0f4791b816c184b612df3bdcfc4e1f9f1a13daca" "code-server.cmd" "--openExternal" %*
endlocal

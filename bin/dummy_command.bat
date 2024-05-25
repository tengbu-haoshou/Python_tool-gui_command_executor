@rem
@rem dummy_command.bat
@rem

@rem This file's encoding is shift-jis.

@echo off
setlocal

echo start of dummy_command

set parameter=%1
if "%parameter%" == "" (
	echo Parameter is not specified.
	goto :abnormal_end
)

echo parameter : %parameter%

set "string=‚ ‚¢‚¤‚¦‚¨ ‚©‚«‚­‚¯‚± ‚³‚µ‚·‚¹‚» ‚½‚¿‚Â‚Ä‚Æ ‚È‚É‚Ê‚Ë‚Ì ‚Í‚Ð‚Ó‚Ö‚Ù ‚Ü‚Ý‚Þ‚ß‚à ‚â‚ä‚æ ‚ç‚è‚é‚ê‚ë ‚í‚ð‚ñ"
set "spacer= : "

for /l %%i in (1,1,%parameter%) do (
    powershell sleep 2
    echo %%i%spacer%%string%
)

echo end of dummy_command (normal end)
exit /b 0

:abnormal_end
echo end of dummy_command (abnormal end)
exit /b 1

pause

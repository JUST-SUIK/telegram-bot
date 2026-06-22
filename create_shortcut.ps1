$WshShell = New-Object -ComObject WScript.Shell
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$projectPath = 'E:\Project\telegram-bot'
$shortcutPath = Join-Path $desktopPath "TelegramBotManager.lnk"
$batchPath = Join-Path $projectPath "start_manager.bat"
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $batchPath
$shortcut.WorkingDirectory = $projectPath
$shortcut.Description = "Telegram Bot Agent Manager"
$shortcut.Save()
Write-Host "Desktop shortcut created: $shortcutPath"
Write-Host "Target: $batchPath"
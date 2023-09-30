
$compress = @{
    LiteralPath= 
    "$PSScriptRoot\Rom Manager GUI.py", 
    "$PSScriptRoot\icon.png",
    "$PSScriptRoot\Generate requirements.bat", 
    "$PSScriptRoot\Install requirements.bat", 
    "$PSScriptRoot\gui", 
    "$PSScriptRoot\obj", 
    "$PSScriptRoot\src", 
    "$PSScriptRoot\workers"
    DestinationPath = "$PSScriptRoot\Rom Manager GUI vx.x.zip"
    Force = $true
    }
Compress-Archive @compress
pause
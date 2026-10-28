$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
New-Item -ItemType Directory -Force -Path (Join-Path $root 'artifacts')|Out-Null
$items=Get-PnpDevice -PresentOnly|Where-Object { $_.InstanceId -match 'VID_0B05&PID_1AA6|VID_0B05&PID_1B9B' -or $_.FriendlyName -match 'SMBus|AURA LED' }|Select-Object Class,FriendlyName,InstanceId,Status
$items|ConvertTo-Json -Depth 4|Set-Content (Join-Path $root 'artifacts\device-inventory.json') -Encoding utf8
$items|Format-Table -Wrap

<#
.SYNOPSIS
    Discovers the WORKGROUP-NOORHEROES root path dynamically.
.DESCRIPTION
    Cross-platform PowerShell script (Windows PowerShell & PowerShell Core on Linux/macOS)
    that discovers the root without hardcoded machine paths.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# 1. Check environment variable override
if ($env:WORKGROUP_ROOT -and (Test-Path (Join-Path $env:WORKGROUP_ROOT ".workgroup-root"))) {
    (Resolve-Path $env:WORKGROUP_ROOT).Path
    exit 0
}

# 2. Ascend from script directory
$current = Split-Path -Parent $MyInvocation.MyCommand.Path
while ($current) {
    $marker = Join-Path $current ".workgroup-root"
    if (Test-Path $marker) {
        (Resolve-Path $current).Path
        exit 0
    }
    $parent = Split-Path -Parent $current
    if ($parent -eq $current) { break }
    $current = $parent
}

# 3. Fallback: ascend from current working directory
$current = (Get-Location).Path
while ($current) {
    $marker = Join-Path $current ".workgroup-root"
    if (Test-Path $marker) {
        (Resolve-Path $current).Path
        exit 0
    }
    $parent = Split-Path -Parent $current
    if ($parent -eq $current) { break }
    $current = $parent
}

Write-Error "Could not locate WORKGROUP root (.workgroup-root missing)"
exit 1

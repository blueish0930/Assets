# Upload the Blender remote library to the R2 bucket "blueish-assets".
# Requires: wrangler authenticated to account 6c8fcc1162bfc367e72396c3a0a3ad31
param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$Bucket = "blueish"
)

$ErrorActionPreference = "Stop"
$assets = Join-Path $Root "blender\assets"
if (-not (Test-Path $assets)) {
    throw "Missing $assets"
}

function Get-ContentType([string]$path) {
    switch -Regex ($path.ToLower()) {
        '\.json$' { "application/json; charset=utf-8"; break }
        '\.txt$' { "text/plain; charset=utf-8"; break }
        '\.webp$' { "image/webp"; break }
        '\.png$' { "image/png"; break }
        '\.jpe?g$' { "image/jpeg"; break }
        '\.mp4$' { "video/mp4"; break }
        '\.blend$' { "application/octet-stream"; break }
        default { "application/octet-stream" }
    }
}

$wrangler = $null
foreach ($c in @("wrangler.cmd", "wrangler")) {
    $cmd = Get-Command $c -ErrorAction SilentlyContinue
    if ($cmd) { $wrangler = $cmd.Source; break }
}
if (-not $wrangler) {
    $npx = Join-Path $env:LOCALAPPDATA "hermes\node\npx.cmd"
    if (Test-Path $npx) { $wrangler = $npx; $wranglerArgsPrefix = @("wrangler") }
    else { throw "wrangler is not installed" }
} else {
    $wranglerArgsPrefix = @()
}

$files = Get-ChildItem $assets -Recurse -File | Where-Object {
    $_.Name -ne ".last_modified" -and $_.Name -notlike "*.blend1" -and $_.Name -notlike "*~"
}

Write-Host "Uploading $($files.Count) files to r2://$Bucket ..."
foreach ($f in $files) {
    $rel = $f.FullName.Substring($Root.Length).TrimStart("\", "/") -replace "\\", "/"
    $ctype = Get-ContentType $f.Name
    Write-Host "-> $rel ($([math]::Round($f.Length/1MB, 2)) MB)"
    $args = $wranglerArgsPrefix + @(
        "r2", "object", "put", "$Bucket/$rel",
        "--file", $f.FullName,
        "--content-type", $ctype,
        "--remote"
    )
    & $wrangler @args
    if ($LASTEXITCODE -ne 0) { throw "Failed uploading $rel" }
}
Write-Host "Done."

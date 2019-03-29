#!/usr/bin/env pwsh

Set-StrictMode -Version 5.0

$include_files = @( 'addon.py', 'addon.xml', 'LICENSE', 'README.md', 'service.py' )
$include_paths = @( 'resources/' )
$exclude_files = @( '*.new', '*.orig', '*.pyc' )

# Get addon metadata
[xml]$XmlDocument = Get-Content -LiteralPath 'addon.xml'
$name = $XmlDocument.addon.id
$version = $XmlDocument.addon.version
$git_hash = Invoke-Expression 'git rev-parse --short HEAD'
$zip_name = "$name-$version-$git_hash.zip"

# Remove file if it exists
if (Test-Path -LiteralPath $zip_name) {
    Remove-Item -LiteralPath $zip_name
}

# Ensure .NET's current directory is Powershell's working directory
# NOTE: This is to ensure .NET can find our files correctly
[System.IO.Directory]::SetCurrentDirectory($PWD)

Add-Type -AssemblyName System.IO.Compression.FileSystem

# Create ZIP file
Write-Host -fore blue '= Building new package'
$zip_file = [System.IO.Compression.ZipFile]::Open($zip_name, 'Create')
ForEach ($relative_file in $include_files) {
    $archive_file = Join-Path -Path $name -ChildPath $relative_file
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip_file, $relative_file, $archive_file)
}
ForEach ($path in $include_paths) {
    Get-ChildItem -Recurse -File -Path $path -Exclude $exclude_files | ForEach-Object {
        $relative_file = Resolve-Path -Path $_.FullName -Relative
        # NOTE: Powershell lacks functionality to normalize a path
        $archive_file = (Join-Path -Path $name -ChildPath $relative_file).Replace('/./', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip_file, $relative_file, $archive_file)
    }
}
$zip_file.Dispose()
Write-Host "= Successfully wrote package as: " -ForegroundColor:Blue -NoNewLine
Write-Host "$zip_name" -ForegroundColor:Cyan

#!powershell
#
$include_files = @( 'addon.py', 'addon.xml', 'LICENSE', 'README.md', 'service.py' )
$include_paths = @( 'resources/' )
$exclude_paths = @( 'test/' )

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

# Create ZIP file
Add-Type -AssemblyName System.IO.Compression

Write-Host '= Building new package'
$zip_file = [System.IO.Compression.ZipFile]::Open($zip_name, 'Create')
ForEach ($file in $include_files) {
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip_file, $file, "$name/$file")
}
ForEach ($path in $include_paths) {
    Get-ChildItem -Recurse -File -LiteralPath $path | ForEach-Object {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip_file, $_.FullName, "$name/$(Resolve-Path -Path $_.FullName -Relative)")
    }
}
$zip_file.Dispose()
Write-Host "= Successfully wrote package as: $zip_name"

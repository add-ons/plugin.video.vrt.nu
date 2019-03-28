#!powershell
#
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

# Create ZIP file
Add-Type -AssemblyName System.IO.Compression

Write-Host '= Building new package'
$zip_file = [System.IO.Compression.ZipFile]::Open($zip_name, 'Create')
ForEach ($relative_file in $include_files) {
    $archive_file = Join-Path -Path $name -ChildPath $relative_file
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip_file, $relative_file, $archive_file)
}
ForEach ($path in $include_paths) {
    Get-ChildItem -Recurse -File -Path $path -Exclude $exclude_files | ForEach-Object {
        $relative_file = Resolve-Path -Path $_.FullName -Relative
        $archive_file = Join-Path -Path $name -ChildPath $relative_file
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip_file, $relative_file, $archive_file)
    }
}
$zip_file.Dispose()
Write-Host "= Successfully wrote package as: $zip_name"

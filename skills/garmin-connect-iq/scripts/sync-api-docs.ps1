[CmdletBinding()]
param(
    [string]$BaseUrl = 'https://developer.garmin.com/connect-iq/api-docs/',
    [string]$Destination = (Join-Path $PSScriptRoot '..\references\api-docs')
)

$ErrorActionPreference = 'Stop'
$base = [Uri]$BaseUrl
$destinationRoot = [IO.Path]::GetFullPath($Destination)
$allowedExtensions = @('.html', '.css', '.js', '.png', '.svg', '.gif', '.jpg', '.jpeg', '.webp', '.woff', '.woff2', '.ttf')
$pending = [Collections.Generic.Queue[Uri]]::new()
$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$pending.Enqueue([Uri]::new($base, 'index.html'))
$pending.Enqueue([Uri]::new($base, 'class_list.html'))
$pending.Enqueue([Uri]::new($base, 'method_list.html'))
$http = [Net.Http.HttpClient]::new()

New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null

while ($pending.Count -gt 0) {
    $uri = $pending.Dequeue()
    if ($uri.Host -ne $base.Host -or -not $uri.AbsolutePath.StartsWith($base.AbsolutePath, [StringComparison]::Ordinal)) {
        continue
    }

    $relative = [Uri]::UnescapeDataString($uri.AbsolutePath.Substring($base.AbsolutePath.Length))
    if ([string]::IsNullOrWhiteSpace($relative)) { $relative = 'index.html' }
    if (-not $seen.Add($relative)) { continue }

    $extension = [IO.Path]::GetExtension($relative).ToLowerInvariant()
    if ($allowedExtensions -notcontains $extension) { continue }

    $target = [IO.Path]::GetFullPath((Join-Path $destinationRoot $relative.Replace('/', [IO.Path]::DirectorySeparatorChar)))
    if (-not $target.StartsWith($destinationRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing path outside destination: $relative"
    }

    New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($target)) -Force | Out-Null
    $bytes = $http.GetByteArrayAsync($uri).GetAwaiter().GetResult()
    [IO.File]::WriteAllBytes($target, $bytes)

    if ($extension -in @('.html', '.css', '.js')) {
        $text = [Text.Encoding]::UTF8.GetString($bytes)
        foreach ($match in [regex]::Matches($text, '(?:href|src|url)\s*[:=(]?\s*["'']?([^"''\)\s#?]+)', [Text.RegularExpressions.RegexOptions]::IgnoreCase)) {
            $value = $match.Groups[1].Value.Trim()
            if ($value -match '^(?:data:|mailto:|javascript:)') { continue }
            try {
                $candidate = [Uri]::new($uri, $value)
                if ($candidate.Host -eq $base.Host -and $candidate.AbsolutePath.StartsWith($base.AbsolutePath, [StringComparison]::Ordinal)) {
                    $pending.Enqueue($candidate)
                }
            } catch {
                Write-Verbose "Skipping malformed URL '$value' in $relative"
            }
        }
    }
}

$http.Dispose()
Write-Output "Mirrored $($seen.Count) unique paths to $destinationRoot"

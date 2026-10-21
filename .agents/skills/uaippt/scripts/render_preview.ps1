# Renderiza cada slide de um .pptx em PNG para conferência visual.
# Uso: powershell -ExecutionPolicy Bypass -File render_preview.ps1 -Pptx <arquivo.pptx> [-OutDir <pasta>] [-Width 1600]
# Requer Microsoft PowerPoint instalado (Windows). Sem PowerPoint, tenta LibreOffice (soffice) gerando PDF.
param(
    [Parameter(Mandatory = $true)][string]$Pptx,
    [string]$OutDir = "",
    [int]$Width = 1600
)
$Pptx = (Resolve-Path $Pptx).Path
if (-not $OutDir) { $OutDir = Join-Path (Split-Path $Pptx) ("preview_" + [IO.Path]::GetFileNameWithoutExtension($Pptx)) }
New-Item -ItemType Directory -Force $OutDir | Out-Null
$Height = [int]($Width * 7.5 / 13.333)

try {
    $app = New-Object -ComObject PowerPoint.Application
    $pres = $app.Presentations.Open($Pptx, $true, $false, $false)  # somente leitura, sem janela
    $i = 1
    foreach ($s in $pres.Slides) {
        $s.Export((Join-Path $OutDir ("slide{0:D2}.png" -f $i)), "PNG", $Width, $Height)
        $i++
    }
    $pres.Close()
    Write-Output "OK: $($i - 1) slides -> $OutDir"
}
catch {
    $soffice = Get-Command soffice -ErrorAction SilentlyContinue
    if ($soffice) {
        & $soffice.Source --headless --convert-to pdf --outdir $OutDir $Pptx | Out-Null
        Write-Output "PowerPoint indisponível; PDF gerado via LibreOffice em $OutDir"
    }
    else {
        Write-Error "Nem PowerPoint nem LibreOffice disponíveis para renderizar: $_"
        exit 1
    }
}

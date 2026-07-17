param(
    [string]$DocumentPath = "deliverables\ETRI_시맨틱_미디어_용역결과보고서.docx"
)

$ErrorActionPreference = "Stop"
$candidatePath = if ([IO.Path]::IsPathRooted($DocumentPath)) {
    $DocumentPath
} else {
    Join-Path (Split-Path -Parent $PSScriptRoot) $DocumentPath
}
$resolvedPath = (Resolve-Path -LiteralPath $candidatePath).Path
$word = $null
$document = $null
$blocks = @()
$current = $null

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $document = $word.Documents.Open($resolvedPath)

    for ($index = 1; $index -le $document.Paragraphs.Count; $index++) {
        $paragraph = $document.Paragraphs.Item($index)
        try {
            $marker = $paragraph.Range.ListFormat.ListString.Trim()
            $kind = if ($marker -match '^\d+[\.)]?$') { "number" } elseif ($marker) { "bullet" } else { "none" }
            if ($kind -eq "none") {
                if ($null -ne $current) {
                    $blocks += $current
                    $current = $null
                }
                continue
            }

            if ($null -eq $current -or $current.Kind -ne $kind -or $current.LastIndex + 1 -ne $index) {
                if ($null -ne $current) {
                    $blocks += $current
                }
                $current = [pscustomobject]@{
                    Kind = $kind
                    Start = $paragraph.Range.Start
                    End = $paragraph.Range.End
                    LastIndex = $index
                }
            } else {
                $current.End = $paragraph.Range.End
                $current.LastIndex = $index
            }
        } finally {
            [void][Runtime.InteropServices.Marshal]::ReleaseComObject($paragraph)
        }
    }
    if ($null -ne $current) {
        $blocks += $current
    }

    for ($blockIndex = $blocks.Count - 1; $blockIndex -ge 0; $blockIndex--) {
        $block = $blocks[$blockIndex]
        $range = $document.Range($block.Start, $block.End)
        try {
            $galleryId = if ($block.Kind -eq "number") { 2 } else { 1 }
            $template = $word.ListGalleries.Item($galleryId).ListTemplates.Item(1)
            try {
                $range.ListFormat.ApplyListTemplateWithLevel($template, $false, 2, 1, 1)
                $range.ParagraphFormat.LeftIndent = 36
                $range.ParagraphFormat.FirstLineIndent = -18
                $range.ParagraphFormat.SpaceAfter = 8
                $range.ParagraphFormat.LineSpacingRule = 5
                $range.ParagraphFormat.LineSpacing = 14
                $range.ParagraphFormat.KeepTogether = -1
            } finally {
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($template)
            }
        } finally {
            [void][Runtime.InteropServices.Marshal]::ReleaseComObject($range)
        }
    }

    $document.Save()
    Write-Output "Finalized $($blocks.Count) Word list blocks."
} finally {
    if ($null -ne $document) {
        $document.Close(0)
    }
    if ($null -ne $word) {
        $word.Quit()
    }
    if ($null -ne $document) {
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($document)
    }
    if ($null -ne $word) {
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

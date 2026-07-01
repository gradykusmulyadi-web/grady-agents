<#
.SYNOPSIS
  Deterministic scorer for the screen-cv skill (PowerShell version).

.DESCRIPTION
  Identical logic to score.py, for Windows machines without Python installed.

  The percentage and tier used to be computed by the LLM screener by hand,
  which made the same CV land in different tiers across runs. Computers never
  miscount, so the arithmetic lives here instead.

  The cv-screener agent supplies ONLY raw judgments:
    - must_haves:    M-id -> "met" | "partial" | "missing"
    - nice_to_haves: N-id -> { raw: 0..3, weight: int }
    - red_flags:     [{ detected: bool, severity: "note"|"concern"|"disqualify" }]
  This script fills in score_pct and tier with a fixed formula.

.EXAMPLE
  powershell -File score.ps1 records.json    # reads file, writes enriched JSON to stdout
#>
param([Parameter(Position = 0)][string]$Path)

$ErrorActionPreference = 'Stop'

if ($Path) { $raw = Get-Content -Raw -Encoding UTF8 -Path $Path }
else       { $raw = [Console]::In.ReadToEnd() }

$records = $raw | ConvertFrom-Json
if ($records -isnot [System.Array]) { $records = @($records) }

foreach ($rec in $records) {
    # Parse-error records pass straight through, untouched by the math.
    if ($rec.parse_error -or $rec.tier -eq 'Parse error') {
        $rec | Add-Member -NotePropertyName tier      -NotePropertyValue 'Parse error' -Force
        $rec | Add-Member -NotePropertyName score_pct -NotePropertyValue -1            -Force
        continue
    }

    # --- Nice-to-haves: weighted sum and max possible -----------------------
    # max possible is ALWAYS (sum of weights) x 3 -- each criterion caps at 3.
    $achieved = 0
    $maxPossible = 0
    if ($rec.nice_to_haves) {
        foreach ($n in $rec.nice_to_haves.PSObject.Properties) {
            $raw_score = [int]$n.Value.raw
            $weight = [int]$n.Value.weight
            if ($raw_score -lt 0) { $raw_score = 0 }
            if ($raw_score -gt 3) { $raw_score = 3 }
            $weighted = $raw_score * $weight
            $n.Value | Add-Member -NotePropertyName weighted -NotePropertyValue $weighted -Force
            $achieved += $weighted
            $maxPossible += 3 * $weight
        }
    }
    $pct = if ($maxPossible) { [math]::Round($achieved / $maxPossible * 100, 1) } else { 0.0 }

    # --- Must-haves: a "partial" counts as missing --------------------------
    $missing = 0
    if ($rec.must_haves) {
        foreach ($m in $rec.must_haves.PSObject.Properties) {
            if ($m.Value -ne 'met') { $missing++ }
        }
    }

    # --- Red flags ----------------------------------------------------------
    $hasDisqualify = $false
    $hasConcern = $false
    foreach ($f in @($rec.red_flags)) {
        if ($f.detected -and $f.severity -eq 'disqualify') { $hasDisqualify = $true }
        if ($f.detected -and $f.severity -eq 'concern')    { $hasConcern = $true }
    }

    # --- Tier (rubric thresholds, strict precedence) ------------------------
    if ($missing -ge 2 -or $hasDisqualify) {
        $tier = 'Not a fit'
    } elseif ($missing -eq 1 -or $hasConcern -or $pct -lt 50) {
        $tier = 'Moderate fit'
    } elseif ($pct -ge 80) {
        $tier = 'Best fit'
    } else {
        $tier = 'Good fit'
    }

    $detail = [ordered]@{
        achieved_weighted     = $achieved
        max_possible_weighted = $maxPossible
        must_haves_missing    = $missing
        disqualifying_flag    = $hasDisqualify
        concern_flag          = $hasConcern
    }
    $rec | Add-Member -NotePropertyName score_pct     -NotePropertyValue $pct    -Force
    $rec | Add-Member -NotePropertyName tier          -NotePropertyValue $tier   -Force
    $rec | Add-Member -NotePropertyName _score_detail -NotePropertyValue ([pscustomobject]$detail) -Force
}

$records | ConvertTo-Json -Depth 10

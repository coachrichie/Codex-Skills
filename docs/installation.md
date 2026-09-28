# Installation

## Before installing

Clone the repository:

```text
git clone https://github.com/coachrichie/Codex-Skills.git
cd Codex-Skills
```

Codex uses `$CODEX_HOME/skills` when `CODEX_HOME` is set. Otherwise use `~/.codex/skills`. If an existing skill has the same name, make a backup before updating it. The commands below do not intentionally delete an existing skill.

## Windows PowerShell

```powershell
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$skillRoot = Join-Path $codexRoot 'skills'
$skills = @('hockey-evidence', 'garmin-connect-iq')

foreach ($skill in $skills) {
    $destination = Join-Path $skillRoot $skill
    if (Test-Path -LiteralPath $destination) {
        throw "Existing skill found at $destination. Back it up and use the deliberate update procedure below."
    }
}

New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
foreach ($skill in $skills) {
    Copy-Item -Recurse -LiteralPath (Join-Path 'skills' $skill) -Destination $skillRoot
}
```

## macOS and Linux

```sh
codex_root="${CODEX_HOME:-$HOME/.codex}"
for skill in hockey-evidence garmin-connect-iq; do
  if [ -e "$codex_root/skills/$skill" ]; then
    echo "Existing skill found at $codex_root/skills/$skill. Back it up and use the deliberate update procedure below." >&2
    exit 1
  fi
done

mkdir -p "$codex_root/skills"
cp -R skills/hockey-evidence "$codex_root/skills/"
cp -R skills/garmin-connect-iq "$codex_root/skills/"
```

To install only one skill, run only its copy command. Restart or refresh Codex after installation if the new skill does not appear immediately.

## Updating

Pull the latest repository changes and back up any local modifications to the existing skill. Then deliberately rename or remove only that existing skill directory before repeating its copy command, or merge the changes manually. Never assume a copied update preserves unpublished local edits.

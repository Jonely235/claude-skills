# Script to push to GitHub once gh CLI is installed and you're authenticated
# Run this after: gh auth login

$repoName = "claude-skills"
$currentDir = Get-Location

Write-Host "Creating GitHub repo and pushing..." -ForegroundColor Green

# Create repo and push
gh repo create $repoName --public --source=$currentDir --remote=origin --push

Write-Host "Done! Your repo is at: https://github.com/$((gh api user --jq '.login'))/$repoName" -ForegroundColor Green

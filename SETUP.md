# Set up your animated GitHub profile

This package is prepared for **JISHAN-HI**. No photo, personal access token, Python packages, or hosted stats service is required. It includes a real public contribution snapshot retrieved on 6 October 2026. The workflow refreshes that snapshot after publishing.

## Preview

Open `preview.html` in Edge or Chrome. Reload to replay the animations. All artwork is local. GitHub's layout and image caching can differ from the local preview.

## Publish from Windows PowerShell

Install Git and GitHub CLI if needed. Extract this ZIP and open PowerShell inside the `JISHAN-HI` folder. Confirm your signed-in account before creating the repository:

```powershell
gh auth login
gh api user --jq .login
```

The result should be `JISHAN-HI`. If the repository `JISHAN-HI/JISHAN-HI` already exists, clone it and copy these files into that checkout, reviewing the old README first. Do not run the create command for an existing repository.

For a NEW profile repository:

```powershell
git init -b main
git add README.md assets scripts data .github SETUP.md preview.html
git commit -m "Create animated DevOps profile"
gh repo create JISHAN-HI/JISHAN-HI --public --source . --remote origin --push
```

GitHub displays the README of the public repository whose name matches your username. The initial push triggers the artwork workflow. You can also run it manually from **Actions → Refresh profile artwork → Run workflow** after it is present on the default branch.

The daily schedule is **07:53 AM IST**, subject to GitHub scheduling delays. It runs on the default branch. Scheduled workflows in inactive public repositories may be disabled after 60 days; re-enable through Actions if needed. This is a GitHub Actions workflow, not a ChatGPT scheduled task.

## Customize

- Edit biography, skills and focus areas in `README.md`.
- Edit the headings, colors and monogram in `scripts/build_profile.py`.
- Regenerate artwork with `py scripts/build_profile.py` (Python 3.11 or later).
- Fetch fresh public activity with `py scripts/fetch_contributions.py`, then regenerate.
- Add public project links under `explore` when you choose which projects to feature.

## Troubleshooting

- **404 repository:** check that the name is exactly `JISHAN-HI` and visibility is public.
- **Push denied in Actions:** check Settings → Actions → General → Workflow permissions. Organization policy or branch protection may prevent bot commits even with the requested `contents: write` permission.
- **Contribution fetch fails:** the parser depends on GitHub's public calendar HTML. It validates dates and activity levels and fails without overwriting the last successful JSON. Inspect the Actions log if GitHub changes its markup.
- **Image appears old:** GitHub can cache images; allow time for refresh.
- **No motion:** animations play once and settle. Reduced-motion preferences disable them. Text remains visible in static SVG renderers.

The calendar displays public activity intensity, not invented contribution totals or private repository details. No employer infrastructure names or private project links are included.

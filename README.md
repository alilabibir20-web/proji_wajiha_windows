# proji_wajiha Windows EXE CI Repository

This repository is prepared to build your Kivy/KivyMD app into a Windows `.exe` using **GitHub Actions** (windows-latest runner).
You can either run the build **locally** using the `build_exe.bat` or use **GitHub Actions** to build the EXE in the cloud and download the artifact.

## Files in this repo
- `proji_wajiha_1.py` - Your app source (provided).
- `requirements.txt` - Python dependencies.
- `build_exe.bat` - Local builder script for Windows.
- `.github/workflows/build_windows.yml` - GitHub Actions workflow to build and upload EXE artifact.
- `assets/` - Placeholder folder for icons or extra assets.
- `README.md` - This file.

## How to use GitHub Actions (build in the cloud)
1. Create a new GitHub repository (private or public).
2. Upload the contents of this ZIP into the repository root.
3. Commit to the `main` branch.
4. Go to the "Actions" tab in GitHub, select the workflow "Build Windows EXE" and click "Run workflow" (or push to main).
5. Wait for the workflow to finish (usually 5-15 minutes).
6. Download the produced artifact under the workflow run — it will be named `proji_wajiha_windows_exe`.

## Notes / Troubleshooting
- Kivy can be tricky to install on Windows runners; if the workflow fails due to Kivy wheel issues, try pinning a compatible Kivy wheel or use a GitHub Actions runner with preinstalled Kivy.
- If your app uses additional data (images, kv files), place them in `assets/` and update your code to load from relative paths.
- To include data files in the EXE, modify the PyInstaller command to use `--add-data "assets;assets"`.

## If you want me to run the build for you:
I cannot run GitHub Actions from here myself, but I can:
- Prepare and upload the repository to a GitHub repo (if you give me a GitHub repo URL and permission tokens) — **I cannot accept tokens**.
- Or, you can upload this ZIP to GitHub (through your phone browser) and trigger the action. I will guide you step-by-step and help fix any issues that appear in the workflow logs.


# Changelog

## Migration from Google Cloud to GitHub Actions ✅

### What Changed
Migrated from Google Cloud Platform to **GitHub Actions** for 100% free automation with **no credit card required**.

---

### Files Deleted (GCP-related)
- ❌ `deploy_to_gcp.sh` - GCP deployment script for Mac/Linux
- ❌ `deploy_to_gcp.ps1` - GCP deployment script for Windows
- ❌ `cloud_run_wrapper.py` - Flask wrapper for Cloud Run
- ❌ `Dockerfile` - Docker config for Cloud Run
- ❌ `DEPLOYMENT_GUIDE.md` - Old GCP deployment guide

---

### Files Created (GitHub Actions)
- ✅ `.github/workflows/tournament-automation.yml` - GitHub Actions workflow
- ✅ `QUICK_START.md` - 5-minute setup guide
- ✅ `GITHUB_ACTIONS_SETUP.md` - Detailed setup instructions
- ✅ `CHANGELOG.md` - This file

---

### Files Updated
- ✅ `README.md` - Removed GCP references, now GitHub Actions focused
- ✅ `repeat-gg-automated.py` - Updated from Cloud Run to GitHub Actions
  - Renamed `IS_CLOUD_RUN` → `IS_GITHUB_ACTIONS`
  - Renamed `load_cookies_from_secret()` → `load_cookies_from_env()`
  - Updated all print messages
- ✅ `export_cookies.py` - Updated instructions to reference GitHub
- ✅ `requirements.txt` - Removed Flask (no longer needed)

---

### Benefits
✅ **No credit card** - GitHub Actions is 100% free  
✅ **Simpler setup** - Just upload to GitHub  
✅ **More generous** - 2000+ free minutes/month (vs GCP's complex billing)  
✅ **Easier to manage** - Built-in UI, no CLI needed  

---

### Next Steps
**See [QUICK_START.md](QUICK_START.md) to get started!**

This migration was completed on: October 9, 2025


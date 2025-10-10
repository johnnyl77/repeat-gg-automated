<p align="center">
  <img src="imgs/logo.png" alt="This is the repeat-gg logo"/>
</p>

# Repeat.gg Automated

Automatically join free tournaments on repeat.gg. Runs 24/7 on GitHub's servers for free (no PC needed, no credit card required).

## 🚀 Quick Start

**[👉 Follow the QUICK_START.md guide](QUICK_START.md)** ← 5 minute setup!

Or read the detailed guide: **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)**

---

## ✨ Features

✅ **100% Free** - No payment info required  
✅ **Automatic** - Runs every 6 hours  
✅ **Cloud-based** - No local computer needed  
✅ **Easy Setup** - Just upload to GitHub  

---

## 📝 Setup Summary

1. Export your cookies: `python export_cookies.py`
2. Upload code to GitHub
3. Add cookies as a secret
4. Enable GitHub Actions

**That's it!** See [QUICK_START.md](QUICK_START.md) for step-by-step instructions.

---

## 🎮 Changing the Game

Edit line 224 in `repeat-gg-automated.py`:

```python
driver.get("https://www.repeat.gg/mobile/brawl-stars")
```

Change to:
- `https://www.repeat.gg/pc/league-of-legends`
- `https://www.repeat.gg/pc/fortnite`
- Or any other game on repeat.gg

---

## 🔧 Managing It

**Run manually (test):**
- Go to Actions tab → Click workflow → "Run workflow"

**View results:**
- Actions tab → Click any run to see logs

**Update cookies (when they expire):**
1. Run `python export_cookies.py` locally
2. Go to Settings → Secrets → Actions
3. Update `REPEAT_GG_COOKIES` secret

**Change schedule:**
- Edit `.github/workflows/tournament-automation.yml`

**Pause automation:**
- Comment out the schedule lines in the workflow file

---

## 📊 Usage Stats

- **Free minutes/month:** 2000+
- **Used per run:** ~2 minutes
- **Runs per month (every 6 hours):** ~120
- **Monthly usage:** ~240 minutes (12% of quota)

**You have plenty of free quota!** 🎉

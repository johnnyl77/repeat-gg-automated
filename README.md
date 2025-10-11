<p align="center">
  <img src="imgs/logo.png" alt="This is the repeat-gg logo"/>
</p>

# Repeat.gg Automated

Automatically join free tournaments on repeat.gg. 

## 🎯 Two Ways to Use

### Option 1: Local (Your Computer) - 2 Minute Setup!

✅ **Super Easy** - Just run setup script and log in  
✅ **Reliable** - Uses your actual Chrome session  
✅ **Full Control** - Watch it work on your PC  

**Quick Setup:**
1. Install dependencies: `pip install -r requirements.txt`
2. Run setup: `python setup_profile.py`
3. Log into repeat.gg when browser opens
4. Run automation: `python repeat-gg-automated.py`

### Option 2: Cloud (GitHub Actions - 24/7)

**[👉 Follow GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)** ← 5 minute setup!

✅ **100% Free** - No payment info required  
✅ **Automatic** - Runs every 6 hours, 24/7  
✅ **No PC Needed** - Runs on GitHub's servers  
✅ **Set and Forget** - Just check results  

---

## ✨ Features

✅ Auto-joins free tournaments (no password required)  
✅ Auto-claims all prizes  
✅ Supports all games on repeat.gg  
✅ Headless mode option (invisible browser)  
✅ Detailed logging of what was joined  

---

## 📝 Detailed Local Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the setup script:**
   ```bash
   python setup_profile.py
   ```
   This will open Chrome. Log into repeat.gg, then press Enter in the terminal.

3. **Run the automation:**
   ```bash
   python repeat-gg-automated.py
   ```

**That's it!** Your login is saved and will be reused automatically.

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

**Update session token (when it expires):**
1. Get new PHPSESSID from repeat.gg cookies
2. Go to Settings → Secrets → Actions
3. Update `REPEAT_GG_SESSION_TOKEN` secret

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

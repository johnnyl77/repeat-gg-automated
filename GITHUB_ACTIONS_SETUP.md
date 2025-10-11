# GitHub Actions Setup (100% Free - No Credit Card!)

This guide shows you how to run your tournament automation 24/7 on GitHub's servers for FREE.

## ✅ Benefits
- **Completely free** - No payment info required
- **Runs every 6 hours automatically** 
- **No local computer needed**
- **Easy to manage**

## 📋 Setup Steps (5 minutes)

### 1. Create GitHub Account (if you don't have one)
Go to https://github.com and sign up (it's free)

### 2. Create a New Repository
1. Click the **"+"** in top right → **"New repository"**
2. Name it: `repeat-gg-automated`
3. Make it **Public** (for unlimited free minutes) or **Private** (3000 minutes/month free)
4. Click **"Create repository"**

### 3. Upload Your Code
**Option A - Using GitHub Website (easier):**
1. Click **"uploading an existing file"**
2. Drag and drop all files from this folder
3. Click **"Commit changes"**

**Option B - Using Git (if you know how):**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/repeat-gg-automated.git
git push -u origin main
```

### 4. Add Your Cookies as a Secret
1. In your GitHub repo, click **"Settings"** tab
2. Click **"Secrets and variables"** → **"Actions"** (in left sidebar)
3. Click **"New repository secret"**
4. Name: `REPEAT_GG_COOKIES`
5. Value: Copy the entire contents from `repeat_gg_cookies.txt`
6. Click **"Add secret"**

### 5. Enable GitHub Actions
1. Go to **"Actions"** tab in your repo
2. Click **"I understand my workflows, go ahead and enable them"**
3. Done! ✅

## 🎮 How to Use

### Run Manually (Test It)
1. Go to **"Actions"** tab
2. Click **"Repeat.gg Tournament Automation"** on the left
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait ~2 minutes, then click on the run to see results

### Automatic Schedule
It will automatically run every 6 hours at:
- 12:00 AM (midnight)
- 6:00 AM
- 12:00 PM (noon)
- 6:00 PM

(Times are in UTC - adjust the schedule in `.github/workflows/tournament-automation.yml` if needed)

### View Results
1. Go to **"Actions"** tab
2. Click any run to see what tournaments were joined

## 🔧 Changing the Schedule

Edit `.github/workflows/tournament-automation.yml` line 6:

```yaml
# Every 6 hours (default)
- cron: '0 */6 * * *'

# Every 4 hours
- cron: '0 */4 * * *'

# Twice a day (8 AM and 8 PM UTC)
- cron: '0 8,20 * * *'

# Once a day at noon UTC
- cron: '0 12 * * *'
```

Cron format: `minute hour day month weekday`

## 🔄 Updating Cookies (when they expire)

1. Run `python export_cookies.py` locally
2. Copy contents of `repeat_gg_cookies.txt`
3. Go to repo **Settings** → **Secrets and variables** → **Actions**
4. Click on `REPEAT_GG_COOKIES` → **Update**
5. Paste new cookies → **Update secret**

## ⏸️ Pause/Stop Automation

**Pause temporarily:**
1. Edit `.github/workflows/tournament-automation.yml`
2. Comment out the schedule lines:
```yaml
# schedule:
#   - cron: '0 */6 * * *'
```

**Delete completely:**
Just delete the `.github` folder from your repository

## 🐛 Troubleshooting

**"No tournaments found"**
- Your cookies might have expired - update them (see above)

**"Workflow failed"**
- Click on the failed run in Actions tab to see error details
- Most likely: cookies expired

**Want to change games?**
Edit `repeat-gg-automated.py` line 224:
```python
driver.get("https://www.repeat.gg/mobile/brawl-stars")
```

## 💡 Tips

- GitHub gives you 2000+ free minutes/month (each run takes ~2 minutes)
- Running every 6 hours = 4 runs/day × 30 days = 120 runs/month = 240 minutes
- You have PLENTY of free minutes!
- Make repo public for unlimited minutes


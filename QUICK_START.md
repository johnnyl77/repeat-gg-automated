# 🎮 Quick Start - Get Running in 5 Minutes

## Step 1: Export Your Cookies
```bash
python export_cookies.py
```
This creates `repeat_gg_cookies.txt` - you'll need this!

---

## Step 2: Upload to GitHub

1. Go to https://github.com
2. Sign up/login (free, no credit card)
3. Click **"New repository"** 
4. Name it anything you want
5. Make it **Public** (for unlimited free minutes)
6. Upload all files from this folder

---

## Step 3: Add Cookies Secret

1. In your repo, click **"Settings"** tab
2. **"Secrets and variables"** → **"Actions"**
3. **"New repository secret"**
4. Name: `REPEAT_GG_COOKIES`
5. Paste entire contents from `repeat_gg_cookies.txt`
6. Click **"Add secret"**

---

## Step 4: Enable & Test

1. Go to **"Actions"** tab
2. Enable workflows
3. Click **"Repeat.gg Tournament Automation"**
4. **"Run workflow"** → **"Run workflow"**
5. Wait 2 minutes
6. Click the run to see results

---

## ✅ Done!

It will now run automatically every 6 hours forever!

**View runs:** Go to Actions tab anytime  
**Update cookies:** Settings → Secrets → Update `REPEAT_GG_COOKIES`  
**Change schedule:** Edit `.github/workflows/tournament-automation.yml`

---

## 📊 Cost: $0.00
- No credit card needed
- 2000+ free minutes/month
- Each run takes ~2 minutes
- Running every 6 hours = ~240 minutes/month
- You're using 12% of your free quota

**Need help?** Check [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions.


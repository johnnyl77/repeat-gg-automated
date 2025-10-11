# 🎮 Quick Start - Local Setup (2 Minutes!)

## Step 1: Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

---

## Step 2: Run Setup Script

```bash
python setup_profile.py
```

A Chrome window will open. Log into repeat.gg, then press Enter in the terminal.

---

## Step 3: Run Automation

```bash
python repeat-gg-automated.py
```

Done! It will automatically join tournaments and claim prizes.

---

# 🌐 Cloud Setup (GitHub Actions - 5 Minutes)

Want it to run 24/7 in the cloud for free? Follow these steps:

## Step 1: Export Your Authentication

First, set up locally (from steps above), then run:

```bash
python export_auth_for_github.py
```

This will create `github_auth_data.txt` with your complete authentication data.

**Why this method?** It captures ALL cookies, localStorage, and sessionStorage - much more reliable than individual cookies!

---

## Step 2: Upload to GitHub

1. Go to https://github.com
2. Sign up/login (free, no credit card)
3. Click **"New repository"** 
4. Name it anything you want
5. Make it **Public** (for unlimited free minutes)
6. Upload all files from this folder

---

## Step 3: Add Authentication Secret

1. In your repo, click **"Settings"** tab
2. **"Secrets and variables"** → **"Actions"**
3. **"New repository secret"**
   - Name: `REPEAT_GG_AUTH_DATA`
   - Value: Copy the entire long string from `github_auth_data.txt`
4. Click **"Add secret"**

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
**Update auth:** Run `export_auth_for_github.py` again and update the `REPEAT_GG_AUTH_DATA` secret  
**Change schedule:** Edit `.github/workflows/tournament-automation.yml`

---

## 📊 Cost: $0.00
- No credit card needed
- 2000+ free minutes/month
- Each run takes ~2 minutes
- Running every 6 hours = ~240 minutes/month
- You're using 12% of your free quota

---

## 🔄 When Auth Expires

If GitHub Actions stops working after a while:
1. Locally, run: `python export_auth_for_github.py`
2. Update `REPEAT_GG_AUTH_DATA` secret in GitHub with the new value
3. Done! The automation will work again

**This new method is MUCH more reliable than copying individual cookies!**

**Need help?** Check [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions.


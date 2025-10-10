"""
Export cookies from your Chrome profile to use in GitHub Actions

WHAT THIS DOES:
- Reads cookies from YOUR OWN Chrome profile (that you specify in .env)
- Only exports cookies for repeat.gg (not other websites)
- Saves them as base64 text in repeat_gg_cookies.txt
- Does NOT send cookies anywhere or access the internet
- You manually copy/paste the result into GitHub secrets

WHY THIS IS SAFE:
- Runs locally on YOUR computer only
- You can read this entire script (it's < 120 lines)
- Only accesses YOUR Chrome profile folder (that you own)
- Cookies stay on YOUR computer until you manually upload them
- Open source - no hidden behavior

NOTE: If this feels uncomfortable, you can manually extract cookies
from Chrome DevTools instead (see GitHub Actions setup guide).

Run this script locally after logging into repeat.gg in Chrome.
"""

import os
import json
import base64
import sqlite3
import shutil
from pathlib import Path

def export_cookies_from_profile():
    """Export cookies from Chrome Profile 6"""
    
    # Get profile path from .env
    from dotenv import load_dotenv
    load_dotenv()
    
    profile_path = os.getenv("PROFILE_PATH")
    profile_name = os.getenv("PROFILE_NAME")
    
    if not profile_path or not profile_name:
        print("❌ Could not find PROFILE_PATH or PROFILE_NAME in .env file")
        return
    
    # Path to Chrome cookies database
    cookies_db_path = os.path.join(profile_path, profile_name, "Network", "Cookies")
    
    if not os.path.exists(cookies_db_path):
        # Try alternative location
        cookies_db_path = os.path.join(profile_path, profile_name, "Cookies")
    
    if not os.path.exists(cookies_db_path):
        print(f"❌ Could not find Cookies database at: {cookies_db_path}")
        return
    
    # Copy the database to avoid locking issues
    temp_db = "temp_cookies.db"
    try:
        shutil.copy2(cookies_db_path, temp_db)
    except Exception as e:
        print(f"❌ Could not copy cookies database: {e}")
        print("💡 Make sure Chrome is closed before running this script")
        return
    
    # Connect to the database
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    
    # Get cookies for repeat.gg
    try:
        cursor.execute("""
            SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, samesite
            FROM cookies 
            WHERE host_key LIKE '%repeat.gg%'
        """)
        
        cookies = []
        for row in cursor.fetchall():
            cookie = {
                'domain': row[0],
                'name': row[1],
                'value': row[2],
                'path': row[3],
                'expiry': row[4],
                'secure': bool(row[5]),
                'httpOnly': bool(row[6]),
                'sameSite': 'None' if row[7] == 0 else 'Lax' if row[7] == 1 else 'Strict'
            }
            cookies.append(cookie)
        
        conn.close()
        os.remove(temp_db)
        
        if not cookies:
            print("❌ No repeat.gg cookies found. Make sure you're logged into repeat.gg in Chrome Profile 6")
            return
        
        print(f"✅ Found {len(cookies)} repeat.gg cookies")
        
        # Convert to JSON and base64 encode
        cookies_json = json.dumps(cookies)
        cookies_base64 = base64.b64encode(cookies_json.encode()).decode()
        
        # Save to file
        with open("repeat_gg_cookies.txt", "w") as f:
            f.write(cookies_base64)
        
        print("\n" + "="*70)
        print("✅ Cookies exported successfully!")
        print("="*70)
        print("\n📋 Next steps:")
        print("1. Open: repeat_gg_cookies.txt")
        print("2. Copy the entire contents (it's base64 encoded)")
        print("3. Add to GitHub as a secret named REPEAT_GG_COOKIES")
        print("   (See QUICK_START.md for detailed instructions)")
        print("\n⚠️  Important: Re-export cookies every 30-90 days when they expire")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Error reading cookies: {e}")
        conn.close()
        if os.path.exists(temp_db):
            os.remove(temp_db)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  Repeat.gg Cookie Exporter")
    print("="*70 + "\n")
    print("⚠️  Make sure Chrome is CLOSED before running this script!\n")
    input("Press ENTER to continue...")
    export_cookies_from_profile()


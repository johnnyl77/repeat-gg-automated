"""
Export Authentication Data for GitHub Actions
==============================================
Run this script after setting up your local profile with setup_profile.py
It will extract essential cookies and storage data for use in GitHub Actions.
(Optimized to fit within GitHub's 64KB secret size limit)
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import json
import time
import base64

print("\n" + "="*70)
print("  Export Authentication for GitHub Actions")
print("="*70)

# Get ChromeDriver path
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
if not CHROMEDRIVER_PATH:
    possible_paths = [
        "./chromedriver-win64/chromedriver.exe",
        "chromedriver.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            CHROMEDRIVER_PATH = path
            break

if not CHROMEDRIVER_PATH:
    print("\n⚠ ChromeDriver not found!")
    print("Please set CHROMEDRIVER_PATH or place chromedriver.exe in this folder")
    input("\nPress Enter to exit...")
    exit(1)

# Check if profile exists
automation_profile = os.path.join(os.getcwd(), "chrome_automation_profile")
if not os.path.exists(automation_profile):
    print("\n⚠ No authenticated profile found!")
    print("Please run setup_profile.py first to set up your local authentication.")
    input("\nPress Enter to exit...")
    exit(1)

print(f"\n✓ Found authenticated profile")
print("\nOpening browser to extract authentication data...")

# Set up Chrome with the authenticated profile
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={automation_profile}")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Navigate to repeat.gg
    print("✓ Navigating to repeat.gg...")
    driver.get("https://www.repeat.gg/mobile/brawl-stars")
    time.sleep(5)
    
    print("\n" + "="*70)
    print("  Extracting authentication data...")
    print("="*70)
    
    # Extract all cookies
    all_cookies = driver.get_cookies()
    
    # Filter to only essential cookies (remove tracking/analytics cookies)
    essential_domains = ['.repeat.gg', 'www.repeat.gg', 'repeat.gg']
    essential_cookies = [c for c in all_cookies if c.get('domain') in essential_domains]
    
    print(f"\n✓ Found {len(all_cookies)} total cookies")
    print(f"✓ Keeping {len(essential_cookies)} essential cookies (filtered out tracking cookies)")
    
    # Get ALL localStorage items (don't filter - we need them all!)
    local_storage = driver.execute_script("""
        let items = {};
        for (let i = 0; i < localStorage.length; i++) {
            let key = localStorage.key(i);
            items[key] = localStorage.getItem(key);
        }
        return items;
    """)
    print(f"✓ Found {len(local_storage)} localStorage items")
    
    # Get sessionStorage too
    session_storage = driver.execute_script("""
        let items = {};
        for (let i = 0; i < sessionStorage.length; i++) {
            let key = sessionStorage.key(i);
            items[key] = sessionStorage.getItem(key);
        }
        return items;
    """)
    print(f"✓ Found {len(session_storage)} sessionStorage items")
    
    # Create auth data package
    auth_data = {
        "cookies": essential_cookies,
        "localStorage": local_storage,
        "sessionStorage": session_storage
    }
    
    # Convert to JSON string
    auth_json = json.dumps(auth_data, separators=(',', ':'))  # Compact JSON (no spaces)
    
    # Encode to base64
    auth_base64 = base64.b64encode(auth_json.encode()).decode()
    
    # Check size
    size_bytes = len(auth_base64)
    size_kb = size_bytes / 1024
    
    print(f"\n✓ Auth data size: {size_kb:.2f} KB")
    
    if size_kb > 64:
        print("\n⚠ WARNING: Data is larger than 64KB!")
        print("   Trying to compress by removing large items...")
        
        # Try removing large localStorage items
        filtered_local_storage = {k: v for k, v in local_storage.items() if len(v) < 10000}
        
        auth_data_compressed = {
            "cookies": essential_cookies,
            "localStorage": filtered_local_storage,
            "sessionStorage": session_storage
        }
        
        auth_json = json.dumps(auth_data_compressed, separators=(',', ':'))
        auth_base64 = base64.b64encode(auth_json.encode()).decode()
        size_bytes = len(auth_base64)
        size_kb = size_bytes / 1024
        
        print(f"✓ Compressed to: {size_kb:.2f} KB (removed items > 10KB)")
        
        if size_kb > 64:
            print("\n⚠ Still too large! Saving anyway, but GitHub may reject it.")
    else:
        print("✓ Size is within GitHub's 64KB limit!")
    
    # Save to file
    output_file = "github_auth_data.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("="*70 + "\n")
        f.write("COPY THIS ENTIRE VALUE TO GITHUB SECRETS\n")
        f.write("="*70 + "\n")
        f.write("Secret Name: REPEAT_GG_AUTH_DATA\n")
        f.write(f"Size: {size_kb:.2f} KB\n")
        f.write("="*70 + "\n\n")
        f.write(auth_base64)
        f.write("\n\n" + "="*70 + "\n")
        f.write("INSTRUCTIONS:\n")
        f.write("1. Go to your GitHub repo -> Settings -> Secrets -> Actions\n")
        f.write("2. Click 'New repository secret'\n")
        f.write("3. Name: REPEAT_GG_AUTH_DATA\n")
        f.write("4. Value: Copy the long string above (just the base64, not the headers)\n")
        f.write("5. Click 'Add secret'\n")
        f.write("="*70 + "\n")
    
    print("\n" + "="*70)
    print("  SUCCESS!")
    print("="*70)
    print(f"\n✓ Auth data saved to: {output_file}")
    print("\nNext steps:")
    print(f"   1. Open {output_file}")
    print("   2. Copy ONLY the base64 string (the long line)")
    print("   3. Update REPEAT_GG_AUTH_DATA secret in GitHub")
    print("\nThis includes ALL cookies and storage for full authentication!\n")
    
    # Also save as JSON for debugging
    debug_file = "github_auth_data_debug.json"
    with open(debug_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(auth_data, indent=2))
    print(f"Debug version saved to: {debug_file} (human-readable)")
    
    driver.quit()
    print("\n✓ Browser closed")
    
    input("\nPress Enter to exit...")

except Exception as e:
    print(f"\n⚠ Error: {e}")
    try:
        driver.quit()
    except:
        pass
    input("\nPress Enter to exit...")
    exit(1)


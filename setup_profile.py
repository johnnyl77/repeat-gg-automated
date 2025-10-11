"""
Repeat.gg Profile Setup Script
================================
This script helps you set up authentication for the automation.
Just run it once, log into repeat.gg, and you're done!
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time

print("\n" + "="*70)
print("  Repeat.gg Profile Setup")
print("="*70)
print("\nThis script will open Chrome so you can log into repeat.gg.")
print("After logging in, the session will be saved for automation.\n")

# Get ChromeDriver path from environment or use default
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

if not CHROMEDRIVER_PATH:
    # Try common locations
    possible_paths = [
        "./chromedriver-win64/chromedriver.exe",  # Local folder
        "chromedriver.exe",  # Current directory
        "C:\\chromedriver\\chromedriver.exe",  # Common install location
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            CHROMEDRIVER_PATH = path
            break
    
    if not CHROMEDRIVER_PATH:
        print("⚠ ChromeDriver not found!")
        print("\nPlease either:")
        print("1. Add chromedriver.exe to this folder, OR")
        print("2. Set CHROMEDRIVER_PATH in your .env file")
        print("\nDownload ChromeDriver from:")
        print("https://googlechromelabs.github.io/chrome-for-testing/")
        input("\nPress Enter to exit...")
        exit(1)

print(f"✓ Using ChromeDriver: {CHROMEDRIVER_PATH}\n")

# Create automation profile directory
automation_profile = os.path.join(os.getcwd(), "chrome_automation_profile")
if not os.path.exists(automation_profile):
    os.makedirs(automation_profile)
    print(f"✓ Created profile directory: {automation_profile}")
else:
    print(f"✓ Using existing profile: {automation_profile}")

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={automation_profile}")

# Add realistic user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

# Make browser visible for login
options.add_argument("--start-maximized")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("detach", True)  # Keep browser open

# Initialize WebDriver
try:
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    print("✓ Chrome browser opened!\n")
except Exception as e:
    print(f"⚠ Error starting Chrome: {e}")
    input("\nPress Enter to exit...")
    exit(1)

# Navigate to repeat.gg
print("="*70)
print("  Opening repeat.gg...")
print("="*70 + "\n")

try:
    driver.get("https://www.repeat.gg/mobile/brawl-stars")
    time.sleep(3)
    
    print("\n" + "="*70)
    print("  INSTRUCTIONS")
    print("="*70)
    print("\n1. Log into repeat.gg in the browser window that just opened")
    print("   (Use your Google account or preferred login method)")
    print("\n2. After you're logged in, come back here and press Enter")
    print("\n3. That's it! The automation will remember your login\n")
    
    input("Press Enter after you've logged in...")
    
    # Verify login by checking current page
    print("\n" + "="*70)
    print("  Verifying login...")
    print("="*70)
    
    time.sleep(2)
    driver.refresh()
    time.sleep(3)
    
    # Try to detect if logged in
    from selenium.webdriver.common.by import By
    
    try:
        # Look for login-related elements (bad sign)
        login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Log in') or contains(text(), 'Sign in') or contains(text(), 'Login')]")
        
        # Look for user-related elements (good sign)
        user_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'user') or contains(@class, 'profile') or contains(@class, 'avatar')]")
        
        if login_elements and not user_elements:
            print("\n⚠ It looks like you might not be logged in yet.")
            print("   You can still proceed, but the automation may not work properly.")
            proceed = input("\nDo you want to continue anyway? (y/n): ")
            if proceed.lower() != 'y':
                print("\nPlease log in and run this setup script again.")
                driver.quit()
                exit(0)
        else:
            print("\n✓ Login detected!")
    except:
        print("\n⚠ Could not verify login status, but that's okay.")
        print("   If you logged in successfully, the automation should work.\n")
    
    print("\n" + "="*70)
    print("  SUCCESS! Setup Complete")
    print("="*70)
    print("\n✓ Your login session has been saved!")
    print("\n📝 Next steps:")
    print("   1. Run: python repeat-gg-automated.py")
    print("   2. The script will automatically use your saved login")
    print("\n💡 Tip: You can keep the browser open or close it.")
    print("   The automation will use your saved session either way.\n")
    
    # Keep browser open for a moment so user can see
    time.sleep(3)
    
    print("Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
    print("✓ Browser closed. Setup complete!\n")

except Exception as e:
    print(f"\n⚠ Error during setup: {e}")
    print("\nYou can try running the setup again.")
    try:
        driver.quit()
    except:
        pass
    input("\nPress Enter to exit...")
    exit(1)


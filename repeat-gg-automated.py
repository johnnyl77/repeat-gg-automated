from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import signal
import subprocess
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION - Set to True for headless (invisible) or False to see browser
# ============================================================================
HEADLESS_MODE = True  # Change to False to see the browser while it works
# ============================================================================

# Check if running in GitHub Actions (or other cloud environment)
IS_GITHUB_ACTIONS = os.getenv("K_SERVICE") is not None  # Set by cloud environments

def authenticate_with_session_token(driver):
    """Authenticate using session token from environment variable"""
    try:
        session_token = os.getenv("REPEAT_GG_SESSION_TOKEN")
        
        if not session_token:
            print("⚠ No session token found in environment variables")
            print("💡 Add REPEAT_GG_SESSION_TOKEN to GitHub secrets")
            return False
        
        print("Authenticating with session token...")
        
        # Navigate to repeat.gg first
        driver.get("https://www.repeat.gg")
        time.sleep(3)
        
        # Set the session token as a cookie (most reliable method)
        driver.add_cookie({
            'name': 'PHPSESSID',
            'value': session_token,
            'domain': 'www.repeat.gg',
            'path': '/',
            'secure': True,
            'httpOnly': True
        })
        
        # Refresh to activate authentication
        driver.refresh()
        time.sleep(3)
        
        # Verify authentication
        try:
            driver.get("https://www.repeat.gg/mobile/brawl-stars")
            time.sleep(3)
            
            # Check if we're logged in by looking for login elements
            login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Log in') or contains(text(), 'Sign in') or contains(text(), 'Login')]")
            if not login_elements:
                print("✓ Successfully authenticated!")
                return True
            else:
                print("⚠ Authentication failed - still seeing login elements")
                return False
        except Exception as e:
            print(f"⚠ Could not verify authentication: {e}")
            return False
        
    except Exception as e:
        print(f"⚠ Session token authentication failed: {e}")
        return False

# Function to close all Chrome processes and clean up lock files
def close_chrome_processes():
    try:
        # Use taskkill to force close all Chrome processes
        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        print("Closed all Chrome processes")
    except Exception as e:
        print(f"Note: No Chrome processes to close or error closing: {e}")

def remove_chrome_lock_files(profile_path, profile_name):
    """Remove Chrome lock files to prevent profile conflicts"""
    try:
        import glob
        # Lock files to remove
        profile_dir = os.path.join(profile_path, profile_name)
        lock_files = [
            os.path.join(profile_path, "SingletonLock"),
            os.path.join(profile_path, "lockfile"),
            os.path.join(profile_dir, "SingletonLock"),
            os.path.join(profile_dir, "lockfile")
        ]
        
        for lock_file in lock_files:
            if os.path.exists(lock_file):
                try:
                    os.remove(lock_file)
                    print(f"Removed lock file: {lock_file}")
                except:
                    pass
    except Exception as e:
        print(f"Note: Could not remove lock files: {e}")

def copy_login_session(source_profile_path, source_profile_name, dest_profile_path):
    """Copy login session from Profile 6 to automation profile for auto-login"""
    try:
        import shutil
        source_dir = os.path.join(source_profile_path, source_profile_name)
        
        # Files to copy for login session (cookies, local storage, etc.)
        files_to_copy = [
            "Cookies",
            "Network\\Cookies",
            "Local Storage",
            "Session Storage",
            "IndexedDB",
            "Preferences",
            "Secure Preferences"
        ]
        
        copied_count = 0
        for file_name in files_to_copy:
            source_file = os.path.join(source_dir, file_name)
            dest_file = os.path.join(dest_profile_path, "Default", file_name)
            
            # Create destination directory if needed
            dest_file_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_file_dir):
                os.makedirs(dest_file_dir, exist_ok=True)
            
            # Copy file or directory
            if os.path.exists(source_file):
                try:
                    if os.path.isfile(source_file):
                        shutil.copy2(source_file, dest_file)
                        copied_count += 1
                    elif os.path.isdir(source_file):
                        if os.path.exists(dest_file):
                            shutil.rmtree(dest_file)
                        shutil.copytree(source_file, dest_file)
                        copied_count += 1
                except Exception as e:
                    pass  # Skip files that can't be copied
        
        if copied_count > 0:
            print(f"✓ Copied login session from {source_profile_name} to automation profile")
            return True
        return False
    except Exception as e:
        print(f"Note: Could not copy login session: {e}")
        return False

# Set up paths based on environment
if IS_GITHUB_ACTIONS:
    print("Running in GitHub Actions environment")
    PROFILE_PATH = None
    PROFILE_NAME = None
    CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # Linux path
else:
    PROFILE_PATH = os.getenv("PROFILE_PATH")
    PROFILE_NAME = os.getenv("PROFILE_NAME")
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
    
    # Debug: Print paths to verify they're loaded
    print(f"Profile Path: {PROFILE_PATH}")
    print(f"Profile Name: {PROFILE_NAME}")
    print(f"ChromeDriver Path: {CHROMEDRIVER_PATH}")

# Set up Chrome options
options = webdriver.ChromeOptions()

# Set up profile based on environment
if IS_GITHUB_ACTIONS:
    # In GitHub Actions, use a fresh profile (will load cookies from environment)
    automation_profile = os.path.join(os.getcwd(), "chrome_automation_profile")
    if not os.path.exists(automation_profile):
        os.makedirs(automation_profile)
    print("Using fresh profile for GitHub Actions")
else:
    # Local: Use automation profile and copy cookies from Profile 6
    automation_profile = os.path.join(os.getcwd(), "chrome_automation_profile")
    if not os.path.exists(automation_profile):
        os.makedirs(automation_profile)
        print(f"Created automation profile directory: {automation_profile}")
    
    # Copy login session from Profile 6 to automation profile for auto-login
    print("Copying login session from Profile 6...")
    copy_login_session(PROFILE_PATH, PROFILE_NAME, automation_profile)

options.add_argument(f"--user-data-dir={automation_profile}")

# Add realistic user agent for both modes
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

# Conditionally add headless mode
if HEADLESS_MODE:
    print("Running in HEADLESS mode (invisible browser)...")
    options.add_argument("--headless=new")  # Run in headless mode (no visible browser)
    options.add_argument("--window-size=1920,1080")  # Set window size for headless mode
    # Additional options to make headless work better
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
else:
    print("Running in VISIBLE mode (browser will be shown)...")
    options.add_argument("--start-maximized")  # Start maximized when visible

options.add_argument("--remote-debugging-port=9222")  # Add debugging port
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Only detach if not in headless mode (so browser stays open)
if not HEADLESS_MODE:
    options.add_experimental_option("detach", True)

# Set up the Service with the path to chromedriver.exe
service = Service(executable_path=CHROMEDRIVER_PATH)

# Initialize the WebDriver with the specified service and options
driver = webdriver.Chrome(service=service, options=options)

# Open a website to test
driver.get("https://www.repeat.gg/mobile/brawl-stars")

# Other example formats:
# driver.get("https://www.repeat.gg/pc/league-of-legends")
# driver.get("https://www.repeat.gg/pc/fortnite")


# Allow the page to load initially
time.sleep(3)

# If running in GitHub Actions, authenticate with session token
if IS_GITHUB_ACTIONS:
    print("\n" + "="*70)
    print("  GitHub Actions: Authenticating...")
    print("="*70)
    
    auth_success = authenticate_with_session_token(driver)
    
    if not auth_success:
        print("\n" + "="*70)
        print("  AUTHENTICATION FAILED")
        print("="*70)
        print("\nTo fix this:")
        print("1. Get your PHPSESSID from repeat.gg cookies")
        print("2. Add REPEAT_GG_SESSION_TOKEN to your GitHub repository secrets")
        print("3. Re-run this workflow")
        print("\nContinuing without authentication...")
    else:
        print("✓ Authentication successful!")

print("\n" + "="*70)
print("  Starting tournament search and auto-join...")
print("="*70 + "\n")

# Initialize the counter for free tournaments
free_tourneys = 0

# Wait for tournament elements to load (explicit wait for React)
print("Waiting for tournaments to load...")
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tournament row"]'))
    )
    print("✓ Tournaments loaded!")
    time.sleep(2)  # Give a bit more time for all elements to render
except:
    print("⚠ No tournaments found or page didn't load properly")

# Locate all tournament elements
tournament_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tournament row"]')
print(f"Found {len(tournament_elements)} tournament(s) on the page")

# Store the qualifying tournament links
tournament_links = []

# Process each tournament
for element in tournament_elements:
    outer_html = element.get_attribute("outerHTML")

    # Check for "Free Entry" and "Join Now" but exclude "Password"
    if "Free Entry" in outer_html and "Join Now" in outer_html and "Password" not in outer_html:
        # Extract the link
        tournament_link = element.get_attribute("href")
        if tournament_link:
            tournament_links.append(tournament_link)

# Open each tournament link in a new tab
for link in tournament_links:
    driver.execute_script(f"window.open('{link}', '_blank');")
    time.sleep(1) # Delay for opening each link to new tab

# Wait for all tabs to open & load
time.sleep(3) #prev 5s

# Recheck window handles and loop through each tab
window_handles = driver.window_handles

print('\n\n|--------------------------------------------------------------------|')
for i in range(1, len(window_handles)):
    try:
        driver.switch_to.window(window_handles[i])

        # Check if the entry is free
        fee_label = driver.find_element(By.CLASS_NAME, 'entryFee')
        
        if "Free Entry" in fee_label.get_attribute("outerHTML"):
            print(f"Processing tournament in tab {i}")

            # Tourney Name
            tourney_header = driver.find_element(By.CSS_SELECTOR, '[data-testid="tournament header"]')
            tourney_name = tourney_header.find_element(By.TAG_NAME, 'h1')
            print("Tournament Name: " + tourney_name.get_attribute("innerHTML"))

            # Tourney Duration
            try:
                duration_div = tourney_header.find_element(By.XPATH, '//div[@data-notranslate="true" and contains(., "•")]')
                duration_html = duration_div.get_attribute('innerHTML')
                date_pattern = r'\b[A-Za-z]+\s\d{1,2}(?:st|nd|rd|th)?\s•\s\d{1,2}:\d{2}\s[APM]{2}\b'
                matches = re.findall(date_pattern, duration_html)
                
                if matches:
                    print("Dates: " + ' ⟶ '.join(matches))
                else:
                    print("No dates found.")
            except Exception as e:
                print(f"Error finding duration: {e}")

            # Prize Pool
            try:
                prize_pool_element = driver.find_element(By.XPATH, '//div[contains(@class, "prizePool")]')
                
                try:
                    # Check for USD prize
                    span_element = prize_pool_element.find_element(By.XPATH, './/span[@data-testid="USD"]')
                    img_element = span_element.find_element(By.XPATH, './/img[@alt="dollar"]')
                    prize_text = span_element.text.strip()
                    print("USD: " + prize_text)
                
                except:
                    try:
                        # Check for Coins prize 
                        span_element = prize_pool_element.find_element(By.XPATH, './/span[@data-testid="PM"]')
                        img_element = span_element.find_element(By.XPATH, './/img[@alt="coins"]')
                        prize_text = span_element.text.strip()
                        print("Coins: " + prize_text)
                    
                    except Exception as e:
                        print(f"Error finding prize pool: {e}")
            
            except Exception as e:
                print(f"Error processing prize pool: {e}")

            # Join Button
            try:
                # Find and click the join button
                join_button = tourney_header.find_element(By.TAG_NAME, 'button')
                join_button.click()
                time.sleep(1) #prev 3s
                
                # Checks to see if there is an error msg when joining tourney
                try:
                    modal_element = driver.find_element(By.CLASS_NAME, 'MuiDialog-container')
                    
                    if modal_element:
                        print("\nJoin Unsuccessful")

                        # Print the contents of the h2 tag (Header of Reason for not being able to join tourney)
                        try:
                            h2_element = modal_element.find_element(By.TAG_NAME, 'h2')
                            print("Reason: " + h2_element.text)
                        except Exception as e:
                            print(f"Error finding reason: {e}")
                        
                        # Print the contents of all p tags (Explanation to Reason for not being able to join tourney)
                        try:
                            p_elements = modal_element.find_elements(By.TAG_NAME, 'p')
                            for p in p_elements:
                                print(p.text)
                            print('\n\n|--------------------------------------------------------------------|')
                        except Exception as e:
                            print(f"Error finding explanation for reason: {e}")
                except Exception as e:
                    # If the modal is not found, the join was successful
                    free_tourneys += 1
                    print("Successfully Joined Tourney")
                    print('|--------------------------------------------------------------------|')
            except Exception as e:
                print(f"Error clicking join button: {e}")
                print('|--------------------------------------------------------------------|')
            time.sleep(1) #prev 3s

    except Exception as e:
        print(f"Error processing tournament in tab {i}: {e}")
        print('|--------------------------------------------------------------------|')

#Optionally close all tabs except the original one
for i in range(1, len(window_handles)):
    driver.switch_to.window(window_handles[i])
    driver.close()

driver.switch_to.window(window_handles[0])

print("\nTourneys Joined this Session: " + str(free_tourneys))

# Refresh the main page
print("\n" + "="*70)
print("  Refreshing main page...")
print("="*70)
driver.refresh()
time.sleep(3)

# Navigate to claim prizes page
print("\n" + "="*70)
print("  Navigating to claim prizes page...")
print("="*70)
driver.get("https://www.repeat.gg/marketplace/claim-prizes")

# Wait for page to load with explicit wait
print("Waiting for claim prizes page to load...")
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "button"))
    )
    print("✓ Page loaded!")
    time.sleep(3)  # Give extra time for React to render all buttons
except:
    print("⚠ Claim prizes page didn't load properly")

# Click the "Claim All Cash & Coins" button
try:
    print("\n" + "="*70)
    print("  Attempting to claim all prizes...")
    print("="*70)
    
    # Try multiple ways to find the button
    claim_button = None
    
    # Method 1: Wait for and find button with text containing "Claim All"
    try:
        claim_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'claim all cash')]"))
        )
    except:
        pass
    
    # Method 2: Try looking for button by looping through all buttons
    if not claim_button:
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"Scanning {len(buttons)} buttons on the page...")
            for btn in buttons:
                btn_text = btn.text.lower()
                if "claim all" in btn_text and ("cash" in btn_text or "coins" in btn_text):
                    claim_button = btn
                    print(f"Found button with text: '{btn.text}'")
                    break
        except:
            pass
    
    # Method 3: Try by class name from the HTML
    if not claim_button:
        try:
            claim_button = driver.find_element(By.XPATH, "//button[contains(@class, 'mui-xezng5')]")
        except:
            pass
    
    if claim_button:
        # Check if button is enabled (not disabled)
        is_disabled = claim_button.get_attribute("disabled")
        if not is_disabled:
            claim_button.click()
            print("\n✓ Successfully clicked 'Claim All Cash & Coins' button!")
            time.sleep(2)
        else:
            print("\n⚠ 'Claim All Cash & Coins' button is currently disabled (you may have no prizes to claim)")
    else:
        print("\n⚠ Could not find 'Claim All Cash & Coins' button on the page")
        print("This may be because you have no prizes to claim or the page layout changed.")
        
except Exception as e:
    print(f"\n⚠ Error while trying to claim prizes: {e}")
    print("This may be because you have no prizes to claim or the page layout changed.")

print("\n" + "="*70)
print("  Script completed successfully!")
print("="*70 + "\n")

# Close the browser
if HEADLESS_MODE:
    driver.quit()
else:
    # In visible mode, keep browser open for 10 seconds so you can see results
    print("Browser will stay open for 10 seconds so you can see the results...")
    time.sleep(10)
    driver.quit()

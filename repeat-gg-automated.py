from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION - Set to True for headless (invisible) or False to see browser
# ============================================================================
HEADLESS_MODE = True  # Change to False to see the browser while it works
# ============================================================================

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

# Load configuration from .env file
PROFILE_PATH = os.getenv("PROFILE_PATH")
PROFILE_NAME = os.getenv("PROFILE_NAME")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

# Debug: Print paths to verify they're loaded
print(f"Profile Path: {PROFILE_PATH}")
print(f"Profile Name: {PROFILE_NAME}")
print(f"ChromeDriver Path: {CHROMEDRIVER_PATH}")

# Set up Chrome options
options = webdriver.ChromeOptions()

# Create automation profile directory
automation_profile = os.path.join(os.getcwd(), "chrome_automation_profile")
if not os.path.exists(automation_profile):
    os.makedirs(automation_profile)
    print(f"Created automation profile directory: {automation_profile}")

# Copy login session from Profile 6 to automation profile for auto-login
print("Copying login session from Profile 6...")
copy_login_session(PROFILE_PATH, PROFILE_NAME, automation_profile)

options.add_argument(f"--user-data-dir={automation_profile}")

# Add realistic user agent
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

# ============================================================================
# GAMES LIST - Add or remove games as needed
# ============================================================================
GAMES_LIST = [
    {"name": "League of Legends", "url": "https://www.repeat.gg/pc/league-of-legends"},
    {"name": "Rocket League", "url": "https://www.repeat.gg/pc/rocket-league"},
    {"name": "Brawl Stars", "url": "https://www.repeat.gg/mobile/brawl-stars"}
]
# ============================================================================

print("\n" + "="*70)
print(f"  Checking {len(GAMES_LIST)} game(s) for tournaments...")
print("="*70 + "\n")

# Initialize the counter for free tournaments
free_tourneys = 0

# Loop through each game
for game_index, game in enumerate(GAMES_LIST, 1):
    print("\n" + "="*70)
    print(f"  [{game_index}/{len(GAMES_LIST)}] Checking {game['name']}...")
    print("="*70)
    
    # Navigate to the game's tournament page
    driver.get(game['url'])
    
    # Allow the page to load initially
    time.sleep(3)
    
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
        continue  # Skip to next game if no tournaments found

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

    if len(tournament_links) == 0:
        print(f"⚠ No qualifying free tournaments found for {game['name']}")
        continue  # Skip to next game if no qualifying tournaments

    print(f"Found {len(tournament_links)} qualifying tournament(s) for {game['name']}")

    # Open each tournament link in a new tab
    for link in tournament_links:
        driver.execute_script(f"window.open('{link}', '_blank');")
        time.sleep(1) # Delay for opening each link to new tab

    # Wait for all tabs to open & load
    time.sleep(3) #prev 5s

    # Recheck window handles and loop through each tab
    window_handles = driver.window_handles

    print('\n|--------------------------------------------------------------------|')
    for i in range(1, len(window_handles)):
        try:
            driver.switch_to.window(window_handles[i])

            # Check if the entry is free
            fee_label = driver.find_element(By.CLASS_NAME, 'entryFee')
            
            if "Free Entry" in fee_label.get_attribute("outerHTML"):
                print(f"Processing tournament in tab {i} for {game['name']}")

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
                                print('\n|--------------------------------------------------------------------|')
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

    # Close all tabs except the original one for this game
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

# Click all individual "Claim Prize" buttons
try:
    print("\n" + "="*70)
    print("  Attempting to claim individual prizes...")
    print("="*70)
    
    # Find all prize articles
    prize_articles = driver.find_elements(By.CSS_SELECTOR, "article.mui-2ss2o8")
    print(f"Found {len(prize_articles)} prize article(s) on the page")
    
    if len(prize_articles) == 0:
        print("⚠ No prize articles found on the page")
        print("This may be because you have no prizes to claim or the page layout changed.")
    else:
        total_claimed_value = 0
        claimed_count = 0
        
        # Process each prize article
        for i, article in enumerate(prize_articles, 1):
            try:
                print(f"\n--- Processing Prize {i}/{len(prize_articles)} ---")
                
                # Extract prize information
                prize_name = ""
                prize_value = 0
                currency_type = ""
                
                # Get prize value from h3 tag (e.g., "2500 coins")
                try:
                    prize_name_element = article.find_element(By.TAG_NAME, "h3")
                    prize_text = prize_name_element.text.strip()
                    print(f"Prize: {prize_text}")
                    
                    # Extract numeric value and currency type from the h3 text
                    import re
                    # Look for patterns like "2500 coins" or "100 dollars"
                    if "coins" in prize_text.lower():
                        currency_type = "Coins"
                        numeric_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d+)?)', prize_text)
                        if numeric_match:
                            # Remove commas and convert to float
                            prize_value = float(numeric_match.group(1).replace(',', ''))
                        print(f"Value: {prize_value} ({currency_type})")
                    elif "dollars" in prize_text.lower() or "$" in prize_text:
                        currency_type = "Dollars"
                        numeric_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d+)?)', prize_text)
                        if numeric_match:
                            # Remove commas and convert to float
                            prize_value = float(numeric_match.group(1).replace(',', ''))
                        print(f"Value: ${prize_value} ({currency_type})")
                    else:
                        print("Could not determine currency type from prize text")
                        
                except Exception as e:
                    print(f"Could not find or parse prize information: {e}")
                
                # Find and click the "Claim Prize" button
                try:
                    claim_button = article.find_element(By.CSS_SELECTOR, "button.mui-i6q8cd.tss-zagdkk-core-md-fill-roundCorners")
                    
                    # Check if button is enabled
                    is_disabled = claim_button.get_attribute("disabled")
                    btn_text = claim_button.text.strip()
                    
                    print(f"Button text: '{btn_text}'")
                    
                    if not is_disabled and btn_text == "Claim Prize":
                        try:
                            # Scroll the button into view
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", claim_button)
                            time.sleep(0.5)
                            
                            # Try regular click first
                            claim_button.click()
                            print("✓ Successfully clicked 'Claim Prize' button!")
                            
                            # Add to totals
                            total_claimed_value += prize_value
                            claimed_count += 1
                            
                            time.sleep(1)  # Wait between clicks
                            
                        except Exception as e:
                            # If regular click fails, try JavaScript click
                            print(f"Regular click failed ({e}), trying JavaScript click...")
                            driver.execute_script("arguments[0].click();", claim_button)
                            print("✓ Successfully clicked 'Claim Prize' button using JavaScript!")
                            
                            # Add to totals
                            total_claimed_value += prize_value
                            claimed_count += 1
                            
                            time.sleep(1)  # Wait between clicks
                    else:
                        print(f"⚠ Button is disabled or text doesn't match: '{btn_text}'")
                        
                except Exception as e:
                    print(f"⚠ Could not find or click 'Claim Prize' button: {e}")
                    
            except Exception as e:
                print(f"⚠ Error processing prize {i}: {e}")
        
        # Summary
        print(f"\n" + "="*70)
        print("  CLAIMING SUMMARY")
        print("="*70)
        print(f"Total prizes processed: {len(prize_articles)}")
        print(f"Successfully claimed: {claimed_count}")
        print(f"Total value claimed: ${total_claimed_value:.2f}")
        print("="*70)
        
except Exception as e:
    print(f"\n⚠ Error while trying to claim individual prizes: {e}")
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
import signal
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Function to close all Chrome processes
def close_chrome_processes():
    # Get the list of Chrome processes
    chrome_processes = subprocess.check_output(['tasklist', '/FI', 'IMAGENAME eq chrome.exe']).decode('utf-8').splitlines()

    # Close each Chrome process
    for process in chrome_processes:
        if 'chrome.exe' in process:
            pid = int(process.split()[1])
            os.kill(pid, signal.SIGTERM)

# Close all existing Chrome tabs
close_chrome_processes()

PROFILE_PATH = os.getenv("PROFILE_PATH")
PROFILE_NAME = os.getenv("PROFILE_NAME")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")


# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={PROFILE_PATH}")
options.add_argument(f"--profile-directory={PROFILE_NAME}")
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


# Allow the page to load
time.sleep(6)

# Initialize the counter for free tournaments
free_tourneys = 0

# Locate all tournament elements
tournament_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tournament row"]')

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

# Close the browser after some time
time.sleep(10)
driver.quit()

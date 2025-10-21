# main.py
import os
import re
import json
import time
from selenium import webdriver
from bid_generator import generate_bid
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BIDS_FILE = "submitted_bids.json"
SKIPPED_FILE = "skipped_bids.json"
exclude_keywords = ["wordpress", "woocommerce", "template", "shopify", "wix"]

# --- configure Selenium ---
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def load_skipped_bids():
    """Load skipped bids."""
    if os.path.exists(SKIPPED_FILE):
        with open(SKIPPED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_skipped_bids(skipped):
    """Save skipped bids."""
    with open(SKIPPED_FILE, "w", encoding="utf-8") as f:
        json.dump(skipped, f, ensure_ascii=False, indent=4)

def mark_skipped(project, reason):
    """Mark a project as skipped permanently."""
    skipped = load_skipped_bids()
    title = project.get("title", "Unknown").strip()
    if title not in skipped:
        skipped[title] = {
            "title": project.get("title", "N/A"),
            "link": project.get("link", ""),
            "budget": project.get("budget", "N/A"),
            "reason": reason,
            "description": project.get("description", "N/A"),
            "skills": project.get("skills", [])
        }
        save_skipped_bids(skipped)

def get_total_bids():
    """Return total number of unique bids placed (cached in submitted_bids.json)."""
    bids = load_submitted_bids()
    return len(bids)

def print_bid_stats(session_count=0):
    """Print total and session bid counts."""
    total_bids = get_total_bids()
    print(f"📈 Total bids placed so far: {total_bids} | Current session: {session_count}")

def load_submitted_bids():
    """Load already submitted bids from local JSON."""
    if os.path.exists(BIDS_FILE):
        with open(BIDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_submitted_bids(bids):
    """Save updated bids to local JSON."""
    with open(BIDS_FILE, "w", encoding="utf-8") as f:
        json.dump(bids, f, ensure_ascii=False, indent=4)

def get_min_budget(budget_str):
    """
    Extract the lowest numeric value from a budget string.
    Example: 'Budget £10 – 20 GBP' -> 10
    """
    # Find all numbers in the string
    numbers = re.findall(r'\d+', budget_str.replace(',', ''))
    if numbers:
        # Return the minimum as integer
        return int(numbers[0])  # first number is usually the lowest in these strings
    return 0  # fallback if no number found

def login_freelancer(email: str, password: str):
    driver.get("https://www.freelancer.com/login")
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return document.readyState") == "complete")
    try:
        driver.find_element(By.ID, "emailOrUsernameInput").send_keys(email)
        driver.find_element(By.ID, "passwordInput").send_keys(password)
        login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(normalize-space(.), 'Log in') or contains(normalize-space(.), 'Log In')]"
        ))
    )
    
        # Click the button
        login_button.click()
        print("✅ Login successfully!")
        time.sleep(6)  # wait for login to complete
    except Exception as e:
        print("❌ Login failed!:", e)
        print(driver.page_source[:1000])  # print first 1000 chars for debuggingas Freelancer changes; these are placeholders

def find_projects():
    search_url = "https://www.freelancer.in/search/projects?projectLanguages=en&projectSkills=9,13,92,263,292,439,500,913,1031,1092,1093,2165,2376,2801,2833,2916,2935,2940,2966,2986"
    driver.get(search_url)
    
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(
            lambda d: d.find_elements(By.CLASS_NAME, "ProjectCard") or
                      d.find_elements(By.CSS_SELECTOR, "ul.search-result-list li")
        )
    except:
        print("⚠️ No projects found on the page.")
        return []

    # Auto-scroll
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            wait.until(lambda d: driver.execute_script("return document.body.scrollHeight") > last_height)
        except:
            break
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    projects = []

    # --- Old format (ProjectCard) ---
    old_cards = driver.find_elements(By.CLASS_NAME, "ProjectCard")
    for c in old_cards:
        try:
            title_el = c.find_element(By.CSS_SELECTOR, ".Title-text")
            link_el = c.find_element(By.XPATH, ".//ancestor::a[1]")
            title = title_el.text.strip()
            link = link_el.get_attribute("href")

            try:
                budget_el = c.find_element(By.CSS_SELECTOR, ".BudgetUpgradeWrapper-budget .text-foreground")
                budget = budget_el.text.strip()
            except:
                budget = "N/A"

            try:
                desc_el = c.find_element(By.CSS_SELECTOR, "p[data-margin-bottom]")
                description = desc_el.get_attribute("innerText").split("\n")[0].strip()
            except:
                description = ""

            try:
                skill_els = c.find_elements(By.CSS_SELECTOR, ".SkillsWrapper .Content")
                skills = [s.text.strip() for s in skill_els if s.text.strip()]
            except:
                skills = []

            # Combine title + skills for filtering
            title_clean = title.lower().strip()
            skills_clean = [s.lower().strip() for s in skills if s.strip()]
            combined_text = " ".join([title_clean] + skills_clean)

            skip_project = False
            for keyword in exclude_keywords:
                if keyword in combined_text:
                    print(f"❌ Skipping project (excluded by filter): {title} (matched: {keyword})")
                    skip_project = True
                    break

                
            if skip_project:
                continue  # Skip this project entirely
            
            projects.append({
                "title": title,
                "link": link,
                "budget": budget,
                "description": description,
                "skills": skills,
            })
        except:
            continue

    # --- New format (search-result-list) ---
    new_cards = driver.find_elements(By.CSS_SELECTOR, "ul.search-result-list li")
    for c in new_cards:
        try:
            title_el = c.find_element(By.CSS_SELECTOR, ".info-card-title a")
            title = title_el.text.strip()
            link = title_el.get_attribute("href")
            
            try:
                budget_span = c.find_element(By.CSS_SELECTOR, ".info-card-price span")
                budget = budget_span.text.strip() if budget_span else "N/A"
            except:
                budget = "N/A"

            try:
                description = c.find_element(By.CSS_SELECTOR, ".info-card-description").text.strip()
            except:
                description = ""

            try:
                skill_els = c.find_elements(By.CSS_SELECTOR, ".info-card-skills span")
                skills = [s.text.strip() for s in skill_els if s.text.strip()]
            except:
                skills = []

            # Filter using exclude_keywords
            title_clean = title.lower().strip()
            skills_clean = [s.lower().strip() for s in skills if s.strip()]
            combined_text = " ".join([title_clean] + skills_clean)

            skip_project = False
            for keyword in exclude_keywords:
                if keyword in combined_text:
                    print(f"❌ Skipping project (excluded by filter): {title} (matched: {keyword})")
                    skip_project = True
                    break
                
            if skip_project:
                continue  # Skip this project entirely
            
            projects.append({
                "title": title,
                "link": link,
                "budget": budget,
                "description": description,
                "skills": skills,
            })
        except:
            continue

    finalProjects = []
    submitted_bids = load_submitted_bids()
    skipped_bids = load_skipped_bids()
    for p in projects:
        pTitle = p.get("title", "N/A")
        if pTitle in submitted_bids:
            mark_skipped(p, "Already bid previously")
            return False
        elif pTitle in skipped_bids:
            return False
        else:
            finalProjects.append(p)

    print(f"🔍 Found {len(finalProjects)} projects after filtering.")
    return finalProjects

def prefill_bid(project):
    # Load existing bids
    daysState = True
    submitted_bids = load_submitted_bids()
    skipped_bids = load_skipped_bids()
    title = project.get("title", "N/A")

    if title in submitted_bids:
        mark_skipped(project, "Already bid previously")
        return False
    elif title in skipped_bids:
        return False

    driver.get(project["link"])
    wait = WebDriverWait(driver, 10)

    # Print project details beautifully
    print("\n" + "="*60)
    print("📌 Project Details")
    print("="*60)
    print(f"Title      : {title}")
    print(f"Budget     : {project.get('budget', 'N/A')}")
    print(f"Description: {project.get('description', 'N/A')}")
    print("="*60 + "\n")

    # Extract full description from page
    try:
        full_desc_el = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "app-project-details-description .ProjectDescription fl-interactive-text .ContentWrapper span")
            )
        )
        full_description = full_desc_el.get_attribute("innerText").strip()
    except:
        full_description = project.get("description", "N/A")

    # Check that all required input fields exist
    try:
        amount_el = wait.until(EC.presence_of_element_located((By.ID, "bidAmountInput")))
        try:
            period_el = driver.find_element(By.ID, "periodInput")
            period_type = "days"
        except:
            weekly_el = driver.find_element(By.ID, "weeklyLimitInput")
            period_type = "hours"
        desc_el = driver.find_element(By.ID, "descriptionTextArea")
    except Exception as e:
        print("⚠️ Proposal restricted!")
        mark_skipped(project, "Cannot bid on this project due to restrictions")
        return False

    min_budget = get_min_budget(project.get("budget", "0"))
    proposal = generate_bid(
        project_title=title,
        project_desc=full_description,
        budget=min_budget
    )

    try:
        # Fill Bid Amount
        driver.execute_script("""
            const input = arguments[0];
            const value = arguments[1];
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, amount_el, min_budget)

        # Fill Period / Weekly
        if period_type == "days":
            days = 5
            period_el.clear()
            period_el.send_keys(str(days))
        else:
            daysState = False
            weekly_el.clear()
            weekly_el.send_keys(str(50))

        # Fill Proposal / Description
        desc_el.clear()
        desc_el.send_keys(proposal)
        
        try:
            time.sleep(1)
            # Wait until the Place Bid button is clickable
            place_bid_btn = WebDriverWait(driver, 10).until( EC.element_to_be_clickable( (By.XPATH, "//fl-button[@fltrackinglabel='PlaceBidButton']//button[contains(text(),'Place Bid')]") ) ) 
            place_bid_btn.click() 
            print(f"✅ Proposal submitted successfully! Budget: {min_budget}, Time: {'5 days' if period_type == "days" else '50 hours'}")

            
            # Save to local JSON
            if daysState:
                submitted_bids[title] = {
                    "title": title,
                    "budget": project.get("budget", "N/A"),
                    "description": project.get("description", "N/A"),
                    "full_description": full_description,
                    "proposal": proposal,
                    "min_budget": min_budget,
                    "days": days,
                    "link": project.get("link", "")
                }
            else:
                submitted_bids[title] = {
                    "title": title,
                    "budget": project.get("budget", "N/A"),
                    "description": project.get("description", "N/A"),
                    "full_description": full_description,
                    "proposal": proposal,
                    "min_budget": min_budget,
                    "hours": 50,
                    "link": project.get("link", "")
                }
            save_submitted_bids(submitted_bids)
            return True
        except Exception as e:
            print("⚠️ Could not click Place Bid button:", e)
            mark_skipped(project, "Could not place bid")
            return False


    except Exception as e:
        print("❌ Proposal skipped successfully!")
        mark_skipped(project, "Unhandled exception during prefill")
        return False


def main():
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PSSWD")
    session_bids = 0

    login_freelancer(EMAIL, PASSWORD)

    while True:  # Loop indefinitely
        print("\n🔄 Fetching new projects...")
        print_bid_stats(session_bids)
        projects = find_projects()

        for p in projects:
            ok = prefill_bid(p)
            if ok:
                session_bids += 1
                print_bid_stats(session_bids)
                time.sleep(1)
                continue

        print("⏱ Waiting 1000ms before checking for new projects...")
        time.sleep(1)


if __name__ == "__main__":
    main()

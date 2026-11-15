cat << 'EOF' > bot.py
import time
import json
import os
from playwright.sync_api import sync_playwright

print("-----------------------------------------")
print("  RAZEN MESS REPORT BOT  ")
print("    Continuous Bot + Proxy & IP Rotation ")
print("-----------------------------------------")

# 1. Load Cookies from cookies.json
COOKIE_FILE = "cookies.json"
if not os.path.exists(COOKIE_FILE):
    default_cookies = [
    {"name": "datr", "value": "z8H5alU8nGZ93LnMM9tFO0UL", "domain": ".facebook.com", "path": "/"},
    {"name": "fr", "value": "06RHVxWHnjrgOiikK.AWe8CYVDiyLFp24VwIhqSUyEBYD8Mhp50K2aVy0btNpUTwlb_Cc.Bq-cHP..AAA.0.0.Bq-cH2.AWclRo8xcndocnJdGLTfFDrAUeY", "domain": ".facebook.com", "path": "/"},
    {"name": "vpd", "value": "v1%3B893x486x2.2222222222222223", "domain": ".facebook.com", "path": "/"},
    {"name": "xs", "value": "23%3AGMPODyTGnlc7dQ%3A2%3A1794753009%3A-1%3A-1", "domain": ".facebook.com", "path": "/"},
    {"name": "fbl_st", "value": "100431442%3BT%3A29912550", "domain": ".facebook.com", "path": "/"},
    {"name": "locale", "value": "en_US", "domain": ".facebook.com", "path": "/"},
    {"name": "m_pixel_ratio", "value": "1", "domain": ".facebook.com", "path": "/"},
    {"name": "c_user", "value": "61596716423543", "domain": ".facebook.com", "path": "/"},
    {"name": "pas", "value": "61596716423543%3AAlJT6YEtNR", "domain": ".facebook.com", "path": "/"},
    {"name": "sb", "value": "z8H5auwfdeMbzdNfcK1lpvEo", "domain": ".facebook.com", "path": "/"},
    {"name": "wd", "value": "486x1080", "domain": ".facebook.com", "path": "/"},
    {"name": "wl_cbv", "value": "v2%3Bclient_version%3A3357%3Btimestamp%3A1794753015", "domain": ".facebook.com", "path": "/"}
]
    with open(COOKIE_FILE, "w") as f:
        json.dump(default_cookies, f, indent=4)

try:
    with open(COOKIE_FILE, "r") as f:
        cookies_list = json.load(f)
    print(f"[✓] Successfully loaded cookies from {COOKIE_FILE}")
except Exception as e:
    print(f"[-] Error loading {COOKIE_FILE}: {e}")
    exit(1)

# 2. Load Targets from targets.txt
TARGET_FILE = "targets.txt"
if not os.path.exists(TARGET_FILE):
    default_targets = [
        "https://m.facebook.com/profile.php?id=61595483787104"
    ]
    with open(TARGET_FILE, "w") as f:
        f.write("\n".join(default_targets))

targets = []
with open(TARGET_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            if line.isdigit():
                url = f"https://m.facebook.com/profile.php?id={line}"
            elif "facebook.com" in line:
                url = line.replace("www.facebook.com", "m.facebook.com").replace("m.n.facebook.com", "m.facebook.com")
                if not url.startswith("http"):
                    url = "https://" + url
            else:
                url = f"https://m.facebook.com/profile.php?id={line}"
            targets.append(url)

print(f"[+] Loaded {len(targets)} target(s) from {TARGET_FILE}")

# 3. Load Proxies from proxies.txt (Optional)
PROXY_FILE = "proxies.txt"
if not os.path.exists(PROXY_FILE):
    with open(PROXY_FILE, "w") as f:
        f.write("# Add your proxies here (Format: http://ip:port or http://username:password@ip:port)\n")

proxies_list = []
if os.path.exists(PROXY_FILE):
    with open(PROXY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                proxies_list.append(line)

print(f"[+] Loaded {len(proxies_list)} proxy/proxies from {PROXY_FILE}")

def run_bot():
    with sync_playwright() as p:
        loop_count = 1
        while True:
            print(f"\n=========================================")
            print(f" >>> STARTING PROXY ROTATION ROUND [{loop_count}] <<<")
            print(f"=========================================")
            
            current_proxy = None
            if proxies_list:
                proxy_url = proxies_list[(loop_count - 1) % len(proxies_list)]
                current_proxy = {"server": proxy_url}
                print(f"[+] Using Proxy for this round: {proxy_url}")
            else:
                print("[-] No proxies found in proxies.txt. Running on direct connection.")

            print(f"\n[+] Launching browser in Mobile View...")
            
            browser_kwargs = {"headless": True, "args": ['--no-sandbox', '--disable-setuid-sandbox']}
            if current_proxy:
                browser_kwargs["proxy"] = current_proxy
                
            browser = p.chromium.launch(**browser_kwargs)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                viewport={'width': 390, 'height': 844}
            )
            
            try:
                context.add_cookies(cookies_list)
                print("[✓] Cookies injected successfully into browser session!")
            except Exception as e:
                print(f"[-] Cookie injection warning: {e}")
                
            page = context.new_page()
            
            for index, target_url in enumerate(targets, 1):
                print(f"\n-----------------------------------------")
                print(f" Processing Target [{index}/{len(targets)}]: {target_url}")
                print(f"-----------------------------------------")
                
                try:
                    page.goto(target_url, timeout=40000)
                    time.sleep(5)
                    
                    if "login" in page.url or "checkpoint" in page.url:
                        print("[-] CRITICAL: Cookie appears to be DEAD or flagged! Please update your cookies.json.")
                        browser.close()
                        return
                    
                    try:
                        not_now_btn = page.locator('text=/Not now|Close/i').first
                        if not_now_btn.is_visible(timeout=3000):
                            not_now_btn.click()
                            print("[✓] Dismissed mobile banner successfully.")
                            time.sleep(2)
                    except Exception as ex:
                        print(f"[-] Banner dismiss notice: {ex}")

                    print("[+] Step 1: Clicking mobile options / three-dots button...")
                    page.evaluate("""() => {
                        const allEls = Array.from(document.querySelectorAll('a, button, div[role="button"], span[role="button"]'));
                        for (let el of allEls) {
                            const txt = el.innerText.trim();
                            const aria = el.getAttribute('aria-label') || '';
                            const lowTxt = (txt + ' ' + aria).toLowerCase();
                            if (lowTxt.includes('more') || lowTxt.includes('option') || lowTxt.includes('report') || lowTxt.includes('...')) {
                                el.click();
                                return true;
                            }
                        }
                        return false;
                    }""")
                    
                    time.sleep(3)
                    print("[+] Step 2: Clicking 'Find support or report' option...")
                    try:
                        report_opt = page.locator('text=/Find support or report|Report profile|Report|Give feedback/i').first
                        if report_opt.is_visible(timeout=4000):
                            report_opt.click()
                            print("[✓] Successfully clicked report option!")
                    except Exception as ex:
                        print(f"[-] Report search notice: {ex}")

                    time.sleep(4)
                    print("[+] Step 3: Selecting initial report category...")
                    try:
                        reason_opt = page.locator('text=/Fake account|Pretending to be someone|Something else|Bullying or harassment/i').first
                        if reason_opt.is_visible(timeout=3000):
                            reason_opt.click()
                            print("[✓] Selected initial report category.")
                            time.sleep(2)
                    except Exception as ex:
                        print(f"[-] Category selection notice: {ex}")

                    time.sleep(3)
                    print("[+] Step 4: Selecting specific sub-option / reason...")
                    try:
                        sub_opt = page.locator('text=/Bullying or harassment|Threatening to share|Sexual exploitation|Human trafficking/i').first
                        if sub_opt.is_visible(timeout=3000):
                            sub_opt.click()
                            print("[✓] Selected specific sub-option.")
                            time.sleep(3)
                    except Exception as ex:
                        print(f"[-] Sub-option selection notice: {ex}")

                    for step_name in ["Next", "Submit", "Done"]:
                        try:
                            btn = page.locator(f'text=/{step_name}/i').first
                            if btn.is_visible(timeout=3000):
                                btn.click()
                                print(f"[✓] Clicked '{step_name}' button successfully.")
                                time.sleep(3)
                        except Exception as e:
                            print(f"[-] Notice for '{step_name}': {e}")

                    print(f"[✓] Successfully submitted report round for target {index}!")
                    time.sleep(5)
                    
                except Exception as e:
                    print(f"[-] Error processing target {target_url}: {e}")
            
            browser.close()
            print(f"\n[+] Completed Round {loop_count} with Proxy Rotation. Waiting 10 seconds before next wave...")
            loop_count += 1
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
    print("\n[+] Proxy-Rotated Continuous Reporting Stopped, Bruv! 🚀")
EOF
import time
import json
import os
import random
from playwright.sync_api import sync_playwright

print("-----------------------------------------")
print("  RAZEN MESS REPORT BOT V2  ")
print("      [ SNIPER MODE ]   ")
print("-----------------------------------------")

COOKIE_FILE = "cookies.json"
if not os.path.exists(COOKIE_FILE):
    default_cookies = [
    {"name": "datr", "value": "WC38asQhNeNLyM1ljF6Q3d2k", "domain": ".facebook.com", "path": "/"},
    {"name": "fr", "value": "0JhzXL5M4GmuNUq3D.AWewFgTwm3jb-ImvBfFiaQ3tgEhb2thSTHxMD3x0p9NBh8OY-xg.Bq_C1Y..AAA.0.0.Bq_C1o.AWfSKA3ixalZU8Z1G2h5FmS2xAA", "domain": ".facebook.com", "path": "/"},
    {"name": "vpd", "value": "v1%3B893x486x2.2222222222222223", "domain": ".facebook.com", "path": "/"},
    {"name": "xs", "value": "8%3AX4LKM2u80jc5tQ%3A2%3A1794911587%3A-1%3A-1", "domain": ".facebook.com", "path": "/"},
    {"name": "fbl_st", "value": "101728021%3BT%3A29915193", "domain": ".facebook.com", "path": "/"},
    {"name": "locale", "value": "en_US", "domain": ".facebook.com", "path": "/"},
    {"name": "m_pixel_ratio", "value": "1", "domain": ".facebook.com", "path": "/"},
    {"name": "c_user", "value": "61596760136594", "domain": ".facebook.com", "path": "/"},
    {"name": "pas", "value": "61596760136594%3AM3W5UJze6A", "domain": ".facebook.com", "path": "/"},
    {"name": "sb", "value": "WC38ankFMWMh09A8BNXbqQy3", "domain": ".facebook.com", "path": "/"},
    {"name": "wd", "value": "486x1080", "domain": ".facebook.com", "path": "/"},
    {"name": "wl_cbv", "value": "v2%3Bclient_version%3A3359%3Btimestamp%3A1794911592", "domain": ".facebook.com", "path": "/"}
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

TARGET_FILE = "targets.txt"
if not os.path.exists(TARGET_FILE):
    default_targets = [
        "https://www.facebook.com/JotiApu1"
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

def human_delay(min_sec=3, max_sec=6):
    time.sleep(random.uniform(min_sec, max_sec))

def run_bot():
    with sync_playwright() as p:
        loop_count = 1
        while True:
            print(f"\n=========================================")
            print(f" >>> SNIPER ROUND [{loop_count}] - SHARP MODE <<<")
            print(f"=========================================")
            
            current_proxy = None
            if proxies_list:
                proxy_url = proxies_list[(loop_count - 1) % len(proxies_list)]
                current_proxy = {"server": proxy_url}
                print(f"[+] Active Proxy IP: {proxy_url}")
            else:
                print("[-] Running on Direct Connection (No proxies found).")

            browser_kwargs = {
                "headless": True, 
                "args": [
                    '--no-sandbox', 
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-infobars'
                ]
            }
            if current_proxy:
                browser_kwargs["proxy"] = current_proxy
                
            browser = p.chromium.launch(**browser_kwargs)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                viewport={'width': 390, 'height': 844},
                device_scale_factor=3,
                is_mobile=True,
                has_touch=True
            )
            
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.navigator.chrome = { runtime: {} };
            """)
            
            try:
                context.add_cookies(cookies_list)
                print("[✓] Cookies injected securely!")
            except Exception as e:
                print(f"[-] Cookie injection error: {e}")
                
            page = context.new_page()
            
            for index, target_url in enumerate(targets, 1):
                print(f"\n-----------------------------------------")
                print(f" Processing Target [{index}/{len(targets)}]: {target_url}")
                print(f"-----------------------------------------")
                
                try:
                    page.goto(target_url, timeout=50000, wait_until="domcontentloaded")
                    human_delay(3, 5)
                    
                    if "login" in page.url or "checkpoint" in page.url:
                        print("[-] CRITICAL: Session expired or account flagged!")
                        browser.close()
                        return
                    
                    # Dismiss banner safely
                    try:
                        banner = page.locator('text=/Not now|Close/i').first
                        if banner.is_visible(timeout=2000):
                            banner.click()
                            human_delay(1, 2)
                    except:
                        pass

                    print("[+] Step 1: Clicking profile options (...)")
                    clicked_options = page.evaluate("""() => {
                        const candidates = Array.from(querySelectorAllSafe('a, button, div[role="button"], span[role="button"]'));
                        for (let el of candidates) {
                            const txt = el.innerText.trim().toLowerCase();
                            const aria = (el.getAttribute('aria-label') || '').toLowerCase();
                            if (txt.includes('...') || txt.includes('more') || aria.includes('more') || aria.includes('options')) {
                                el.click();
                                return true;
                            }
                        }
                        // Fallback query for common FB mobile three dots
                        const dots = document.querySelector('i[data-visualcompletion="css-img"]');
                        if (dots) { dots.click(); return true; }
                        return false;
                    }""")
                    
                    if not clicked_options:
                        # Fallback direct selector click
                        try:
                            page.locator("div[aria-label='More'], div[aria-label='Options']").first.click(timeout=3000)
                        except:
                            pass

                    human_delay(3, 4)
                    print("[+] Step 2: Selecting 'Find support or report'")
                    try:
                        page.locator('text=/Find support or report|Report profile|Report/i').first.click(timeout=4000)
                        print("[✓] Support menu clicked.")
                    except Exception as ex:
                        print(f"[-] Support menu notice: {ex}")

                    human_delay(3, 4)
                    print("[+] Step 3: Choosing violation category")
                    try:
                        page.locator('text=/Fake account|Pretending to be someone|Bullying or harassment|Something else/i').first.click(timeout=4000)
                        print("[✓] Category selected.")
                    except Exception as ex:
                        print(f"[-] Category notice: {ex}")

                    human_delay(3, 4)
                    print("[+] Step 4: Confirming sub-option")
                    try:
                        page.locator('text=/Bullying or harassment|Threatening to share|Hate speech/i').first.click(timeout=3000)
                    except:
                        pass

                    for action_btn in ["Next", "Submit", "Done"]:
                        human_delay(2, 3)
                        try:
                            btn = page.locator(f'text=/{action_btn}/i').first
                            if btn.is_visible(timeout=2500):
                                btn.click()
                                print(f"[✓] Clicked button: {action_btn}")
                        except:
                            pass

                    print(f"[✓] Successfully executed sniper target [{index}]!")
                    human_delay(4, 6)
                    
                except Exception as e:
                    print(f"[-] Error processing target: {e}")
            
            browser.close()
            print(f"\n[+] Completed Round {loop_count}. Cooling down for 10 seconds...")
            loop_count += 1
            human_delay(8, 12)

if __name__ == "__main__":
    def querySelectorAllSafe(sel) {
        return document.querySelectorAll(sel);
    }
    run_bot()
    print("\n[+] Sniper Bot Finished Safely, BOSS! 🚀")
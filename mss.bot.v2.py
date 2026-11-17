import time
import json
import os
import random
from playwright.sync_api import sync_playwright

# ANSI Color Codes for Terminal
CYAN = "\033[96m"
PINK = "\033[95m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

banner = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   {PINK}██████╗     █████╗ ███████╗ ███████╗███╗     ██╗{CYAN}                     ║
║   {PINK}██╔══██╗██╔══██╗╚══███╔  ██╔════╝████╗   ██║{CYAN}                     ║
║   {PINK}██████╔╝███████║  ███╔╝     █████╗     ██╔██╗ ██║{CYAN}                     ║
║   {PINK}██╔══██╗██╔══██║ ███╔╝      ██╔══╝     ██║╚██╗██║{CYAN}                    ║
║   {PINK}██║     ██║██║     ██║███████╗███████╗██║ ╚████║{CYAN}                     ║
║   {PINK}╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝{CYAN}  {YELLOW}[ MESS REPORT BOT ]{CYAN}    ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  {GREEN}⚡ TOOL     :{WHITE} RAZEN MESS REPORT SYSTEM                           {CYAN}║
║  {GREEN}🎯 MODE     :{WHITE} [ FAST ENGINE ]                 {CYAN}║
╚══════════════════════════════════════════════════════════════════╝{RESET}
"""

print(banner)

COOKIE_FILE = "cookies.json"
if not os.path.exists(COOKIE_FILE):
    default_cookies = [
    {"name": "ps_l", "value": "1", "domain": ".facebook.com", "path": "/"},
    {"name": "datr", "value": "4B78amkJJg5QjvkfDVtk3LsI", "domain": ".facebook.com", "path": "/"},
    {"name": "fr", "value": "12hKQAxc85ZwtBe0s.AWd1qHkPg2MtLzV9uukGXMdxLjbUllXaE4yudMZ9LqYq-1rmyzw.Bq_CGU..AAA.0.0.Bq_CIV.AWedb07KiRtQjjXwyOwA1NeVhKc", "domain": ".facebook.com", "path": "/"},
    {"name": "vpd", "value": "v1%3B893x486x2.2222222222222223", "domain": ".facebook.com", "path": "/"},
    {"name": "xs", "value": "40%3A7cFHnXk8vNpcLQ%3A2%3A1794908486%3A-1%3A-1%3A%3AAc28GgjuvG_2yISf61eC1tkY1elzjSn9o4Sfa3s-Dg", "domain": ".facebook.com", "path": "/"},
    {"name": "fbl_st", "value": "101436978%3BT%3A29915144", "domain": ".facebook.com", "path": "/"},
    {"name": "locale", "value": "en_US", "domain": ".facebook.com", "path": "/"},
    {"name": "m_pixel_ratio", "value": "1", "domain": ".facebook.com", "path": "/"},
    {"name": "c_user", "value": "61596541506476", "domain": ".facebook.com", "path": "/"},
    {"name": "presence", "value": "C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1794908570731%2C%22v%22%3A1%7D", "domain": ".facebook.com", "path": "/"},
    {"name": "dpr", "value": "2.2222222222222223", "domain": ".facebook.com", "path": "/"},
    {"name": "pas", "value": "61596716423543%3AG0hdoqIzbF%2C61596541506476%3AHxGzKBPKLl", "domain": ".facebook.com", "path": "/"},
    {"name": "ps_n", "value": "1", "domain": ".facebook.com", "path": "/"},
    {"name": "sb", "value": "4B78ah109cRIIUtEr-iCjTB9", "domain": ".facebook.com", "path": "/"},
    {"name": "wd", "value": "486x893", "domain": ".facebook.com", "path": "/"},
    {"name": "wl_cbv", "value": "v2%3Bclient_version%3A3359%3Btimestamp%3A1794908693", "domain": ".facebook.com", "path": "/"}
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
            C = "\033[96m"  # Cyan
    P = "\033[95m"  # Pink
    Y = "\033[93m"  # Yellow
    W = "\033[97m"  # White
    B = "\033[1m"   # Bold
    R = "\033[0m"   # Reset

    print(f"\n{C}{B}╭─────────────────────────────────────────────╮ {R}")
    print(f"{C}{B}   │  {P}>>> {W}𝐒𝐍𝐈𝐏𝐄𝐑 𝐑𝐎𝐔𝐍𝐃 {Y}[{loop_count}] {C}- {P}𝐒𝐇𝐀𝐑𝐏 𝐌𝐎𝐃𝐄 <<<  {C}{B}│{R}")
    print(f"{C}{B}   ╰─────────────────────────────────────────────╯{R}")
            
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
    # Terminal Colors
C = "\033[96m"  # Cyan
G = "\033[92m"  # Green
Y = "\033[93m"  # Yellow
P = "\033[95m"  # Pink
W = "\033[97m"  # White
B = "\033[1m"   # Bold
R = "\033[0m"   # Reset

print(f"""
{C}{B}╭────────────────────────────────────────╮
│  {G}✔ 𝐒𝐓𝐀𝐓𝐔𝐒 : {W}𝐌𝐈𝐒𝐒𝐈𝐎𝐍 𝐀𝐂𝐂𝐎𝐌𝐏𝐋𝐈𝐒𝐇𝐄𝐃        {C}│
├────────────────────────────────────────┤
│  {P}⚡ 𝐒𝐧𝐢𝐩𝐞𝐫 𝐁𝐨𝐭 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝 𝐒𝐚𝐟𝐞𝐥𝐲, 𝐁𝐨𝐬𝐬! 🚀 {C}│
│  {Y}   [ 𝐑𝐀𝐙𝐄𝐍 𝐌𝐄𝐒𝐒 𝐁𝐎𝐓 • 𝐀𝐋𝐋 𝐃𝐎𝐍𝐄 ]         {C}│
╰────────────────────────────────────────╯{R}
""")
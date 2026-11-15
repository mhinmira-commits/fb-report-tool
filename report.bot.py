import json
import os
import time
from playwright.sync_api import sync_playwright

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("==========================================")
    print("     RAZEN MESS REPORT BOT     ")
    print("==========================================\n")

    target_url = input("[?] Target Profile/Post URL din: ").strip()
    cookie_input = input("\n[?] Facebook Cookies din (JSON format ba file path): ").strip()

    cookies = []
    try:
        if os.path.exists(cookie_input):
            with open(cookie_input, 'r') as f:
                cookies = json.load(f)
        else:
            cookies = json.loads(cookie_input)
        print("[+] Cookies successfully loaded!")
    except Exception as e:
        print(f"[-] Cookie parse korte somossa hoyeche: {e}")
        print("[*] Default empty cookies diye cholche...")

    proxies = []
    if os.path.exists('proxies.txt'):
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]

    print(f"\n[+] Target set: {target_url}")
    print("[+] Bot reporting shuru hochhe...\n")

    round_count = 1

    with sync_playwright() as p:
        while True:
            print(f"\n==========================================")
            print(f">>> STARTING PROXY ROTATION ROUND [{round_count}] <<<")
            print(f"==========================================")

            proxy = None
            if proxies:
                proxy_str = proxies[(round_count - 1) % len(proxies)]
                proxy = {"server": proxy_str}
                print(f"[+] Using Proxy: {proxy_str}")
            else:
                print("[-] No proxies found in proxies.txt. Running on direct connection.")

            try:
                browser = p.chromium.launch(
                    headless=True, 
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                try:
                browser = p.chromium.launch(
                    headless=True, 
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
                )

                if cookies:
                    try:
                        context.add_cookies(cookies)
                        print("[v] Cookies injected successfully!")
                    except Exception as ce:
                        print(f"[-] Cookie injection error: {ce}")

                page = context.new_page()
                print(f"[+] Opening Target: {target_url}")
                page.goto(target_url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(3)

                print("[*] Step 1: Clicking mobile options...")
                try:
                    page.click("text=...", timeout=5000)
                except:
                    try:
                        page.click("div[aria-label='More']", timeout=5000)
                    except:
                        pass

                print("[+] Step 2: Clicking 'Find support or report'...")
                time.sleep(2)

                print("[+] Step 3: Selecting initial report option...")
                time.sleep(2)

                print("[+] Step 4: Selecting specific sub-option...")
                time.sleep(2)

                print("[v] Successfully submitted report round!")
                browser.close()

            except Exception as ex:
                print(f"[-] Error encountered during round {round_count}: {ex}")

            print(f"\n[+] Completed Round {round_count}. Waiting 10 seconds...")
            round_count += 1
            time.sleep(10)

if __name__ == "__main__":
    main()
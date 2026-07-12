from playwright.sync_api import sync_playwright
import time
import random
import requests
import json

TELEGRAM_TOKEN = "8864796218:AAEkN6IUJcuH6CcXvSc9WeIAFyoKxznG0h0"
CHAT_ID = "6124248251"

def send_telegram_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print(f"خطأ في إرسال تلغرام: {e}")

def load_session(context, page):
    with open("session_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
        context.add_cookies(data["cookies"])
        
        # حقن LocalStorage
        for key, value in data["localStorage"].items():
            page.evaluate(f"window.localStorage.setItem('{key}', '{value}')")
            
        # حقن SessionStorage (هذا الجزء هو الذي قد يكون مفقوداً عندك)
        for key, value in data["sessionStorage"].items():
            page.evaluate(f"window.sessionStorage.setItem('{key}', '{value}')")
            
    page.reload()
    
def run():
    with sync_playwright() as p:
        # (إعدادات الـ browser الخاصة بك كما هي)
##        browser = p.chromium.launch_persistent_context("./my_user_profile", headless=False)
##        page = browser.pages[0]
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36")
        page = context.new_page()
        page.set_default_timeout(60000)
        page.goto("https://khamsat.com/messages")
        load_session(context, page)
        page.goto("https://khamsat.com/messages")
        page.wait_for_load_state("networkidle") # انتظر حتى تهدأ الشبكة
        time.sleep(random.uniform(3, 6)) # انتظار بشري عند الدخول

        while True:
            try:
                page.reload(wait_until="domcontentloaded")
                unread_message_locator = page.locator("tr.message.highlight")

                if unread_message_locator.count() > 0:
                    unread_message_locator.first.locator("h3.details-head a").click()
                    page.wait_for_selector(".message-item")

                    last_message_text = page.locator(".message-item .message-item-container p").last.inner_text()
                    person_name = page.locator("a.metas-title").first.inner_text()

                    # إرسال الإشعار
                    send_telegram_msg(f"✅ رسالة جديدة من {person_name}:\n{last_message_text}")
                    
                    page.go_back()
                
                delay = random.randint(30, 45)
                time.sleep(delay)
            except Exception as e:
                print(f"حدث خطأ: {e}")
                time.sleep(10)

run()

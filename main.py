import re
from playwright.sync_api import Playwright, sync_playwright, expect
import os
from dotenv import load_dotenv
import otp
import scraper
import time

load_dotenv()
username = os.getenv("tuUsername")
password = os.getenv("tuPassword")


def infoMoodle(page):
    print("Login Info Moodle")

    #Seite aufrufen
    page.goto("https://moodle.informatik.tu-darmstadt.de/")

    #Login
    page.get_by_role("link", name="Anmelden").click()
    page.locator("#login-method-idp").get_by_role("link").click()
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(username)
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()
    page.get_by_label("Please select token.").select_option("TOTP41107FF1")
    page.get_by_role("button", name="Next").click()
    page.locator("#fudis_otp_input").click()
    print(otp.getOTP())
    page.locator("#fudis_otp_input").fill(otp.getOTP())
    page.get_by_role("button", name="Validate").click()

    page.wait_for_load_state("networkidle")
    print(f"Info Moodle Loin erfolgreich: {page.title()}")

    return scraper.extractTasks(page, "InfoMoodle")


def uniMoodle(page):
    #Seite aufrufen
    page.goto("https://moodle.tu-darmstadt.de/")

    #Login
    page.get_by_role("link", name="Anmelden").click()
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(username)
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()
    page.get_by_label("Please select token.").select_option("TOTP41107FF1")
    page.get_by_role("button", name="Next").click()
    page.locator("#fudis_otp_input").click()
    print(otp.getOTP())
    page.locator("#fudis_otp_input").fill(otp.getOTP())
    page.get_by_role("button", name="Validate").click()

    page.wait_for_load_state("networkidle")
    print(f"Uni Moodle Loin erfolgreich: {page.title()}")

    return scraper.extractTasks(page, "UniMoodle")


def run():
    allTasks = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        #UniMoodle---------------------------
        contextUni = browser.new_context()
        pageUni = contextUni.new_page()

        try:
            allTasks.extend(uniMoodle(pageUni))
        finally:
            contextUni.close()
        
        time.sleep(30)

        #InfoMoodle---------------------------
        contextInfo = browser.new_context()
        pageInfo = contextInfo.new_page()

        try:
            allTasks.extend(infoMoodle(pageInfo))
        finally:
            contextInfo.close()

        browser.close()
    
    print("\n----------TASKS-----------")
    for t in allTasks:
        print(f"{t['uni']} | {t['title']} | {t['deadline']} | {t['modul']}")
        


if __name__ == "__main__":
    run()
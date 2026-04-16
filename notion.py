import os
import requests
from dotenv import load_dotenv
import re
import json

load_dotenv()
NOTION_TOKEN = os.getenv("notionSecret")
NOTION_ID = os.getenv("notionID")
NOTION_VERSION = os.getenv("notionVersion")

def getDataBaseStructure(headers):
    response = requests.post(
        f"https://api.notion.com/v1/data_sources/{getDataSourceID(headers)}/query", headers=headers
    ).json()

    first_page = response["results"][0]
    print(first_page)
    for prop_name, prop_value in first_page["properties"].items():
        print(f"{prop_name}: {prop_value['type']}")

def getDataSourceID(headers):
    data_source_id = requests.get(f"https://api.notion.com/v1/databases/{NOTION_ID}", headers=headers).json()["data_sources"][0]["id"]
    return data_source_id

def getOldTasks(headers):
    oldTasks = []
    data_source_id = getDataSourceID(headers)
    response = requests.post(
        f"https://api.notion.com/v1/data_sources/{data_source_id}/query", headers=headers
    )

    for page in response.json()["results"]:
        props = page["properties"]

        title_list = props.get("Task", {}).get("title", [])
        title = title_list[0]["plain_text"] if title_list else "Unbenannt"

        deadline_list = props.get("Deadline", {}).get("date")
        deadline = deadline_list.get("start") if deadline_list else "Keine Deadline"

        modul_list = props.get("Modul", {}).get("relation", [])
        modul = modul_list[0]["id"] if modul_list else "Kein Modul"

        oldTasks.append({
            "title": title,
            "deadline": deadline,
            "modul": modul
        })


    return oldTasks


def checkExisiting(headers, newTask):
    oldTasks = getOldTasks(headers)
    newTitle = newTask["title"]
    newModul = newTask["modul"]

    for t in oldTasks:
        if newTitle == t["title"] and newModul == t["modul"]:
            return True
    return False


def getModulID(modulFromScraper):
    with open("config.json") as f:
        mapping = json.load(f)
    return mapping.get(modulFromScraper)




def addTasks(tasks):
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Notion-Version": NOTION_VERSION,
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # dsID = getDataSourceID(headers)
    oldTasks = getOldTasks(headers)

    for t in tasks:
        if checkExisiting(headers, t):
            continue

        title = t["title"]
        deadline = t["deadline"]
        modul = getModulID(t["modul"])
            
        payload = {
                "parent": {
                    "type": "data_source_id",
                    "data_source_id": "1aed2df0-67f4-4e84-a657-f0df45f3387f"
                },
                "properties": {
                    "Task": {"title": [{ "text":{"content": title}}]},
                    "Deadline": {"date":{"start": deadline}},
                    "Modul": {"relation": [{"id": modul}]}
                },
            }

        response = requests.post(url, json=payload, headers=headers)

        # print(response.text)

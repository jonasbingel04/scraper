import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def updateConfig():
    MODUL_DB_ID = os.getenv("modulDbId")
    headers = {
        "Notion-Version": os.getenv("notionVersion"),
        "Authorization": f"Bearer {os.getenv('notionSecret')}"
    }
    url = f"https://api.notion.com/v1/data_sources/{MODUL_DB_ID}/query"
    response = requests.post(url, headers=headers, json={})
    
    if response.status_code != 200:
        print(f"Fehler: {response.status_code}")
        print(response.text)
        return

    pages = response.json().get("results", [])
    module_map = {}
    
    for page in pages:
        pID = page["id"]
        props = page["properties"]

        title = "unbekannt"
        for p in props.values():
            if p["type"] == "title":
                if p["title"]:
                    title = p["title"][0]["plain_text"]
                break
        moodleNameProp = props.get("MoodleName", {}).get("rich_text", [])
        if moodleNameProp:
            moodleName = moodleNameProp[0]["plain_text"].strip()
            module_map[moodleName] = pID
            print(f"Mapping: {moodleName} -> {title}")
        else:
            module_map[title] = pID
            print(f"Kein MoodleName für {title}")
    
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(module_map, f, indent=4, ensure_ascii=False)
    print("config.json aktualisiert")




if __name__ == "__main__":
    updateConfig()
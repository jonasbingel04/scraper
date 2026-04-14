import re

def extractTasks(page, label):
    print(f"[{label}] Suche nach Aufgaben")

    try:
        page.wait_for_selector("h6.event-name a", timeout=8000)
        tasks = page.query_selector_all("h6.event-name a")

        results = []
        for t in tasks:
            aria = t.get_attribute("aria-label")
            link = t.get_attribute("href")
            title = t.inner_text().strip()
            
            modulMatch = re.search(r"in (.*) ist", aria if aria else "")
            modul = modulMatch.group(1) if modulMatch else "Kein Modul gefunden"

            deadlineMatch = re.search(r"ist (.*) fällig", aria if aria else "")
            deadlineDate = deadlineMatch.group(1) if deadlineMatch else "Kein Datum gefunden"

            results.append({
                "uni": label,
                "title": title,
                "deadline": deadlineDate,
                "modul": modul,
                "fullInfo": aria,
                "link": link
            })
        
        print(f"{label} |  {len(results)} Aufgaben")
        return results
    
    except Exception as e:
        print(f"{label} | Keine Aufgaben oder Fehler: {e}")
        return []


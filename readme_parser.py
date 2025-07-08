import re
import sqlite3
from typing import Optional, Dict

import internship_db

#These are words you can add to filter out roles you do not want
SKIP_KEYWORDS = {'quant', 'trader'}

#Method checking if internship at specific line contains keywords in SKIP_KEYWORDS
def should_skip_internship(role: str, keywords: set[str]) -> bool:
    role_lower = role.lower()
    return any(kw.lower() in role_lower for kw in keywords)


#Filters out lines of the README that are considered inactive until <details> and </detials> counts cancel each other out
def filter_active_sections(lines):
    skip = False
    depth = 0

    for line in lines:
        # When we hit the inactive summary, start skipping
        if not skip and '<summary>🗃️ Inactive roles' in line:
            skip = True
            # We assume the opening <details> was just before this,
            # so we start with depth=1
            depth = 1
            continue

        if skip:
            # If we see another <details>, bump the depth
            if '<details' in line:
                depth += 1
            # If we see a </details>, drop the depth
            if '</details>' in line:
                depth -= 1
                # If we’ve closed them all, stop skipping
                if depth == 0:
                    skip = False
            # In skip mode, never yield
            continue

        # Normal mode: hand the line back to your parser
        yield line




import re
from typing import Optional, Dict

def parse_request_into_internship(line: str) -> Optional[Dict[str, str]]:
    parts = [p.strip() for p in line.strip().strip('|').split('|')]
    # 1) company name & markdown link
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', parts[0])
    if not m:
        return None
    company = m.group(1)

    # 2) role & location
    role     = parts[1] if len(parts) > 1 else ""
    location = parts[2] if len(parts) > 2 else ""

    # 3) grab every href from the HTML cell
    html_cell = parts[3] if len(parts) > 3 else ""
    hrefs     = re.findall(r'href="([^"]+)"', html_cell)

    # 4) pick the simplify.jobs link if present, else fall back to the first href
    app_link = None
    for href in hrefs:
        if "simplify.jobs" in href:
            app_link = href
            break
    if not app_link and hrefs:
        app_link = hrefs[0]

    # 5) if for some reason there wasn’t any <a href> at all, fall back to company-link
    if not app_link:
        app_link = m.group(2)

    return {
        "Company":         company,
        "Role":            role,
        "Location":        location,
        "Application Link": app_link
    }





def process_line(conn: sqlite3.Connection, line: str, skip_keywords: set[str] = SKIP_KEYWORDS) -> Optional[Dict[str, str]]:

    #1) Checks to see if line on README begins with "|" or "|-", will not parse line
    #otherwise as it is not a line containing an internship
    ls = line.lstrip()
    if not ls.startswith('|') or ls.startswith('|-'):
        return None

    #2) Parsing the line into an internship dict
    internship = parse_request_into_internship(line)
    if not internship:
        return None
    
    #3) Checking if line contains SKIP_KEYWORDS, will skip if it does
    if should_skip_internship(internship['Role'], skip_keywords):
        return None

    #4) Checks if line is already contained in database
    link = internship['Application Link']
    if internship_db.internship_exists(conn, link):
        # already sent
        return None

    #5) Otherwise a new internship is found. Inserted into database and returned for emailing
    internship_db.insert_internship(conn, internship)
    return internship
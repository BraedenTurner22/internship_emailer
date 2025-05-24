import sqlite3
from internship_db import init_db
from readme_parser import process_line, filter_active_sections
from readme_fetcher import fetch_readme
from internship_emailer import send_email

def main():
    conn = init_db('internships.db')

    fetch_readme()

    with open('most_recent_readme.txt', encoding='utf-8') as f:
        for line in filter_active_sections(f):
            internship = process_line(conn, line)
            if internship:
                send_email(internship)

if __name__ == '__main__':
    main()
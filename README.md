# CS Internship Emailer Script

A python script for fetching, parsing, and emailing computer science internships.

While running, this script will send new internships to a designated email using the Python smtplib. Internships are stored in a sqlite3 database, so previously emailed internships are not emailed again.

Using the public README from Simplify and Pitt CSC: https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/README.md
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file.

For the Google Password Key, create an App Password on you Google account settings. Ensure 2FA is turned on.

`GOOGLE_PASSWORD_KEY` = Google Password Key

`SENDER_EMAIL` = Your google email

`RECEIVER_EMAIL` = Email you are sending to

## Run Locally

Clone the project

```bash
  git clone git@github.com:BraedenTurner22/internship_emailer.git
```

Create/activate virtual environment

```bash
  python3 -m venv venv
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run application

```bash
  python3 main.py
```


## Cron Job

To run on your computer continuously, think about setting up a cron jon to run the program at a consective given time period.

These commands assume you are using a Unix based machine.

Open/edit crontab:
```bash
crontab -e
```


Add this to crontab:
```bash
*/30 * * * * cd /full/path/to/your/project && /home/youruser/yourproject/.venv/bin/python
 main.py >> /full/path/to/your/project/cron.log 2>&1
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


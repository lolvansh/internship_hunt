# Automate Intership hunt 

v 0.2
Right now its not fully connected to each other, i will do it in upcoming days, what it does is make it easy to apply for jobs in your specified area, it finds company near you, scrap their company url and emais then starts sending cold emails to those companies



## Requirements:
```
1. your emails app password(find in your mail setting)
2. google's Places api key
3. install the dependencies
```


## Usage Workflow

### Phase 1: Data Collection
1.  **Initial Scrape:** Fetches data from Google Maps.
    ```bash
    python company_details.py
    ```
2.  **Deep Scan:** Get emails from the companies url
    ```bash
    python get_emails.py
    python retry_missed.py
    ```

### Phase 2: Database Setup
3.  **Initialize Database:** Creates the `applications.db` schema.
    ```bash
    python db_conn.py
    ```
4.  **Import Data:** Loads scraped JSON data into the database.
    ```bash
    python database.py
    ```

### Phase 3: Outreach
5.  **Send Applications:**
    * Set `TEST_MODE = True` in `mailer.py` to verify logic.
    * Set `TEST_MODE = False` to start sending.
    ```bash
    python mailer.py
    ```

## ⚠️ Disclaimer
Do not abuse otherwise your email will be banned. only send 80 mails per day
# 📍 Crowdsourced Campus Issue Tracker

This web application is a class project for a software engineering course. It provides a platform for students, faculty, and staff at Northern Kentucky University to report, track, and upvote campus maintenance issues, facilitating a direct line of communication with campus administration.

## Live Demo
Check out the live website here: [Campus Issue Tracker](https://campus-issue-tracker-qggs.onrender.com/)

## ✨ Core Features

* **Dynamic Dashboard:** A filterable and sortable view of all issues with live summary-count cards for "Total Issues," "Reported," "In Progress," and "Resolved."
* **Full User Authentication:** A complete frontend system for user registration, login, and logout.
* **Issue Reporting:** Logged-in users can submit detailed issue reports, including a title, category, description, photo upload, and a building selected from a predefined list of NKU campuses.
* **Admin Status Updates:** Users designated as "staff" (via the Django admin panel) can see a special "Admin Actions" card on the issue detail page to update an issue's status.
* **Real-time Voting:** Logged-in users can upvote issues. The vote count updates instantly on the page without a refresh, thanks to JavaScript (Fetch API) and a Django backend.
* **Activity Timeline:** A full historical log on each issue detail page, automatically tracking its creation and all subsequent status changes.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (ES6+)
* **Database:** SQLite (for development), PostgreSQL/MySQL (for production)
* **Authentication:** Django's built-in `auth` system with `UserCreationForm`
* **Secrets:** `python-dotenv` for managing environment variables

## 🚀 Getting Started: Running Locally

To get a local copy up and running, follow these simple steps.

### Prerequisites

You must have Python (3.10+), `pip`, and `git` installed on your system.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/NLama77/campus-issue-tracker.git](https://github.com/NLama77/campus-issue-tracker.git)
    cd campus-issue-tracker
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # On Windows
    py -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Create your local secrets (`.env`) file:**
    * Create a file named `.env` in the root of your project folder.
    * Open the file and add a `SECRET_KEY`. You can use a simple placeholder for development, or generate a new one.
    ```
    SECRET_KEY=my-local-dev-key-is-not-very-secret
    ```

5.  **Run the database migrations:**
    This will create your local `db.sqlite3` file and set up all the tables.
    ```sh
    python manage.py migrate
    ```

6.  **Create a superuser account:**
    You will need this to log in as an admin and test the staff-only features.
    ```sh
    python manage.py createsuperuser
    ```
    (Follow the prompts to create your admin username and password.)

7.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```

8.  **You're all set!**
    Open your browser and navigate to `http://127.0.0.1:8000/` to see the application.
    * Log in as a regular user at `http://127.0.0.1:8000/login/`.
    * Log in as an admin at `http://127.0.0.1:8000/admin/`.

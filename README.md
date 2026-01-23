# FastAPI Blog Project

This is a learning-based FastAPI project for a blogging platform.

## Features

-   **Authentication**: JWT-based login and registration.
-   **User Management**: Create and view users.
-   **Blog Management**: Create, read, update, and delete blogs.
-   **Database**: SQLite database with SQLAlchemy ORM.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

5.  **Access the API docs:**
    Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## Notes

-   The database file `blog.db` will be created in the `env` directory.
-   **Important**: The secret key is currently hardcoded for learning purposes. **Do not use this in production without changing it.**

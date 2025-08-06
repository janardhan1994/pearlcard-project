# PearlCard Fare Calculator

A full-stack fare calculation system for a metro transit system. This application features a dynamic React frontend, a robust Python/FastAPI backend, and a web-based admin panel for managing zones and fares.

---

## Features

- **Dynamic Fare Calculation:** Instantly calculates fares as journeys are added.
- **Database-Driven:** All zones and fares are stored in a database and are fully configurable.
- **Web-Based Admin Panel:** An `/admin` interface for easily managing zones and fare prices without needing to touch any code.
- **Full Test Coverage:** Includes comprehensive backend and frontend test suites.
- **Configuration-Ready:** Uses environment variables (`.env` files) to manage configuration, separating it from the code.

---

## Local Architecture

The application uses a modern, decoupled architecture. The React frontend is a standalone development server running on port **3000**. It communicates with a separate Python/FastAPI backend API, which runs on port **8000** and connects to a SQLite database.



---

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLAdmin, Pytest
- **Frontend:** JavaScript, React, Axios, React Testing Library, Jest
- **Database:** SQLite

---

## Getting Started (Local Development)

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.9+ and `pip`
- Node.js and `npm`
- Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/janardhan1994/pearlcard-project.git
    cd pearlcard-project
    ```

2.  **Set up the Backend:**
    ```bash
    # Navigate to the backend directory
    cd backend

    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    # Install Python dependencies
    pip install -r requirements.txt

    # Return to the root directory
    cd ..
    ```
    *Note: The backend is configured via environment variables. For local setup, it uses sensible defaults in `backend/settings.py`. You can create a `backend/.env` file to override them if needed.*

3.  **Set up the Frontend:**
    ```bash
    # Navigate to the frontend directory
    cd frontend

    # Install Node.js dependencies
    npm install
    
    # Create the environment file for the frontend
    # (You can use a text editor to create .env and add the line below)
    echo "REACT_APP_API_BASE_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)" > .env

    cd ..
    ```

### Running the Application

You will need two separate terminals to run both servers.

1.  **Terminal 1 (Run the Backend Server):**
    ```bash
    # (From the project root)
    source backend/venv/bin/activate
    uvicorn backend.main:app --reload
    ```
 1.1  **Terminal 1 (Run the Backend Server):**
    - The backend API will be running at `http://127.0.0.1:8000`.

 1.2 ** Admin Panel Page is used to add the additional Zones or Fares:**
    - The Admin Panel will be at `http://127.0.0.1:8000/admin`.

2.  **Terminal 2 (Run the Frontend Server):**
    ```bash
    # (From the project root)
    cd frontend
    npm start
    ```
    - The frontend application will open at `http://localhost:3000`.

---

## Running Tests

- **Backend Tests:** From the root directory, activate your virtual environment (`source backend/venv/bin/activate`) and run `pytest`.
- **Frontend Tests:** From the `frontend` directory, run `npm test`.

---

## API Documentation

With the backend server running, interactive API documentation (provided by FastAPI/Swagger) is available at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

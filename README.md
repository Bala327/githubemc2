# Health Record Management App

A simple CRUD (Create, Read, Update, Delete) application for managing health records. Built with Flask and SQLAlchemy.

## Features

- Create new health records
- View existing health records
- Update health record information
- Delete health records
- Responsive web interface

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:5000`

## Running Tests

To run the test suite:
```bash
pytest test_app.py
```

## Project Structure

- `app.py`: Main application file with routes and database models
- `templates/`: HTML templates for the web interface
- `test_app.py`: Unit tests
- `requirements.txt`: Project dependencies

## Project Setup

To set up and run the project, follow these steps:

1. Navigate to the project directory:
   ```
   <Project location>
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For Unix or Linux
   ```

3. Set the PYTHONPATH environment variable:
   ```
   set PYTHONPATH=%PYTHONPATH%;<Project location>
   ```

4. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set the path for the Flask environment:
   ```
   set PATH=%PATH%;<venv PATH>\Scripts
   ```

6. Set the FLASK_APP environment variable:
   ```
   set FLASK_APP=qbank.py
   ```

## Running the Project

To run the project, follow these steps:

1. Start the Flask server:
   ```
   flask run
   ```

   This will start the Flask server, and the application will be accessible at the provided URL.

2. Access the Flask shell:
   ```
   flask shell
   ```

3. Import the necessary modules and create the database tables:
   ```python
   from qbank.schema import db, User
   db.create_all()
   ```

4. Add a new user to the database (example):
   ```python
   db.session.add(student_john)  # Replace with the appropriate User object
   db.session.commit()
   ```

By following these steps, you should be able to set up the project, create and activate a virtual environment, install dependencies, and run it successfully. Make sure to replace any placeholder values with the actual values specific to your project.
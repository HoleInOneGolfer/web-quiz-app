![Logo](./quiz_server/static/images/icon.png)

# Web Quiz App

Quiz Server - A simple quiz application that allows users to create and take quizzes and track results in a spreadsheet.

## To-Do

- [ ] Add audio (music and sound effects)
- [ ] Add quiz timeout refresh
- [ ] ...

## Development Setup

1. Clone the repository

   ```bash
   git clone https://github.com/HoleInOneGolfer/web-quiz-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd web-quiz-app
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

5. Install the project

   ```bash
   pip install -e .
   ```

## Running the Application

To run the application, use the following command:

```bash
flask --app quiz_server run
```

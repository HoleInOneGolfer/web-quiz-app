# ![Logo](./quiz_server/static/images/icon.png) Web Quiz App

Quiz Server - A simple quiz application that allows users to create and take quizzes and track results in a spreadsheet.

## To-Do

- [ ] Add audio (music and sound effects)
- [ ] Add quiz timeout refresh
- [ ] Quiz start and end screens
- [ ] Refactor code
- [ ] Add error handling

## Development Setup

To set up the development environment, follow these steps:

```bash
git clone https://github.com/HoleInOneGolfer/web-quiz-app.git
cd web-quiz-app
python3 -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Running the Application

To run the application, use the following command:

```bash
flask --app quiz_server run
```

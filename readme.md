# Job Preference Ranking App

A full-stack Python application that infers user job preferences from pairwise comparisons using the Bradley-Terry model via the `choix` library.

## Features

- **Pairwise Comparisons**: Users compare two job options and select their preferred choice
- **Preference Inference**: Uses the `choix` library to infer user preferences from comparison data
- **Modern UI**: Clean, responsive web interface with modern design
- **Real-time Rankings**: View preference rankings that update as you make more comparisons
- **Modular Architecture**: Ranking engine is isolated and swappable (ready for BradleyTerryScalable)

## Job Attributes

Each job option consists of four attributes:
- **Size**: Small, Medium, Large
- **Mission**: Mission-driven, Commercial, Non-profit, RTO, Academia
- **Sector**: Current, Previous, New
- **Stage**: Startup, Scaleup, Corporate, Multinational

## API Endpoints

- `GET /`: Main comparison interface
- `GET /next`: Get two random job options for comparison
- `POST /compare`: Submit a user's choice between two options
- `GET /rankings`: Get current preference rankings
- `GET /rankings-page`: View rankings in the web interface
- `POST /reset`: Reset all comparison data
- `GET /health`: Health check endpoint

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. Open your browser and go to `http://localhost:8000`

## Usage

1. **Make Comparisons**: Click on your preferred job option between the two presented choices
2. **Submit Choice**: Click "Submit Choice" to record your preference
3. **View Rankings**: Click "📊 View My Preferences" to see your inferred preferences
4. **Reset Data**: Use the reset button to clear all comparison data

## Demo

Run the included demo script to see the complete workflow:

```bash
python test_demo.py
```

This will:
- Make 5 random job comparisons with random choices
- Show how preferences are inferred from the comparison data
- Display the final preference rankings for each attribute
- Reset all data back to the initial state

## Technical Details

- **Backend**: FastAPI with Python 3.13+
- **Frontend**: HTML/CSS/JavaScript (no framework dependencies)
- **Ranking Algorithm**: Bradley-Terry model via `choix` library
- **Data Storage**: In-memory (easily extensible to database)
- **Deployment Ready**: Containerizable and cloud-ready

## Architecture

- `models.py`: Pydantic data models for job options and API requests/responses
- `ranking_engine.py`: Isolated ranking logic using choix library
- `job_generator.py`: Utility for generating diverse job comparison pairs
- `main.py`: FastAPI application with all endpoints
- `templates/`: HTML templates for the web interface

## Future Enhancements

- Database persistence (SQLite/PostgreSQL)
- Multi-user support with authentication
- Advanced analytics dashboard
- Export preferences to CSV/JSON
- Integration with job board APIs
- A/B testing for different ranking algorithms

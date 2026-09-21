# MyKoreanDish

MyKoreanDish is a full-stack web application for discovering Korean dishes and ingredients through community reviews. Users can explore dishes, compare taste and dietary information, record personal notes, save favorites, and receive similar-dish recommendations.

**Live demo:** [food-suggestion.onrender.com](https://food-suggestion.onrender.com/)

## Features

- Google OAuth authentication
- Korean dish and ingredient search
- Filtering by taste, dietary preferences, and ingredients
- Community reviews for:
  - Taste and overall rating
  - Price
  - Dietary properties
  - Dish ingredients
  - Ingredient nutrients
- Similar-dish recommendations based on taste profiles
- Favorite dishes and ingredients
- Personal notes for dishes and ingredients
- User activity history
- Review aggregation and insight pages
- User profiles and user-management pages
- Responsive server-rendered frontend with browser-side API interactions

## Technology stack

| Area | Technology |
| --- | --- |
| Backend | Python, Flask |
| Frontend | Jinja templates, vanilla JavaScript, HTML, CSS |
| Database | Firebase Cloud Firestore |
| Authentication | Google OAuth through Flask-Dance |
| Data processing | Python CSV modules, NumPy, pandas, NLTK |
| Production server | Gunicorn |
| Deployment | Render |

## Project structure

```text
.
├── backend/
│   ├── config/              Application and Firebase configuration
│   ├── controllers/
│   │   ├── api/             JSON API blueprints
│   │   └── web/             Server-rendered page routes
│   ├── data/                Dish, ingredient, dietary, country, and nutrient CSV data
│   ├── models/              Firestore data-access managers
│   ├── services/            Shared business logic and recommendations
│   ├── tests/               Backend tests
│   ├── app.py               Local application entry point
│   └── requirements.txt     Python dependencies
├── frontend/
│   ├── static/              JavaScript, CSS, and favicon assets
│   └── templates/           Jinja HTML templates
├── Procfile                 Render/Gunicorn process definition
└── readme.md
```

## Architecture

The Flask application is created by `backend.create_app()`. It registers separate web and API blueprints:

- Web routes render pages from `frontend/templates`.
- API routes under `/api` return data for frontend interactions.
- Model managers encapsulate Firestore reads and writes.
- CSV files provide relatively static reference data such as dishes, ingredients, countries, dietary labels, and nutrients.
- Firestore stores users, reviews, favorites, notes, histories, and aggregated review information.

Taste recommendations represent each dish as a six-dimensional vector:

```text
[spiciness, sweetness, sourness, healthiness, texture, temperature]
```

The values are normalized to the `0..1` range, compared using normalized Manhattan distance, and returned as a ranked list of similar dishes.

## Firestore collections

The application uses the following Firestore collections:

| Collection | Purpose |
| --- | --- |
| `Users` | User profiles and account information |
| `Dishes` | Firestore-backed dish data where applicable |
| `Ingredients` | Ingredient reviews and ingredient-related data |
| `Dietaries` | Dietary reviews |
| `UserSelections` | Taste and rating reviews |
| `Prices` | Price reviews |
| `Nutrients` | Ingredient nutrient reviews |
| `Favorites` | Saved dishes and ingredients |
| `Notes` | User notes |
| `Aggregates` | Per-dish review averages and distributions |

## Local development

### Requirements

- Python 3.10 or newer
- A Firebase project with Firestore enabled
- Google OAuth credentials
- Git

### Setup

1. Clone the repository and enter the project:

   ```bash
   git clone <repository-url>
   cd mykoreandish-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install backend dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. Create a `.env` file in the repository root:

   ```dotenv
   SECRET_KEY=replace-with-a-long-random-secret
   GOOGLE_CLIENT_ID=your-google-oauth-client-id
   GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
   OAUTHLIB_INSECURE_TRANSPORT=1
   ```

   `OAUTHLIB_INSECURE_TRANSPORT=1` is intended for local HTTP development only. Do not enable it in production.

5. Provide Firebase service-account credentials. Either:

   - Place the service-account JSON file at `credentials.json` in the repository root, or
   - Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON file.

   Never commit `.env` or service-account credentials. Both are ignored by Git.

6. Start the development server:

   ```bash
   python -m backend.app
   ```

   The application listens on `http://127.0.0.1:10000` by default. Set `PORT` to use another port.

## API overview

The JSON API is grouped into resource-specific blueprints:

| Resource | Base path |
| --- | --- |
| Dishes | `/api/dishes` |
| Ingredients | `/api/ingredients` |
| Reviews | `/api/reviews` |
| Taste reviews | `/api/tastes` |
| Dietary reviews | `/api/dietaries` |
| Nutrients | `/api/nutrients` |
| Prices | `/api/prices` |
| Favorites | `/api/favorites` |
| Notes | `/api/notes` |
| History | `/api/histories` |
| Users | `/api/users` |
| Countries | `/api/countries` |

Examples:

```bash
# List dishes
curl http://127.0.0.1:10000/api/dishes/

# Get one dish
curl http://127.0.0.1:10000/api/dishes/Bibimbap

# Get aggregated information for a dish
curl http://127.0.0.1:10000/api/dishes/aggregates/Bibimbap

# Get taste-based recommendations
curl http://127.0.0.1:10000/api/tastes/similar/Bibimbap
```

Some endpoints require an authenticated session and accept request bodies used by the frontend. Refer to the corresponding controller in `backend/controllers/api/` for the current request and response shape.

## Testing

Run Python syntax validation:

```bash
python -m compileall -q backend
```

Run the backend test discovery command:

```bash
python -m unittest discover -s backend/tests -p 'test_*.py' -v
```

Tests that access Firestore should be run with valid Firebase test configuration or suitable mocks. Do not use production credentials for automated tests.

## Deployment

The project includes a `Procfile` for Render:

```text
web: gunicorn "backend:create_app()" --bind 0.0.0.0:$PORT --timeout 120
```

Configure the following environment variables in the deployment platform:

- `SECRET_KEY`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_APPLICATION_CREDENTIALS` or the platform's secure Firebase credential configuration
- `PORT` when required by the platform

The Google OAuth redirect URI must match the deployed application's callback URL. Production deployments should use HTTPS and should not set `OAUTHLIB_INSECURE_TRANSPORT=1`.

## Contributing

1. Create a feature branch.
2. Make a focused change.
3. Run syntax checks and relevant tests.
4. Update documentation when behavior or setup changes.
5. Open a pull request with a clear description of the change.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# Movies - Movie Shelf Web App

A Flask web application to manage and display your movie collection with a beautiful dark-themed shelf interface.

## Features
- 🎬 Beautiful movie shelf display with poster images
- ➕ Add movies to your collection
- 🗑️ Delete movies from collection
- 📊 Export collection to Excel
- 🖨️ Print your collection
- 🔍 Search functionality
- 📺 Uses OMDb API for movie data

## Local Setup

### Requirements
- Python 3.8+
- pip

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Rakkasan3187101/Movies.git
cd Movies
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open in browser: `http://localhost:5000`

## Deployment

### Deploy to Railway (Recommended - Free)
1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "Deploy from GitHub repo"
4. Select your Movies repository
5. Railway will automatically detect and deploy your Flask app

### Deploy to Render
1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Deploy!

### Deploy to Heroku (Paid now, but available)
1. Install Heroku CLI
2. Run:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## API Key
The app uses OMDb API (fa72850d) for movie data. Consider replacing with your own API key for production use.

## License
MIT

from flask import Flask, render_template_string, request, redirect, url_for, send_file
import requests
import io
from openpyxl import Workbook
import os

API_KEY = 'fa72850d'  #

app = Flask(__name__)
movie_database = []

navbar = '''
<div style="background:#181818; padding:16px 0; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
    <a href="{{ url_for('main') }}" style="color:#fff; margin:0 18px; text-decoration:none; font-weight:bold;">Home</a>
    <a href="{{ url_for('add_movie') }}" style="color:#fff; margin:0 18px; text-decoration:none; font-weight:bold;">Add Movie</a>
    <a href="{{ url_for('about') }}" style="color:#fff; margin:0 18px; text-decoration:none; font-weight:bold;">About</a>
    <a href="{{ url_for('print_collection') }}" style="color:#fff; margin:0 18px; text-decoration:none; font-weight:bold;">Print Collection</a>
    <a href="{{ url_for('export_excel') }}" style="color:#fff; margin:0 18px; text-decoration:none; font-weight:bold;">Export to Excel</a>
</div>
'''

main_page = '''
<!doctype html>
<html>
<head>
<title>Movie Shelf</title>
<style>
body {
    background: #222;
    color: #eee;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
h1 {
    text-align: center;
    margin-top: 30px;
    letter-spacing: 2px;
}
.shelf-container {
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
    justify-content: center;
    padding: 40px 0 60px 0;
    background: repeating-linear-gradient(
        to bottom,
        #444 0px,
        #444 8px,
        #222 8px,
        #222 60px
    );
    min-height: 100vh;
}
.dvd-case {
    width: 160px;
    background: #333;
    border-radius: 12px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.5), 0 2px 8px rgba(0,0,0,0.3);
    padding: 16px 12px 18px 12px;
    text-align: center;
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
}
.dvd-case:hover {
    transform: translateY(-10px) scale(1.04);
    box-shadow: 0 16px 32px rgba(0,0,0,0.7), 0 4px 16px rgba(0,0,0,0.4);
    z-index: 2;
}
.dvd-cover {
    width: 120px;
    height: 180px;
    object-fit: cover;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    background: #555;
    margin-bottom: 10px;
}
.dvd-title {
    font-weight: bold;
    font-size: 1.1em;
    margin: 6px 0 2px 0;
    color: #fff;
}
.dvd-meta {
    font-size: 0.95em;
    color: #ccc;
    margin-bottom: 2px;
}
.delete-btn {
    background: #c00;
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 5px 12px;
    margin-top: 10px;
    cursor: pointer;
    font-size: 0.95em;
    transition: background 0.2s;
}
.delete-btn:hover {
    background: #a00;
}
</style>
</head>
<body>
''' + navbar + '''
<h1>🎬 My Movie Shelf</h1>
<div class="shelf-container">
    {% for movie in movies %}
    <div class="dvd-case">
        <img src="{{ movie.poster }}" class="dvd-cover" onerror="this.style.background='#444'">
        <div class="dvd-title">{{ movie.title }}</div>
        <div class="dvd-meta">{{ movie.year }}</div>
        <div class="dvd-meta">{{ movie.director }}</div>
        <form action="{{ url_for('delete_movie', index=loop.index0) }}" method="POST" style="margin:0;">
            <button type="submit" class="delete-btn">Delete</button>
        </form>
    </div>
    {% endfor %}
</div>
</body>
</html>
'''

add_movie_page = '''
<!doctype html>
<html>
<head>
<title>Add Movie</title>
<style>
body {
    background: #222;
    color: #eee;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
.form-container {
    max-width: 500px;
    margin: 40px auto;
    background: #333;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.5);
}
h1 {
    text-align: center;
}
input, button {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: none;
    border-radius: 6px;
    font-size: 1em;
    box-sizing: border-box;
}
input {
    background: #555;
    color: #eee;
}
input::placeholder {
    color: #999;
}
button {
    background: #007bff;
    color: #fff;
    cursor: pointer;
    font-weight: bold;
    transition: background 0.2s;
}
button:hover {
    background: #0056b3;
}
</style>
</head>
<body>
''' + navbar + '''
<div class="form-container">
    <h1>Add a Movie</h1>
    <form method="POST">
        <input type="text" name="title" placeholder="Movie Title" required>
        <input type="text" name="director" placeholder="Director" required>
        <input type="text" name="year" placeholder="Year" required>
        <button type="submit">Add Movie</button>
    </form>
</div>
</body>
</html>
'''

about_page = '''
<!doctype html>
<html>
<head>
<title>About</title>
<style>
body {
    background: #222;
    color: #eee;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
.content {
    max-width: 600px;
    margin: 40px auto;
    padding: 30px;
    background: #333;
    border-radius: 12px;
}
</style>
</head>
<body>
''' + navbar + '''
<div class="content">
    <h1>About Movie Shelf</h1>
    <p>Movie Shelf is a simple web application to manage and display your movie collection.</p>
    <p><strong>Features:</strong></p>
    <ul>
        <li>Add movies to your collection</li>
        <li>View movies in a beautiful shelf format</li>
        <li>Delete movies from your collection</li>
        <li>Export collection to Excel</li>
        <li>Print your collection</li>
    </ul>
</div>
</body>
</html>
'''

print_collection_page = '''
<!doctype html>
<html>
<head>
<title>Print Collection</title>
<style>
body {
    font-family: Arial, sans-serif;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}
th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}
th {
    background-color: #4CAF50;
    color: white;
}
tr:nth-child(even) {
    background-color: #f2f2f2;
}
h1 {
    text-align: center;
}
</style>
</head>
<body>
<h1>Movie Collection</h1>
<table>
    <thead>
        <tr>
            <th>Title</th>
            <th>Director</th>
            <th>Year</th>
        </tr>
    </thead>
    <tbody>
        {% for movie in movies %}
        <tr>
            <td>{{ movie.title }}</td>
            <td>{{ movie.director }}</td>
            <td>{{ movie.year }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<script>window.print();</script>
</body>
</html>
'''

search_page = '''
<!doctype html>
<html>
<head>
<title>Search Results</title>
<style>
body {
    background: #222;
    color: #eee;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
h1 {
    text-align: center;
    margin-top: 30px;
}
.shelf-container {
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
    justify-content: center;
    padding: 40px 0 60px 0;
}
.dvd-case {
    width: 160px;
    background: #333;
    border-radius: 12px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.5);
    padding: 16px 12px 18px 12px;
    text-align: center;
}
.dvd-cover {
    width: 120px;
    height: 180px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 10px;
}
.dvd-title {
    font-weight: bold;
    font-size: 1.1em;
    margin: 6px 0 2px 0;
    color: #fff;
}
.dvd-meta {
    font-size: 0.95em;
    color: #ccc;
    margin-bottom: 2px;
}
</style>
</head>
<body>
''' + navbar + '''
<h1>Search Results</h1>
<div class="shelf-container">
    {% for movie in movies %}
    <div class="dvd-case">
        <img src="{{ movie.poster }}" class="dvd-cover" onerror="this.style.background='#444'">
        <div class="dvd-title">{{ movie.title }}</div>
        <div class="dvd-meta">{{ movie.year }}</div>
        <div class="dvd-meta">{{ movie.director }}</div>
    </div>
    {% endfor %}
</div>
</body>
</html>
'''

@app.route('/')
def main():
    return render_template_string(main_page, movies=movie_database)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        year = request.form.get('year')
        
        url = f'http://www.omdbapi.com/?t={title}&apikey={API_KEY}'
        try:
            response = requests.get(url)
            data = response.json()
            
            movie = {
                'title': data.get('Title', title),
                'director': data.get('Director', director),
                'year': data.get('Year', year),
                'poster': data.get('Poster', 'https://via.placeholder.com/150')
            }
        except:
            movie = {
                'title': title,
                'director': director,
                'year': year,
                'poster': 'https://via.placeholder.com/150'
            }
        
        movie_database.append(movie)
        return redirect(url_for('main'))
    return render_template_string(add_movie_page)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_movie(index):
    if 0 <= index < len(movie_database):
        movie_database.pop(index)
    return redirect(url_for('main'))

@app.route('/about')
def about():
    return render_template_string(about_page)

@app.route('/print')
def print_collection():
    return render_template_string(print_collection_page, movies=movie_database)

@app.route('/export')
def export_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Movies"
    ws.append(["Title", "Director", "Year"])
    for movie in movie_database:
        ws.append([movie['title'], movie['director'], movie['year']])
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name='movie_collection.xlsx')

@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title', '').lower()
    director = request.args.get('director', '').lower()
    year = request.args.get('year', '').lower()
    
    matches = []
    for movie in movie_database:
        if title and title not in movie['title'].lower():
            continue
        if director and director not in movie['director'].lower():
            continue
        if year and year not in movie['year'].lower():
            continue
        matches.append(movie)
    return render_template_string(search_page, movies=matches)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

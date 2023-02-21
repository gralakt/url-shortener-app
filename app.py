from flask import Flask, request, jsonify, abort, redirect
import random
import string

# Inicjowanie aplikacji i bazy danych
app = Flask(__name__)
url_database = {}

# Funkcja do generowania losowego skróconego URLa
def generate_short_url():
    # Wybieranie losowych znaków ze zbioru liter i cyfr
    letters_and_digits = string.ascii_letters + string.digits
    # Generowanie skróconego URLa z 6 losowymi znakami
    return ''.join(random.choice(letters_and_digits) for _ in range(6))


# Endpoint dla tworzenia skróconych URLi
@app.route('/short/', methods=['POST'])
def create_short_url():
    # Odczytywanie długiego URLa z żądania HTTP
    long_url = request.json.get('long_url')
    # Generowanie losowego skróconego URLa
    short_url = generate_short_url()
    # Zapisywanie pary klucz-wartość do bazy danych URLi
    url_database[short_url] = long_url
    # Zwracanie skróconego URLa jako odpowiedź HTTP
    return jsonify({'short_url': short_url})


# Endpoint do rozwijania skróconych URLi
@app.route('/<short_url>')
def expand_url(short_url):
    # Pobieranie oryginalnego URLa z bazy danych
    long_url = url_database.get(short_url)
    if long_url:
        # Przekierowywanie na oryginalny URL
        return redirect(long_url)
    else:
        # Zwracanie błędu HTTP 404 Not Found
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
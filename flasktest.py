
from flask import Flask

#initialisiere Flask-Server
app = Flask(__name__)
    # definiere Route für Hauptseite
@app.route('/')
def index():
# gebe Antwort an aufrufenden Client zurück
    return 'Hello World!'
if __name__ == '__main__':
# starte Flask-Server
    app.run(host='0.0.0.0', port=5000)



    from flask import Flask

# Initialisiere Flask-Server
app = Flask(__name__)

# Definiere Route für Hauptseite
@app.route('/')
def index():
    # Gebe Antwort an aufrufenden Client zurück
    return 'Hello World!'

# Definiere Route für /eingaenge
@app.route('/eingaenge')
def eingaenge():
    return 'Dies ist die Eingänge-Seite.'

# Definiere Route für /ausgaenge
@app.route('/ausgaenge')
def ausgaenge():
    return 'Dies ist die Ausgänge-Seite.'

if __name__ == '__main__':
    # Starte Flask-Server
    app.run(host='0.0.0.0', port=5000)






    
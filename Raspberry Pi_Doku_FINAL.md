
# ToDoListVerwaltung – Raspberry Pi Projekt

## Projektübersicht

Diese Dokumentation beschreibt die grundlegende Einrichtung eines Raspberry Pi 4 im Schulnetzwerk sowie die Vorbereitung für das Deployment einer containerisierten Python-Flask-Anwendung. Ziel war es, sichere Benutzerkonten zu erstellen, den Fernzugriff über SSH zu ermöglichen, Docker zu installieren und Netzwerkprobleme mithilfe von Tools wie tcpdump zu analysieren.
Der Raspberry Pi wird als kompakter, headless Webserver genutzt, um eine einfache index.html-Seite bereitzustellen, die mit einem externen Projekt kommuniziert. Als Webserver kommt Apache2 zum Einsatz, während Docker eine saubere und isolierte Umgebung für den späteren Betrieb der Anwendung schafft. Auch wenn das eigentliche Deployment der Flask-App in einem späteren Schritt erfolgt, bildet diese Einrichtung die Grundlage für einen sicheren, stabilen und portablen Betrieb. Nach erfolgreichem Setup ist die Anwendung über eine API-Schnittstelle im Browser erreichbar.

---

## Verwendete Bibliotheken & Tools

### Systemdienste

- `apache2` – Webserver zum Hosten von HTML-Dateien
- `tcpdump` – Zur Überwachung des HTTP-Traffics
- `openssh-server` – SSH-Zugriff 

### Web-Frameworks

- `Flask` – Python-basiertes Web-Framework zur Erstellung einer REST-API
- `Docker` – Containerisierung der Webanwendung
- `NetworkManager` – Verwaltung statischer IP-Konfiguration

### Hardware & Netzwerkumgebung

- Gerät: Raspberry Pi 4 Model B (8 GB RAM)
- IP-Adresse: Schulnetzwerk mit IPv4 (z. B. 192.168.24.101)
- Physische Schnittstelle: Ethernet (RJ45)
- SSH: Zugriff über PowerShell auf Windows-Client
- DNS-Server: 192.168.24.254, 8.8.8.8

---

## Schritt-für-Schritt Setup

### 1. Image flashen & SSH aktivieren

- SD-Karte (16–128 GB) mit Raspberry Pi Imager flashen
- Unter „Erweiterte Einstellungen“:
  - SSH aktivieren
  - Hostname + Passwort setzen:
    •	Pi_Hostname
    •	Pi_password
    

### 2. Netzwerkverbindung & SSH-Zugriff

- SD-Karte einlegen, Raspberry Pi über LAN und Strom verbinden
- Leuchten am LAN-Port prüfen: Orange (Strom), Grün (Datenaktivität)

#### Verbindung per PowerShell (Windows)

```powershell
# Raspberry Pi im Netzwerk finden (ping mit IPv4)
ping raspberrypi -4

# Verbindung aufbauen (ersetze <hostname> mit meinem Hostname)
ssh <Pi_Hostname>@<RaspberryPi_IP>
ssh pi@192.168.24.101
```
- Die Verbindung wurde nach Eingabe des Passworts erfolgreich aufgebaut.

> Falls SSH-Warnung erscheint (z. B. Schlüsselkonflikt):
```powershell
# Löscht veraltete SSH-Schlüssel, wenn es zu einem Sicherheitskonflikt kommt
ssh-keygen -R <RaspberryPi_IP>
ssh-keygen -R 192.168.24.101
```

#### Erste Verbindung

- Bei der Verbindung:
  - Mit „yes“ bestätigen, dass du der Verbindung vertraust
  - Passwort eingeben, das du im Imager gesetzt hast

- Authenticate: 
  •	yes for authentitytest
  •	enter Pi_password
---

## 3. Statische IP-Adresse setzen (optional)

```bash
# Installiert NetworkManager, um Netzwerkeinstellungen (wie statische IP) komfortabel zu verwalten
sudo apt install network-manager -y

# Deaktiviert den alten Netzwerkdienst (dhcpcd), um Konflikte mit dem NetworkManager zu vermeiden
sudo systemctl disable dhcpcd
sudo systemctl stop dhcpcd

# Aktiviert den neuen Netzwerkdienst
sudo systemctl enable NetworkManager

# Startet den NetworkManager-Dienst
sudo systemctl start NetworkManager

# Zeigt alle verfügbaren Netzwerkverbindungen – wichtig, um den Namen der LAN-Verbindung zu finden.
nmcli connection show

# Statische IP zuweisen
# Weise der ausgewählten Netzwerkverbindung eine feste IP-Adresse zu (inkl. Subnetzmaske und Gateway)
nmcli connection modify "<Verbindung>" ipv4.addresses <deine.IP>/<Subnetz> ipv4.gateway <Gateway> ipv4.method manual

# Deaktiviert die Verbindung, um die neuen Einstellungen zu übernehmen
nmcli connection down "<Verbindung>"

# Aktiviert die Verbindung erneut mit den neuen IP-Einstellungen
nmcli connection up "<Verbindung>"
```
- Warum statische IP?
Eine statische IP-Adresse sorgt dafür, dass Raspberry Pi immer unter derselben Adresse erreichbar bleibt – was für den Fernzugriff, die Webanwendung und das Hosting von Diensten wie SSH oder einem Webserver essenziell ist.
---

## 4. Apache Webserver installieren

```bash
# Paketquellen aktualisieren – wichtig, um neueste Versionen zu installieren
sudo apt update
# Apache2-Webserver installieren – stellt HTML-Seiten im Browser bereit
sudo apt install apache2 -y
# Prüfen, ob der Apache-Dienst aktiv läuft (Status: active (running) erwartet
sudo systemctl status apache2
```

### Apache testen

- Im Browser öffnen: `http://<RaspberryPi_IP>`  
- Man soll die Apache2-Debian-Standardseite sehen (Wenn alles funktioniert.)
- Diese zeigt an, dass der Webserver korrekt installiert und erreichbar ist.


### Eigene HTML-Seite anzeigen

```bash
# Öffnet die Standard-HTML-Datei zur Bearbeitung mit dem Texteditor "nano"
# Diese Datei ist der Startpunkt unser Website. Der Inhalt wird im Browser angezeigt, wenn wir http://<RaspberryPi_IP> aufrufen.
sudo nano /var/www/html/index.html
```
Ein Beispiel-HTML:

```html
<!DOCTYPE html>
<html>
<head><title>Raspberry Pi</title></head>
<body><h1>Hello World!</h1><p>Diese Seite läuft auf dem Raspberry Pi.</p></body>
</html>
```

- Speichern & Schließen in nano:
  Drücke CTRL + O (zum Speichern), dann Enter
  Danach CTRL + X (zum Beenden)
---

## 5. Netzwerküberwachung mit `tcpdump`

```bash
# Installiert das Netzwerküberwachungstool tcpdump
sudo apt install tcpdump -y

# Startet eine Aufzeichnung des gesamten HTTP-Datenverkehrs (Port 80) über die Ethernet-Schnittstelle
# Die Ausgabe wird in die Datei "webzugriff.pcap" geschrieben
sudo tcpdump -i eth0 port 80 -w webzugriff.pcap

# Zeigt die Inhalte der Aufzeichnungsdatei im Klartext an (Analyse)
# Aufnahme stoppen mit: STRG + C
sudo tcpdump -r webzugriff.pcap
```
---

## 6. Benutzerverwaltung & SSH-Absicherung

### Benutzer hinzufügen

```bash
# Erstellt einen neuen Standardnutzer namens "bea"
sudo adduser bea
# Erstellt einen Benutzer "fernzugriff" mit Home-Verzeichnis, Bash-Shell und Administratorrechten (Gruppe: sudo)
sudo useradd fernzugriff -m -s /bin/bash -G sudo
# Setzt das Passwort für den Benutzer "fernzugriff"
sudo passwd fernzugriff
```
- Warum?
  Die Trennung von normalen Benutzern und Admin-Zugängen verbessert die Sicherheit.
  Ein spezieller SSH-Admin-Benutzer („fernzugriff“) wird für Fernwartung genutzt – ohne Root-Login.


### SSH-Key-basierten Zugang einrichten

- Warum?  
  Die Anmeldung über einen Public-Key ist sicherer als Passwort-Login und ermöglicht automatisierten Zugang (z. B. für CI/CD oder Wartung).

1. Auf Windows: `ssh-keygen` im Terminal ausführen
2. Den Inhalt von `~/.ssh/id_rsa.pub` kopieren
3. Auf dem Raspberry Pi einfügen:

```bash
# SSH-Verzeichnis erstellen und absichern
mkdir ~/.ssh && chmod 700 ~/.ssh
# Public Key im Editor einfügen
nano ~/.ssh/authorized_keys
# Datei nach dem Einfügen speichern, dann Berechtigungen setzen
chmod 600 ~/.ssh/authorized_keys
```
- Ergebnis:
  Die SSH-Anmeldung erfolgt nun ohne Passwort – vorausgesetzt, der Private Key befindet sich auf dem Client.


### SSH-Konfiguration anpassen
```bash
sudo nano /etc/ssh/sshd_config
```

- Wichtige Einstellungen prüfen oder ergänzen:
```bash
# Ermöglicht bei Bedarf auch Passwort-Login (kann später auf "no" gestellt werden)
PasswordAuthentication yes
# Verhindert direkte Anmeldung als root – erhöht die Sicherheit
PermitRootLogin no
# Aktiviert die Anmeldung per SSH-Key
PubkeyAuthentication yes
 # Erlaubt nur diesen Benutzern den SSH-Zugang
AllowUsers fernzugriff bea pi
```

SSH-Dienst neu starten:
```bash
sudo /etc/init.d/ssh restart
```
- warum restart? Damit Änderungen an der SSH-Konfiguration wirksam werden.
---

## 7. Docker-Installation und Einsatz zur Bereitstellung der Web-App

```bash
# Installiert Docker über den Paketmanager
sudo apt install docker.io -y
# Startet den Docker-Dienst, falls er nicht automatisch läuft
sudo systemctl start docker.service
# Testet die Installation mit einem einfachen Beispielcontainer ("Hello World")
sudo docker run hello-world
# Startet eine interaktive Bash-Sitzung in einem Ubuntu-Container (Testumgebung im Container)
sudo docker run -it ubuntu bash
# Zeigt alle lokal vorhandenen Docker-Images an
sudo docker images
```
- Was passiert hier?
  Mit docker.io wird Docker auf dem Raspberry Pi installiert.
  hello-world prüft, ob Docker korrekt funktioniert.
  Der Ubuntu-Container erlaubt, direkt im Container zu arbeiten.
  Mit docker images bekommt Man einen Überblick über bereits vorhandene Basis- oder Projekt-Images.

* Ziel:
Docker soll später deine Python-Flask-App in einer isolierten Umgebung ausführen. Diese Schritte sind die Vorbereitung dafür.
---

## 8. Eigene Flask-App mit Docker bereitstellen

### Dockerfile

```Dockerfile
# Verwendet ein schlankes Python-Image als Basis (klein & schnell)
FROM python:3.8-alpine
# Installiert das Flask-Framework im Container
RUN pip install flask
# Legt das Arbeitsverzeichnis im Container fest
WORKDIR /app
# Kopiert das lokale Python-Skript (Flask-App) in den Container
COPY app.py /app
# Definiert den Startbefehl: führe "python app.py" aus, wenn der Container gestartet wird
ENTRYPOINT ["python"]
CMD ["app.py"]
```
-  Was macht dieses Dockerfile?
  Es erstellt ein leichtgewichtiges Image mit Flask.
  DUnsere App (app.py) wird in den Container kopiert und beim Start automatisch ausgeführt. 
  So wird sichergestellt, dass der Container immer direkt deine Flask-Webanwendung startet.


### Container bauen & starten

```bash
# Erstellt ein Docker-Image mit dem Namen "webapp" basierend auf dem Dockerfile im aktuellen Verzeichnis (.)
sudo docker build -t webapp .
# Startet einen Container im Hintergrund (-d) und leitet Port 5000 vom Container auf Port 5000 des Raspberry Pi weiter
sudo docker run -p 5000:5000 -d webapp
# Zeigt eine Liste aller laufenden Container – inklusive Container-ID, Namen und Ports
sudo docker ps
```

### Test im Browser

```text
http://192.168.24.101:5000/todo-lists
```
- Was passiert hier?
  Wenn alles korrekt eingerichtet wurde, erreichen wir unsere Flask-Anwendung über die IP-Adresse des Raspberry Pi.
---

## Ergebnis

Die Webanwendung wurde erfolgreich in einem Docker-Container auf dem Raspberry Pi gestartet. Beim Aufruf der API-Endpunktadresse /todo-lists im Browser wird eine korrekte Antwort angezeigt – damit ist die Grundfunktion der Anwendung verifiziert.
Das vollständige Setup (vom Flashen der SD-Karte über Netzwerkkonfiguration bis hin zum Containerbetrieb) wurde remote über SSH durchgeführt – ganz ohne grafische Oberfläche.

- Vorteile des Setups:
  Modular und portabel durch den Einsatz von Docker
  Sicher durch SSH-Zugriff und Benutzerrollen
  Erweiterbar für zukünftige Webservices oder APIs
---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details siehe License.txt (in Repository).

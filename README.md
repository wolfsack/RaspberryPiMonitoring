# RaspberryPiMonitoring

On the RaspberryPi:

    git clone https://github.com/wolfsack/RaspberryPiMonitoring.git
    cd RaspberryPiMonitoring
    bash setup.sh
    docker-compose up -d
 
# Demo

Hier gibt es eine laufende [Demo](http://wutterfly.com/grafana).

    username: user
    password: user

 # How it was made


Das Projekt besteht aus drei Teilen:
    
    - einem Python Server welcher Daten über den Pi erhebt und bereitstellt
    - einem Prometheus Server welcher die Daten sammelt
    - einem Graphana Server welcher sich die Daten vom Prometheus Server holt und hübsch anzeigt

Grundsätzlich können alle 3 Server auf verschiedenen Machinen laufen, wichtig ist nur das der Python Server auf dem RaspberryPi läuft.

In diesem Projekt werden alle drei Server als Docker Container bereitgestellt.

----
## Der Python Server

Der Python Server läuft auf dem RaspberryPi und soll Daten über den Pi abfragen können und als WebSite darstellen.

Um eine WebSite mit Python zu erstellen bietet sich das Mini-Framework Flask an. 

Folgende Abhängigkeiten werden in diesem Projekt gebraucht:

    Flask==2.0.2 # Framework zum erstellen von HTTP-Server Anwendungen
    psutil==5.8.0 # Paket zum sammeln von System Daten
    waitress==2.0.0 # WSGI Server um Flask in einer Production Umgebung zu starten

Der Einstiegspunkt für die Flask App ist die Datei [app.py](./exporter/app/app.py). Hier wird eine FlaskApp erstellt und ein HTTP-Endpoint regestriert. Der Pfad des Endpoints kann dabei beliebig gewählt werden.

In der Methode die beim abfragen des Endpoints aufgerufen wird, wird zunächst ein HTTP-Response Objekt mit dem Status-Code 200 erstellt. Der Inhalt des Response Objekts sind die Daten welche wir über den RaspberryPi erheben wollen als String. Anschließen wird der [Mime-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) der Antwort auf "text/plain" gesetzt. Die Formatierung der Daten als auch der Response-Type sind wichtig, da Prometheus die Daten parsen muss. Zuletzt wird die Antwort zurück geschickt.

Das sammeln der gewünschten Daten passiert in der Funktion "metrics" in [metrics.py](./exporter/app/metrics.py).

Auf den meisten (und auch auf meinem) RaspberryPis läuft ein Linux basiertes OS. Um Metriken über das System und Hardware zu erhalten werden Dateien in dem Ordner "/proc" ausgelesen. Daher ist es wichtig psutil mitzuteilen wo dieser Ordner ist.

 Hier werden zunächst alle Daten gesammelt, und dann in  "Metrics" Objekte verpackt. Die "Metrics" Klasse aus [metric.py](./exporter/app/metric.py) macht es einfacher einzelne Daten formatiert als String auszugeben. Wie genau eine Metric formatiert werden muss ist von Prometheus vorgegeben und kann [hier](https://prometheus.io/docs/instrumenting/writing_exporters/) nachgelesen werden. Alternativ kann auch ein Python Package verwendet werden, statt die Formatierung selber zu schreiben. Die "Metric" Objekte werden in einer Liste gesammelt und in der Funktion "generate_metrics" aus [metrics.py](./exporter/app/metrics.py) in einen String formatiert. Diese kann dann in einer HTTP-Response verwendet werde.

Im Momement werden folgende Metriken gesammlt:

    cpu_usage -> CPU Last
    cpu_cores -> Nummer der CPU Kerne
    memory_usage -> Arbeitsspeicher Last
    boot_time -> Zeitpunkt an dem der Pi gestarted wurde
    system_time -> Zeitpunkt der Abfrage
    tcp_connections -> Anzahl der TCP Verbindungen
    partitions -> Partitionen
    cpu_temperature -> CPU Temperatur

Zusätzlich zu dem Typ und dem Namen der Metrik können auch noch Tags definiert werden, welche die Metrik näher spezifizeren.

Folgende Tags gibt es:

- für "cpu_cores":
  - "type":
    - "all" -> alle CPU Kerne die das System erkennt
    - "physical" -> nur physische CPU Kerne

- für "memory_usage":
  - "type":
    - "total" -> größe des Arbeitsspeichers
    - "available" -> verfügbarer Arbeitsspeicher
    - "used" -> genutzter Arbeitsspeicher
    - "free" -> freier Arbeitsspeicher

  (Näheres zur Klassifizierung von Arbeitsspeicher kann [hier](https://haydenjames.io/free-vs-available-memory-in-linux/) gefunden werden.)
  
Alle Metriken haben zusätzlich einen Tag "node". Dieser gibt die Nummber des RaspberryPis an. Diese ist nützlich falls meherer Pis überwacht werden sollen. Dies macht es möglich die Metriken zu gruppieren.

Die Flask App ist hiermit schon fertig. Flask bietet zum erstellen einer Flask App einen Development Server bereit, diese ist jedoch nicht für eine Production Umgebung geeignet. 

Eine Flask App bietet jedoch auch ein WSG Interface, welches von WSGI Servern genutzt werden kann. Ein solcher Server ist "waitress".

Damit "waitress" die Flask App nutzen kann wird ein Python file [wsgi.py](./exporter/wsgi.py) erstellt. Wichtig ist hier nur der import Teil.

Nun kann die App mit

    waitress-serve --listen=*:5000 wsgi:app

auf port 5000 gestartet werden.

Zu letzt wird die Python App noch in ein Dockerfile verpackt.

Als BaseImage wird "Python:3.9" genutzt. Anschließend werden die nötigen Abhängigkeiten mit pip installiert, die Python Datei in das Image Copiert und waitress als Entrypoint festgelegt. Sollte das DockerImage nun als Container gestartet werden, startet automatisch die Flask App.

----
## Prometheus

Prometheus ist ein Programm zum sammeln und speichern von Zeitreihen-Daten. Auf DockerHub wird ein DockerImage für Prometheus bereitgestellt. Es müssen nur noch Ziele konfiguriert werden, welche Prometheus abfragen soll.

In der [prometheus.yml](./prometheus/prometheus.yml) Konfigurations Datei wird als Ziel die FlaskApp angegeben.

    scrape_configs:
      - job_name: 'raspberry-1'
        metrics_path: /node/1/metrics
        scrape_interval: 5s
        static_configs:
          - targets: ['wutterfly.com']

Als job_name kann ein beliebiger Name gewählt werden.

Der metrics_path ist vom Deployment der Flask App abhängig. Wenn kein ReverseProxy oder ähnliches verwendet wird welcher den Request Pfad ändert, muss hier der Pfad zum HTTP-Endpoint angegeben werden welcher in der FlaskApp ("@app.route('/node/1/metrics')") angegben wurde.

Der scrape_interval legt fest in welchem Interval an dem Ziel Daten gesammelt werden soll.

Und unter static_config > targets wird der host und port festgelegt unter dem das Ziel zu finden ist. Das kann eine Domain, aber auch eine IP-Addresse sein. 

Achtung mit Localhost. Da sich Prometheus in einem DockerContainer befindet funktionier Localhost nicht, auch wenn der Flask DockerContainer auf der gleichen Maschine läuft. Dafür kann hier aber auch Docker DNS genutzt werden.

----
## Graphana

Graphana ist ein Programm welches Daten aus einer Datenquelle, hier Prometheus, abfragt und in Graphen und ähnlichem anzeigt.

Auch für Graphana gibt es bereits ein DockerImage auf DockerHub.

Graphana ist ein wenig komplizierter zu konfigurieren als Prometheus.

Hier gibt es verschiedene Wege Graphana zu konfigurieren. In diesem Projekt wird ein eigenes DockerImage gebaut welches alle Dashbords und Datenquellen Konfigurationen enthält.

In der [grafana.ini](./grafana/grafana.ini) Datei werden algemeine Konfigurationen eingetragen.

In dem Ordner [provisioning](./grafana/provisioning/) gibt es die beiden Ordner [dashboards](./grafana/provisioning/dashboards/) und [datasources](./grafana/provisioning/datasources/).

In dem Ordner [dashboards](./grafana/provisioning/dashboards/) werden Konfigurations Dateien hinterlegt welche beschreiben welche Dashboards es gibt. Die konkreten Dashboards werden als JSON Datei im Order [dashboards](./grapahana/dashboards) hinterlegt.

Tipp: Dashboards können in der Graphana GUI erzeugt und als JSON exportiert werden.

In dem Ordner [datasources](./grafana/provisioning/datasources/) werden Konfigurations Dateien hinterlegt welche beschreiben welche Datenquellen es gibt. Hier wird als Datenquelle der Prometheus Server angegben.

In dem Dockerfile wird als "grafana/grafana:8.2.1" gewählt, und anschließend die Order [provisioning](./grafana/provisioning/) und [dashboards](./grapahana/dashboards) hinzugefügt. Zusätzlich können über Umgebungs Variablen zusätzliche Konfigurationen getätigt werden.

----
## All in One  - DockerCompose

Um alle Server auf einmal zu starten und um zusätzliche Konfiguration so einfach zu möglich zu machen wird DockerCompose genutzt.

Als Services wird die FlaskApp, Prometheus und Graphana angegeben.

In der FlaskApp ist es wichtig das der "/proc" Ordner in den Container gemountet wird. Über die Umgebungsvariable "ROOT_FS" wird der FlaskApp mitgeteilt wo im Container der "/proc" Ordner ist. Als Image wird das  FlaskApp DockerFile angegeben. Zuletzt wird noch der Port 5000 freigegeben damit Anfragen von außerhalb in den Container gelangen können.

Für den Prometheus Service muss nur der Port 9090 freigegeben werden und die Konfigurations Datei [prometheus.yml](./prometheus/prometheus.yml) in den Container gemounted werden. Zusätzlich wird noch ein Volume bereitgestellt in dem Prometheus die gesammelten Daten persistent speichern kann.

Für den Graphana Service muss der Port 3000 freigeben werden. Zusätzlich wird noch ein Volume bereit gestellt in dem Graphana entstehende Daten persistent speichern kann, als auch der Admin Nutzername und Password über Umgebungsvariablen gesetzt.

Mit 

    docker-compose up -d

können so alle 3 Services gleichzeitig im Hintergrund gestartet werden.

----
## Volumes und Rechte

In der DockerCompose Datei wurden einige Volumes festgelegt in dem Programm e Daten persistent speichern können. Volumes sind in dem Fall Order in dem Daten gespeichert werden können. Sollten diese Order noch nicht existieren werden sie automatisch von Docker erstellt.

Dies kann jedoch zu Problemen führen, wenn die Programme in den DockerContainern nicht die Rechte haben neue Datei anzulegen oder diese zu bearbeiten.

Da ich Linux nur nutze wenn es sein muss und mich nie wirklich mit dem System hinter Berechtigungen und Besitz von Ordnern und Datei beschäftigt habe, gibt es ein einfaches [Script](./setup.sh) welches vor dem ersten Aufruf der DockerCompose Datei die benötigten Order mit entsprechenden Rechten erstellt. 

Dies ist zwar eine Lösung die Funktioniert, sollte jedoch noch überarbeitet werden.



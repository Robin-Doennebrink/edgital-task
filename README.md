# backend_task_02
Die Aufgabe setzt sich aus drei Teilaufgaben zusammen, die alle bearbeitet werden müssen. Ziel ist die Erstellung einer einfachen Rest-API zur Verwaltung von Straßennetzen. Zur Aufgabenbearbeitung befinden sich hierzu beigefügt drei Beispiel-Straßennetze (Knoten-Kanten-Modelle) im GeoJSON-Format.
## Aufgabe 1
Die ersten beiden Straßennetze sollen über einen Endpunkt hochgeladen und in einer PostgreSQL Datenbank gespeichert werden können. Da die Straßennetze im Wesentlichen aus Geometrien bestehen, ist die Nutzung einer Geo-Erweiterung wie PostGIS zu empfehlen, um die Daten effizient speichern zu können. Da die Straßennetze zu unterschiedlichen Kunden gehören müssen sie über ein entsprechendes Attribut verfügen, um eine einfache Authorisierung zu ermöglichen.
## Aufgabe 2
Das dritte Straßennetz stellt eine aktualisierte Version des zweiten Netzes dar. Über einen weiteren Endpunkt soll es möglich sein, ein Update durchzuführen indem die aktualisierte Version des Netzes hochgeladen wird. Bei einem Update sollen die ursprünglichen Kanten nicht gelöscht werden, sondern nur als nicht aktuell gekennzeichnet werden.
## Aufgabe 3
Die Kanten der Straßennetze sollen über einen weiteren Endpunkt im GeoJSON Format abgerufen werden können. Der Endpunkt soll nur die Kanten des angegebenen Netzes eines jeweils authentifizierten Kunden zurückgeben. Über einen Parameter soll zudem angegeben werden können, welchem Zeitpunkt das Netz entsprechen soll. D.h. Netz 2 soll in seinem Zustand vor und nach Update abgerufen werden können.
## Vorgaben
1. Als API-Framework soll Flask oder FastAPI zu verwenden, während die Datenbank mittels Postgres zu realisieren ist.
2. Eine README.md soll die Anwendung sowie die Herangehensweise an die Aufgabenstellung dokumentieren.
3. Die Lösung muss zwingend containerisiert und mittels Docker-Compose ausführbar sein.

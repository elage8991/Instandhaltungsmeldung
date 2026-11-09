# Product Requirements Document (PRD)

**Titel:** Instandhaltungsmeldung AI Agent  
**Datum:** 2026-11-09  
**Eigentümer:** Facility Management / Asset Management  
**Solution Category:** AI Agent

---

## Produktzweck & Wertversprechen

**Elevator Pitch:**  
Nutzer verschiedener Rollen melden Schäden an Gebäuden oder technischen Anlagen heute über SAP Fiori — ein komplexes Werkzeug, das SAP-Kenntnisse voraussetzt. Der Instandhaltungsmeldung AI Agent führt jeden Nutzer in einem einfachen, natürlichsprachlichen Dialog durch den Meldeprozess: Er findet den richtigen technischen Platz, prüft die Vollständigkeit der Beschreibung, bereitet Texte auf und legt die Meldung direkt in SAP S/4HANA an.

**Geschäftlicher Bedarf:**  
Aktuell sind 30 % aller Instandhaltungsmeldungen unvollständig. Das führt zu Rückfragen, Verzögerungen und erhöhtem manuellem Aufwand beim Instandhaltungsteam. Ein dialogbasierter Agent senkt die Fehlerquote, indem er Vollständigkeit aktiv prüft und Nutzer ohne SAP-Kenntnisse sicher durch den Prozess führt.

**Erwarteter Nutzen:**  
Steigerung der Vollständigkeitsrate von Meldungen von 70 % auf ≥ 95 %, Reduktion von Rückfragen und Bearbeitungsaufwand, sowie Verbesserung der Nutzerzufriedenheit durch einfache Bedienung.

**Produktziele (priorisiert):**
1. Vollständigkeit sicherstellen: ≥ 95 % der über den Agent angelegten Meldungen sind auf Anhieb vollständig.
2. Nutzbarkeit für alle Rollen: Kein SAP-Wissen erforderlich; Nutzung in natürlicher Sprache.
3. Mehrsprachigkeit: Eingaben in beliebiger Sprache werden akzeptiert; Meldungstexte in S/4HANA werden auf Deutsch generiert.

---

## Business Metrics

| Metrik | Baseline | Ziel | Zeitrahmen | Prozess / Fähigkeit | Quelle |
|--------|----------|------|------------|---------------------|--------|
| Vollständigkeitsrate Instandhaltungsmeldungen | 70 % vollständig | ≥ 95 % vollständig | — | Instandhaltungsmeldung anlegen (SAP PM) | user |

---

## Nutzerprofile & Personas

### Primäre Persona: Klaus – Hausmeister vor Ort

Klaus, 45, ist Hausmeister in einem Wohnkomplex mit 200 Einheiten. Er erledigt täglich Kontrollrunden und nimmt Störungsmeldungen von Mietern entgegen. Er nutzt sein Mobiltelefon, hat aber kaum SAP-Erfahrung. Wenn er einen Schaden sieht oder gemeldet bekommt, muss er eine Meldung erfassen — bisher über SAP Fiori, was er als umständlich empfindet. Er möchte eine Meldung schnell und richtig absetzen können, ohne lange zu suchen oder Felder zu kennen.

### Sekundäre Persona: Maria – Mieterin

Maria, 38, wohnt im Erdgeschoss. Sie bemerkt einen Wasserschaden im Treppenhaus. Sie hat keinen SAP-Zugang und möchte den Schaden unkompliziert melden. Sie kommuniziert auf Spanisch. Sie erwartet, dass ihre Meldung ankommt und bearbeitet wird.

### Weitere Nutzertypen

- **Instandhaltungsplaner:** SAP-erfahren, nutzt den Agent gelegentlich für schnelle Meldungen ohne Fiori-Navigation.
- **Facility Manager:** Überblick über Objekte; nutzt den Agent selten, erwartet korrekte Datenlage in S/4HANA.

---

## Nutzer-Ziele & Aufgaben

### Für Klaus (Hausmeister):

**Ziele:**
- Schaden schnell und korrekt als Meldung in SAP erfassen
- Keine SAP-Transaktionskenntnisse benötigen

**Aufgaben:**
- Objekt oder Adresse nennen, passenden technischen Platz bestätigen
- Schaden beschreiben (Ort, Art, Beginn, Gefährdung)
- Zusammenfassung prüfen und Meldung bestätigen

### Für Maria (Mieterin):

**Ziele:**
- Schaden in ihrer Sprache melden können
- Bestätigung erhalten, dass die Meldung angekommen ist

**Aufgaben:**
- Schadensbeschreibung in natürlicher Sprache eingeben
- Rückfragen des Agents beantworten

---

## Produktprinzipien

1. **Dialog vor Formular:** Der Agent stellt gezielte Fragen statt komplexe Formulare zu präsentieren.
2. **Vollständigkeit zuerst:** Der Agent legt keine unvollständige Meldung an — er fragt solange nach, bis alle Pflichtinformationen vorliegen.
3. **Sprache des Nutzers:** Der Agent kommuniziert in der Sprache des Nutzers; SAP-Daten werden immer auf Deutsch erzeugt.
4. **Mensch behält die Kontrolle:** Der Agent zeigt vor dem Anlegen immer eine Zusammenfassung zur Bestätigung.
5. **Einfachheit vor Vollständigkeit:** Nur das Nötigste fragen — keine überflüssigen Felder.

---

## Geschäftskontext

**Aktueller Zustand:**  
Meldungen werden über SAP Fiori (Transaktion IW21 bzw. entsprechende Fiori-App) erfasst. Der Prozess erfordert Kenntnisse zu technischen Plätzen, Meldungsarten und Feldstrukturen. Resultat: 30 % unvollständige Meldungen, Rückfragen und Verzögerungen.

**Strategische Ausrichtung:**  
Digitalisierung des Facility Managements; Reduktion manueller Fehler; Verbesserung der Datenqualität in SAP PM für verlässliche Instandhaltungsplanung.

---

## Ziele & Nicht-Ziele

### Ziele (Im Scope)

- Geführte Anlage von Instandhaltungsmeldungen (Meldungsart M1) in SAP S/4HANA Cloud Private Edition
- Live-Suche nach technischen Plätzen über SAP API
- Vollständigkeitsprüfung und Textaufbereitung durch den Agenten
- Mehrsprachige Dialogführung mit Deutschen Ausgabetexten für SAP
- Prioritäts-, Ausfallkennzeichen- und Terminvorschlag

### Nicht-Ziele (Außerhalb des Scope)

- Bearbeitung, Abschluss oder Auswertung von Meldungen
- Anlage von Wartungsaufträgen oder Arbeitsplänen
- Eigene Fiori/UI5-Oberfläche
- Push-Benachrichtigungen oder Statusverfolgung nach Anlage
- Verwaltung von Stammdaten (technische Plätze, Materialien)

---

## Anforderungen

### Must-Have-Anforderungen

**REQ-01: Technischen Platz ermitteln**

- **Problem:** Nutzer kennen das SAP-Strukturkennzeichen (ZTP) nicht; sie kennen Adressen oder Gebäudebezeichnungen.
- **User Story:** Als Nutzer möchte ich einen Ort per Adresse oder Bezeichnung nennen können, damit der Agent den richtigen technischen Platz findet und ich ihn bestätigen kann.
- **Akzeptanzkriterien:**
  - Der Agent fragt nach Objekt oder Adresse.
  - Er ruft die S/4HANA API auf und gibt passende technische Plätze zurück.
  - Der Nutzer wählt einen aus oder korrigiert die Eingabe.
  - Erst nach Bestätigung geht der Agent weiter.
- **Priorität:** 1

**REQ-02: Schadensbeschreibung aufnehmen und auf Vollständigkeit prüfen**

- **Problem:** Meldungen sind oft unvollständig, weil Nutzern unklar ist, welche Informationen benötigt werden.
- **User Story:** Als Nutzer möchte ich mein Problem frei beschreiben können, damit der Agent fehlende Informationen gezielt nachfragt.
- **Akzeptanzkriterien:**
  - Der Agent prüft, ob Ort (Geschoss/Raum), Schadensart, Beginn der Störung und Gefährdung/Nutzungseinschränkung vorhanden sind.
  - Für jeden fehlenden Aspekt stellt der Agent eine gezielte Nachfrage.
  - Erst wenn alle Pflichtfelder gefüllt sind, geht der Agent weiter.
- **Priorität:** 2

**REQ-03: Text aufbereiten**

- **Problem:** Rohbeschreibungen sind oft unklar, zu lang oder in einer anderen Sprache als Deutsch.
- **User Story:** Als Instandhaltungsplaner möchte ich Meldungen mit klarem Kurztext und strukturiertem Langtext erhalten, damit ich sofort handeln kann.
- **Akzeptanzkriterien:**
  - Der Agent erzeugt einen Kurztext mit maximal 40 Zeichen auf Deutsch.
  - Der Agent erzeugt einen strukturierten Langtext auf Deutsch.
  - Eingaben in anderen Sprachen werden ins Deutsche übersetzt.
  - Unklare oder fehlerhafte Formulierungen werden verständlich umformuliert.
- **Priorität:** 3

**REQ-04: Werte vorschlagen**

- **Problem:** Nutzer kennen SAP-PM-Felder wie Priorität oder Ausfallkennzeichen nicht.
- **User Story:** Als Nutzer möchte ich, dass der Agent Priorität, Ausfallkennzeichen und Beginn-Termin automatisch vorschlägt, damit ich diese Felder nicht kennen muss.
- **Akzeptanzkriterien:**
  - Der Agent schlägt einen Prioritätswert vor (basierend auf Gefährdung und Schadensart).
  - Der Agent schlägt ein Ausfallkennzeichen vor.
  - Der Agent schlägt einen Beginn-Termin vor.
  - Der Nutzer kann Vorschläge übernehmen oder ändern.
- **Priorität:** 4

**REQ-05: Bestätigen und Meldung anlegen**

- **Problem:** Nutzer wollen Kontrolle behalten und keine falschen Meldungen in SAP anlegen.
- **User Story:** Als Nutzer möchte ich vor dem Anlegen eine Zusammenfassung sehen und bestätigen, damit keine Fehler passieren.
- **Akzeptanzkriterien:**
  - Der Agent zeigt alle gesammelten Daten in einer Zusammenfassung an.
  - Erst nach Nutzerbestätigung legt der Agent die Meldung an.
  - Nach Anlage gibt der Agent die Meldungsnummer aus S/4HANA zurück.
  - Im PoC-Modus kann die Anlage auch simuliert werden.
- **Priorität:** 5

**REQ-06: Mehrsprachige Dialogführung**

- **Problem:** Nutzer (z. B. Mieter) kommunizieren nicht auf Deutsch.
- **User Story:** Als nicht deutschsprachiger Nutzer möchte ich den Agenten in meiner Sprache verwenden können.
- **Akzeptanzkriterien:**
  - Der Agent erkennt die Eingabesprache und antwortet in derselben Sprache.
  - Alle in SAP gespeicherten Texte (Kurztext, Langtext) werden auf Deutsch generiert.
- **Priorität:** 6

---

## Lösung & Architektur

**Architekturübersicht:**  
Ein Python AI Agent (A2A-Protokoll) führt den Dialog mit dem Nutzer. Er greift über einen MCP-Server (MCP Translation File) auf die SAP S/4HANA API `API_MAINTNOTIFICATION` (OData v2) zu, um technische Plätze zu suchen und Meldungen anzulegen. Der Agent nutzt ein Large Language Model (LLM) via SAP Generative AI Hub für Textaufbereitung, Übersetzung und Vollständigkeitsprüfung.

**Schlüsselkomponenten:**

- **AI Agent (Python, A2A):** Konversationslogik, Vollständigkeitsprüfung, Textaufbereitung, Prioritätsvorschlag
- **MCP Translation File für `API_MAINTNOTIFICATION`:** Abstraktionsschicht für die S/4HANA OData API
- **SAP S/4HANA Cloud Private Edition:** Quell- und Zielsystem (technische Plätze, Meldungsanlage)
- **SAP Generative AI Hub:** LLM-Laufzeitumgebung für den Agenten

**Integrationspunkte:**

- S/4HANA `API_MAINTNOTIFICATION` (OData v2): Lesen von technischen Plätzen, Anlegen von Meldungen (schreibend)

---

### Agent Extensibility & Instrumentation

**Agent-Erweiterbarkeit:**
- Der Agent ist als erweiterbare Python-Anwendung gebaut; neue Meldungsarten oder zusätzliche Validierungsregeln können als separate Module ergänzt werden.
- Der Konversationsfluss ist konfigurierbar, sodass neue Pflichtfelder hinzugefügt werden können, ohne den Kern zu ändern.

**Business Step Instrumentation:**
- Jeder der fünf Prozessschritte emittiert strukturierte Log-Einträge für Monitoring und Debugging.
- Log-Format: `[MILESTONE_ID].[achieved|missed]: [Beschreibung]`
- Alle Milestone-Logs sind maschinenlesbar und können in SAP AI Launchpad / OpenTelemetry-kompatible Systeme geleitet werden.

---

### Automation & Agent Behaviour

**Automatisierungsgrad:** Hybridagent – LLM-gesteuerte Konversation mit definierten Prozessschritten

**Aktionen ohne Nutzerbestätigung:**
- Technische Plätze über API suchen
- Textaufbereitung und Übersetzung
- Prioritäts- und Terminvorschlag berechnen

**Aktionen mit Nutzerbestätigung (Human-in-the-Loop):**
- Auswahl des technischen Platzes
- Anlage der Meldung in S/4HANA (nach Zusammenfassung)

**Modell:** LLM via SAP Generative AI Hub

**Wissens- und Datenquellen:**
- SAP S/4HANA Cloud Private Edition: technische Plätze, Meldungsanlage
- Nutzereingaben im Dialog

**Eingesetzte Tools / Konnektoren:**
- `API_MAINTNOTIFICATION` MCP Tool (search_functional_locations): Suche nach technischen Plätzen anhand von Adresse/Bezeichnung (lesend)
- `API_MAINTNOTIFICATION` MCP Tool (create_maintenance_notification): Anlage der Meldung in S/4HANA (schreibend, hochrisikant – erst nach Nutzerbestätigung)

**Guardrails & Fail-Safes:**
- Die Meldung wird nie ohne explizite Nutzerbestätigung angelegt.
- Bei mehrdeutigen Suchergebnissen (>5 technische Plätze) bittet der Agent um Präzisierung statt zu raten.
- Unvollständige Meldungen werden nicht abgesendet.
- Fallback: Bei API-Fehler informiert der Agent den Nutzer und schlägt manuelle Anlage vor.

---

## Meilensteine

### M1: Technischer Platz ermittelt

- **Beschreibung:** Der Nutzer hat einen technischen Platz (ZTP) aus den Suchergebnissen ausgewählt und bestätigt.
- **Erreicht wenn:** Die Struktur-ID des technischen Platzes liegt im Kontext vor und der Nutzer hat bestätigt.
- **Log bei Erreichen:** `M1.achieved: functional_location identified and confirmed by user`
- **Log bei Nichterreichen:** `M1.missed: functional_location could not be determined or not confirmed`

### M2: Schadensbeschreibung vollständig

- **Beschreibung:** Alle Pflichtaspekte der Schadensbeschreibung wurden erhoben (Ort, Schadensart, Beginn, Gefährdung).
- **Erreicht wenn:** Agent hat alle vier Pflichtfelder mit Nutzerantworten gefüllt.
- **Log bei Erreichen:** `M2.achieved: damage description complete with all mandatory fields`
- **Log bei Nichterreichen:** `M2.missed: one or more mandatory description fields missing after follow-up`

### M3: Text aufbereitet

- **Beschreibung:** Kurztext (≤ 40 Zeichen) und strukturierter Langtext auf Deutsch wurden durch den Agenten erzeugt.
- **Erreicht wenn:** Beide Texte liegen im Kontext vor und haben das korrekte Format.
- **Log bei Erreichen:** `M3.achieved: short_text and long_text generated in German`
- **Log bei Nichterreichen:** `M3.missed: text preparation failed or output format invalid`

### M4: Werte vorgeschlagen

- **Beschreibung:** Priorität, Ausfallkennzeichen und Beginn-Termin wurden vom Agenten vorgeschlagen.
- **Erreicht wenn:** Alle drei Felder haben einen Wert (Vorschlag oder Nutzeranpassung).
- **Log bei Erreichen:** `M4.achieved: priority, breakdown_indicator, and start_date proposed`
- **Log bei Nichterreichen:** `M4.missed: value proposal incomplete`

### M5: Meldung angelegt

- **Beschreibung:** Die Instandhaltungsmeldung wurde erfolgreich in SAP S/4HANA angelegt.
- **Erreicht wenn:** API-Antwort enthält eine Meldungsnummer und kein Fehler liegt vor.
- **Log bei Erreichen:** `M5.achieved: maintenance_notification created with id={notification_id}`
- **Log bei Nichterreichen:** `M5.missed: notification creation failed — reason={error_message}`

---

## Risiken, Annahmen und Abhängigkeiten

### Risiken

- **API-Zugang:** Die `API_MAINTNOTIFICATION` muss aus der BTP-Laufzeitumgebung erreichbar sein und entsprechende Berechtigungen besitzen.
- **Mehrdeutige technische Plätze:** Bei unklaren Adressen liefert die API viele Treffer — der Dialog kann länger dauern.
- **LLM-Qualität bei Übersetzungen:** In Randsprachen kann die Übersetzungsqualität variieren.

### Annahmen

- SAP S/4HANA Cloud Private Edition ist verfügbar und die API `API_MAINTNOTIFICATION` ist freigeschaltet.
- Die technischen Plätze sind in S/4HANA mit aussagekräftigen Bezeichnungen gepflegt.
- Der Agent wird über SAP Generative AI Hub mit einem geeigneten LLM betrieben.

### Abhängigkeiten

- MCP Translation File für `API_MAINTNOTIFICATION` muss generiert und deployt sein.
- SAP BTP-Laufzeitumgebung (AI Launchpad / Agent Runtime) muss bereitgestellt sein.

---

## Anhang

### Glossar

- **ZTP:** Strukturkennzeichen eines technischen Platzes in SAP PM
- **API_MAINTNOTIFICATION:** SAP OData API v2 für Instandhaltungsmeldungen
- **A2A:** Agent-to-Agent Protokoll — standardisiertes Kommunikationsprotokoll für KI-Agenten in SAP Joule Studio
- **MCP:** Model Context Protocol — Schnittstellenstandard für Tool-Anbindung von KI-Agenten
- **Kurztext:** Maximal 40-Zeichen-Bezeichnung der Meldung in SAP PM
- **Langtext:** Freitextbeschreibung der Meldung in SAP PM

### Referenzen

- SAP Help: API_MAINTNOTIFICATION (OData v2)
- SAP S/4HANA Cloud Private Edition — Plant Maintenance (PM)
- SAP Joule Studio — Agent Development Guidelines

---
name: instandhaltungsmeldung
description: Geführter fünfstufiger Dialog zum Anlegen einer SAP PM Instandhaltungsmeldung – technischen Platz ermitteln, Schaden aufnehmen, Text aufbereiten, Werte vorschlagen, Meldung anlegen.
allowed-tools: all
---

# Instandhaltungsmeldung anlegen – Geführter Dialog

## Wann diesen Skill verwenden

Lade diesen Skill wenn der Nutzer einen Schaden melden, eine Instandhaltungsmeldung anlegen oder ein Problem an einem Gebäude oder technischen Objekt erfassen möchte.

## Sprachregeln

- Antworte immer in der Sprache des Nutzers (Deutsch, Englisch, Spanisch, etc.).
- Alle SAP-Felder (Kurztext, Langtext) werden **immer auf Deutsch** generiert, unabhängig von der Dialogsprache.
- Übersetze Nutzereingaben bei Bedarf ins Deutsche für die SAP-Felder.

---

## Schritt 1: Technischen Platz ermitteln

### Ziel
Den korrekten technischen Platz (Funktionaler Standort / Strukturkennzeichen ZTP) in SAP identifizieren und vom Nutzer bestätigen lassen.

### Vorgehen

1. Frage den Nutzer nach dem Objekt oder der Adresse des Schadens (z. B. „Beeskowdamm 3", „Hauptgebäude", „Halle B").
2. Rufe das Suchwerkzeug für technische Plätze auf (suche nach `FunctionalLocation` über die Bezeichnung / Adresse).
3. Zeige die gefundenen technischen Plätze als nummerierte Liste an (Name, Beschreibung, Standort).
4. Bitte den Nutzer, einen Eintrag auszuwählen oder die Eingabe zu verfeinern.

### Regeln

- Werden mehr als 5 Treffer zurückgegeben, bitte um eine präzisere Eingabe.
- Gehe nur weiter, wenn der Nutzer explizit einen technischen Platz bestätigt hat.
- Speichere die `FunctionalLocation`-ID für alle folgenden Schritte.

### Meilenstein-Log

```
M1.achieved: functional_location identified and confirmed by user
M1.missed: functional_location could not be determined or not confirmed
```

---

## Schritt 2: Schadensbeschreibung aufnehmen und prüfen

### Ziel
Eine vollständige Schadensbeschreibung erhalten, die alle vier Pflichtaspekte enthält.

### Pflichtaspekte

| Nr | Aspekt | Beispiel |
|----|--------|---------|
| 1 | **Ort** | „2. OG, Raum 204", „Treppenhaus links" |
| 2 | **Schadensart** | „Wasserschaden", „defekte Leuchte", „gerissene Fuge" |
| 3 | **Beginn der Störung** | „seit gestern Abend", „seit Montag", „heute morgen entdeckt" |
| 4 | **Gefährdung / Nutzungseinschränkung** | „Rutschgefahr vorhanden", „Raum nicht nutzbar", „keine Einschränkung" |

### Vorgehen

1. Fordere den Nutzer auf, den Schaden frei zu beschreiben.
2. Prüfe die Eingabe auf alle vier Pflichtaspekte.
3. Für jeden fehlenden Aspekt stelle eine gezielte Nachfrage (nicht generisch, sondern konkret zum fehlenden Aspekt).
4. Erst wenn alle vier Aspekte vorliegen, gehe weiter zu Schritt 3.

### Beispiel-Nachfragen

- Ort fehlt: „An welcher genauen Stelle ist der Schaden? (Geschoss, Raum oder Bereich)"
- Schadensart fehlt: „Wie würden Sie den Schaden beschreiben? (Was ist defekt oder beschädigt?)"
- Beginn fehlt: „Wann wurde die Störung erstmals bemerkt?"
- Gefährdung fehlt: „Besteht eine Gefährdung oder Nutzungseinschränkung? (z. B. Rutschgefahr, Raum nicht nutzbar)"

### Meilenstein-Log

```
M2.achieved: damage description complete with all mandatory fields
M2.missed: one or more mandatory description fields missing after follow-up
```

---

## Schritt 3: Text aufbereiten

### Ziel
Einen SAP-konformen Kurztext (≤ 40 Zeichen) und einen strukturierten Langtext auf Deutsch erstellen.

### Kurztext-Regeln

- **Maximal 40 Zeichen** (harte Grenze – kürze wenn nötig)
- Prägnant: Schadensart + Ort (z. B. „Wasserschaden 2.OG Raum 204")
- Immer auf Deutsch
- Keine Sonderzeichen außer Bindestrich und Schrägstrich

### Langtext-Format (Deutsch)

```
Ort: <Geschoss/Raum/Bereich>
Schaden: <Schadensart und Beschreibung>
Beginn: <Datum/Zeitpunkt der Störung>
Gefährdung: <Ja/Nein – genaue Beschreibung>
Beschreibung: <Vollständige aufbereitete Beschreibung>
```

### Regeln

- Unklare oder fehlerhafte Formulierungen werden professionell umformuliert.
- Eingaben in anderen Sprachen werden ins Deutsche übersetzt.
- Zeige dem Nutzer den generierten Kurztext und Langtext zur Prüfung an.

### Meilenstein-Log

```
M3.achieved: short_text and long_text generated in German
M3.missed: text preparation failed or output format invalid
```

---

## Schritt 4: Werte vorschlagen

### Ziel
SAP PM-Felder (Priorität, Ausfallkennzeichen, Beginn-Termin) automatisch vorschlagen.

### Prioritäts-Ermittlung

Lade `references/prioritaet-regeln.md` und bestimme die Priorität:

| Priorität | SAP-Wert | Kriterium |
|-----------|----------|-----------|
| Sehr hoch | 1 | Gefährdung vorhanden (Personenschaden möglich) |
| Hoch | 2 | Nutzungseinschränkung vorhanden ODER sicherheitsrelevanter Schaden |
| Mittel | 3 | Schaden ohne direkte Nutzungseinschränkung, aber zeitnah zu beheben |
| Niedrig | 4 | Kosmetischer Schaden oder geringe Auswirkung |

### Ausfallkennzeichen

Lade `references/ausfallkennzeichen.md`:

| Kennzeichen | SAP-Wert | Kriterium |
|-------------|----------|-----------|
| Ausfall | X | Anlage / Raum ist ausgefallen oder nicht nutzbar |
| Kein Ausfall | (leer) | Betrieb läuft weiter, nur eingeschränkt oder kosmetisch |

### Beginn-Termin (RequiredStartDate)

| Priorität | Vorgeschlagenes Datum |
|-----------|-----------------------|
| 1 – Sehr hoch | Heute |
| 2 – Hoch | Heute |
| 3 – Mittel | Heute + 3 Werktage |
| 4 – Niedrig | Heute + 7 Werktage |

### Vorgehen

1. Ermittle Priorität, Ausfallkennzeichen und Datum wie oben beschrieben.
2. Zeige alle drei Vorschläge mit kurzer Begründung an.
3. Erlaube dem Nutzer, jeden Wert zu übernehmen oder zu ändern.

### Meilenstein-Log

```
M4.achieved: priority, breakdown_indicator, and start_date proposed
M4.missed: value proposal incomplete
```

---

## Schritt 5: Bestätigen und Meldung anlegen

### Ziel
Dem Nutzer eine vollständige Zusammenfassung zeigen, Bestätigung einholen und die Meldung in SAP anlegen.

### Zusammenfassung anzeigen

Zeige folgende strukturierte Übersicht (in der Sprache des Nutzers):

```
📋 Zusammenfassung der Instandhaltungsmeldung

Technischer Platz: <ZTP-ID + Bezeichnung>
Kurztext:          <max. 40 Zeichen>
Priorität:         <Wert + Beschreibung>
Ausfallkennzeichen: <Wert>
Beginn-Termin:     <Datum>

Langtext:
<vollständiger strukturierter Langtext>
```

### Bestätigung

- Frage den Nutzer explizit: „Soll die Meldung so angelegt werden?" (Ja / Nein / Änderungen)
- Lege die Meldung **nur nach expliziter Bestätigung** an.
- Bei Änderungswunsch: Gehe zum betreffenden Schritt zurück.

### Meldung anlegen

1. Rufe das Werkzeug zur Anlage einer Meldung auf (`MaintenanceNotification` – POST/Create) mit:
   - `FunctionalLocation`
   - `NotifShortText` (Kurztext, ≤ 40 Zeichen)
   - `Priority`
   - `MaintNotifLongTextForEdit` (Langtext)
   - `RequiredStartDate`
   - Ausfallkennzeichen (falls zutreffend)
2. Bei Erfolg: Gib die zurückgegebene Meldungsnummer aus.
3. Bei Fehler: Gib die exakte Fehlermeldung aus und frage ob der Nutzer es erneut versuchen möchte.

### Meilenstein-Log

```
M5.achieved: maintenance_notification created with id={notification_id}
M5.missed: notification creation failed — reason={error_message}
```

---

## Fehlerbehandlung

- API-Fehler werden immer im Originalwortlaut weitergegeben.
- Keine Erfindung von Daten oder Schätzung fehlender Werte.
- Bei unklaren API-Antworten den Nutzer informieren und manuelle Anlage via SAP Fiori vorschlagen.

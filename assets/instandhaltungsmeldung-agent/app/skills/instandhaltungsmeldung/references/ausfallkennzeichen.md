# Ausfallkennzeichen für Instandhaltungsmeldungen (SAP PM)

## SAP-Ausfallkennzeichen

| SAP-Wert | Bedeutung | Verwendung |
|----------|-----------|------------|
| `X` | Ausfall / Breakdown | Die Anlage, der Raum oder die Einrichtung ist vollständig ausgefallen oder nicht nutzbar |
| `` (leer) | Kein Ausfall | Die Anlage funktioniert noch, ist aber eingeschränkt oder weist einen Mangel auf |

## Entscheidungsregeln

### Ausfallkennzeichen = X (Ausfall)

Setze das Ausfallkennzeichen auf `X` wenn **eines** der folgenden zutrifft:
- Anlage ist vollständig ausgefallen (Heizung, Aufzug, Sanitär komplett nicht nutzbar)
- Raum oder Bereich ist nicht nutzbar (gesperrt, überflutet, gesundheitsgefährdend)
- Sicherheitsanlage ausgefallen (Brandmeldeanlage, Notbeleuchtung)
- Stromausfall in Teilbereich
- Wasserversorgung oder Abwasser vollständig nicht funktionsfähig

### Ausfallkennzeichen = (leer, kein Ausfall)

Setze das Ausfallkennzeichen leer wenn:
- Anlage läuft noch, aber mit Einschränkungen
- Kosmetischer oder ästhetischer Schaden
- Teildefekt ohne Betriebsunterbrechung (z. B. einzelne Leuchte von mehreren)
- Instandhaltungsarbeit als vorbeugende Maßnahme

## Beispiele

| Szenario | Ausfallkennzeichen |
|----------|--------------------|
| Aufzug fährt nicht mehr | X |
| Einzelne Leuchtstoffröhre defekt, andere Beleuchtung vorhanden | (leer) |
| Heizungsanlage komplett ausgefallen | X |
| Heizkörper in einem Zimmer warm, aber nicht heiß genug | (leer) |
| Toilette defekt, Bereich gesperrt | X |
| Waschbecken tropft leicht | (leer) |
| Brandmeldeanlage außer Betrieb | X |
| Farbe blättert ab an Außenwand | (leer) |

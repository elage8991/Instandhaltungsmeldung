# Instandhaltungsmeldung AI Agent

Dialogbasierter KI-Agent für das geführte Anlegen von SAP PM Instandhaltungsmeldungen

## Business Challenge

Nutzer verschiedener Rollen (Hausmeister, Mieter, Instandhaltungsplaner, Facility Manager) müssen Schäden an technischen Plätzen in SAP S/4HANA melden. Der bisherige Prozess über Fiori-Transaktionen ist fehleranfällig: aktuell sind 30 % aller Meldungen unvollständig. Ein dialogbasierter KI-Agent soll Nutzer Schritt für Schritt durch den Meldeprozess führen, Vollständigkeit sicherstellen, Texte aufbereiten, Priorität vorschlagen und die Meldung direkt über die API_MAINTNOTIFICATION anlegen.

## Business Goals & Success Criteria

| Metrik | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Vollständigkeitsrate Instandhaltungsmeldungen | 70 % vollständig | ≥ 95 % vollständig | — | Instandhaltungsmeldung anlegen (SAP PM) | user |

## Key Milestones

| Meilenstein | Bedingung |
|-------------|-----------|
| 1. Technischen Platz ermittelt | Nutzer hat Objekt/Adresse genannt; Agent hat passende technische Plätze (ZTP) über API gesucht und Nutzer hat einen bestätigt |
| 2. Schadensbeschreibung vollständig | Agent hat alle Pflichtfelder (Ort, Schadensart, Beginn, Gefährdung) erhoben und geprüft |
| 3. Text aufbereitet | Kurztext (≤ 40 Zeichen) und strukturierter Langtext auf Deutsch generiert; Eingaben anderer Sprachen übersetzt |
| 4. Werte vorgeschlagen | Priorität, Ausfallkennzeichen und Beginn-Termin wurden durch den Agent ermittelt und angezeigt |
| 5. Meldung angelegt | Nutzer hat Zusammenfassung bestätigt; Meldung wurde erfolgreich in SAP S/4HANA über API_MAINTNOTIFICATION angelegt |

## Business Architecture (RBA)

### End-to-End Process

Acquire to Decommission (E2E)

### Process Hierarchy

```
Acquire to Decommission (E2E)
└── Operate to Maintain (generic)
    └── Execute Asset Maintenance (BPS-378)
        └── Perform asset maintenance
```

### Summary

Das geführte Anlegen von Instandhaltungsmeldungen ist Teil des Sub-Prozesses „Execute Asset Maintenance" im Rahmen von „Acquire to Decommission". Der Agent deckt den ersten Schritt des Instandhaltungszyklus ab: die strukturierte Erfassung und Anlage einer Meldung.

## Fit Gap Analysis

| Anforderung (fachlich) | Standard Asset(s) | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Lücke? | Hinweise |
|---|---|---|---|---|---|---|---|---|
| Technischen Platz (ZTP) über Bezeichnung suchen | SAP S/4HANA Cloud Private Edition | `sap.s4:apiResource:API_MAINTNOTIFICATION:v1` | — | — | — | — | Ja | Kein MCP-Server vorhanden; eigene MCP-Integration notwendig |
| Instandhaltungsmeldung anlegen | SAP S/4HANA Cloud Private Edition | `sap.s4:apiResource:API_MAINTNOTIFICATION:v1` | — | — | — | — | Ja | MCP Translation File muss generiert werden |
| Dialogführung, Vollständigkeitsprüfung, Textaufbereitung | — | — | — | — | — | — | Ja | KI-Agent (LLM) übernimmt Konversationslogik |
| Prioritäts- und Terminvorschlag | — | — | — | — | — | — | Ja | Regelbasierte Logik im Agent |
| Mehrsprachige Eingabe, Ausgabe auf Deutsch für Meldungstext | — | — | — | — | — | — | Ja | LLM-gestützte Übersetzung im Agent |

### Key Findings

- SAP S/4HANA Cloud Private Edition deckt die Maintenance-Execution-Fähigkeit als Pflichtkapabilität ab (SC5398, SC5061).
- Die API `API_MAINTNOTIFICATION` (OData v2) ist für das Anlegen von Meldungen geeignet; kein MCP-Server vorhanden → MCP Translation File muss generiert werden.
- Die Suche nach technischen Plätzen erfolgt ebenfalls über die S/4HANA API (live, nicht statisch).
- Der Agent muss mehrsprachige Eingaben verarbeiten; der generierte Meldungstext (Kurz- und Langtext) muss auf Deutsch sein.
- Vollständige Dialogführung, Validierung und Textaufbereitung sind reine KI-Agenten-Logik ohne Standard-SAP-Deckung.

## Recommendations

### KI-Agent für geführte Instandhaltungsmeldung

#### Executive Summary

Python AI Agent (A2A) mit MCP-Integration zu SAP S/4HANA PM API

#### Recommended Solution

Pro-Code Python Agent (A2A-Protokoll) mit:
- Konversationslogik für den fünfstufigen Meldeprozess (Platz ermitteln → Beschreibung → Textaufbereitung → Werte vorschlagen → Anlegen)
- MCP Translation File für `API_MAINTNOTIFICATION` (OData v2) zur Anbindung an SAP S/4HANA Cloud Private Edition
- LLM-gestützte Vollständigkeitsprüfung, Textformatierung, Übersetzung und Prioritätsvorschlag
- Mehrsprachige Dialogführung; Meldungstexte werden auf Deutsch generiert

#### Problem Statement

Der manuelle Meldeprozess über SAP Fiori ist fehleranfällig und erfordert SAP-Kenntnisse. 30 % aller Meldungen sind unvollständig, was zu Verzögerungen in der Instandhaltung führt.

#### Affected User Roles

- Hausmeister / Facility-Techniker vor Ort
- Mieter / Bewohner (Endkunde)
- Instandhaltungsplaner
- Facility Manager

#### Important Factors

##### Keine SAP-Kenntnisse erforderlich

Der Agent führt den Nutzer durch einen einfachen Dialog in natürlicher Sprache — keine Kenntnisse der SAP-Transaktionen notwendig.

##### Mehrsprachige Unterstützung

Eingaben in beliebiger Sprache werden akzeptiert; der Agent antwortet in der Sprache des Nutzers. Meldungstexte in S/4HANA werden auf Deutsch generiert.

#### Potential Risks

##### API-Verfügbarkeit und Berechtigung

Die direkte Verbindung zu S/4HANA über API_MAINTNOTIFICATION erfordert entsprechende API-Zugriffsberechtigungen und Netzwerkkonnektivität aus der BTP-Laufzeitumgebung.

##### Datenqualität bei technischen Plätzen

Die KI-gestützte Suche nach technischen Plätzen über Adresse/Bezeichnung liefert möglicherweise mehrdeutige Treffer — der Nutzer muss stets manuell bestätigen.

#### Recommended Solution Category

AI Agent

#### Intent Fit

90%

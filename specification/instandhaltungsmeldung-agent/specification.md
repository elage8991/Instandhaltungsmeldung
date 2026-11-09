# Specification: instandhaltungsmeldung-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read the project input (`product-requirements-document.md`, `intent.md`)
- [ ] Bootstrap agent code in `assets/instandhaltungsmeldung-agent/` using instructions from the sap-agent-bootstrap section (invoke from inside `assets/instandhaltungsmeldung-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

The agent requires a runtime skill for the guided maintenance notification workflow — it implements a complex multi-step dialog with decision logic and domain-specific SAP PM field rules.

- [ ] Create runtime skill `assets/instandhaltungsmeldung-agent/app/skills/instandhaltungsmeldung/SKILL.md` with:
  - YAML frontmatter: `name: instandhaltungsmeldung`, `description: Geführter Dialog zum Anlegen einer Instandhaltungsmeldung in SAP S/4HANA`
  - Step-by-step instructions covering the five-stage dialog (see Project-Specific Tasks below)
  - Companion reference file: `references/prioritaet-regeln.md` — priority mapping rules (based on Gefährdung + Schadensart)
  - Companion reference file: `references/ausfallkennzeichen.md` — SAP PM breakdown indicator rules

---

## Project-Specific Tasks

### REQ-01: Technischen Platz ermitteln

- [ ] Implement system prompt instruction: the agent must ask the user for an address or object name (e.g. "Beeskowdamm 3") to find matching functional locations (Strukturkennzeichen ZTP)
- [ ] Wire MCP tool call for searching functional locations via `API_MAINTNOTIFICATION` (entity: `MaintenanceNotification` / functional location search) — use the MCP tool returned by the translation file, never a direct HTTP call
- [ ] Implement disambiguation: if more than one functional location is found, the agent presents a numbered list and asks the user to confirm; if more than 5 results are returned, the agent asks for a more specific input
- [ ] Implement confirmation gate: only after the user selects and confirms a functional location does the agent proceed to the next step
- [ ] Store the confirmed `FunctionalLocation` ID in conversation context for use in subsequent steps

### REQ-02: Schadensbeschreibung aufnehmen und prüfen

- [ ] Implement completeness check: after the user provides a free-text description, the agent checks for the presence of four mandatory aspects:
  1. **Ort** (Geschoss, Raum, genaue Stelle)
  2. **Schadensart** (Art des Schadens oder der Störung)
  3. **Beginn** (wann wurde die Störung bemerkt)
  4. **Gefährdung / Nutzungseinschränkung** (ja/nein + Beschreibung)
- [ ] For each missing aspect, the agent asks a targeted follow-up question (not a generic "please provide more details")
- [ ] The agent proceeds to the next step only when all four aspects are present in the conversation context

### REQ-03: Text aufbereiten

- [ ] Implement Kurztext generation: the agent generates a concise German short text of **maximum 40 characters** summarising the damage (used as SAP `NotifShortText`)
- [ ] Implement Langtext generation: the agent generates a structured German long text in the following format:
  ```
  Ort: <Geschoss/Raum>
  Schaden: <Schadensart>
  Beginn: <Datum/Zeitpunkt>
  Gefährdung: <Ja/Nein – Beschreibung>
  Beschreibung: <vollständige Beschreibung>
  ```
- [ ] Implement translation: if the user's input is not in German, translate the content to German before generating Kurztext and Langtext; the dialog with the user continues in the user's language
- [ ] Implement reformulation: unclear or grammatically incorrect German input is reformulated into clear, professional German in the output texts

### REQ-04: Werte vorschlagen

- [ ] Implement priority suggestion: load `skills/instandhaltungsmeldung/references/prioritaet-regeln.md` and derive a SAP PM priority value (1=very high, 2=high, 3=medium, 4=low) based on Gefährdung and Schadensart; show the suggested value to the user with a brief explanation
- [ ] Implement Ausfallkennzeichen suggestion: load `skills/instandhaltungsmeldung/references/ausfallkennzeichen.md` and suggest a breakdown indicator (X = breakdown, blank = no breakdown) based on whether a usage restriction is reported
- [ ] Implement Beginn-Termin: derive a suggested `RequiredStartDate` (today's date for Priorität 1 or 2; today + 3 working days for Priorität 3; today + 7 working days for Priorität 4)
- [ ] Allow the user to accept or override each suggested value before proceeding

### REQ-05: Bestätigen und Meldung anlegen

- [ ] Implement summary display: before creating the notification, the agent shows a structured confirmation summary in the user's language:
  ```
  Technischer Platz: <ZTP>
  Kurztext: <max 40 Zeichen>
  Priorität: <Wert + Beschreibung>
  Ausfallkennzeichen: <Wert>
  Beginn-Termin: <Datum>
  Langtext: <vollständiger Text>
  ```
- [ ] Implement confirmation gate: the agent creates the notification only after explicit user confirmation ("Ja", "OK", "confirm", etc.)
- [ ] Wire MCP tool call to create the maintenance notification via `API_MAINTNOTIFICATION` (entity: `MaintenanceNotification`, action: POST / create) with all collected fields: `FunctionalLocation`, `NotifShortText`, `Priority`, `MaintNotifLongTextForEdit`, `RequiredStartDate`, and breakdown indicator
- [ ] After successful creation, display the returned SAP notification number to the user
- [ ] Handle API errors: if creation fails, report the exact error message and offer the option to retry or cancel

### REQ-06: Mehrsprachige Dialogführung

- [ ] Add system prompt instruction: the agent detects the user's input language and responds in the same language throughout the entire dialog
- [ ] Add system prompt instruction: all SAP field values (Kurztext, Langtext) are always generated in German regardless of the dialog language
- [ ] Add system prompt instruction: if the user switches language mid-conversation, the agent adapts immediately

---

## MCP API Integration

```text
MCP API: sap.s4:apiResource:API_MAINTNOTIFICATION:v1
MCP tool scope: read-write
Resources in scope: MaintenanceNotification, FunctionalLocation
```

---

## Business Instrumentation

- [ ] Implement business step instrumentation for all five milestones from the PRD:
  - `M1.achieved: functional_location identified and confirmed by user` / `M1.missed: functional_location could not be determined or not confirmed`
  - `M2.achieved: damage description complete with all mandatory fields` / `M2.missed: one or more mandatory description fields missing after follow-up`
  - `M3.achieved: short_text and long_text generated in German` / `M3.missed: text preparation failed or output format invalid`
  - `M4.achieved: priority, breakdown_indicator, and start_date proposed` / `M4.missed: value proposal incomplete`
  - `M5.achieved: maintenance_notification created with id={notification_id}` / `M5.missed: notification creation failed — reason={error_message}`
- [ ] Add OpenTelemetry custom spans for each milestone using the decorator form on helper methods (never inside `stream()` generator)
- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

> Read [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) for complete MCP integration patterns.

- [ ] Verify `specification/instandhaltungsmeldung-agent/api-specs/api-spec.edmx` exists (API spec already downloaded — 71 KB EDMX for `API_MAINTNOTIFICATION`)
- [ ] Invoke `mcp-translation-file` skill with `api-spec.edmx` (OData / EDMX) and API ORD ID `sap.s4:apiResource:API_MAINTNOTIFICATION:v1`; scope the generated tools to `MaintenanceNotification` and `FunctionalLocation` entities only (read-write)
- [ ] Invoke `setup-solution` skill to register the generated MCP server asset
- [ ] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module — see [guidelines-agent-python.md](../guidelines-agent-python.md) for canonical pattern; NEVER import directly from `sap_cloud_sdk.agentgateway`; NEVER create direct HTTP clients
- [ ] Add MCP server dependency to `asset.yaml` under `requires` — use exact ORD ID from generated `asset.yaml` (read via `grep '^ordId:' assets/<mcp-server-asset-name>/asset.yaml`)
- [ ] Generate `mcp-mock.json` using the `mcp-mock-config` skill (required before tests can run)

---

## Testing

> See [guidelines-agent-python.md](../guidelines-agent-python.md) for Python testing setup and patterns.

- [ ] `conftest.py` only sets `IBD_TESTING=true`
- [ ] Write unit test for functional location search tool (mocked MCP response)
- [ ] Write unit test for maintenance notification create tool (mocked MCP response)
- [ ] Write one integration test: full end-to-end dialog flow — user provides address → agent searches ZTP → user confirms → user describes damage → agent checks completeness → agent proposes values → user confirms → agent creates notification → agent returns notification number (all external systems mocked)
- [ ] Run `pytest` from `assets/instandhaltungsmeldung-agent/` (no args) — if coverage < 70%, add tests
- [ ] Run `pytest` again (no args) to generate final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/instandhaltungsmeldung-agent/`

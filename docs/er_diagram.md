# ER Diagram — Personalized Networking Assistant

This document describes the Entity-Relationship (ER) diagram for the Personalized Networking Assistant project.

---

## Entities Involved

The ER diagram features six primary entities:

- User Profile
- Event Context
- Networking Session
- Generated Starter
- Wikipedia Fact Check
- Log Entry

---

## Primary Keys

Each entity is uniquely identified by its primary key:

| Entity | Primary Key |
|---|---|
| User Profile | `UserID` |
| Event Context | `EventID` |
| Networking Session | `SessionID` |
| Generated Starter | `StarterID` |
| Wikipedia Fact Check | `FactCheckID` |
| Log Entry | `LogID` |

---

## Attributes

### User Profile
| Attribute | Type |
|---|---|
| `UserID` | Primary Key |
| `BioText` | Text |
| `currentEventCache` | Text |

### Event Context
| Attribute | Type |
|---|---|
| `EventID` | Primary Key |
| `EventDescription` | Text |
| `AnalyzedThemes` | Text |

### Networking Session
| Attribute | Type |
|---|---|
| `SessionID` | Primary Key |
| `UserID` | Foreign Key → User Profile |
| `EventID` | Foreign Key → Event Context |
| `SessionTimestamp` | DateTime |

### Generated Starter
| Attribute | Type |
|---|---|
| `StarterID` | Primary Key |
| `SessionID` | Foreign Key → Networking Session |
| `StarterText` | Text |
| `ContextPromptUsed` | Text |

### Wikipedia Fact Check
| Attribute | Type |
|---|---|
| `FactCheckID` | Primary Key |
| `SessionID` | Foreign Key → Networking Session |
| `VerifiedQueryText` | Text |
| `VerificationStatus` | Text (e.g., verified, disputed) |
| `WikipediaSourceURL` | Text |

### Log Entry
| Attribute | Type |
|---|---|
| `LogID` | Primary Key |
| `SessionID` | Foreign Key → Networking Session (optional) |
| `ActionType` | Text (e.g., 'generate_starter') |
| `PayloadJSON` | JSON |
| `Timestamp` | DateTime |

---

## Relationships

| Relationship | Cardinality | Description |
|---|---|---|
| User Profile → Networking Session | 1 : m | One user can participate in multiple networking sessions |
| Event Context → Networking Session | 1 : m | A single event context can be associated with multiple networking sessions |
| Networking Session → Generated Starter | 1 : m | A single session can yield multiple AI-generated conversation starters |
| Networking Session → Wikipedia Fact Check | 1 : m | A single session can involve multiple fact-checking queries |
| Networking Session → Log Entry | 1 : m | A single session can generate multiple system log entries for auditing |

---

## Foreign Keys

- **Networking Session** references User Profile via `UserID` and Event Context via `EventID`
- **Generated Starter** references Networking Session via `SessionID`
- **Wikipedia Fact Check** references Networking Session via `SessionID`
- **Log Entry** optionally references Networking Session via `SessionID`

---

## Cardinality

A single user or event can have multiple networking sessions. Each networking session can generate multiple conversation starters and trigger multiple fact-checks. Each action within the system can generate its own log entry linked back to the session.

---

## Normalization and Structure

The diagram is normalized — data for users, event contexts, core session transactions, AI outputs, and system logs are stored in separate entities. This reduces redundancy and ensures clear traceability of data and AI interactions.

---

## Use Case Coverage

This ER model supports the following core features of the Personalized Networking Assistant:

- **User biography tracking** — Persistent user bios are mapped to dynamic event descriptions
- **AI prompt recording** — Individual AI-generated conversation prompts are tracked per session
- **Fact verification logging** — Wikipedia verification queries are logged to ensure factual reliability
- **Interaction auditing** — Detailed interaction logs support system auditing, analytics, and performance debugging
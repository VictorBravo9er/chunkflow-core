# Chunkflow Core Subsystems Documentation

Welcome to the subsystems architecture documentation for **Chunkflow Core**.

---

## 🗺️ Subsystem Architecture Map

The system is organized into decoupled layers and specialized services:

```mermaid
flowchart TD
    subgraph Presentation["1. Presentation Layer"]
        UI["Web / Client Interface"]
    end

    subgraph ServiceLayer["2. Microservice / API Layer"]
        API["Backend API & Orchestration"]
    end

    subgraph Persistence["3. Persistence & Storage Layer"]
        DB[("Database & Stores")]
    end

    UI --> API
    API --> DB
```

---

## 📁 Subsystem Dossiers

| Subsystem Document | Scope & Responsibilities |
| :--- | :--- |
| Core API & Services | High-level request lifecycle, routing, and domain service dispatch |
| Persistence & Data Model | Database schema design, migrations, relational integrity, and storage |
| Client / Frontend Architecture | UI component architecture, state management, and API clients |

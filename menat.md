# Financial Analyst — System Architecture

---

## Part 1: High-Level Overview

```mermaid
graph TB
    classDef userStyle fill:#fce4ec,stroke:#e91e63,stroke-width:2px,color:#000
    classDef uiStyle fill:#e3f2fd,stroke:#1565c0,color:#000
    classDef orchStyle fill:#e8eaf6,stroke:#283593,color:#000
    classDef stepStyle fill:#e8f5e9,stroke:#2e7d32,color:#000
    classDef externalStyle fill:#fff8e1,stroke:#f9a825,color:#000
    classDef storageStyle fill:#f3e5f5,stroke:#7b1fa2,color:#000
    classDef infraStyle fill:#eceff1,stroke:#546e7a,color:#000

    RM(("👤 RM / CA User")):::userStyle

    subgraph UILayer["UI Layer — Azure App Service"]
        UI["Financial Analyst UI (React.js)"]:::uiStyle
    end

    subgraph OrchLayer["Orchestrator — Azure Container Apps | Agent Framework SDK (Python)"]
        Orch["Orchestrator (Workflow + AI Agent)"]
        Intent["Intent Detection"]
        Guard["I/O Guardrails"]
        OutFmt["Output Formatter"]
    end
    class Orch,Intent,Guard,OutFmt orchStyle

    subgraph ProcessingLayer["Processing Pipeline"]
        direction LR
        S1["Step 1\nData / Document\nPreparation"]:::stepStyle
        Macro["Macro / Market\nTrends Analysis"]:::stepStyle
        S2["Step 2 ⚡\nFinancial Metrics\nPreparation"]:::stepStyle
        S3["Step 3\nCausality\nAnalysis"]:::stepStyle
        S4["Step 4\nReport\nFormatter"]:::stepStyle
    end

    subgraph MoodysAPIs["Moody's Smart APIs (External)"]
        direction LR
        API_E["Entity Resolution"]
        API_D["Doc Retrieval"]
        API_M["Financial Metrics"]
        API_SA["Search All Docs"]
        API_SE["Search Entity Docs"]
        API_SO["Sector Outlook"]
    end
    class API_E,API_D,API_M,API_SA,API_SE,API_SO externalStyle

    subgraph StorageLayer["Storage Layer"]
        direction LR
        Blob["Azure Blob Storage\n(PDF Documents)"]:::storageStyle
        Search["Azure AI Search\n(Document Index)"]:::storageStyle
        SQL["Azure SQL Database\n(Financials & Materiality)"]:::storageStyle
        Redis["Azure Cache for Redis\n(Context & Session)"]:::storageStyle
    end

    subgraph InfraLayer["Infrastructure Layer"]
        direction LR
        Mon["Azure Monitor"]:::infraStyle
        Foundry["AI Foundry"]:::infraStyle
        LLM["Azure OpenAI\n(GPT-5 / GPT-5-mini)"]:::infraStyle
        DocIntel["Azure AI\nDoc Intelligence"]:::infraStyle
    end

    %% --- Connections ---
    RM -->|"prompt / upload PDFs"| UI
    UI -->|"prompt + context"| Orch
    Orch --> Intent
    Orch --- Guard
    Orch --- OutFmt

    Intent --> S1
    S1 -->|"after ingestion"| Macro
    S1 -->|"Moody's ID\n(parallel fork)"| S2
    Macro -->|"macro context"| S3
    S2 -->|"material metrics\n(after RM gate)"| S3
    S3 -->|"causality output"| S4
    S4 --> OutFmt
    OutFmt -->|"final report"| UI

    S1 <-->|"Entity Res, Doc Retrieval"| MoodysAPIs
    Macro <-->|"Search, Sector Outlook"| MoodysAPIs
    S2 <-->|"Financial Metrics"| MoodysAPIs
    S3 <-->|"External context"| MoodysAPIs

    S1 <-->|"ingest / index"| StorageLayer
    S2 -->|"store"| SQL
    S3 <-->|"query"| Search
    Macro <-->|"query"| Search

    ProcessingLayer -.->|"uses"| LLM
    S1 -.->|"extract"| DocIntel
```

---

## Part 2: Step 1 & 2 — Data Preparation (+ Macro Analysis)

```mermaid
graph TB
    classDef userStyle fill:#fce4ec,stroke:#e91e63,stroke-width:2px,color:#000
    classDef processStyle fill:#e8f5e9,stroke:#2e7d32,color:#000
    classDef ingestStyle fill:#c8e6c9,stroke:#1b5e20,color:#000
    classDef externalStyle fill:#fff8e1,stroke:#f9a825,color:#000
    classDef storageStyle fill:#f3e5f5,stroke:#7b1fa2,color:#000
    classDef infraStyle fill:#eceff1,stroke:#546e7a,color:#000
    classDef tbd fill:#fff3cd,stroke:#ffc107,stroke-dasharray:5 5,color:#856404

    RM(("👤 RM")):::userStyle

    %% ===== STEP 1 =====
    subgraph Step1["Step 1: Data / Document Preparation (Background Task)"]
        EntityRes["Entity Resolution\n→ Moody's ID"]:::processStyle
        DocCollect["Document Collection\n(RM Uploads + Moody's Docs)"]:::processStyle
        subgraph OAAI["OAAI Ingest Service (Self-built RAG Product)"]
            IngestPipe["Document Ingestion\n& Indexing Pipeline"]:::ingestStyle
        end
    end

    %% ===== MACRO =====
    subgraph MacroBlock["Macro / Market Trends Analysis (after Data Prep)"]
        MacroAgent["Macro Trends Agent"]:::processStyle
    end

    %% ===== STEP 2 =====
    subgraph Step2["Step 2: Financial Data / Metrics Preparation (⚡ Parallel with Step 1)"]
        MetricsRet["Financial Metrics\nRetrieval"]:::processStyle
        FinTable["Financial Table\nPreparation"]:::processStyle
        YoYCalc["YoY Trend\nCalculation"]:::processStyle
        MatDetect["Materiality\nDetection"]:::tbd
        RMGate["🔀 RM Review Gate\n(Adjust / Supplement)"]:::processStyle
    end

    %% ===== MOODY'S APIs =====
    subgraph MoodysAPIs["Moody's Smart APIs (External)"]
        API_Entity["Entity Resolution\nAPI"]:::externalStyle
        API_DocRet["Doc Retrieval\nAPI"]:::externalStyle
        API_Metrics["Financial Metrics\nAPI"]:::externalStyle
        API_SearchAll["Search All\nDocs API"]:::externalStyle
        API_SearchEnt["Search Entity\nDocs API"]:::externalStyle
        API_Sector["Sector Outlook\nAPI"]:::externalStyle
    end

    %% ===== STORAGE =====
    subgraph StorageLayer["Storage Layer"]
        subgraph BlobStore["Azure Blob Storage"]
            S_Ind[("Industry Reports")]:::storageStyle
            S_Brk[("Broker Reports")]:::storageStyle
            S_Ear[("Earnings Call Transcripts")]:::storageStyle
            S_Bor[("Borrower Reports")]:::storageStyle
        end
        subgraph AISearch["Azure AI Search"]
            DocIndex[("Document Index")]:::storageStyle
        end
        subgraph SQLDB["Azure SQL Database"]
            DB_Mat[("Materiality Output")]:::storageStyle
            DB_Fin[("Processed Financials")]:::storageStyle
        end
    end

    DocIntel["Azure AI\nDocument Intelligence"]:::infraStyle

    %% ===== CONNECTIONS =====

    %% RM uploads
    RM -->|"upload PDFs"| BlobStore

    %% Step 1: Entity Resolution
    EntityRes -->|"call"| API_Entity
    API_Entity -->|"Moody's ID"| DocCollect

    %% Step 1: Doc Collection → Ingest
    DocCollect -->|"call"| API_DocRet
    API_DocRet -->|"Moody's docs"| IngestPipe
    BlobStore -->|"RM docs"| IngestPipe
    IngestPipe -->|"extract"| DocIntel
    IngestPipe -->|"ingest & index"| AISearch

    %% Macro (after ingestion)
    IngestPipe -->|"after ingestion"| MacroAgent
    MacroAgent -->|"query ingested docs"| DocIndex
    MacroAgent -->|"call"| API_SearchAll
    MacroAgent -->|"call"| API_SearchEnt
    MacroAgent -->|"call"| API_Sector

    %% Step 2: parallel fork from Entity Resolution
    API_Entity -->|"Moody's ID\n(parallel fork)"| MetricsRet
    MetricsRet -->|"call"| API_Metrics
    API_Metrics --> FinTable
    FinTable --> YoYCalc
    YoYCalc --> MatDetect
    MatDetect --> RMGate
    MatDetect -->|"store"| SQLDB
    RMGate -.->|"RM adjusts\nvia UI"| RM

    %% TBD annotation
    MatDetect -.- TBDNote>"⚠️ AI Agent vs Python Script — TBD"]
    style TBDNote fill:#fff3cd,stroke:#ffc107,color:#856404

    %% Outputs to next diagram
    MacroAgent -->|"→ to Step 3"| OUT1(["macro context"]):::processStyle
    RMGate -->|"→ to Step 3"| OUT2(["confirmed +\nsupplemented metrics"]):::processStyle
```

---

## Part 3: Step 3 & 4 — Causality Analysis & Report Generation

```mermaid
graph TB
    classDef uiStyle fill:#e3f2fd,stroke:#1565c0,color:#000
    classDef orchStyle fill:#e8eaf6,stroke:#283593,color:#000
    classDef processStyle fill:#e8f5e9,stroke:#2e7d32,color:#000
    classDef externalStyle fill:#fff8e1,stroke:#f9a825,color:#000
    classDef storageStyle fill:#f3e5f5,stroke:#7b1fa2,color:#000
    classDef infraStyle fill:#eceff1,stroke:#546e7a,color:#000

    %% Inputs from previous diagram
    IN1(["macro context\n← from Macro Analysis"]):::processStyle
    IN2(["confirmed + supplemented\nmaterial metrics\n← from Step 2 / RM Gate"]):::processStyle

    %% ===== STEP 3 =====
    subgraph Step3["Step 3: Causality Analysis"]
        CausAgent["Causality &\nWrite-up Agent"]:::processStyle
        PromptConst["Prompt / Query\nConstruction"]:::processStyle
        GapIdent["Gap Identification\n(Missing Info Handler)"]:::processStyle
    end

    %% ===== STEP 4 =====
    subgraph Step4["Step 4: Financial Report Formatter"]
        ContentClean["Content Clean-up\n(Resolve Conflicts,\nMerge / Deduplicate)"]:::processStyle
        ReportFmt["Report Formatter\n(Balance Sheet,\nIncome Statement, etc.)"]:::processStyle
    end

    %% ===== ORCHESTRATOR (output side) =====
    subgraph OrchLayer["Orchestrator — Azure Container Apps"]
        OutFmt["Output Formatter"]:::orchStyle
        Guard["I/O Guardrails"]:::orchStyle
    end

    UI["Financial Analyst UI (React.js)"]:::uiStyle

    %% ===== EXTERNAL & STORAGE =====
    subgraph MoodysAPIs["Moody's Smart APIs (External)"]
        API_SearchAll["Search All Docs API"]:::externalStyle
        API_SearchEnt["Search Entity Docs API"]:::externalStyle
        API_Sector["Sector Outlook API"]:::externalStyle
    end

    subgraph StorageLayer["Storage Layer"]
        DocIndex[("Azure AI Search\nDocument Index")]:::storageStyle
        Redis["Azure Cache for Redis\n(Context & Session)"]:::storageStyle
    end

    subgraph InfraLayer["Infrastructure Layer"]
        LLM["Azure OpenAI\n(GPT-5 / GPT-5-mini)"]:::infraStyle
        Mon["Azure Monitor"]:::infraStyle
        Foundry["Microsoft AI Foundry"]:::infraStyle
    end

    %% ===== CONNECTIONS =====

    %% Inputs → Causality
    IN1 --> CausAgent
    IN2 --> CausAgent

    %% Step 3 internals
    CausAgent --> PromptConst
    PromptConst -->|"internal:\nquery docs"| DocIndex
    PromptConst -->|"external:\ncall APIs"| MoodysAPIs
    CausAgent --> GapIdent
    GapIdent -.->|"request\nmissing info"| MoodysAPIs
    CausAgent -.->|"uses"| LLM
    CausAgent -.->|"session"| Redis

    %% Step 3 → Step 4
    CausAgent -->|"causality output"| ContentClean
    ContentClean --> ReportFmt

    %% Step 4 → Output
    ReportFmt --> Guard
    Guard --> OutFmt
    OutFmt -->|"final report"| UI
```

---

## Legend
- **Green nodes** — Processing components (agents, tools, pipelines)
- **Yellow nodes** — Moody's Smart APIs (external)
- **Purple nodes** — Azure storage services
- **Blue nodes** — UI components
- **Indigo nodes** — Orchestrator components
- **Grey nodes** — Infrastructure services
- **Dashed border (⚠️)** — Decision pending (open for discussion)
- **Dashed arrows** — Async / optional / infrastructure dependency
- **Solid arrows** — Primary data flow

## Flow Summary
1. **Step 1** — RM triggers analysis → Entity Resolution (Moody's API) → parallel fork
2. **Step 1 (background)** — Collect docs (RM upload + Moody's) → OAAI Ingest → Azure AI Search
3. **Macro Analysis** — After ingestion: query docs + Moody's Search/Sector APIs
4. **Step 2 (⚡ parallel)** — Moody's Metrics API → Table → YoY → Materiality → RM Review Gate
5. **Step 3** — Causality Agent receives macro context + material metrics → queries internal & external
6. **Step 4** — Clean-up, dedup, format → final report to UI

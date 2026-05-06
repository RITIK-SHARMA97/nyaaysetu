<div align="center">

<img src="https://img.shields.io/badge/-%E0%A4%A8%E0%A5%8D%E0%A4%AF%E0%A4%BE%E0%A4%AF%20%2B%20%E0%A4%B8%E0%A5%87%E0%A4%A4%E0%A5%81-E8581A?style=flat&labelColor=0D1B4B&color=E8581A" alt="न्याय + सेतु" height="28"/>

# NyaaySetu

### *From Court Judgments to Verified Action Plans — in minutes.*

<br/>

[![AI for Bharat 2026](https://img.shields.io/badge/🏆_AI_for_Bharat_2026-Shortlisted_Top_50-E8581A?style=for-the-badge&labelColor=0D1B4B)](https://hackerearth.com/challenges/hackathon/ai-for-bharat-2)
[![Theme](https://img.shields.io/badge/Theme-Justice_%26_Legal_Tech-0D1B4B?style=for-the-badge)](.)
[![Tests](https://img.shields.io/badge/Tests-10%2F10_Passing-16A34A?style=for-the-badge&logo=pytest&logoColor=white)](./backend/tests)
[![Cost](https://img.shields.io/badge/Infrastructure_Cost-₹0-0E7C7B?style=for-the-badge)](.)
[![License](https://img.shields.io/badge/License-MIT-64748B?style=for-the-badge)](./LICENSE)

<br/>

> ### "An IAS officer was sentenced to imprisonment for missing a court compliance deadline — after being transferred to a new post."
>
> *The previous officer never briefed him. The court did not accept "I didn't know" as a defence.*
>
> **The law does not pause for transfers. NyaaySetu ensures no officer faces this again.**

<br/>

| | |
|:---:|:---:|
| **[🌐 Live Demo](https://nyaaysetu.vercel.app)** | **[🔌 API Docs](https://nyaaysetu-api.railway.app/docs)** |
| **[📊 Dashboard](https://nyaaysetu.vercel.app/dashboard)** | **[📋 Officer Briefing](https://nyaaysetu.vercel.app/briefing)** |

<br/>

</div>

---

## ⚡ See It In 30 Seconds

```
1.  git clone https://github.com/yourteam/nyaaysetu && cd nyaaysetu
2.  echo "GEMINI_API_KEY=your_free_key" >> backend/.env
3.  docker-compose up
4.  Open http://localhost:3000/login → click "Amit Patel (New Transfer)"
5.  See 6 inherited court compliance obligations she didn't know she had.
```

> Get a free Gemini key (no credit card) at [aistudio.google.com](https://aistudio.google.com)

---

## 🎯 The Problem Nobody Solved

Every AI legal tool in India was built for people **inside** the court:

| Existing Tool | Built For | What It Misses |
|:-------------|:----------|:---------------|
| **SUPACE** (Supreme Court of India) | Judges — legal research | Never asks *"what must the government DO now?"* |
| **LegRAA** (NALSA) | Lawyers — document drafting | Zero compliance tracking |
| **Provakil** | Law firms — case management | Private sector only; no government side |
| **Nyaay AI** | Citizens — legal information | No obligation enforcement |
| **CCMS** (NIC) | Courts — case status | Says *"case disposed"* — not *what to do, who, by when* |

<br/>

> ### NyaaySetu is the **first** system built for the government officer on the **other side** of the judgment.
>
> *Not the judge. Not the lawyer. The IAS officer who receives the order and must comply — or face contempt.*

**The market:** 28 states × 8 UTs × 1.2 lakh HC cases vs government × ₹0 existing solutions = white space.

---

## 🚨 The Transfer Gap

```
FRIDAY    Officer A receives transfer order to a new district.

MONDAY    Officer B joins the post.
          ┌─────────────────────────────────────────────────┐
          │  47 court compliance obligations — still active  │
          │  Deadlines: still counting                       │
          │  Court: does not care about transfers            │
          │  Officer B: knows NOTHING                        │
          └─────────────────────────────────────────────────┘

WITHOUT NyaaySetu → 2 weeks of informal phone calls (if lucky)
WITH NyaaySetu    → Officer B sees everything in 10 minutes on first login
```

### Why This Is Urgent — By The Numbers

| Stat | Number | Source |
|:-----|-------:|:-------|
| Contempt proceedings vs Karnataka govt officers / year | **2,000+** | HC records |
| Average IAS officer posting duration | **18 months** | DOPT data |
| Karnataka HC cases involving government departments | **1.2 lakh** | KHC portal |
| eCourts Phase III digitisation budget (2023–2027) | **₹7,210 Cr** | MeitY |
| Existing AI tools solving this specific problem | **0** | Our research |

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Karnataka HC Judgment PDF                          │
│          (uploaded by Reviewer Officer — any format)                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  1. PyMuPDF Text Extraction   │  ← word-level bounding
              │     + Tesseract OCR           │    boxes for highlighting
              │     + Kannada detection       │
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  2. Rule-Based Classifier    │  ← shall / directed to /
              │     (deterministic, fast)    │    must / forthwith
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  3. Gemini 1.5 Flash         │  ← structured JSON,
              │     (grounded extraction)    │    source-cited, free tier
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  4. Deadline Engine          │  ← forthwith→7d
              │     + Contempt Risk Scorer   │    expeditiously→30d
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  5. Officer Verifies         │  ← click field →
              │     (split-pane PDF viewer)  │    PDF highlights source
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  6. Dashboard + Leaderboard  │  ← contempt risk timers,
              │     + Affidavit Generator    │    dept rankings, 1-click
              └─────────────────────────────┘    court filing
```

**Why hybrid AI, not pure LLM?**

```python
# Stage 1 — Rule-based (deterministic, explainable, zero hallucination)
HIGH_CONFIDENCE_VERBS = [
    r'\bis directed to\b', r'\bshall\b', r'\bis hereby ordered\b',
    r'\bis required to\b', r'\bmust\b', r'\bforthwith\b',
]

# Stage 2 — Gemini handles semantic structure extraction
# Critical: output ALWAYS includes source_sentence_verbatim
# Officers verify; nothing reaches dashboard without human approval
```

Pure LLM = black box. Unacceptable for government deployment and contempt proceedings.  
Hybrid = **explainable** (rule-based) + **semantically deep** (Gemini) + **auditable** (source-linked).

---

## 🖥️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      Next.js 14 Frontend                          │
│   /           /verify/[id]      /dashboard    /briefing  /login  │
│  Upload    Split-pane PDF+AI   Actions+Risk  Inherited   RBAC    │
└──────────────────────────┬───────────────────────────────────────┘
                           │  REST API (9 endpoints)
┌──────────────────────────▼───────────────────────────────────────┐
│                      FastAPI Backend                               │
│  POST /judgments/upload    GET /judgments/{id}/status             │
│  PATCH /actions/{id}       GET /dashboard/summary                 │
│  GET /officers/briefing    POST /auth/login                       │
└────────┬─────────────────┬──────────────────┬────────────────────┘
         │                 │                  │
┌────────▼────────┐ ┌──────▼──────┐  ┌───────▼──────────┐
│   AI Pipeline   │ │  PostgreSQL  │  │ Background Tasks  │
│                 │ │             │  │                   │
│  extractor.py   │ │ judgments   │  │  processor.py     │
│  ocr.py         │ │ action_items│  │  (0→100% progress)│
│  classifier.py  │ │ audit_logs  │  │                   │
│  llm.py         │ │ designations│  │  escalation.py    │
│  deadline.py    │ │ compliance  │  │  (cron: 30d/15d/  │
│  appeal.py      │ │ _health     │  │   7d/2d alerts)   │
│  affidavit.py   │ │             │  │                   │
│  conflict.py    │ └─────────────┘  └───────────────────┘
└─────────────────┘
```

---

## ✨ The 25 Unique Factors

No existing tool implements all of these. Most implement none.

### 🎯 Ownership Model
| # | Feature | Why It Matters |
|---|---------|---------------|
| 1 | **Designation-based ownership** | Actions owned by the POST, not the person — survives transfers |
| 2 | **Auto-inherit on login** | New officer sees ALL obligations on first login, zero manual handover |
| 3 | **Inherited briefing screen** | Sorted by contempt risk, not case number — urgent things surface first |

### 🤖 AI Pipeline
| # | Feature | Why It Matters |
|---|---------|---------------|
| 4 | **Hybrid rule + LLM classifier** | Deterministic for obligation verbs, Gemini for semantic structure |
| 5 | **Per-field confidence scoring** | Four scores: directive, department, deadline, overall (0.0–1.0) |
| 6 | **Grounded generation** | Every LLM output includes `source_sentence_verbatim` — no fabrication |
| 7 | **Bounding box extraction** | PyMuPDF word-coordinates → click-to-highlight in PDF viewer |
| 8 | **Kannada page detection** | Unicode U+0C80–U+0CFF → red flag for manual review |

### ⚠️ Risk Engine
| # | Feature | Why It Matters |
|---|---------|---------------|
| 9 | **Live contempt risk countdown** | GREEN → AMBER → RED → CRITICAL with pulse animation |
| 10 | **Cross-judgment conflict detector** | Flags contradicting directives to same department |
| 11 | **7-level escalation hierarchy** | Fires at 30d / 15d / 7d / 2d thresholds automatically |
| 12 | **Automatic overdue marking** | Cron enforces status transitions — no manual intervention |

### ⚖️ Legal Tools
| # | Feature | Why It Matters |
|---|---------|---------------|
| 13 | **Limitation Act appeal windows** | Writ Appeal 30d · SLP 90d · LP Appeal 30d — auto-calculated |
| 14 | **Compliance affidavit generator** | One-click pre-formatted affidavit ready for court filing |
| 15 | **Implicit deadline resolution** | `forthwith`→7d · `expeditiously`→30d · `at the earliest`→14d |
| 16 | **Explicit deadline parsing** | `within 30 days` · `on or before DD.MM.YYYY` |

### 🏛️ Governance
| # | Feature | Why It Matters |
|---|---------|---------------|
| 17 | **Immutable audit trail** | Append-only: who, when, what changed — defence against contempt |
| 18 | **Department compliance leaderboard** | First system to rank Karnataka depts by court compliance score |
| 19 | **RBAC** | 5 roles × 8 permissions: reviewer / officer / head / secretary / admin |
| 20 | **7-state action state machine** | Enforced transitions — no skipping, no inconsistency |
| 21 | **FastAPI auto-docs** | `/docs` endpoint — judges can test every API live |

### 🏗️ Infrastructure
| # | Feature | Why It Matters |
|---|---------|---------------|
| 22 | **`docker-compose up`** | One command, full stack, NIC-compatible, no cloud required |
| 23 | **Zero API cost** | Gemini 1.5 Flash free tier: 1M token context, 15 req/min |
| 24 | **Ollama fallback** | Swap Gemini → Mistral 7B for fully offline production deployment |
| 25 | **Background task processing** | FastAPI BackgroundTasks: 0→100% progress polling, no UI freeze |

---

## 🗂️ Demo For Judges

### Storyline A — The Transfer Gap *(5 min · IAS Officials)*

```
Step 1  →  /login → "Amit Patel (New Transfer)"
Step 2  →  /briefing auto-loads: 6 inherited obligations sorted by urgency
Step 3  →  Top item: CRITICAL · 3 days remaining · click it
Step 4  →  Verify page: PDF (left) + extracted directives (right)
Step 5  →  Click any directive → PDF highlights source sentence in yellow ← THIS IS THE MOMENT
Step 6  →  Click Approve → Mark In Progress → audit log records permanently
Step 7  →  Mark Complied → Generate Affidavit → pre-formatted court filing ready
```

> *"Without NyaaySetu: 2 weeks of informal briefings. With NyaaySetu: 10 minutes on day one."*

### Storyline B — The Leaderboard *(2 min · Investors + Senior Officials)*

```
Step 1  →  /dashboard → Dept Leaderboard tab
Step 2  →  Ask: "Which Karnataka department is worst at complying with court orders?"
Step 3  →  [PAUSE — let judges look]
Step 4  →  Revenue Department: 34% compliance · 1 overdue · trend: WORSENING
Step 5  →  Drill in: 3 days left · untouched for weeks · escalation fired
```

> *"Until NyaaySetu, nobody could answer that question. This is contempt before it happens. We prevent it."*

---

## 🧪 Test Results

```bash
$ cd backend && pytest tests/test_pipeline.py -v

tests/test_pipeline.py::test_classify_high_confidence    PASSED ✓  (obligation verb detection)
tests/test_pipeline.py::test_classify_non_directive      PASSED ✓  (false positive rejection)
tests/test_pipeline.py::test_deadline_explicit_days      PASSED ✓  ("within 30 days" → date)
tests/test_pipeline.py::test_deadline_forthwith          PASSED ✓  ("forthwith" → +7 days)
tests/test_pipeline.py::test_deadline_expeditiously      PASSED ✓  ("expeditiously" → +30 days)
tests/test_pipeline.py::test_department_detection        PASSED ✓  (Revenue / Urban / Health)
tests/test_pipeline.py::test_contempt_risk_critical      PASSED ✓  (overdue → CRITICAL)
tests/test_pipeline.py::test_contempt_risk_green         PASSED ✓  (60d+ → GREEN)
tests/test_pipeline.py::test_appeal_windows              PASSED ✓  (Writ 30d, SLP 90d, LP 30d)
tests/test_pipeline.py::test_affidavit_generation        PASSED ✓  (court-ready format)

========================= 10 passed in 0.10s =========================
```

---

## 🛠️ Tech Stack

| Layer | Technology | Cost | Why This Choice |
|:------|:----------|:----:|:----------------|
| **LLM** | Gemini 1.5 Flash | ₹0 | 1M token context handles full judgments · free tier · structured JSON |
| **PDF** | PyMuPDF | ₹0 | Word-level bounding boxes → click-to-highlight · fastest Python PDF lib |
| **OCR** | Tesseract + `tesseract-ocr-kan` | ₹0 | Kannada language support · open source · confidence scoring |
| **Backend** | FastAPI + SQLAlchemy | ₹0 | Auto-generated `/docs` · async · type-safe · Python |
| **Database** | PostgreSQL 16 | ₹0 | ACID compliance for immutable audit logs · Railway free tier |
| **Frontend** | Next.js 14 + Tailwind | ₹0 | App router · TypeScript · Vercel free tier deployment |
| **PDF Viewer** | PDF.js + custom overlay | ₹0 | Click-to-highlight with exact bbox coordinates |
| **Containers** | Docker + docker-compose | ₹0 | NIC infra compatible · one-command local setup |
| **Hosting** | Vercel + Railway | ₹0 | Both free tier · git-push deploy · auto-SSL |

### **Total infrastructure cost: ₹0 · Total monthly cost at scale: ₹0 (free tiers)**

---

## 📊 Evaluation Criteria Mapping

| Criterion | Weight | Exactly What We Built |
|:----------|:------:|:----------------------|
| **Problem Relevance & Depth** | 20% | Real Madras HC contempt case · 2,000+/yr Karnataka · eCourts Phase III timing · 15-year research gap documented |
| **Technical Implementation** | 25% | Hybrid AI pipeline · 10/10 pytest · FastAPI auto-docs · per-field confidence · bounding boxes · Kannada OCR |
| **Real-World Deployability** | 25% | `docker-compose up` · NIC-compatible · RBAC · designation ownership · on-prem Ollama fallback · immutable audit |
| **Demo Quality** | 15% | 2 storylines · transfer gap · click-to-highlight · leaderboard moment · affidavit in 1 click · 5-min script |
| **Scalability & Impact** | 15% | 36 markets · ₹7,210Cr eCourts tailwind · ₹25L/yr SaaS · 3-month Karnataka pilot plan documented |

---

## 📈 Scalability & Market

```
PHASE 1 — Pilot (Month 1–3)        PHASE 2 — State (Month 4–12)      PHASE 3 — National (Year 2+)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Karnataka Revenue Department        All Karnataka departments           28 States + 8 UTs
5 Revenue Dept officers             1,000+ officers                    Bangladesh · Sri Lanka
50 HC judgments processed           10,000+ judgments                  Similar common law systems
Baseline compliance measured        State-wide leaderboard live         Regional SaaS expansion
Target: 0 missed deadlines          Reference case for other states     ₹25L/yr × 36 = ₹9 Cr ARR
```

**Revenue model:** SaaS licensing to state governments — ₹15–25 lakh per state per year.  
Comparable to existing NIC software contract values. Zero marginal cost per additional judgment.

**The tailwind:** eCourts Phase III (₹7,210 Crore, 2023–2027) is creating machine-readable court orders at national scale. NyaaySetu is the compliance consumption layer — we ride the government's own ₹7,210 Cr infrastructure investment.

---

## 📁 Project Structure

```
nyaaysetu/
├── backend/
│   ├── app/
│   │   ├── api/            # auth · judgments · actions · dashboard · officers
│   │   ├── core/           # config · JWT security · RBAC permission matrix
│   │   ├── models/         # Officer · Judgment · ActionItem · AuditLog · ComplianceHealth
│   │   ├── pipeline/       # extractor · ocr · classifier · llm · deadline · appeal · affidavit · conflict
│   │   ├── schemas/        # Pydantic I/O (powers FastAPI /docs auto-documentation)
│   │   └── workers/        # processor (background) · escalation (cron)
│   ├── scripts/
│   │   ├── seed.py         # 3 Karnataka HC cases · 6 actions · 3 depts · 2 officers
│   │   └── download_judgments.py
│   └── tests/
│       ├── test_pipeline.py  # 10 tests — all passing
│       └── conftest.py       # SQLite test DB · mock Gemini response
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Upload zone (drag-drop PDF)
│   │   ├── verify/[id]/      # Split-pane: PDF viewer + AI fields + confidence scores
│   │   ├── dashboard/        # Action list + contempt timers + dept leaderboard
│   │   ├── briefing/         # Inherited obligations screen (transfer gap solution)
│   │   └── login/            # 5 demo roles (reviewer/officer/head/secretary/admin)
│   ├── components/
│   │   ├── PDFViewer.tsx         # PDF.js + yellow highlight overlay
│   │   ├── FieldReview.tsx       # Confidence badges + approve/edit/reject
│   │   ├── ActionCard.tsx        # Status machine + audit log + affidavit button
│   │   ├── ContemptTimer.tsx     # Live countdown GREEN→AMBER→RED→CRITICAL
│   │   ├── Leaderboard.tsx       # Dept ranking with compliance score + trend
│   │   ├── AuditLog.tsx          # Immutable timeline per action
│   │   ├── AffidavitGenerator.tsx # One-click court-ready affidavit
│   │   ├── AppealWindow.tsx      # Limitation Act deadlines per case
│   │   └── ConflictAlert.tsx     # Side-by-side conflict detection
│   └── lib/
│       ├── api.ts                # All 9 API functions (single source of truth)
│       └── utils.ts              # contemptRiskColor · formatDate · confidenceLabel
│
├── docs/
│   ├── demo-script.md        # Word-for-word 5-minute script · 2 storylines
│   ├── judge-qa.md           # 20 judge questions + exact answers
│   └── sample-judgments/     # 5 real Karnataka HC judgment PDFs
│
├── .github/workflows/ci.yml  # pytest on every push → green checkmark
└── docker-compose.yml        # api + db + frontend · one command
```

---

## 🔒 Judge Q&A (Quick Reference)

<details>
<summary><strong>Q: How is this different from CCMS?</strong></summary>

CCMS tells you a case is disposed. NyaaySetu tells you **what to do, who must do it, by when, and whether it's done**. CCMS is a case tracker. NyaaySetu is a compliance engine.

</details>

<details>
<summary><strong>Q: How do you prevent AI hallucination in legal context?</strong></summary>

Grounded generation — Gemini only extracts from provided text. Every output field includes `source_sentence_verbatim`. Officers approve each field individually. Nothing reaches the dashboard without human verification. Uncertain fields show red — mandatory review before approval.

</details>

<details>
<summary><strong>Q: Can this run on NIC servers without cloud?</strong></summary>

Yes. `docker-compose up` works completely offline after first build. In production: Gemini swapped for Ollama + Mistral 7B — zero internet, zero API keys, fully on-prem. All data stays on government servers.

</details>

<details>
<summary><strong>Q: What happens when an officer transfers?</strong></summary>

Actions are owned by **Designation** (the post: "Secretary, Revenue Dept"), not Officer (the person). New officer logs in → briefing screen shows all inherited obligations sorted by contempt risk. Zero manual handover. Court deadlines don't move. Officer knows everything in 10 minutes.

</details>

<details>
<summary><strong>Q: Why not use a mobile app?</strong></summary>

Government officers in Karnataka use desktop terminals in their offices. PWA is on the roadmap. The web-first approach means zero installation, works on any government computer, and passes IT security review without app store approvals.

</details>

---

## 🚀 Getting Started

### Option A — Docker (Recommended, Zero Config)

```bash
# 1. Clone
git clone https://github.com/yourteam/nyaaysetu
cd nyaaysetu

# 2. Add your free Gemini API key (aistudio.google.com — no credit card)
echo "GEMINI_API_KEY=AIza..." >> backend/.env

# 3. Start everything
docker-compose up

# 4. Open
# Frontend:  http://localhost:3000
# API docs:  http://localhost:8000/docs
```

**First run:** Downloads ~800MB Docker images. After that: 20 seconds to start.  
**Seed data:** 3 Karnataka HC cases · 6 action items · 3 departments · 2 officers — loads automatically.

### Option B — Manual Setup (Windows)

```powershell
# Backend
cd backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
docker run -d --name nyaay-db -p 5432:5432 `
  -e POSTGRES_USER=nyaay -e POSTGRES_PASSWORD=setu2024 `
  -e POSTGRES_DB=nyaaysetu postgres:16-alpine
python -c "from app.database import create_tables; create_tables()"
python scripts/seed.py
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install && npm run dev
```

### Demo Users (no password required)

| Email | Role | What They See |
|:------|:-----|:--------------|
| `reviewer@karnataka.gov` | Reviewer | Upload & verify extracted fields |
| `officer@karnataka.gov` | Officer | Revenue Dept pending actions |
| `new_officer@karnataka.gov` | Officer | **← Start here** — Transfer Gap demo |
| `head@karnataka.gov` | Dept Head | Full department view |
| `secretary@karnataka.gov` | Secretary | State-wide leaderboard |

---

## 🏆 The Opening Line

When presenting NyaaySetu — to judges, investors, or government officials — open with this:

> *"Every AI legal tool in India was built for judges inside the court.*
> *NyaaySetu is the first system built for the government officer on the other side of the judgment —*
> *the one who must comply or face contempt."*

---

<div align="center">

**Built for [AI for Bharat 2026](https://hackerearth.com/challenges/hackathon/ai-for-bharat-2) · Theme: Justice & Legal Tech · PAN IIT Summit May 2026**

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](.)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)](.)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat&logo=next.js&logoColor=white)](.)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)](.)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](.)
[![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-E8581A?style=flat)](.)

<br/>

*₹0 infrastructure · 10/10 tests passing · `docker-compose up` · NIC-compatible*

</div>
# nyaaysetu

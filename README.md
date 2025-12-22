# Constitutional Debate & Report Generation System

## How It Works

This project is a **Streamlit-based application** that automatically generates **FOR and AGAINST constitutional preparation reports** using a **Retrieval-Augmented Generation (RAG)** pipeline and **multi-round LLM debate**.

---

### Step 1: Setup & Input

* The user launches the Streamlit app.
* The UI asks for:

  * Groq API key
  * Exact Groq model name
* The user provides a **case summary document** (text or upload, maximum 2 pages).

---

### Step 2: RAG Grounding

* The system loads `rag_data` containing:

  * Articles 14, 19, and 21 of the Constitution of India
  * Core doctrines: Reasonable Restrictions, Proportionality, Arbitrariness, and Chilling Effect
* This data is injected into **every LLM call** to keep reasoning constitutionally grounded.

---

### Step 3: Debate Phase

* Two LLM roles are created using the **same Grok model**:

  * **FOR side**
  * **AGAINST side**
* The FOR side starts the debate.
* The AGAINST side responds.
* Each side gets **3 rounds** (total **6 rounds**).
* For every round:

  * Maximum **3 points**
  * Maximum **200 words**
  * Uses case summary + RAG data + previous round output
* A short delay is added between calls to avoid API rate limits.

---

### Step 4: Report Generation

* After the debate ends, a final LLM call generates **two reports**:

  * **FOR-side report**
  * **AGAINST-side report**
* Each report contains:

  * Case summary (from that side’s perspective)
  * Arguments for that side (with reasons)
  * Likely counters from the opposite side (with reasons)
  * How to tackle those counters
* Reports are limited to **under 2 pages** and generated as `.md` files.

---

### Step 5: Output

* The reports are displayed in the Streamlit UI.
* Users can download the files without losing the on-screen content.

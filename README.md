# LLM Service for HireGround 19 Project 🎧🧑‍💼
> **Backend Service for the Virtual Job Fair VR (HireGround19).**

This repository is the backend service that acts as the “brain” of NPCs inside the [HireGround 19](https://github.com/krauchelli/hireground19-project-prototype) project.  
The service receives text input from the Unity client, processes it using **Google Gemini 2.5 Flash**, and returns responses that match each company’s profile.  
The system includes *in-memory* session-based memory management to maintain conversation context.

---

## ✨ Main Features
* **Context-Aware NPCs:** Each NPC has a unique “Knowledge Base” (Company Info, Job Listings, Work Culture).
* **Session Management:** Remembers previous conversation history within an active session (Session ID).
* **Gemini 2.5 Integration:** Uses Google’s LLM model for fast and natural responses.

---

## 🏗 Architecture
**Data Flow:**
1. **Unity Client** requests a session ID first.
2. **Unity Client** (VR) sends the `session_id`, `npc_id`, and `user_text` (or question).
3. **FastAPI** receives the request and validates the `session_id` & `npc_id`.
4. **Prompt Builder** combines: *System Instruction* + *Company Data* + *Chat History*.
5. **Google Gemini** processes the prompt and generates a response.
6. **Backend** stores the chat history and returns the answer to the Unity Client.

---

## 🔌 API Reference
Base URL (Live): `https://fajarramadhan-hireground19-llm-service.hf.space`

### 1. Start Session
Starts or resets a new conversation session. Must be called when a user begins interacting.

* **Endpoint:** `GET /api/start-session`
* **Response:**
    ```json
    {
      "session_id": "UUID-UNIQUE-FROM-UNITY"
    }
    ```

### 2. Delete Session
Deletes session data from the server memory (cleanup).  
Called when the user exits the application.

* **Endpoint:** `POST /api/delete-session/{session_id}`

### 3. Chat Query (LLM)
Sends the user’s question and receives the NPC response.

* **Endpoint:** `POST /api/llm-query`
* **Body:**
    ```json
    {
      "session_id": "UUID-UNIQUE-FROM-UNITY",
      "npc_id": "booth_1",
      "user_text": "Are there any openings for fresh graduates?"
    }
    ```
* **Response:**
    ```json
    {
      "npc_id": "booth_1",
      "answer_text": "Yes, we offer a Management Trainee program for new graduates."
    }
    ```

---

## 💻 How to Install & Run (Local)

### Requirements
* Python 3.9+
* Google Gemini API Key

### Steps
1. **Clone Repository**
    ```bash
    git clone https://github.com/username/hireground-llm-service.git
    cd hireground-llm-service
    ```

2. **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup Environment Variables**
    Create a `.env` file and fill it with:
    ```
    GOOGLE_API_KEY=Paste_Your_Key_Here
    ```

5. **Run the Server**
    ```bash
    uvicorn app:app --reload
    ```
    The server will run at `http://127.0.0.1:8000`.

---

## 📂 Folder Structure
```text
hireground-llm/
├── app.py                  # Application entry point (Routes)
├── requirements.txt        # Library list
├── data/
│   └── npc_data.json       # Static NPC profile database
├── models/
│   ├── chat_request.py     # Body for request
│   ├── chat_response.py    # Body for response
└── services/
    ├── gemini_client.py    # Communication with Google API
    ├── memory_manager.py   # Session chat storage logic
    └── prompt_builder.py   # AI prompt construction logic

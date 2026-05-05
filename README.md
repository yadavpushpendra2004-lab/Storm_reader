📚 StormReader: AI-Powered Research Assistant
StormReader is a heavy-duty document analysis tool designed to transform how researchers and students interact with dense technical material. Unlike standard PDF readers, StormReader integrates a high-speed AI side-panel to provide instant context, summaries, and persistent data management.

🚀 The Journey
This project evolved from an interest in automation (the StormSage engine) into a specialized productivity tool. The goal was to solve the "context switch" problem—where users have to leave their reading environment to search for definitions or explanations. StormReader brings the intelligence directly to the page.

🛠️ Tech Stack
Frontend: Streamlit – For a clean, responsive, and data-focused user interface.

PDF Engine: PyMuPDF (fitz) – Used for high-performance document rendering and text extraction.

AI Orchestration: Groq API – Leveraged for ultra-low latency LLM responses during document deep-dives.

Database: SQLite – Handles local data persistence for bookmarks, notes, and session history.

Language: Python 3.x

✨ Key Features
AI Side-Panel: A persistent chat interface that "reads" along with you. It can summarize complex paragraphs or explain technical jargon in real-time.

Dual View Modes: Includes a Single Page View for deep reading and a Grid Layout Mode for rapid scanning and research across multiple pages.

Persistent Annotations: Integration with SQLite ensures that every highlight and sticky note is saved specifically to its page and remains available across restarts.

Responsive Navigation: Manual page jumping, zoom controls, and integrated keyboard shortcut support for a fluid reading experience.

Secure Config: Uses .env management to ensure sensitive API credentials remain local and secure.

⚙️ Setup & Installation
Clone the repository:

Bash
git clone https://github.com/yadavpushpendra2004-lab/Storm_reader.git
cd Storm_reader
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment:

Rename .env.example to .env.

Add your GROQ_API_KEY.

Run the App:

Bash
streamlit run app.py
📈 Future Roadmap
OCR Support: Integrating Tesseract for analyzing scanned/image-based PDFs.

Vector Search (RAG): Implementing a vector database for "Chat with your Folder" capabilities across multiple documents.

Export Engine: One-click export of AI-generated summaries and manual notes into Markdown or Notion.

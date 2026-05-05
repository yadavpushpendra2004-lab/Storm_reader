import streamlit as st
import fitz  # PyMuPDF
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
from streamlit_javascript import st_javascript

# --- 1. INITIALIZATION ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def init_db():
    conn = sqlite3.connect('storm_reader.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (pdf_name TEXT, page_int INTEGER, content TEXT, 
                 PRIMARY KEY (pdf_name, page_int))''')
    conn.commit()
    conn.close()

init_db()

# --- 2. UI CONFIG ---
st.set_page_config(layout="wide", page_title="Storm AI Reader Pro", page_icon="📚")

# Important: Keep page state consistent
if 'page_num' not in st.session_state: st.session_state.page_num = 1
if 'view_mode' not in st.session_state: st.session_state.view_mode = "Reading Mode"

# --- 3. JAVASCRIPT KEYBOARD LISTENER (Reading Mode Only) ---
# Ye script window ke focus ko pakadti hai aur Streamlit ko signal bhejti hai
if st.session_state.view_mode == "Reading Mode":
    st_javascript("""
        const doc = window.parent.document;
        doc.onkeydown = function(e) {
            if (e.key === 'ArrowRight') {
                window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'nav_trigger', value: 'next'}, '*');
            }
            if (e.key === 'ArrowLeft') {
                window.parent.postMessage({type: 'streamlit:set_widget_value', key: 'nav_trigger', value: 'prev'}, '*');
            }
        };
    """)

# Navigation Signal Handling
nav_action = st.session_state.get('nav_trigger')
if nav_action == 'next':
    st.session_state.page_num += 1
    st.session_state['nav_trigger'] = None # Reset
    st.rerun()
elif nav_action == 'prev':
    st.session_state.page_num = max(1, st.session_state.page_num - 1)
    st.session_state['nav_trigger'] = None # Reset
    st.rerun()

# --- 4. SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.title("🚀 Storm Control")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        total_pages = len(doc)
        st.session_state.page_num = max(1, min(st.session_state.page_num, total_pages))
        
        st.divider()
        # View Switcher
        view_choice = st.radio("View Mode", ["Reading Mode", "Grid Layout"], horizontal=True)
        st.session_state.view_mode = view_choice
        
        if st.session_state.view_mode == "Reading Mode":
            st.metric("Current Page", f"{st.session_state.page_num} / {total_pages}")
            target = st.number_input("Jump to Page", 1, total_pages, st.session_state.page_num)
            if target != st.session_state.page_num:
                st.session_state.page_num = target
                st.rerun()

# --- 5. MAIN CONTENT ---
if uploaded_file:
    if st.session_state.view_mode == "Reading Mode":
        col_pdf, col_side = st.columns([2.5, 1.5])
        page = doc.load_page(st.session_state.page_num - 1)

        with col_pdf:
            st.subheader(f"📖 Reading: Page {st.session_state.page_num}")
            # Zoom level for high quality
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            st.image(pix.tobytes("png"), use_container_width=True)

        with col_side:
            st.subheader("📝 Selectable Text & AI")
            st.text_area("Select from here:", value=page.get_text("text"), height=400, key=f"txt_{st.session_state.page_num}")
            
            st.divider()
            st.subheader("🤖 AI Assistant")
            st.text_input("Ask AI about this page:", placeholder="Explain the main concept...")
            st.button("🔍 Search with Groq")
            st.caption("Press → for Next Page | ← for Previous Page")

    else:
        # --- GRID LAYOUT ---
        st.subheader("🖼️ PDF Grid View")
        rows = (total_pages // 4) + 1
        for r in range(rows):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                if idx < total_pages:
                    with cols[c]:
                        thumb_page = doc.load_page(idx)
                        pix = thumb_page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
                        st.image(pix.tobytes("png"), caption=f"Page {idx+1}", use_container_width=True)
                        if st.button(f"Open P.{idx+1}", key=f"btn_{idx}"):
                            st.session_state.page_num = idx + 1
                            st.session_state.view_mode = "Reading Mode"
                            st.rerun()
else:
    st.info("Please upload your PDF to start.")
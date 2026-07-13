import streamlit as st
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="SAU Faculty AI Assistant", page_icon="🤠", layout="centered")

# --- INTERACTIVE TOUR SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #003366;'>🤠 Mulerider Tour Guide</h2>", unsafe_allow_html=True)
    st.write("Welcome to your AI Assistant! Here is how to get the most out of it:")
    
    with st.expander("📖 Quick-Start Instructions", expanded=True):
        st.markdown("""
        1. **Upload Context (Optional):** Drag in syllabi, notes, or policy PDFs.
        2. **Select or Type Task:** Use a one-click demo button or type your custom goal below.
        3. **Execute:** Click launch to run live web grounding and document analysis.
        """)
    
    st.markdown("### 🚀 One-Click Demo Scenarios")
    st.caption("Click any workflow button below to instantly load a tailored test prompt:")
    
    # Session state trick to hold the demo prompts dynamically
    if "demo_prompt" not in st.session_state:
        st.session_state.demo_prompt = ""

    if st.button("📰 Latest SAU News"):
        st.session_state.demo_prompt = "Search the web and summarize the 3 most recent academic announcements or events from the official Southern Arkansas University website."
        
    if st.button("🔍 Policy & Grant Research"):
        st.session_state.demo_prompt = "Search for current Southern Arkansas University institutional policy updates regarding faculty research grants or standard deadlines."
        
    if st.button("📊 Committee Memo Draft"):
        st.session_state.demo_prompt = "Draft a professional, structured internal memo summarizing my uploaded data notes for the upcoming department curriculum committee review."
        
    if st.button("🎓 Syllabus Objectives Check"):
        st.session_state.demo_prompt = "Cross-reference my uploaded syllabus content with standard higher education Bloom's Taxonomy frameworks. Suggest 3 actionable improvements to make the learning objectives more measurable."

    if st.button("🤝 Student Advising Guide"):
        st.session_state.demo_prompt = "Based on standard academic advising best practices, outline a step-by-step framework to help a student navigate a mid-semester transition, detailing critical engagement check-ins."

    if st.button("📝 Rubric & Feedback Engine"):
        st.session_state.demo_prompt = "Analyze my uploaded assignment guidelines and draft a transparent, 4-tier grading rubric focused on critical thinking, clarity, and structural evidence."

    st.write("---")
    st.caption("✨ Grounding Engine: Every query triggers live search parameters to prevent factual hallucinations.")

# --- MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #003366;'>🤠 Southern Arkansas University</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>Mulerider Academic & Admin AI Assistant</h3>", unsafe_allow_html=True)
st.write("---")

st.markdown("#### 📁 Department Document Hub")
uploaded_file = st.file_uploader("Drag and drop an academic document", type=["txt", "csv", "md", "pdf"])

document_content = ""
if uploaded_file:
    try:
        document_content = uploaded_file.read().decode("utf-8")
        st.success(f"Loaded successfully: {uploaded_file.name}")
    except Exception as e:
        st.error("Could not parse file as text. Currently, this prototype processes text-based layouts.")

st.markdown("#### 💬 Instruct your Assistant")
user_prompt = st.text_area(
    "What would you like the agent to do?", 
    value=st.session_state.demo_prompt,
    placeholder="e.g., 'Search the web for the latest guidelines...'"
)

if st.button("Execute Task 🚀", use_container_width=True):
    if not user_prompt:
        st.warning("Please enter an instruction or click a demo scenario button from the sidebar first!")
    else:
        # Start execution timer
        start_time = time.time()
        
        with st.spinner("Mulerider Agent executing task (Searching live web sources & compiling results)..."):
            try:
                client = genai.Client()
                
                config = types.GenerateContentConfig(
                    system_instruction="You are an elite academic administrative AI assistant for Southern Arkansas University.",
                    tools=[{"google_search": {}}]
                )
                
                full_query = user_prompt
                if document_content:
                    full_query = f"Context Document:\n{document_content}\n\nUser Instruction: {user_prompt}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_query,
                    config=config
                )
                
                # Stop execution timer
                elapsed_time = round(time.time() - start_time, 1)
                
                st.success(f"Analysis Complete! ⏱️ Task executed in {elapsed_time} seconds.")
                st.markdown(response.text)
                
                if response.candidates and response.candidates[0].grounding_metadata:
                    metadata = response.candidates[0].grounding_metadata
                    if metadata.web_search_queries:
                        st.markdown("---")
                        st.markdown("**🔍 Grounding Sources Used:**")
                        for query in metadata.web_search_queries:
                            st.caption(f"- Searched: *{query}*")
                            
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
                st.info("Note: Make sure your GEMINI_API_KEY environment variable is set up in your terminal session.")

# ==========================================
# FACULTY FEEDBACK & TRANSPARENCY HUB
# ==========================================
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.markdown("---")
st.header("💬 Faculty Feedback & Transparency Hub")
st.caption("Share your thoughts, report bugs, or request features. All posts are visible to the community below.")

# 1. Establish connection to your backend Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Setup the Input Form
with st.form(key="feedback_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        user_name = st.text_input("Your Name / Department (or leave blank for Anonymous)", placeholder="Anonymous")
    with col2:
        feed_type = st.selectbox("Feedback Type", ["Question", "Suggestion", "Complaint", "Kudos 🤠"])
        
    user_comment = st.text_area("Your Voice", placeholder="What's on your mind? Be as candid as you'd like...")
    submit_button = st.form_submit_button(label="Post to Community Wall 🚀")

# 3. Handle Form Submission
if submit_button and user_comment:
    # Read existing data
    existing_data = conn.read(worksheet="Sheet1", ttl=0)
    
    # Create new row profile
    new_row = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": user_name if user_name else "Anonymous Mulerider",
        "Type": feed_type,
        "Comment": user_comment
    }])
    
    # Concatenate and write back to the cloud sheet
    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated_df)
    st.success("Successfully added to the public wall!")
    st.rerun()

# 4. Display the Public Rolling Wall
st.subheader("📋 Community Notice Board")
try:
    # Read data fresh
    df = conn.read(worksheet="Sheet1", ttl="1m")
    
    if not df.empty and len(df) > 0:
        # Reverse to show newest comments first
        for idx, row in df.iloc[::-1].iterrows():
            with st.container():
                st.markdown(f"**{row['Name']}** ({row['Type']}) • *{row['Timestamp']}*")
                st.info(row['Comment'])
                st.markdown("")
    else:
        st.write("No entries yet. Be the first to start the conversation!")
except Exception as e:
    st.write("Initializing community board data stream...")

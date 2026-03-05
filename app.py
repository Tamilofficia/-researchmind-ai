import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import io
from dotenv import load_dotenv

# Set page config FIRST before doing anything else
st.set_page_config(page_title="ResearchMind AI", page_icon="🧠", layout="wide")

load_dotenv()

# We changed parser to pdf_parser to fix Streamlit Cloud conflicts
from parse_pdf.parse_paper import parse_pdf
from ai.claim_extractor import extract_claims
from ai.relationship import detect_relationships
from ai.arxiv_fetcher import search_arxiv
from ai.fact_checker import verify_claims
from ai.analyzer import analyze_paper_metrics
from graph.graph_builder import build_graph

# --- ADVANCED PREMIUM CSS & ANIMATIONS ---
st.markdown("""
    <style>
    /* Hide the default Streamlit hamburger menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Interactive Button Animations */
    .stButton > button {
        transition: all 0.3s ease-in-out !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
        border-color: #6366f1 !important;
    }
    .stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* Input field focus animations */
    .stTextInput > div > div > input {
        transition: all 0.3s ease-in-out !important;
    }
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.4) !important;
        border-color: #a855f7 !important;
    }

    /* Make metric cards pop and hover */
    [data-testid="metric-container"] {
        background-color: #112240;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #233554;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    [data-testid="metric-container"]:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Fade in animation for the main container */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .block-container {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Style the main title with a gradient */
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #3b82f6, #60a5fa, #3b82f6);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0px;
        animation: shine 3s linear infinite;
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }
    .subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CACHED AI FUNCTIONS (For Instant Tab Switching) ---
@st.cache_data(show_spinner=False)
def cached_parse_pdf(file_bytes):
    # Pass raw bytes to cache correctly, then wrap for PyMuPDF
    return parse_pdf(io.BytesIO(file_bytes))

@st.cache_data(show_spinner=False)
def cached_extract_claims(text):
    return extract_claims(text)

@st.cache_data(show_spinner=False)
def cached_analyze_metrics(text):
    return analyze_paper_metrics(text)

@st.cache_data(show_spinner=False)
def cached_detect_relations(claims):
    return detect_relationships(claims)

@st.cache_data(show_spinner=False)
def cached_search_arxiv(query):
    return search_arxiv(query)

@st.cache_data(show_spinner=False)
def cached_verify_claims(claims, arxiv_results):
    return verify_claims(claims, arxiv_results)


# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_position" not in st.session_state:
    st.session_state.user_position = ""

def login():
    if not st.session_state.email_input or not st.session_state.fname_input:
        st.error("Please enter your First Name and Workspace Email to proceed.")
    else:
        st.session_state.logged_in = True
        st.session_state.user_email = st.session_state.email_input
        st.session_state.user_name = f"{st.session_state.fname_input} {st.session_state.lname_input}".strip()
        st.session_state.user_position = st.session_state.pos_input

def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- MOCK LOGIN PAGE ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<h1 class="gradient-text" style="text-align: center;">ResearchMind AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle" style="text-align: center;">Deep Paper Autopsy & Fact-Checking</p>', unsafe_allow_html=True)
        
        st.text_input("First Name", key="fname_input")
        st.text_input("Last Name", key="lname_input")
        import datetime
        st.date_input(
            "Date of Birth", 
            min_value=datetime.date(1900, 1, 1), 
            max_value=datetime.date.today(), 
            key="dob_input"
        )
        st.selectbox("Position", ["Organization", "Teacher", "Professor", "Student"], key="pos_input")
        st.text_input("Workspace Email", key="email_input")
        st.text_input("Password", type="password", key="pwd_input")
        
        st.button("Sign In →", on_click=login, type="primary", use_container_width=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("This is a demo for the hackathon. Any email will work.")

# --- MAIN DASHBOARD ---
else:
    # Sidebar Navigation mimicking a Web App
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_name}")
        st.caption(f"{st.session_state.user_position}")
        st.markdown("---")
        st.button("⚙️ Settings")
        st.button("📁 My Uploads")
        st.markdown("---")
        st.button("Logout 🚪", on_click=logout, type="primary")

    st.markdown('<h2 class="gradient-text">Intelligence Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type=["pdf"])

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        
        with st.status("Performing Deep Paper Autopsy...", expanded=True) as status:
            st.write("📄 Parsing document...")
            text = cached_parse_pdf(file_bytes)
            
            import time
            try:
                st.write("🧠 Extracting claims & computing metrics...")
                claims = cached_extract_claims(text)
                time.sleep(2) # Prevent Gemini Free Tier rate-limit
                
                metrics = cached_analyze_metrics(text)
                time.sleep(2)
                
                st.write("🔗 Mapping interactive knowledge relationships...")
                relations = cached_detect_relations(claims)
                graph_html = build_graph(relations) # Don't cache HTML generation, it's fast
                time.sleep(2)
                
                st.write("🔎 Performing Literature Review against ArXiv...")
                search_query = claims[:150] if claims else "research paper"
                arxiv_results = cached_search_arxiv(search_query)
                verification_report = cached_verify_claims(claims, arxiv_results) if arxiv_results else "No relevant ArXiv context found."
                
                status.update(label="Analysis Complete! Interface is now lightning fast.", state="complete", expanded=False)
            except Exception as e:
                # If Gemini API gets exhausted, show a clean red warning and stop Instead of crashing the whole Streamlit app
                status.update(label="API Rate Limit Hit", state="error", expanded=True)
                st.error(f"**Google AI API Error:** The free tier is currently overloaded. Please wait 60 seconds and try again.\n\n`{str(e)}`")
                st.stop()

        # --- TABBED INTERFACE ---
        tab1, tab2, tab3, tab4 = st.tabs(["📑 Overview", "🔎 Verification", "📈 Advanced Analytics", "🕸️ Knowledge Graph"])
        
        with tab1:
            st.subheader("Executive Summary")
            st.write(metrics.get("summary", "No summary available."))
            
            st.subheader("Critical Insights")
            st.markdown(metrics.get("critical_insights", "N/A"))
            
            limitations = metrics.get("limitations", "None found.")
            if limitations != "N/A" and limitations.strip() != "":
                st.warning(f"**Key Limitations & Biases admitted in text:**\n\n{limitations}", icon="⚠️")
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Scientific Rigor", value=f"{metrics.get('scientific_rigor', 0)} / 100")
            with col2:
                st.metric(label="Commercial Feasibility", value=f"{metrics.get('commercial_feasibility', 0)} / 100")
            with col3:
                st.metric(label="Tech Readiness Level", value=f"TRL {metrics.get('trl', 1)}")

        with tab2:
            st.subheader("Extracted Claims")
            st.info(claims)
            
            st.subheader("ArXiv Fact-Checking Results")
            st.success(verification_report)
            
            with st.expander("Show Connected ArXiv Papers"):
                st.write(arxiv_results)

        with tab3:
            st.subheader("Quantitative Output")
            colA, colB, colC = st.columns(3)
            
            # Gauge Chart for Rigor
            rigor_score = int(metrics.get('scientific_rigor', 0))
            fig_rigor = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = rigor_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Scientific Rigor"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#10b981"}, # Emerald
                    'steps': [{'range': [0, 50], 'color': "rgba(255,255,255,0.1)"}],
                }
            ))
            fig_rigor.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "#f8fafc"})
            
            # Gauge Chart for Feasibility
            feasibility_score = int(metrics.get('commercial_feasibility', 0))
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = feasibility_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Commercial Feasibility"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#6366f1"},
                    'steps': [{'range': [0, 50], 'color': "rgba(255,255,255,0.1)"}],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "#f8fafc"})
            
            # Simple Bar Chart for TRL
            trl_score = int(metrics.get('trl', 1))
            fig_bar = go.Figure(data=[go.Bar(
                x=['Status'], 
                y=[trl_score],
                marker_color='#a855f7'
            )])
            fig_bar.update_layout(
                title="TRL Score (Max 9)",
                yaxis=dict(range=[0, 9]),
                height=250,
                margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#f8fafc"}
            )

            with colA:
                st.plotly_chart(fig_rigor, use_container_width=True)
            with colB:
                st.plotly_chart(fig_gauge, use_container_width=True)
            with colC:
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab4:
            st.subheader("Interactive Entity Map")
            st.caption("Drag nodes to organize physics. Hover over edges to see relationship types.")
            # Render the PyVis interactive graph
            components.html(graph_html, height=470, scrolling=False)
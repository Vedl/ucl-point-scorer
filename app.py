import streamlit as st
import pandas as pd
import player_score_calculator
import sofascore_adapter
import whoscored_search
import time

st.set_page_config(page_title="UCL Fantasy Point Scorer", page_icon="⚽", layout="wide")

# Custom CSS for premium styling
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Root variables */
    :root {
        --primary: #3b82f6;
        --primary-hover: #2563eb;
        --primary-glow: rgba(59, 130, 246, 0.4);
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.6);
        --border: rgba(148, 163, 184, 0.15);
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 25%),
            radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.12) 0%, transparent 25%),
            radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Custom header styling */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #3b82f6 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        color: var(--text-muted);
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
        color: white;
        padding: 0.35rem 1rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
        color: var(--text-main) !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-glow) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.45) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.45) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
        color: var(--text-muted) !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 0.75rem 0.75rem !important;
    }
    
    /* Status container */
    div[data-testid="stStatusWidget"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Alert styling */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 0.75rem !important;
        color: #34d399 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 0.75rem !important;
        color: #fbbf24 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 0.75rem !important;
        color: #f87171 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 0.75rem !important;
        color: #60a5fa !important;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border-radius: 1rem !important;
        overflow: hidden !important;
    }
    
    div[data-testid="stDataFrame"] > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Table header */
    div[data-testid="stDataFrame"] th {
        background: rgba(59, 130, 246, 0.2) !important;
        color: var(--text-main) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Table rows */
    div[data-testid="stDataFrame"] td {
        background: transparent !important;
        color: var(--text-main) !important;
        border-bottom: 1px solid var(--border) !important;
    }
    
    div[data-testid="stDataFrame"] tr:hover td {
        background: rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
    }
    
    /* Footer styling */
    .footer-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .footer-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-main);
        margin-bottom: 0.5rem;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Position badges */
    .pos-gk { 
        background: linear-gradient(135deg, #f59e0b, #d97706); 
        padding: 0.25rem 0.75rem; 
        border-radius: 0.5rem; 
        font-weight: 600;
        font-size: 0.75rem;
    }
    .pos-def { 
        background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
        padding: 0.25rem 0.75rem; 
        border-radius: 0.5rem; 
        font-weight: 600;
        font-size: 0.75rem;
    }
    .pos-mid { 
        background: linear-gradient(135deg, #10b981, #059669); 
        padding: 0.25rem 0.75rem; 
        border-radius: 0.5rem; 
        font-weight: 600;
        font-size: 0.75rem;
    }
    .pos-fwd { 
        background: linear-gradient(135deg, #ef4444, #dc2626); 
        padding: 0.25rem 0.75rem; 
        border-radius: 0.5rem; 
        font-weight: 600;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div style="text-align: center;"><span class="hero-badge">⚽ Champions League</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">UCL Fantasy Point Scorer</h1>', unsafe_allow_html=True)
st.markdown('''
<p class="hero-subtitle">
    Calculate fantasy points for Champions League players with precision.<br>
    Enter a <strong style="color: #3b82f6;">SofaScore Match URL</strong> below to get started.
</p>
''', unsafe_allow_html=True)

# Input
col1, col2 = st.columns([3, 1])
with col1:
    sofascore_url = st.text_input("SofaScore Match URL", placeholder="https://www.sofascore.com/...")

with st.expander("Advanced: Manual WhoScored URL (Optional)"):
    manual_ws_url = st.text_input("WhoScored URL", placeholder="Leave empty to auto-detect", help="If auto-detection fails, you can paste the URL here to ensure accurate positions.")

if st.button("Calculate Scores", type="primary"):
    if not sofascore_url:
        st.error("Please enter a SofaScore URL.")
    else:
        with st.status("Processing...", expanded=True) as status:
            start_time = time.time()
            
            # 1. Identify Match
            st.write("🔍 Identifying match...")
            try:
                match_id = sofascore_adapter.get_match_id(sofascore_url)
                meta = sofascore_adapter.get_match_metadata(match_id)
                
                if not meta:
                    st.error("Could not fetch match metadata from SofaScore.")
                    status.update(label="Failed", state="error")
                    st.stop()
                    
                home_team = meta['event']['homeTeam']['name']
                away_team = meta['event']['awayTeam']['name']
                st.write(f"Match: **{home_team}** vs **{away_team}**")
                
                # 2. Find WhoScored URL
                whoscored_url = manual_ws_url.strip()
                
                if not whoscored_url:
                    st.write("🕵️‍♂️ Searching for WhoScored data...")
                    whoscored_url, search_logs = whoscored_search.find_match_url(home_team, away_team)
                
                if whoscored_url:
                    st.success(f"Using WhoScored Data: {whoscored_url}")
                else:
                    st.warning("WhoScored match not found automatically. Using SofaScore positions (less accurate for Wing-Backs).")
                    with st.expander("Search Debug Logs (for troubleshooting)"):
                        st.code("\n".join(search_logs))
                
                # 3. Calculate Scores
                st.write("📊 Calculating points...")
                df_scores = player_score_calculator.calc_all_players(sofascore_url, whoscored_url)
                
                if df_scores.empty:
                    st.error("Failed to calculate scores.")
                    status.update(label="Calculation failed", state="error")
                else:
                    duration = time.time() - start_time
                    status.update(label=f"Done in {duration:.2f}s", state="complete")
                    
                    # 4. Display Results
                    st.success("Calculations complete!")
                    
                    # Filter and Sort
                    df_display = df_scores[['name', 'score', 'pos']].copy()
                    df_display = df_display.sort_values(by="score", ascending=False)
                    
                    # Display Table
                    st.dataframe(
                        df_display,
                        column_config={
                            "name": "Player Name",
                            "score": st.column_config.NumberColumn("Points", format="%.0f"),
                            "pos": "Position"
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Download
                    csv = df_display.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f'fantasy_points_{home_team}_{away_team}.csv',
                        mime='text/csv',
                    )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                status.update(label="Error", state="error")
                print(e) # Log to console

# Footer
st.markdown("---")
st.markdown("""
<div class="footer-section">
    <p class="footer-title">🚀 Ready to Deploy?</p>
    <p style="color: #94a3b8; margin: 0;">
        Share this tool with your fantasy league! Deploy to 
        <a href="https://streamlit.io/cloud" target="_blank" style="color: #3b82f6; text-decoration: none;">Streamlit Community Cloud</a> 
        for free hosting.
    </p>
</div>
""", unsafe_allow_html=True)

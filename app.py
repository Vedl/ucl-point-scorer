import streamlit as st
import pandas as pd
import player_score_calculator
import sofascore_adapter
import whoscored_search
import time

st.set_page_config(page_title="UCL Fantasy Point Scorer", page_icon="⚽", layout="wide")

st.title("⚽ UCL Fantasy Point Scorer")
st.markdown("""
This app calculates fantasy points for Champions League players.
Enter the **SofaScore Match URL** below. The system will attempt to automatically find the corresponding WhoScored data for improved accuracy.
""")

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

st.markdown("---")
st.markdown("### Deployment info")
st.info("To share this with others, verify the output and deploy to Streamlit Community Cloud.")

import streamlit as st
import pandas as pd
import yaml
from runner import run

st.set_page_config(page_title="Automation Pipeline", layout="wide")

st.title("Automation Pipeline Dashboard")

# Load config to get sources
try:
    with open("config/sources.yaml", "r") as f:
        config = yaml.safe_load(f)
    sources = config.get("sources", [])
    source_names = [s["name"] for s in sources]
except Exception as e:
    st.error(f"Failed to load sources.yaml: {e}")
    st.stop()

# Sidebar Controls
st.sidebar.header("Configuration")

# Source Selection
selected_sources = st.sidebar.multiselect(
    "Select Sources to Scrape",
    options=range(len(source_names)),
    format_func=lambda x: source_names[x],
    default=range(len(source_names))
)

# Keywords
keywords = st.sidebar.text_input("Filter Keywords (comma-separated)", help="e.g. python, remote")

# Settings
dry_run = st.sidebar.checkbox("Dry Run (No Save)", value=True)
gsheet_name = st.sidebar.text_input("Google Sheet Name (Optional)")

if st.sidebar.button("Run Pipeline", type="primary"):
    with st.spinner("Wrapper running..."):
        try:
            # Determine if running all or specific
            # Logic: If all selected, run_all=True. Else loop or single run?
            # runner.py 'run' function takes single source_index OR run_all.
            # If we select a subset, we might need to run loop here or update runner to accept list.
            # For simplicity, if len(selected) == len(all), use run_all=True.
            # If subset, we will run iteratively and collect results.
            
            # Correction: runner.py `run` returns list. We can aggregate here.
            
            all_results = []
            
            if len(selected_sources) == len(source_names):
                # Run all
                results = run(run_all=True, dry_run=dry_run, gsheet_name=gsheet_name, keywords=keywords)
                all_results.extend(results)
            else:
                # Run selected
                for idx in selected_sources:
                    results = run(source_index=idx, dry_run=dry_run, gsheet_name=gsheet_name, keywords=keywords)
                    # Note: runner's built-in deduplication runs per 'run' call. 
                    # If we run multiple times, we might have dupes between calls if sources overlap (unlikely)
                    # But keyword filtering happens in run().
                    all_results.extend(results)

            if all_results:
                df = pd.DataFrame(all_results)
                st.success(f"Processed {len(all_results)} records!")
                
                # Display Data
                st.subheader("Results")
                st.dataframe(df, use_container_width=True)
                
                # Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    "pipeline_results.csv",
                    "text/csv",
                    key='download-csv'
                )
            else:
                st.warning("No records found matching criteria.")
                
        except Exception as e:
            st.error(f"Error during execution: {e}")
            st.exception(e)

# Log Viewer
with st.expander("📝 Execution Logs", expanded=False):
    if st.button("Refresh Logs"):
        st.rerun()
    
    try:
        with open("logs/last_run.log", "r") as f:
            log_content = f.read()
            # Show last 2000 chars if too long, or reversed? 
            # Usually seeing the end is most important.
            st.code(log_content, language="log")
    except FileNotFoundError:
        st.warning("No log file found yet.")

st.sidebar.markdown("---")
st.sidebar.info("v1.0.0 - Streamlit Edition")

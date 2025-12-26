import streamlit as st
import requests
import json
import base64
import pandas as pd
from datetime import datetime
import time
import logging

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DFS_API_URL = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
# Using the credentials provided
CREDENTIALS_B64 = "dXNlcjJAcmFua2ZhbS5jb206NzBmZmQ0YWUzNWI0NjdjNw=="

# --- CLASS 1: DATA FOR SEO API HANDLER ---
class DataForSEOClient:
    def __init__(self, auth_header):
        self.headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/json'
        }

    def fetch_serp(self, keyword, location_code, device="desktop"):
        """Fetches the top 100 results for a keyword."""
        post_data = [{
            "language_code": "en",
            "location_code": location_code,
            "keyword": keyword,
            "device": device,
            "depth": 100 
        }]
        
        try:
            response = requests.post(DFS_API_URL, headers=self.headers, data=json.dumps(post_data), timeout=60)
            if response.status_code == 200:
                result = response.json()
                if result['status_code'] == 20000:
                    return result['tasks'][0]['result'][0]['items']
                else:
                    logger.error(f"API Error: {result['status_message']}")
                    return None
            else:
                logger.error(f"HTTP Error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return None

    def analyze_rank(self, items, target_domain):
        """Scans SERP items to find rank, Map Pack status, and top competitor."""
        my_organic_rank = "Not Found"
        my_url = "N/A"
        top_competitor = "N/A"
        in_map_pack = "No" # New field for Map Pack detection
        
        if not items:
            return my_organic_rank, my_url, top_competitor, in_map_pack

        # --- Pass 1: Find Top Competitor and Organic Rank ---
        for item in items:
            # 1. Top Competitor (First organic result found)
            if item['type'] == 'organic' and top_competitor == "N/A" and item.get('domain'):
                 # Ensure top competitor is not the target domain itself
                if target_domain.lower() not in item.get('domain', '').lower():
                    top_competitor = item.get('domain')
            
            # 2. My Organic Rank
            if item['type'] == 'organic':
                if target_domain.lower() in item.get('domain', '').lower():
                    my_organic_rank = item['rank_group']
                    my_url = item['url']
            
            # --- Pass 2: Check for Map Pack Appearance ---
            # Map Pack results have 'type' = 'local_pack'
            if item['type'] == 'local_pack':
                for local_item in item.get('items', []):
                    # Local listings often don't have a 'domain' field, but they have 'url' which contains the domain
                    url_check = local_item.get('url', '')
                    if target_domain.lower() in url_check.lower():
                        in_map_pack = f"Yes (Rank {local_item.get('rank_group', '?')})"
                        # Prioritize the rank from the Map Pack if found
                        my_organic_rank = my_organic_rank if my_organic_rank != "Not Found" else "Not Applicable (Map Pack)"
                        break # Stop searching the local pack once found

        return my_organic_rank, my_url, top_competitor, in_map_pack

# --- HELPER: CSV CONVERTER ---
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# --- MAIN APPLICATION ---
def main():
    st.set_page_config(page_title="Young10 SERP Tracker V3", layout="wide")
    
    st.title("🚀 Young10 SERP Tracker V3")
    st.markdown("🎯 **Enhanced Accuracy:** Now tracks Organic Rank AND Local Map Pack Status")

    # Initialize Session State for Data Persistence
    if 'results_df' not in st.session_state:
        st.session_state['results_df'] = None

    # --- SIDEBAR CONFIG ---
    st.sidebar.header("⚙️ Configuration")
    
    # NEW: DEVELOPER CREDIT
    st.sidebar.caption("Developed by: **Abdullah ZK**")
    st.sidebar.markdown("---")
    
    target_domain = st.sidebar.text_input("Target Domain (e.g., young10)", value="young10")
    location_code = st.sidebar.number_input("Location Code (2840=USA)", value=2840)
    device_type = st.sidebar.selectbox("Device Type", ["desktop", "mobile"])
    
    # --- MAIN INPUT ---
    with st.container():
        st.subheader("1. Enter Keywords")
        keywords_input = st.text_area("One keyword per line (Use local terms for Map Pack test)", height=150,
                                      value="roofing services in Austin,TX\nplumbing in New York\ngraphic design agency")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            run_btn = st.button("🔎 Start Scan", type="primary")
    
    # --- PROCESSING LOGIC ---
    if run_btn:
        dfs = DataForSEOClient(CREDENTIALS_B64)
        keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
        
        if not keywords:
            st.warning("Please enter at least one keyword.")
        else:
            progress_bar = st.progress(0)
            results_data = []
            status_text = st.empty()

            for i, keyword in enumerate(keywords):
                time.sleep(0.5) # Rate limit safety
                
                status_text.text(f"Scanning ({i+1}/{len(keywords)}): {keyword}...")
                
                # API Call
                items = dfs.fetch_serp(keyword, location_code, device_type)
                
                # Analysis
                if items:
                    rank, url, top_comp, map_status = dfs.analyze_rank(items, target_domain)
                    results_data.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Keyword": keyword,
                        "Organic Rank": rank,
                        "Map Pack Status": map_status, # NEW COLUMN
                        "Target URL": url,
                        "Top Competitor (#1)": top_comp,
                        "Device": device_type,
                    })
                else:
                    results_data.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Keyword": keyword,
                        "Organic Rank": "API Fail",
                        "Map Pack Status": "API Fail",
                        "Target URL": "N/A",
                        "Top Competitor (#1)": "N/A",
                        "Device": device_type,
                    })
                
                progress_bar.progress((i + 1) / len(keywords))
            
            status_text.empty()
            st.success("Scan Complete!")
            
            # Save to Session State
            st.session_state['results_df'] = pd.DataFrame(results_data)

    # --- RESULTS DISPLAY ---
    if st.session_state['results_df'] is not None:
        st.markdown("---")
        st.subheader("2. Scan Results")
        
        df = st.session_state['results_df']
        st.dataframe(df, use_container_width=True)
        
        # CSV Download Button
        csv = convert_df_to_csv(df)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f'serp_report_v3_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
            mime='text/csv',
        )
        
        # Metrics Summary
        col1, col2 = st.columns(2)
        
        found_organic = df[df['Organic Rank'].apply(lambda x: isinstance(x, int) or x.isdigit())].shape[0]
        found_map = df[df['Map Pack Status'].str.startswith('Yes')].shape[0]
        
        col1.metric("Keywords Ranked Organically (1-100)", f"{found_organic} / {len(df)}")
        col2.metric("Keywords in Local Map Pack", f"{found_map} / {len(df)}")


if __name__ == "__main__":
    main()










import streamlit as st
import pandas as pd
import json
import api_client
# Lazy imports: analysis and analytics are now imported only where needed to speed up initial load

# Page Config
st.set_page_config(
    page_title="AI Contract Analysis System",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Black & Blue Theme
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #0E1117; /* Dark Background */
        color: #E0E0E0;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #4A90E2 !important; /* Soft Blue */
    }
    
    /* Custom Header Classes */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #4A90E2, #00D2FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #B0BEC5;
        border-bottom: 2px solid #2962FF; /* Deep Blue Border */
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Cards */
    .card {
        background-color: #1E1E1E; /* Dark Grey Card */
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #4A90E2;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(to right, #2962FF, #4A90E2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        opacity: 0.9;
        box-shadow: 0 0 15px rgba(74, 144, 226, 0.6); 
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #262730;
        color: #fff;
        border: 1px solid #4A90E2;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* Landing Page Hero */
    .hero-container {
        text-align: center;
        padding: 100px 20px;
    }
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.8rem;
        color: #4A90E2;
        margin-bottom: 40px;
    }
    .feature-card {
        background: #161B22;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #30363D;
        text-align: center;
    }
    
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = "landing" # landing, auth, dashboard
if "user_session" not in st.session_state:
    st.session_state.user_session = None

# --- NAVIGATION FUNCTIONS ---
def go_to_auth():
    st.session_state.page = "auth"
    st.rerun()

def go_to_dashboard():
    st.session_state.page = "dashboard"
    st.rerun()

def logout():
    st.session_state.user_session = None
    st.session_state.page = "landing"
    st.rerun()

# --- PAGES ---

def landing_page():
    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">AI Contract Analysis</div>
            <div class="hero-subtitle">The Future of Legal Intelligence</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown(
            "<p style='text-align: center; font-size: 1.2rem; color: #ccc; margin-bottom: 30px;'>"
            "Identify risks, automate compliance, and extract insights from your legal documents in seconds."
            "</p>", unsafe_allow_html=True
        )
        # Giant CTA Button
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        with btn_col2:
            if st.button("🚀 Get Started Now", use_container_width=True):
                go_to_auth()

    # Features Section
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: white;'>Why Choose Us?</h2>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
            <div class="feature-card">
                <h3>⚡ Fast Analysis</h3>
                <p>Process complex contracts in under 30 seconds using advanced Gemini Flash models.</p>
            </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
            <div class="feature-card">
                <h3>🛡️ Risk Detection</h3>
                <p>Automatically identify high-risk clauses and missing compliance requirements.</p>
            </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
            <div class="feature-card">
                <h3>📊 Smart Dashboard</h3>
                <p>Track your entire contract lifecycle with interactive charts and alerts.</p>
            </div>
        """, unsafe_allow_html=True)


def auth_page():
    st.markdown("<div class='main-header'>Welcome Back</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        with st.container(border=True):
            auth_mode = st.radio("Access Mode", ["Login", "Signup"], horizontal=True)
            st.divider()
            
            if auth_mode == "Login":
                st.subheader("Login")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.button("Secure Login", use_container_width=True):
                    # Simplified logic for demo
                    user_data = {
                        "email": email, 
                        "login_attempts": 1, 
                        "ip_address": "192.168.1.5",
                        "user_agent": "Chrome/120.0"
                    }
                    
                    sec_check = api_client.validate_security("login", user_data)
                        
                    if sec_check.get("error"):
                            st.error(f"Security Error: {sec_check['error']}")
                    else:
                        login_sec = sec_check.get("login_security") or {}
                        risk = login_sec.get("risk_level", "High")
                        action = login_sec.get("recommended_action", "Block")
                        
                        if action == "Allow":
                            role = "User"
                            st.session_state.user_session = {"name": email.split("@")[0], "email": email, "role": role}
                            st.success(f"Login Approved. Risk: {risk}")
                            go_to_dashboard()
                        else:
                            st.error(f"Login Blocked. Risk: {risk}")

            elif auth_mode == "Signup":
                st.subheader("Create Account")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("New Email")
                new_pass = st.text_input("New Password", type="password")
                # Role is always User
                
                if st.button("Create Account", use_container_width=True):
                     user_data = {
                        "name": new_name, "email": new_email, "password": new_pass, "role": "User"
                    }
                     with st.spinner("Analyzing Password Strength & Policy..."):
                        sec_check = api_client.validate_security("signup", user_data)
                        
                        if sec_check.get("error"):
                             st.error(f"Signup Error: {sec_check['error']}")
                        else:
                            signup_val = sec_check.get("signup_validation") or {}
                            if signup_val.get("is_valid", False):
                                st.success("Account Created! Please Login.")
                            else:
                                st.error("Signup Failed")
                                for issue in signup_val.get("issues", []):
                                    st.warning(f"Issue: {issue}")
    
    # Back button
    st.markdown("---")
    if st.button("← Back to Home"):
        st.session_state.page = "landing"
        st.rerun()

def dashboard_page():
    # Stop execution if not logged in
    if not st.session_state.user_session:
        st.session_state.page = "auth"
        st.rerun()
        
    current_user = st.session_state.user_session
    user_role = current_user['role']

    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2620/2620541.png", width=50) 
        st.title("Contract AI")
        st.info(f"User: {current_user['name']} ({user_role})")
        
        st.divider()
        st.markdown("### 🔔 System Alerts")
        if st.button("Scan for Expiries"):
            with st.status("Scanning database..."):
                alerts = api_client.check_alerts(trigger_email=False)
                if "error" in alerts:
                    st.error(alerts['error'])
                else:
                    count = len(alerts.get('alerts_generated', []))
                    if count > 0:
                        st.warning(f"Found {count} alerts!")
                    else:
                        st.success("No active alerts.")
        
        st.divider()
        st.write("**Recent History**")
        history_list = api_client.get_contracts()
        if history_list:
            for item in history_list[:5]: # Show last 5
                 if st.button(f"📄 {item[1][:15]}...", key=f"hist_{item[0]}"):
                      st.session_state['loaded_analysis'] = item
        
        st.divider()
        if st.button("Logout", type="primary"):
            logout()


    # --- MAIN CONTENT ---
    st.markdown('<div class="main-header">Contract Dashboard</div>', unsafe_allow_html=True)

    # Tabs (RBAC Filtered)
    visible_tabs = ["Analyze Contract", "Contract Dashboard", "Ask AI", "Compare Contracts", "Compliance Audit", "Search Contracts", "Translation"]
    tab_icons = ["🔍", "📊", "💬", "⚔️", "📋", "🔎", "🌍"]
    tabs = st.tabs([f"{icon} {name}" for icon, name in zip(tab_icons, visible_tabs)])

    # --- TAB 1: ANALYZE ---
    with tabs[0]:
        st.markdown('<div class="sub-header">Upload & Analyze</div>', unsafe_allow_html=True)
        
        input_method = st.radio("Choose Input", ["Upload PDF", "Paste Text"], horizontal=True)
        
        contract_text = ""
        filename = "Manual Entry"
        
        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader("Upload Contract PDF/DOCX", type=["pdf", "docx"])
            if uploaded_file:
                if uploaded_file.name.endswith(".docx"):
                    import analysis
                    contract_text = analysis.extract_text_from_docx(uploaded_file)
                else:
                    import analysis
                    contract_text = analysis.extract_text_from_pdf(uploaded_file)
                st.session_state['current_contract_text'] = contract_text 
                filename = uploaded_file.name
                st.success("PDF Loaded Successfully")
        else:
            contract_text = st.text_area("Paste Contract Text Here", height=300)
            if contract_text:
                 st.session_state['current_contract_text'] = contract_text
        
        if st.button("Analyze Contract", type="primary"):
            if not contract_text:
                st.warning("Please upload a PDF or paste text first.")
            else:
                with st.spinner("AI is analyzing the contract... roughly 10-20 seconds"):
                    result = api_client.analyze_contract(contract_text, filename)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.session_state['current_result'] = result
                        st.success("Analysis Complete & Saved!")
                        st.rerun()
    
        # Display Results
        display_data = None
        if 'current_result' in st.session_state:
            display_data = st.session_state['current_result']
        elif 'loaded_analysis' in st.session_state:
            db_item = st.session_state['loaded_analysis']
            try:
                display_data = json.loads(db_item[6])
            except:
                st.error("Error loading saved analysis.")
    
        if display_data:
            st.divider()
            status = display_data.get("lifecycle_status", "Draft")
            score = display_data.get("compliance_score", 50)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Status", status)
            c2.metric("Score", f"{score}/100")
            c3.metric("Risks", display_data.get("highlight_summary", {}).get("high_risk_count", 0))
            
            st.info(f"**Summary:** {display_data.get('contract_summary', 'No summary')}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Key Clauses")
                for k in display_data.get("key_clauses_summary", []):
                    st.write(f"• {k}")
            with col2:
                st.subheader("Risks")
                clauses = display_data.get("clauses", [])
                risk_clauses = [c for c in clauses if isinstance(c, dict) and c.get("risk_level") in ["High", "Medium"]]
                for c in risk_clauses:
                    emoji = "🔴" if c.get("risk_level") == "High" else "🟠"
                    st.write(f"{emoji} **{c.get('clause_name')}**: {c.get('risk_reason')}")

    # --- TAB 2: DASHBOARD (ANALYTICS) ---
    with tabs[1]:
        st.markdown("### 📊 Contract Ecosystem Analytics")
        history = api_client.get_contracts()
        
        if history:
            analytics_payload = []
            for item in history:
                contract_data = {}
                try:
                    full_analysis = json.loads(item[6])
                except:
                    full_analysis = {}
                
                contract_data['id'] = item[0]
                contract_data['filename'] = item[1]
                contract_data['upload_date'] = item[3]
                try:
                    contract_data['compliance_score'] = float(item[5]) if item[5] else 0
                except:
                    contract_data['compliance_score'] = 0

                contract_data['contract_type'] = full_analysis.get('contract_type', 'Unknown')
                contract_data['contract_text'] = item[7] if len(item) > 7 else item[2] 
                contract_data['highlight_summary'] = full_analysis.get('highlight_summary', {})
                contract_data['clauses'] = full_analysis.get('clauses', [])
                
                analytics_payload.append(contract_data)
            
            with st.spinner("Generating Analytics Report..."):
                import analytics
                report = analytics.generate_analytics_report(analytics_payload)
            
            k1, k2, k3, k4 = st.columns(4)
            try:
                trend_data = report['trend_analysis']['average_compliance_over_time']
                current_avg = trend_data[-1]['average_score'] if trend_data else 0
                expiries_count = len(report['expiry_analysis']['expiring_within_30_days']) + len(report['expiry_analysis']['expired_contracts'])
                high_risks = sum([x['high_risk_count'] for x in report['trend_analysis']['risk_trends']])
                
                k1.metric("Total Contracts", len(history))
                k2.metric("Avg Compliance", f"{current_avg:.1f}")
                k3.metric("Critical Expiries", expiries_count, delta_color="inverse")
                k4.metric("Total High Risks", high_risks, delta_color="inverse")
            except Exception as e:
                st.error(f"Error displaying metrics: {e}")

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📈 Compliance Trend")
                trend_list = report['trend_analysis']['average_compliance_over_time']
                if trend_list:
                    df_trend = pd.DataFrame(trend_list)
                    df_trend.set_index('period', inplace=True)
                    st.line_chart(df_trend)
            with c2:
                st.subheader("⚠️ Risk Analysis")
                risk_list = report['trend_analysis']['risk_trends']
                if risk_list:
                    df_risk = pd.DataFrame(risk_list)
                    df_risk.set_index('period', inplace=True)
                    st.bar_chart(df_risk[['high_risk_count', 'medium_risk_count']])
            
            st.divider()
            col_alerts, col_table = st.columns([1, 2])
            with col_alerts:
                st.caption("Active Alerts")
                if report['alerts']:
                    for alert in report['alerts']:
                        if "EXPIRED" in alert: st.error(f"🚨 {alert}")
                        else: st.warning(f"⚠️ {alert}")
                else:
                    st.success("No immediate expiry alerts.")
            with col_table:
                st.caption("Detailed Expiry Forecast")
                all_expiries = (
                    report['expiry_analysis']['expired_contracts'] + 
                    report['expiry_analysis']['expiring_within_30_days'] +
                    report['expiry_analysis']['predicted_upcoming_expiries']
                )
                if all_expiries:
                    st.dataframe(pd.DataFrame(all_expiries)[['contract_type', 'expiry_date', 'is_predicted']], use_container_width=True)
        else:
            st.info("No contracts to analyze yet.")

    # --- TAB 3: ASK AI ---
    with tabs[2]:
        st.markdown("### 💬 Ask AI")
        
        loaded_text = ""
        if 'current_contract_text' in st.session_state:
            loaded_text = st.session_state['current_contract_text']
            
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
        if prompt := st.chat_input("Ask about your contract..."):
             if not loaded_text:
                 st.error("Please analyze a contract first (Tab 1).")
             else:
                 st.session_state.chat_history.append({"role": "user", "content": prompt})
                 with st.chat_message("user"): st.write(prompt)
                 
                 with st.spinner("AI Thinking..."):
                     response = api_client.chat_with_contract(loaded_text, prompt)
                     st.session_state.chat_history.append({"role": "assistant", "content": response})
                     with st.chat_message("assistant"): st.write(response)

    # --- TAB 4: COMPARE CONTRACTS ---
    with tabs[3]:
        st.markdown("### ⚔️ Compare Contracts")
        st.write("Upload two contracts to identify differences.")
        
        c1, c2 = st.columns(2)
        text_a = ""
        text_b = ""
        
        with c1:
            file_a = st.file_uploader("Contract A", type=["pdf", "docx"], key="compare_a")
            if file_a:
                if file_a.name.endswith(".docx"):
                    import analysis
                    text_a = analysis.extract_text_from_docx(file_a)
                else:
                    import analysis
                    text_a = analysis.extract_text_from_pdf(file_a)
                st.success("Loaded A")
        with c2:
            file_b = st.file_uploader("Contract B", type=["pdf", "docx"], key="compare_b")
            if file_b:
                if file_b.name.endswith(".docx"):
                    import analysis
                    text_b = analysis.extract_text_from_docx(file_b)
                else:
                    import analysis
                    text_b = analysis.extract_text_from_pdf(file_b)
                st.success("Loaded B")
                
        if st.button("Compare Contracts", type="primary"):
            if text_a and text_b:
                with st.spinner("Comparing..."):
                    comparison_result = api_client.compare_contracts(text_a, text_b)
                    st.markdown(comparison_result)
            else:
                st.warning("Please upload both contracts.")

    # --- TAB 5: COMPLIANCE AUDIT ---
    with tabs[4]:
        st.markdown("### 📋 Quick Compliance Audit")
        
        audit_text = ""
        au_input = st.radio("Source", ["Upload PDF", "Paste Text"], horizontal=True, key="audit_input")
        
        if au_input == "Upload PDF":
            au_file = st.file_uploader("Audit Contract", type=["pdf", "docx"], key="audit_upload")
            if au_file:
                if au_file.name.endswith(".docx"):
                    import analysis
                    audit_text = analysis.extract_text_from_docx(au_file)
                else:
                    import analysis
                    audit_text = analysis.extract_text_from_pdf(au_file)
        else:
            audit_text = st.text_area("Paste Text", height=200, key="audit_paste")
            
        if st.button("Run Audit", type="primary"):
            if audit_text:
                with st.spinner("Auditing..."):
                    audit_result = api_client.audit_contract(audit_text)
                    if "error" in audit_result:
                        st.error(audit_result["error"])
                    else:
                        st.subheader(f"Type: {audit_result.get('contract_type')}")
                        st.metric("Score", f"{audit_result.get('template_compliance_score')}/100")
                        
                        st.write("**Critical Gaps**")
                        for gap in audit_result.get('critical_gaps', []):
                            st.error(f"- {gap}")
                        
                        st.write("**Assessment**")
                        st.write(audit_result.get('overall_assessment'))
            else:
                 st.warning("Provide text.")

    # --- TAB 6: SEARCH ---
    with tabs[5]:
        st.markdown("### Search Contract History")
        search_query = st.text_input("Enter filename or keyword")
        if st.button("Search"):
            results = []
            all_contracts = api_client.get_contracts()
            if all_contracts:
                for c in all_contracts:
                    if search_query.lower() in c[1].lower() or search_query.lower() in c[2].lower():
                         results.append(c)
                if results:
                    st.success(f"Found {len(results)} contracts.")
                    for item in results:
                        with st.container():
                            st.write(f"**{item[1]}** - {item[4]}")
                            if st.button("Load", key=f"search_view_{item[0]}"):
                                st.session_state['loaded_analysis'] = item
                                st.rerun()
                else:
                    st.warning("No matches.")
            else:
                st.warning("Database empty.")

    # --- TAB 7: TRANSLATION ---
    with tabs[6]:
        st.markdown("## 🌍 Legal Translation")
        
        trans_text = st.text_area("Text to translate", height=300)
        if 'loaded_analysis' in st.session_state and st.button("Load from Viewed Contract"):
             item = st.session_state['loaded_analysis']
             if len(item) > 7: trans_text = item[7]
             elif len(item) > 2: trans_text = item[2] 
             st.rerun() 
        
        target_lang = st.selectbox("Target Language", ["Spanish", "French", "German", "Chinese", "Hindi", "Arabic", "Portuguese", "Japanese"])
        
        if st.button("Translate", type="primary"):
            if trans_text:
                with st.spinner("Translating..."):
                    trans_result = api_client.translate_contract(trans_text, target_lang)
                    if "translated_text" in trans_result:
                        c1, c2 = st.columns(2)
                        with c1: st.text_area("Original", trans_text, height=400)
                        with c2: st.text_area(f"Translated ({target_lang})", trans_result['translated_text'], height=400)
                    else:
                        st.error("Failed.")
            else:
                st.warning("Enter text.")
    
    # Optional Smart CTA at end
    st.divider()
    c_start, c_end = st.columns([4, 1])
    with c_end:
        if st.button("Start New Analysis"):
            st.session_state['current_result'] = None
            st.session_state['current_contract_text'] = None
            st.rerun()

# --- MAIN ROUTER ---

if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "auth":
    auth_page()
elif st.session_state.page == "dashboard":
    dashboard_page()

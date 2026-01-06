import streamlit as st
import auth
import logic
import re
from music_recommender import MusicRecommender
from datetime import datetime
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mental Health AI", page_icon="🌿", layout="wide")

# --- CALMING CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    :root {
        --bg-cream: #FDFBF7;
        --sage-primary: #8AA6A3;
        --soft-sand: #EAD7BB;
        --text-deep: #2D3E40;
        --card-white: #FFFFFF;
        --border-soft: rgba(138, 166, 163, 0.15);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-cream);
        color: var(--text-deep);
        font-family: 'Outfit', sans-serif;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #F4F7F6;
        border-right: 1px solid var(--border-soft);
    }

    /* Button Styling */
    .stButton>button {
        background-color: var(--sage-primary);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #6D8A87;
        box-shadow: 0 4px 12px rgba(138, 166, 163, 0.3);
        transform: translateY(-1px);
    }

    /* Card Styling */
    .main-card {
        background: var(--card-white);
        padding: 2.5rem;
        border-radius: 28px;
        box-shadow: 0 12px 40px rgba(138, 166, 163, 0.06);
        border: 1px solid var(--border-soft);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }

    .main-card:hover {
        transform: translateY(-2px);
    }

    h1, h2, h3 {
        color: var(--text-deep);
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .emergency-banner {
        background-color: #FFF2F2;
        border-left: 6px solid #FF8E8E;
        padding: 1.8rem;
        border-radius: 16px;
        color: #9B2C2C;
        margin-top: 2rem;
    }

    .stat-box {
        text-align: center;
        padding: 1.8rem;
        background: #F9FAFB;
        border-radius: 20px;
        border: 1px solid var(--border-soft);
        height: 100%;
    }

    .stat-value {
        font-size: 2.8rem;
        font-weight: 600;
        color: var(--sage-primary);
        line-height: 1;
        margin: 0.5rem 0;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        background-color: transparent;
        border-radius: 0px;
        color: var(--text-deep);
        font-weight: 400;
    }

    .stTabs [aria-selected="true"] {
        font-weight: 600;
        color: var(--sage-primary);
        border-bottom-color: var(--sage-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTH INITIALIZATION ---
auth.init_db()

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    
    if not st.session_state.authenticated:
        render_auth()
    else:
        if st.session_state.page == "emergency":
            render_emergency()
        else:
            render_dashboard()

def render_auth():
    st.markdown("<div style='text-align: center; margin-top: 5vh;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3rem;'>Mental Health AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #667A78;'>Your companion for mental peace and clarity.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("Enter AI Hub", use_container_width=True):
                if auth.login_user(u, p):
                    st.session_state.authenticated = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Gently double-check your credentials.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            nu = st.text_input("Choose Username", key="reg_u")
            np = st.text_input("Password", type="password", key="reg_p")
            em = st.text_input("Email", key="reg_e")
            if st.button("Begin Your Journey", use_container_width=True):
                if auth.register_user(nu, np, em):
                    st.success("Your space is ready. Please sign in.")
                else:
                    st.error("That name is already being used.")
            st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    # Modular Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.user} 🌿")
        
        # Mapping from image
        menu_options = {
            "🏠 Dashboard Overview": "overview",
            "🏆 Wellness Analysis": "wellness",
            "🎯 Suicide Risk (ML)": "suicide",
            "🔮 Condition Prediction": "condition",
            "📋 DSM-5 Diagnostics": "dsm5",
            "🌱 Situational Analyzer": "situational",
            "📊 Dataset Explorer": "explorer"
        }
        
        selection = st.radio("Navigation", list(menu_options.keys()), label_visibility="collapsed")
        page = menu_options[selection]
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🆘 Emergency Support", use_container_width=True, type="secondary"):
            st.session_state.page = "emergency"
            st.rerun()
            
        if st.button("🚪 Sign Out", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.rerun()

    # Route to views
    if page == "overview":
        show_overview()
    elif page == "wellness":
        show_wellness()
    elif page == "suicide":
        show_suicide()
    elif page == "condition":
        show_condition()
    elif page == "dsm5":
        show_dsm5()
    elif page == "situational":
        show_situational()
    elif page == "explorer":
        show_explorer()

def show_overview():
    st.title("Daily Check-in 🏠")
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    journal = st.text_area("How are you feeling in this moment?", height=150, 
                          placeholder="Share your thoughts...")
    
    if st.button("Run Clinical Analysis"):
        if journal.strip():
            with st.spinner("Analyzing signals..."):
                diag = logic.DiagnosticAssistant()
                situ = logic.SituationalAnalyzer()
                st.session_state.last_results = diag.analyze(journal)
                st.session_state.last_situ = situ.analyze(journal)
                st.session_state.last_journal = journal
                st.success("New analysis synchronized. Explore the tabs for details.")
    st.markdown('</div>', unsafe_allow_html=True)

    if 'last_results' in st.session_state:
        results = st.session_state.last_results
        situ_res = st.session_state.last_situ
        
        # Summary Tiles
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-box"><h4>Wellness Score</h4><div class="stat-value">{situ_res["pom_score"]}%</div></div>', unsafe_allow_html=True)
        with c2:
            top_pred = results['ml_insights'][0][0] if results.get('ml_insights') else "Stability"
            st.markdown(f'<div class="stat-box"><h4>Primary Indicator</h4><div style="font-size: 1.4rem; font-weight: 600;">{top_pred}</div></div>', unsafe_allow_html=True)
        with c3:
            status = "Immediate Support" if situ_res['is_emergency'] else "Stable"
            st.markdown(f'<div class="stat-box"><h4>System Status</h4><div style="font-size: 1.4rem; font-weight: 600; color: {"#FF6B6B" if situ_res["is_emergency"] else "#8AA6A3"}">{status}</div></div>', unsafe_allow_html=True)

def show_wellness():
    st.title("Wellness Analysis 🏆")
    if 'last_situ' not in st.session_state:
        st.warning("Please perform a check-in on the Dashboard Overview first.")
        return
        
    situ = st.session_state.last_situ
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Peace of Mind (PoM) Metric")
    st.progress(situ['pom_score'] / 100)
    st.write(f"Your current stability index is **{situ['pom_score']}%**. This is calculated based on emotional density and linguistic markers.")
    
    # Music Therapy Integration
    top_state = "Stable"
    if situ['is_emergency']: top_state = "Panic Attack"
    elif situ['pom_score'] < 40: top_state = "High Stress"
    
    rec = MusicRecommender.get_recommendation(top_state)
    st.markdown("---")
    st.subheader("Therapeutic Soundscapes")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Recommended Genre:** {rec['Recommended_Genre']}")
        st.write(f"**Target Tempo:** {rec['Tempo']}")
    with col2:
        st.info(rec['Clinical_Logic'])
    st.markdown('</div>', unsafe_allow_html=True)

def show_suicide():
    st.title("Suicide Risk (ML) 🎯")
    if 'last_situ' not in st.session_state:
        st.warning("Please perform a check-in on the Dashboard Overview first.")
        return
        
    situ = st.session_state.last_situ
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    risk_color = "#FF6B6B" if situ['is_emergency'] else "#8AA6A3"
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; border-radius: 20px; background: {risk_color}11; border: 2px solid {risk_color}">
        <h2 style="color: {risk_color}; margin: 0;">{"CRITICAL RISK DETECTED" if situ['is_emergency'] else "LOW RISK DETECTED"}</h2>
        <p style="font-size: 1.2rem; margin-top: 1rem;">ML Confidence Score: <b>{situ.get('ml_confidence', 0)*100:.1f}%</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if situ['is_emergency']:
        st.error("Protocol: Our AI has detected high-risk language patterns. Please refer to Emergency Support immediately.")
    else:
        st.success("Our AI suggests your current patterns do not indicate acute crisis markers.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_condition():
    st.title("Condition Prediction 🔮")
    if 'last_results' not in st.session_state:
        st.warning("Please perform a check-in on the Dashboard Overview first.")
        return
        
    results = st.session_state.last_results
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("SVM Probability Distribution")
    
    if results.get('ml_insights'):
        df = pd.DataFrame(results['ml_insights'], columns=['Condition', 'Certainty'])
        fig = px.bar(df, x='Certainty', y='Condition', orientation='h', 
                     color='Certainty', color_continuous_scale='Teal', template='plotly_white')
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for ML probability mapping.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_dsm5():
    st.title("DSM-5 Diagnostics 📋")
    if 'last_results' not in st.session_state:
        st.warning("Please perform a check-in on the Dashboard Overview first.")
        return
        
    results = st.session_state.last_results['rule_based']
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Category Match Intensity")
    
    for cat, score in results.items():
        st.write(f"**{cat}**")
        st.progress(score / 100)
        st.caption(f"Pattern correlation strength: {score}%")
    st.markdown('</div>', unsafe_allow_html=True)

def show_situational():
    st.title("Situational Analyzer 🌱")
    if 'last_journal' not in st.session_state:
        st.warning("Please perform a check-in on the Dashboard Overview first.")
        return
        
    journal = st.session_state.last_journal
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Stressor Pattern Detection")
    
    stressors = {
        "Academic": [r"work", r"study", r"grade", r"exam", r"assignment"],
        "Social": [r"friend", r"lonely", r"argument", r"relationship", r"people"],
        "Financial": [r"money", r"debt", r"broke", r"pay", r"bills"]
    }
    
    found = False
    for cat, patterns in stressors.items():
        if any(re.search(p, journal, re.IGNORECASE) for p in patterns):
            st.info(f"📍 Potential **{cat}** stressor detected in your narrative.")
            found = True
            
    if not found:
        st.write("No distinct situational stressors isolated in current input.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_explorer():
    st.title("Dataset Explorer 📊")
    
    datasets = {
        "Student Mental health.csv": "General student demographics and mental health indicators.",
        "Suicide_Detection.csv": "Raw text logs for training suicide risk detection models."
    }
    
    target_file = st.selectbox("Select Training Dataset", list(datasets.keys()))
    st.caption(datasets[target_file])
    
    try:
        if target_file == "Suicide_Detection.csv":
            # Load a sample for performance
            df = pd.read_csv(target_file).head(500)
            st.warning("Displaying a sample of 500 records from the Suicide Detection dataset for performance.")
        else:
            df = pd.read_csv(target_file)

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader(f"Source Data: {target_file}")
        st.dataframe(df, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Total Records (Current View):**", len(df))
        with c2:
            st.write("**Columns:**", len(df.columns))
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")

def render_emergency():
    st.title("Support is Here 🆘")
    st.markdown("""
    <div class="emergency-banner">
        <h3>You are not alone. Help is available 24/7.</h3>
        <p>If you or someone you know is in immediate danger, please reach out to professional services.</p>
        <hr>
        <ul>
            <li><b>National Lifeline:</b> 988 (Call or Text)</li>
            <li><b>Crisis Text Line:</b> Text HOME to 741741</li>
            <li><b>International Support:</b> findahelpline.com</li>
        </ul>
        <br>
        <button onclick="window.location.reload();" style="background:#B22222; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer;">Return to Hub</button>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

if __name__ == "__main__":
    main()

import streamlit as st
import time

# -----------------------------------------------------------------------------
# 1. Page Config & Modern UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Shadow Operator OS", page_icon="🕵️‍♂️", layout="wide")

st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        color: #00FF94 !important; /* Cyber Green */
        font-size: 2.5rem !important;
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #161B22;
        color: white;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #238636, #2EA043);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(46, 160, 67, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Authentication Logic (SaaS Gate)
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_login():
    # HARDCODED KEY FOR MVP (You can change this)
    VALID_KEY = "SHADOW-ACCESS" 
    
    key = st.session_state.license_input
    if key == VALID_KEY:
        st.session_state.authenticated = True
    else:
        st.session_state.login_error = "❌ Invalid License Key"

if not st.session_state.authenticated:
    # --- LOGIN SCREEN ---
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.title("🔐 Shadow Operator OS")
        st.markdown("### Members Only Access")
        
        st.text_input("Enter License Key", key="license_input", type="password")
        st.button("Unlock Access", on_click=check_login)
        
        if "login_error" in st.session_state:
            st.error(st.session_state.login_error)
            
    st.stop() # STOP HERE if not logged in

# -----------------------------------------------------------------------------
# 3. Main App (Protected Content)
# -----------------------------------------------------------------------------

# --- Session Init ---
if "audit_followers" not in st.session_state: st.session_state.audit_followers = 50000
if "audit_likes" not in st.session_state: st.session_state.audit_likes = 1500
if "audit_comments" not in st.session_state: st.session_state.audit_comments = 50
if "audit_name" not in st.session_state: st.session_state.audit_name = ""

st.title("🕵️‍♂️ Shadow Operator OS")

# --- Auto-Fetch Section ---
with st.expander("🕵️‍♂️ Auto-Fetch Data (Optional)", expanded=True):
    col_search, col_btn = st.columns([0.8, 0.2])
    with col_search:
        search_query = st.text_input("Profile URL or Username", placeholder="e.g. https://instagram.com/coachkarfei")
    with col_btn:
        st.write("") 
        st.write("")
        fetch_clicked = st.button("Fetch Stats")

    # --- ADVANCED SETTINGS (LOGIN) ---
    with st.expander("⚙️ Advanced Scraper Settings (If you get errors)"):
        st.info("💡 Pro Tip: Instagram often blocks 'anonymous' searches. If you get a 401 error, enter your Instagram credentials below to bypass the limit.")
        ig_user = st.text_input("IG Username (Optional)", value="")
        ig_pass = st.text_input("IG Password (Optional)", type="password", value="")
        st.warning("⚠️ Using your personal account can lead to temporary IG blocks. Use a 'Burner' account if possible.")

    if fetch_clicked:
        import instaloader
        L = instaloader.Instaloader(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Clean username
        username = search_query.replace("https://www.instagram.com/", "").replace("https://instagram.com/", "").replace("/", "").replace("@", "").strip()
        if "?" in username: username = username.split("?")[0]
        
        try:
            with st.spinner(f"Spying on @{username}..."):
                # Handle Login if provided
                if ig_user and ig_pass:
                    try:
                        # Attempt login with 2FA support or common CSRF bypass
                        L.login(ig_user, ig_pass)
                    except Exception as login_err:
                        if "CSRF" in str(login_err):
                            st.error("🔒 **CSRF Token Error**: Instagram is blocking this login attempt. \n\n**Fix**: Try logging in to this account on your phone/browser first, or use a different account. Instagram thinks this app is 'suspicious'.")
                        elif "checkpoint" in str(login_err):
                            st.error("🔒 **2FA / Verification Required**: Check your Instagram app for a 'That was me' notification, then try again.")
                        else:
                            st.error(f"Login failed: {str(login_err)}")
                        st.stop()
                
                profile = instaloader.Profile.from_username(L.context, username)
                
                st.session_state.audit_followers = profile.followers
                st.session_state.audit_name = profile.full_name if profile.full_name else username
                
                posts = profile.get_posts()
                likes = 0; comments = 0; count = 0
                for post in posts:
                    if count >= 3: break
                    likes += post.likes
                    comments += post.comments
                    count += 1
                
                if count > 0:
                    st.session_state.audit_likes = int(likes / count)
                    st.session_state.audit_comments = int(comments / count)
                
                st.success("✅ Target Acquired!")
                time.sleep(0.5)
                st.rerun()
                
        except Exception as e:
            if "401" in str(e):
                st.error("🔒 Instagram blocked the anonymous request. Enter your IG credentials in 'Advanced Settings' above.")
            else:
                st.error(f"Suggest manual entry. Error: {str(e)}")

# --- Manual Inputs ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 👤 Target Info")
    creator_name = st.text_input("Creator Name", value=st.session_state.audit_name, placeholder="e.g. Coach Karfei")

with col2:
    st.markdown("#### 📊 Metrics")
    followers = st.number_input("Followers", min_value=0, value=st.session_state.audit_followers, step=100)
    avg_likes = st.number_input("Avg Likes", min_value=0, value=st.session_state.audit_likes)
    avg_comments = st.number_input("Avg Comments", min_value=0, value=st.session_state.audit_comments)

with col3:
    st.markdown("#### 💰 Product Model")
    product_price = st.number_input("Target Product Price ($)", value=47)
    conversion_rate = st.slider("Est. Conversion Rate (%)", 0.5, 5.0, 1.0, 0.1)

st.markdown("---")

# --- The Math Engine ---
if followers > 0:
    total_interactions = avg_likes + avg_comments
    engagement_rate = (total_interactions / followers) * 100
    est_buyers = int(followers * (conversion_rate / 100))
    est_revenue = est_buyers * product_price
    your_cut = est_revenue * 0.40
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Engagement Rate", f"{engagement_rate:.2f}%", delta="Target > 3%" if engagement_rate > 3 else "Low Engagement")
    m2.metric("Est. Monthly Sales", f"{est_buyers} units")
    m3.metric("Total Revenue", f"${est_revenue:,.0f}", delta="Opportunity")
    m4.metric("YOUR 40% CUT", f"${your_cut:,.0f}", delta="Passive Income", delta_color="normal")
    
    st.progress(min(engagement_rate / 10, 1.0), text=f"Health Score: {min(engagement_rate*10, 100):.0f}/100")

# --- The Sniper DM ---
st.markdown("### 🎯 The Sniper DM")

col_prod, col_gap = st.columns(2)
with col_prod:
    product_idea = st.text_input("Product Idea (The Hook)", placeholder="e.g. 7-Day Mindset Protocol")
with col_gap:
    current_gap = st.text_input("Current Gap", placeholder="e.g. only sells high-ticket coaching")

if creator_name and product_idea:
    gap_text = current_gap if current_gap else "no clear 'low-ticket' product for them to buy"
    
    dm_script = f"""
Hey {creator_name.split(' ')[0]}, been digging through your content. Huge fan of the unique angle you take.

I ran some numbers on your page—you've got {followers/1000:.1f}k followers with a solid {engagement_rate:.1f}% engagement rate.

But I noticed a gap: {gap_text}. 
You are capturing the 'Whales' but letting thousands of 'Minnows' swim away because they can't afford you yet.

Conservatively, you're leaving about ${est_revenue:,.0f}/mo on the table by not having a low-ticket entry point.

I actually mocked up a **{product_idea}** for you today. It captures those smaller followers and warms them up for your main offer.

I’ve already outlined the modules. Want me to send over the PDF? No charge, just thought it was a perfect fit.
"""
    st.success("✅ DM Generated!")
    st.text_area("📋 Copy to Instagram/LinkedIn:", dm_script, height=250)
    
elif not creator_name:
    st.info("👈 Enter Creator Name/Handle above.")
else:
    st.info("👈 Enter the Product Idea to unlock the script.")

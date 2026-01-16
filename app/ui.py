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
# 2. Session State Calculation
# -----------------------------------------------------------------------------
if "audit_followers" not in st.session_state: st.session_state.audit_followers = 50000
if "audit_likes" not in st.session_state: st.session_state.audit_likes = 1500
if "audit_comments" not in st.session_state: st.session_state.audit_comments = 50
if "audit_name" not in st.session_state: st.session_state.audit_name = ""

# -----------------------------------------------------------------------------
# 3. Main Layout
# -----------------------------------------------------------------------------
st.title("🕵️‍♂️ Shadow Operator OS")

# --- Auto-Fetch Section ---
with st.expander("🕵️‍♂️ Auto-Fetch Data (Optional)", expanded=True):
    col_search, col_btn = st.columns([0.8, 0.2])
    with col_search:
        search_query = st.text_input("Profile URL or Username", placeholder="e.g. https://instagram.com/coachkarfei")
    with col_btn:
        st.write("") 
        st.write("")
        if st.button("Fetch Stats"):
            import instaloader
            L = instaloader.Instaloader()
            
            # Clean username
            username = search_query.replace("https://www.instagram.com/", "").replace("https://instagram.com/", "").replace("/", "").replace("@", "").strip()
            # Remove any trailing slash or query params
            if "?" in username: username = username.split("?")[0]
            
            try:
                with st.spinner(f"Spying on @{username}..."):
                    profile = instaloader.Profile.from_username(L.context, username)
                    
                    # Store in session state
                    st.session_state.audit_followers = profile.followers
                    st.session_state.audit_name = profile.full_name if profile.full_name else username
                    
                    # Get Engagement (Last 3 Posts)
                    posts = profile.get_posts()
                    likes = 0
                    comments = 0
                    count = 0
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
                st.error(f"Suggest manual entry. Error: {str(e)}")

# --- Manual Inputs (Synced with Session State) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 👤 Target Info")
    # key=... updates the session state automatically when user types
    creator_name = st.text_input("Creator Name", value=st.session_state.audit_name, placeholder="e.g. Coach Karfei")

with col2:
    st.markdown("#### 📊 Metrics")
    # We use separate keys for the widgets to avoid conflict, then sync if needed
    followers = st.number_input("Followers", min_value=0, value=st.session_state.audit_followers, step=100)
    avg_likes = st.number_input("Avg Likes", min_value=0, value=st.session_state.audit_likes)
    avg_comments = st.number_input("Avg Comments", min_value=0, value=st.session_state.audit_comments)

with col3:
    st.markdown("#### 💰 Product Model")
    product_price = st.number_input("Target Product Price ($)", value=47)
    conversion_rate = st.slider("Est. Conversion Rate (%)", 0.5, 5.0, 1.0, 0.1)

st.markdown("---")

# -----------------------------------------------------------------------------
# 4. The Math Engine
# -----------------------------------------------------------------------------
if followers > 0:
    # 1. Engagement Rate
    total_interactions = avg_likes + avg_comments
    engagement_rate = (total_interactions / followers) * 100
    
    # 2. Revenue Projection
    # Formula: Followers * ConversionRate * Price
    est_buyers = int(followers * (conversion_rate / 100))
    est_revenue = est_buyers * product_price
    
    # 3. Your Cut (40%)
    your_cut = est_revenue * 0.40
    
    # Display Metrics
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric(
        "Engagement Rate", 
        f"{engagement_rate:.2f}%", 
        delta="Target > 3%" if engagement_rate > 3 else "Low Engagement"
    )
    
    m2.metric(
        "Est. Monthly Sales", 
        f"{est_buyers} units"
    )
    
    m3.metric(
        "Total Revenue", 
        f"${est_revenue:,.0f}",
        delta="Opportunity"
    )
    
    m4.metric(
        "YOUR 40% CUT", 
        f"${your_cut:,.0f}",
        delta="Passive Income",
        delta_color="normal"
    )
    
    st.progress(min(engagement_rate / 10, 1.0), text=f"Health Score: {min(engagement_rate*10, 100):.0f}/100")

# -----------------------------------------------------------------------------
# 5. The Sniper DM Generator
# -----------------------------------------------------------------------------
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

import streamlit as st
import random
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Live Green",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for warm, welcoming design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 50%, #fef3c7 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(16, 185, 129, 0.4);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #10b981;
        margin-bottom: 1rem;
    }
    .welcome-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #059669;
    }
    .logout-btn {
        background: #ef4444 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'contributions' not in st.session_state:
    st.session_state.contributions = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'


# Mock Data Generator
def generate_mock_data():
    """Generate realistic environmental mock data for Bengaluru"""
    base_temp = 27 + random.uniform(-2, 4)
    base_humidity = 62 + random.uniform(-5, 10)
    base_pollution = 48 + random.uniform(-10, 20)
    base_uv = 6 + random.uniform(-1, 2)
    base_wind = 8 + random.uniform(-2, 4)

    weathers = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Clear']

    pollution_index = round(base_pollution)
    if pollution_index < 40:
        smog_level = 'Good'
    elif pollution_index < 60:
        smog_level = 'Moderate'
    else:
        smog_level = 'Unhealthy'

    return {
        'location': 'Bengaluru, India',
        'weather': random.choice(weathers),
        'temperature': round(base_temp, 1),
        'humidity': round(base_humidity),
        'pollutionIndex': pollution_index,
        'smogLevel': smog_level,
        'uvIndex': round(base_uv, 1),
        'windSpeed': round(base_wind, 1)
    }


# Recommendation Engine
def get_recommendations(data):
    """Generate personalized environmental recommendations"""
    recommendations = []

    if data['pollutionIndex'] < 40:
        recommendations.append("🚴 Air quality is great! Perfect day for outdoor activities.")
    elif data['pollutionIndex'] < 60:
        recommendations.append("🚶 Air quality is moderate; walking is a great choice today.")
    else:
        recommendations.append("🏠 Pollution index is elevated; consider indoor activities.")

    if data['uvIndex'] > 7:
        recommendations.append("🧢 UV index is high — take a shaded route and wear sunscreen.")
    elif data['uvIndex'] > 5:
        recommendations.append("😎 Moderate UV levels — sunglasses recommended.")

    if data['temperature'] > 30:
        recommendations.append("💧 Stay hydrated! It's warm outside.")
    elif data['temperature'] < 20:
        recommendations.append("🧥 A bit cool today — layer up!")

    return recommendations


# Generate Weekly EcoScore Data
def generate_weekly_data():
    """Generate mock weekly environmental scores"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return [
        {
            'day': day,
            'score': random.randint(60, 90),
            'pollution': random.randint(30, 70)
        }
        for day in days
    ]


# Authentication Functions
def mock_login(name, email):
    """Mock login function (Demo Mode)"""
    st.session_state.user = {
        'name': name,
        'email': email,
        'picture': f'https://ui-avatars.com/api/?name={name.replace(" ", "+")}&background=10b981&color=fff'
    }
    st.session_state.page = 'dashboard'


def logout():
    """Logout function"""
    st.session_state.user = None
    st.session_state.page = 'home'


# Home Page
def home_page():
    """Landing page with welcome message"""
    st.markdown("""
    <div class="welcome-header">
        <h1 style="font-size: 4rem; color: #065f46; margin-bottom: 1rem;">🌿 Live Green</h1>
        <p style="font-size: 1.5rem; color: #059669;">
            Your personal environmental companion for mindful living in harmony with nature
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ☁️ Real-time Insights")
        st.write("Monitor environmental conditions in your area")

    with col2:
        st.markdown("### ❤️ Smart Recommendations")
        st.write("Personalized eco-friendly tips for daily living")

    with col3:
        st.markdown("### 📈 Track Progress")
        st.write("See your environmental impact over time")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.user:
            if st.button("🌿 Go to Dashboard", key="goto_dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            if st.button("🌿 Sign In to Start", key="goto_login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()


# Login Page
def login_page():
    """Login/Authentication page"""
    st.markdown("""
    <div class="welcome-header">
        <h1 style="font-size: 3rem; color: #065f46;">🌿 Welcome to Live Green</h1>
        <p style="font-size: 1.2rem; color: #059669;">
            Sign in to start your environmental journey
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🔐 Authentication")

        # Demo Login
        st.markdown("#### Continue as Demo User")

        with st.form("demo_login"):
            name = st.text_input("Name", value="Demo User", placeholder="Enter your name")
            email = st.text_input("Email", value="demo@livegreen.com", placeholder="Enter your email")

            submitted = st.form_submit_button("Continue as Demo User", use_container_width=True)

            if submitted:
                if name and email:
                    mock_login(name, email)
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

        st.markdown("---")

        # Google OAuth Info (Not implemented in demo)
        with st.expander("ℹ️ Google Sign-In (Production Setup)"):
            st.info("""
            **To enable Google Sign-In in production:**

            1. Set up Google Cloud Console project
            2. Enable Google Sign-In API
            3. Get OAuth 2.0 Client ID
            4. Use `streamlit-google-auth` library
            5. Configure credentials

            For now, use the Demo User option above!
            """)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = 'home'
            st.rerun()


# Dashboard Page
def dashboard_page():
    """Main dashboard with environmental data"""
    env_data = generate_mock_data()
    recommendations = get_recommendations(env_data)

    # Header
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <p style="color: #059669; font-size: 1.1rem;">Welcome back, {st.session_state.user['name']}! 👋</p>
        <h1 style="color: #065f46; font-size: 2.5rem;">📍 {env_data['location']}</h1>
        <h2 style="color: #059669;">Environmental Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

    # Environmental Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("☁️ Weather", env_data['weather'])
        st.metric("🌡️ Temperature", f"{env_data['temperature']}°C")

    with col2:
        st.metric("💧 Humidity", f"{env_data['humidity']}%")
        st.metric("💨 Wind Speed", f"{env_data['windSpeed']} km/h")

    with col3:
        pollution_color = "🟢" if env_data['pollutionIndex'] < 40 else "🟡" if env_data['pollutionIndex'] < 60 else "🔴"
        st.metric(f"{pollution_color} Pollution Index", env_data['pollutionIndex'])
        st.metric("☀️ UV Index", env_data['uvIndex'])

    # Recommendations
    st.markdown("---")
    st.markdown("### 🌿 Today's Recommendations")

    for rec in recommendations:
        st.markdown(f"""
        <div class="recommendation-card">
            <p style="margin: 0; color: #065f46; font-size: 1.05rem;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)


# Contribution Page
def contribution_page():
    """User contribution form"""
    st.markdown("""
    <div class="welcome-header">
        <h1 style="font-size: 2.5rem; color: #065f46;">❤️ Share Your Observations</h1>
        <p style="font-size: 1.2rem; color: #059669;">
            Help us build a better environmental picture together 🌍
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("contribution_form"):
            st.markdown("#### 🏭 Pollution Level")
            pollution = st.radio("", ["Low", "Medium", "High"], horizontal=True, label_visibility="collapsed")

            st.markdown("#### 🌡️ Temperature Perception")
            temperature = st.radio("", ["Cool", "Warm", "Hot"], horizontal=True, label_visibility="collapsed",
                                   key="temp")

            st.markdown("#### 👁️ Visibility")
            visibility = st.radio("", ["Clear", "Hazy", "Smoggy"], horizontal=True, label_visibility="collapsed",
                                  key="vis")

            submitted = st.form_submit_button("Submit Contribution 🌱", use_container_width=True)

            if submitted:
                contribution = {
                    'pollution': pollution,
                    'temperature': temperature,
                    'visibility': visibility,
                    'timestamp': datetime.now().isoformat(),
                    'user': st.session_state.user['email']
                }
                st.session_state.contributions.append(contribution)
                st.success("✅ Thank you for your contribution! 🌱")

    # Show recent contributions
    if st.session_state.contributions:
        st.markdown("---")
        st.markdown(f"### Your Contributions ({len(st.session_state.contributions)})")

        for contrib in reversed(st.session_state.contributions[-3:]):
            st.markdown(f"""
            <div style="background: #d1fae5; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                <p style="margin: 0; color: #065f46;">
                    {contrib['pollution']} pollution • {contrib['temperature']} • {contrib['visibility']} visibility
                </p>
            </div>
            """, unsafe_allow_html=True)


# EcoScore Page
def ecoscore_page():
    """EcoScore tracking and visualization"""
    weekly_data = generate_weekly_data()
    avg_score = sum(d['score'] for d in weekly_data) / len(weekly_data)

    st.markdown("""
    <div class="welcome-header">
        <h1 style="font-size: 2.5rem; color: #065f46;">📈 Your EcoScore</h1>
        <p style="font-size: 1.2rem; color: #059669;">
            Tracking your environmental awareness journey
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Weekly Average
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 2rem; border-radius: 1rem; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">Weekly Average</p>
            <p style="font-size: 4rem; font-weight: bold; margin: 0;">{round(avg_score)}</p>
            <p style="font-size: 1rem; opacity: 0.9;">You're helping the planet! 🌍</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Weekly Trends Chart
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=[d['day'] for d in weekly_data],
            y=[d['score'] for d in weekly_data],
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=10, color='#10b981'),
            name='EcoScore'
        ))
        fig_line.update_layout(
            title="Weekly Trends",
            xaxis_title="Day",
            yaxis_title="Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#065f46'),
            height=300
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # Pollution Bar Chart
    st.markdown("### Pollution Levels This Week")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=[d['day'] for d in weekly_data],
        y=[d['pollution'] for d in weekly_data],
        marker=dict(color='#10b981', cornerradius=10),
        name='Pollution'
    ))
    fig_bar.update_layout(
        xaxis_title="Day",
        yaxis_title="Pollution Level",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#065f46'),
        height=300
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 1.5rem; border-radius: 1rem; text-align: center;">
            <p style="font-size: 3rem; margin: 0;">📅</p>
            <p style="font-size: 2rem; font-weight: bold; color: #065f46; margin: 0.5rem 0;">7</p>
            <p style="color: #059669; margin: 0;">Days Active</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 1.5rem; border-radius: 1rem; text-align: center;">
            <p style="font-size: 3rem; margin: 0;">✍️</p>
            <p style="font-size: 2rem; font-weight: bold; color: #065f46; margin: 0.5rem 0;">{len(st.session_state.contributions)}</p>
            <p style="color: #059669; margin: 0;">Contributions</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        impact_score = round(avg_score * 1.2)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 1.5rem; border-radius: 1rem; text-align: center;">
            <p style="font-size: 3rem; margin: 0;">⭐</p>
            <p style="font-size: 2rem; font-weight: bold; color: #065f46; margin: 0.5rem 0;">+{impact_score}</p>
            <p style="color: #059669; margin: 0;">Impact Score</p>
        </div>
        """, unsafe_allow_html=True)


# Main App Logic
def main():
    """Main application logic with routing"""

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🌿 Live Green")

        if st.session_state.user:
            # User Profile
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #d1fae5; border-radius: 0.75rem; margin-bottom: 1rem;">
                <img src="{st.session_state.user['picture']}" 
                     style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #10b981; margin-bottom: 0.5rem;">
                <p style="margin: 0; font-weight: bold; color: #065f46;">{st.session_state.user['name']}</p>
                <p style="margin: 0; font-size: 0.9rem; color: #059669;">{st.session_state.user['email']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Navigation
            st.markdown("### Navigation")
            if st.button("🏠 Home", key="nav_home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()

            if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()

            if st.button("✍️ Contribute", key="nav_contribute", use_container_width=True):
                st.session_state.page = 'contribute'
                st.rerun()

            if st.button("📈 EcoScore", key="nav_ecoscore", use_container_width=True):
                st.session_state.page = 'ecoscore'
                st.rerun()

            st.markdown("---")

            # Logout
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.info("Please sign in to access all features")
            if st.button("🔐 Sign In", key="sidebar_login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

    # Page Routing
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.user is None and st.session_state.page != 'home':
        st.session_state.page = 'login'
        st.rerun()
    elif st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == 'contribute':
        contribution_page()
    elif st.session_state.page == 'ecoscore':
        ecoscore_page()


if __name__ == "__main__":
    main()
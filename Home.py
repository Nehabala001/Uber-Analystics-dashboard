import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# Set page config
st.set_page_config(page_title="NCR Ride Bookings Dashboard", page_icon="🚕", layout="wide")

# Optional: Add a logo or banner image if available
# image = Image.open('path_to_logo.png')
# st.image(image, width=150)
st.title("🚕 NCR Ride Bookings Dashboard")
st.markdown("""
Welcome to the NCR Ride Bookings Dashboard!

This dashboard provides interactive analytics and visualizations for ride bookings data in the NCR region. Explore booking trends, cancellations, ride metrics, ratings, and payment methods.

**Navigation:**
- Use the sidebar to access different analysis pages (Main, About, etc).
- Visualizations and insights are updated live as you interact with the dashboard.

---
""")

st.header("Get Started")
st.info("Select a page from the sidebar to begin exploring the data.")

st.markdown("""
#### Project Features
- Booking status analysis
- Cancellation reasons
- Ride value and distance trends
- Ratings and payment method insights

*Developed with Streamlit, pandas, and Plotly.*
""")


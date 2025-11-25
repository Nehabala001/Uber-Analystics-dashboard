import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard - Main", page_icon="📊", layout="wide")

st.title("📊 NCR Ride Bookings Dashboard - Main")

# Load data
@st.cache_data


def load_data():
    df = pd.read_csv("ncr_ride_bookings.csv")
    # Clean up quotes in string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.replace('"', '').str.strip()
    # Parse datetime
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    # Numeric conversions
    for col in ['Avg VTAT', 'Avg CTAT', 'Booking Value', 'Ride Distance', 'Driver Ratings', 'Customer Rating']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# Show key metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", f"{len(df):,}")
col2.metric("Completed", f"{(df['Booking Status']=='Completed').sum():,}")
col3.metric("Cancelled", f"{((df['Booking Status']=='Cancelled by Customer') | (df['Booking Status']=='Cancelled by Driver')).sum():,}")
col4.metric("No Driver Found", f"{(df['Booking Status']=='No Driver Found').sum():,}")

st.markdown("---")

# Booking Status Distribution
st.subheader("Booking Status Distribution")
status_counts = df['Booking Status'].value_counts().reset_index()
status_counts.columns = ['Booking Status', 'Count']
fig = px.bar(status_counts, x='Booking Status', y='Count', color='Booking Status',
             title='Booking Status Distribution', text='Count')
st.plotly_chart(fig, use_container_width=True)

# Time-based trends (monthly)
st.subheader("Completed Rides per Month")
completed = df[df['Booking Status'] == 'Completed'].copy()
if not completed.empty:
    completed['Month'] = completed['Datetime'].dt.to_period('M').astype(str)
    monthly_counts = completed.groupby('Month').size().reset_index(name='Count')
    fig2 = px.line(monthly_counts, x='Month', y='Count', markers=True, title='Completed Rides per Month')
    st.plotly_chart(fig2, use_container_width=True)

# Ride Value and Distance Distributions
st.subheader("Ride Value and Distance Distributions (Completed Rides)")
col5, col6 = st.columns(2)
with col5:
    fig3, ax1 = plt.subplots()
    sns.histplot(completed['Booking Value'].dropna(), bins=30, kde=True, color='skyblue', ax=ax1)
    ax1.set_title('Ride Value Distribution')
    ax1.set_xlabel('Booking Value (₹)')
    st.pyplot(fig3)
with col6:
    fig4, ax2 = plt.subplots()
    sns.histplot(completed['Ride Distance'].dropna(), bins=30, kde=True, color='salmon', ax=ax2)
    ax2.set_title('Ride Distance Distribution')
    ax2.set_xlabel('Ride Distance (km)')
    st.pyplot(fig4)

# Ratings Analysis
st.subheader("Ratings Analysis (Completed Rides)")
col7, col8 = st.columns(2)
with col7:
    fig5, ax3 = plt.subplots()
    sns.histplot(completed['Driver Ratings'].dropna(), bins=20, kde=True, color='blue', ax=ax3, label='Driver')
    sns.histplot(completed['Customer Rating'].dropna(), bins=20, kde=True, color='green', ax=ax3, label='Customer')
    ax3.set_title('Distribution of Ratings')
    ax3.set_xlabel('Rating')
    ax3.legend()
    st.pyplot(fig5)
with col8:
    avg_ratings_vehicle = completed.groupby('Vehicle Type')[['Driver Ratings', 'Customer Rating']].mean().sort_values('Driver Ratings', ascending=False)
    fig6 = px.bar(avg_ratings_vehicle, barmode='group', title='Average Ratings by Vehicle Type')
    st.plotly_chart(fig6, use_container_width=True)

# Add Sunburst: hierarchical view of Vehicle Type -> Payment Method -> Booking Status
st.subheader("Bookings Breakdown: Vehicle → Payment → Status")

# Helper to find columns by keywords
def _find_col(df, keywords):
    for c in df.columns:
        name = c.lower()
        if all(k in name for k in keywords):
            return c
    for c in df.columns:
        name = c.lower()
        if any(k in name for k in keywords):
            return c
    return None

vehicle_col = _find_col(df, ['vehicle'])
payment_col = _find_col(df, ['payment'])
booking_col = _find_col(df, ['booking', 'status']) or _find_col(df, ['status'])

if vehicle_col and payment_col and booking_col:
    sunburst_df = df[[vehicle_col, payment_col, booking_col]].copy()
    sunburst_df = sunburst_df.fillna('Unknown')
    sunburst_df['count'] = 1
    sunburst_agg = sunburst_df.groupby([vehicle_col, payment_col, booking_col]).size().reset_index(name='Count')

    fig_sun = px.sunburst(sunburst_agg, path=[vehicle_col, payment_col, booking_col], values='Count', color=vehicle_col,
                          title='Bookings by Vehicle Type, Payment Method and Status')
    st.plotly_chart(fig_sun, use_container_width=True)
else:
    st.info("Sunburst visualization requires columns for Vehicle Type, Payment Method and Booking Status.\n"
            f"Detected columns: vehicle={vehicle_col}, payment={payment_col}, booking/status={booking_col}")

# Show data sample
with st.expander("Show Raw Data Sample"):
    st.dataframe(df.head(50))

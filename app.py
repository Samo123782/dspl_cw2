import pandas as pd
import streamlit as st
import plotly.express as px

#  Page Configuration 
st.set_page_config(page_title="Sri Lanka Displacements Dashboard", page_icon="🇱🇰", layout="wide")

#  Load Dataset 
df = pd.read_csv("/Users/samodamarasinghe/Desktop/dspl_cw2/internal-displacements-new-displacements-associated-with-disasters_lka.csv")

#  Data Cleaning 
df.columns = df.columns.str.strip()

# Ensure 'year' is numeric
df["year"] = pd.to_numeric(df["year"], errors='coerce')
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

# Ensure 'new_displacement' is numeric
df["new_displacement"] = pd.to_numeric(df["new_displacement"], errors='coerce')
df = df.dropna(subset=["new_displacement"])

# Sidebar Filters 
st.sidebar.header("🔎 Filter Data")

years = st.sidebar.multiselect(
    "Select Year(s)", 
    options=sorted(df["year"].unique()), 
    default=[df["year"].max()]
)

filtered_df = df[df["year"].isin(years)]

# App Title 
st.title("🇱🇰 Sri Lanka Disaster-Related Displacements Dashboard")
st.markdown("Analyze disaster-induced displacement patterns across Sri Lanka based on available data.")

# Key Statistics 
st.subheader("Key Metrics")

total_displacements = filtered_df["new_displacement"].sum()
total_events = filtered_df["event_name"].nunique()

if not filtered_df.empty:
    max_displacement_event = filtered_df.loc[filtered_df["new_displacement"].idxmax(), "event_name"]
else:
    max_displacement_event = "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Displacements", f"{int(total_displacements):,}")
col2.metric("Number of Events", total_events)
col3.metric("Highest Displacement Event", max_displacement_event)

# Expandable Raw Data 
with st.expander(" See Raw Data"):
    st.dataframe(filtered_df)

# --- Charts Section ---

# Line Chart
st.subheader(" Line Chart: New Displacements per Event")
if "event_name" in filtered_df.columns and "new_displacement" in filtered_df.columns:
    fig1 = px.line(filtered_df, x="event_name", y="new_displacement", markers=True,
                   title="New Displacements per Event", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Required columns for line chart not found.")

# Bar Chart
st.subheader(" Bar Chart: Displacement by Hazard Category")
if "hazard_category_name" in filtered_df.columns and "new_displacement" in filtered_df.columns:
    fig2 = px.bar(filtered_df, x="hazard_category_name", y="new_displacement",
                  color="hazard_category_name",
                  title="Displacements by Hazard Category", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Required columns for bar chart not found.")

# Pie Chart
st.subheader(" Pie Chart: Distribution by Hazard Sub-Type")
if "hazard_subtype_name" in filtered_df.columns and "new_displacement" in filtered_df.columns:
    fig3 = px.pie(filtered_df, names="hazard_subtype_name", values="new_displacement",
                  title="Displacement Distribution by Hazard Sub-Type")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Required columns for pie chart not found.")

# Area Chart
st.subheader(" Area Chart: New Displacements Across Events")
if "event_name" in filtered_df.columns and "new_displacement" in filtered_df.columns:
    fig_area = px.area(filtered_df, x="event_name", y="new_displacement",
                       title="Area Chart of New Displacements Across Events", template="plotly_white")
    st.plotly_chart(fig_area, use_container_width=True)
else:
    st.warning("Required columns for area chart not found.")

# Box Plot
st.subheader(" Box Plot: Spread by Hazard Category")
if "hazard_category_name" in filtered_df.columns and "new_displacement" in filtered_df.columns:
    fig_box = px.box(filtered_df, x="hazard_category_name", y="new_displacement",
                     points="all", color="hazard_category_name",
                     title="Displacement Spread by Hazard Category", template="plotly_white")
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.warning("Required columns for box plot not found.")

# Histogram
st.subheader(" Histogram: Distribution of New Displacements")
if "new_displacement" in filtered_df.columns:
    fig_hist = px.histogram(filtered_df, x="new_displacement", nbins=20,
                             title="Histogram of New Displacements", template="plotly_white")
    st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("Required column for histogram not found.")

# --- Summary Statistics ---
st.subheader(" Summary Statistics")
st.dataframe(filtered_df.describe(include='all'))

# --- Download Filtered Data ---
st.subheader(" Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download CSV File", data=csv, file_name=f'displacement_data_filtered.csv', mime='text/csv')

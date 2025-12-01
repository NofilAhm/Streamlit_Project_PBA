#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt
import numpy as np

# Initialize session state for navigation
if "current_tab" not in st.session_state:
    st.session_state["current_tab"] = "Sales Overview" # Default tab

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Styling and Readability
# -------------------------
FOODPANDA_THEME = """
<style>
/* 1. MAIN BACKGROUND: Transparent Foodpanda Pink */
[data-testid="stAppViewContainer"] {
    background-color: rgba(215, 15, 100, 0.8) !important; 
    color: #D70F64 !important; 
}

/* 2. PUSH CONTENT DOWN (Top Space Reduction on Main Content) */
[data-testid="stApp"] {
    padding-top: 0px !important; 
}

/* AGGRESSIVE FIX: Target the main content container to remove built-in padding */
[data-testid="stVerticalBlock"] {
    padding-top: 0px !important;
    margin-top: 0px !important;
}

/* 3. INPUT FIELD STYLING: FIXING READABILITY (White Box, Black Text) */
.stTextInput > div:first-child {
    background-color: white !important; 
    border-radius: 0.25rem; 
    padding: 0.5rem; 
}
.stTextInput > div > div > input {
    color: black !important; 
    background-color: transparent !important; 
    border: none !important; 
}

/* 4. Ensure input labels and titles are visible */
/* 4A. INPUT LABELS FIX: Set to WHITE for the pink LOGIN screen background */
.stTextInput > label {
    color: white !important;
}

/* 4B. H1, H2, H3, H4, .stMarkdown - Keep Pink for titles/headers on the login screen */
h1, h2, h3, h4, .stMarkdown {
    color: #D70F64 !important; 
}


/* 5. General Button Styling (Default) */
.stButton > button {
    background-color: #FFFFFF;
    border: 1px solid #D70F64;
    color: #D70F64 !important;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #FF5A93;
    color: white !important; 
}

/* KPI LABEL FIX: Large, bold titles for metrics */
[data-testid="stMetricLabel"] {
    font-size: 1.35rem !important; 
    font-weight: bold !important; 
    color: #333333 !important; 
}
[data-testid="stMetricLabel"] div {
    font-size: 1.35rem !important; 
    font-weight: bold !important; 
    color: #333333 !important; 
}

/* Sidebar Styling for Spacing and Font Color */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 10px !important; 
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4, 
[data-testid="stSidebar"] .stMarkdown {
    color: white !important; 
}

/* Login Dashboard Title Styling (White text on pink background) */
.login-title {
    color: white !important; 
    text-align: center;
    font-size: 2em;
    font-weight: bold;
}

</style>
"""
st.markdown(FOODPANDA_THEME, unsafe_allow_html=True)

# -------------------------
# Hardcoded users & Session State
# -------------------------
USERS = {
    "nofil": "12345",
    "admin": "admin123"
}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# -------------------------
# Login function 
# -------------------------
def login():
    col1, col2, col3 = st.columns([1, 1, 1]) 
    
    with col2:
        st.markdown("<h2 class='login-title'>FOODPANDA SALES DASHBOARD</h2>", unsafe_allow_html=True)
        
        with st.container(border=True): 
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login", use_container_width=True):
                if username in USERS and USERS[username] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("Logged in successfully! Redirecting...")
                    st.rerun()
                    return 
                else:
                    st.error("Invalid username or password")
                    
# -------------------------
# Data Loading and Preparation Function
# -------------------------
@st.cache_data
def load_data():
    """Loads, cleans, and engineers features for the sales dashboard."""
    
    # Reverting to the local path as requested by the user
    DATA_FILE = Path(__file__).parent / "dataset" 

    try:
        df = pd.read_csv(DATA_FILE)
        
        # --- DATA CLEANING & FEATURE ENGINEERING ---
        DATE_COLUMNS = ['signup_date', 'order_date', 'last_order_date', 'rating_date']
        for col in DATE_COLUMNS:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
        
        # Ensure text columns are clean
        df['item_name'] = df['item_name'].astype(str).fillna('Unknown Item')
        df['category'] = df['category'].astype(str).fillna('Unknown Category')
        df['restaurant_name'] = df['restaurant_name'].astype(str).fillna('Unknown Restaurant')

        # Create sales column
        df['sales'] = df['quantity'] * df['price']
        
        df['Order_Day'] = df['order_date'].dt.normalize()
        df['DayOfWeek'] = df['order_date'].dt.day_name()
        
        # Ensure essential columns are clean
        df.dropna(subset=['order_id', 'order_date', 'sales', 'customer_id'], inplace=True)
        
        return df

    except Exception as e:
        # Simplified error message for local file failure
        st.error(f"Failed to load or process data from '{DATA_FILE}'. Error: {e}")
        return pd.DataFrame() 

# -------------------------
# Tab Content Functions
# -------------------------

def show_sales_overview(df):
    """Generates the content for the Sales Overview tab."""
    ORDER_COL = 'order_id' 
    PRICE_COL = 'sales'

    st.title("Foodpanda Sales Overview Dashboard 🐼")
    st.write("---")
    
    if ORDER_COL in df.columns and PRICE_COL in df.columns:
        
        total_revenue = df[PRICE_COL].sum()
        total_orders = df[ORDER_COL].nunique()
        average_order_value = total_revenue / total_orders if total_orders else 0
        
        st.header("Sales Overview")
        st.subheader("Key Performance Indicators (KPIs) for All Time")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
        with kpi_col2:
            st.metric(label="📦 Total Orders", value=f"{total_orders:,}")
        with kpi_col3:
            st.metric(label="💸 Average Order Value (AOV)", value=f"${average_order_value:,.2f}")
        
        st.write("---")
    
    # MONTH-WISE SALES CHART
    if 'order_date' in df.columns and PRICE_COL in df.columns:
        st.subheader("Monthly Revenue Trend (Month and Year)")
        
        df['Order_Month_Date'] = df['order_date'].dt.to_period('M').dt.start_time
        
        monthly_sales = df.groupby('Order_Month_Date')[PRICE_COL].sum().reset_index()
        monthly_sales.columns = ['Month', 'Total Sales']

        chart = alt.Chart(monthly_sales).mark_line(point=True, color='#D70F64').encode(
            x=alt.X('Month:T', 
                    axis=alt.Axis(title='Month and Year', format='%b %Y')),
            y=alt.Y('Total Sales:Q', axis=alt.Axis(title='Total Revenue ($)')),
            tooltip=[alt.Tooltip('Month', format='%b %Y'), alt.Tooltip('Total Sales', format='$,.2f')]
        ).properties(
            title='Monthly Revenue Over Time'
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        st.write("---")
    else:
        st.warning("Cannot generate monthly sales chart. Check 'order_date' and 'sales' columns.")

def show_customer_overview(df):
    """Generates the content for the Customer Overview tab, including KPIs and Charts."""
    CUST_COL = 'customer_id' 
    PRICE_COL = 'sales'
    DATE_COL = 'order_date'
    AGE_GROUP_COL = 'age' 

    st.title("Customer Overview Dashboard 👥")
    st.write("---")
    
    if CUST_COL in df.columns and PRICE_COL in df.columns and DATE_COL in df.columns:
        
        # --- KPI Calculations ---
        total_customers = df[CUST_COL].nunique()
        total_revenue = df[PRICE_COL].sum()
        
        sales_per_customer = total_revenue / total_customers if total_customers else 0
        
        present_date = df[DATE_COL].max()
        last_order_df = df.groupby(CUST_COL)[DATE_COL].max().reset_index()
        last_order_df['days_since_last_order'] = (present_date - last_order_df[DATE_COL]).dt.days
        CHURN_THRESHOLD_DAYS = 180
        churned_customers = last_order_df[last_order_df['days_since_last_order'] > CHURN_THRESHOLD_DAYS][CUST_COL].count()
        churn_rate_percent = (churned_customers / total_customers) * 100 if total_customers else 0
        
        # --- KPI Display ---
        st.header("Customer KPIs")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric(label="👥 Total Customers", value=f"{total_customers:,}")
        with kpi_col2:
            st.metric(label="💸 Sales Per Customer (ACV)", value=f"${sales_per_customer:,.2f}")
        with kpi_col3:
            st.metric(
                label="📉 Customer Churn Rate", 
                value=f"{churn_rate_percent:.2f}%",
                help=f"Customers are considered churned if they have not ordered in the last {CHURN_THRESHOLD_DAYS} days."
            )
        
        st.write("---")

        # --- Chart Section ---
        st.header("Customer Demographics and Payment Analysis")
        chart_col1, chart_col2 = st.columns(2)

        # 1. Bar Chart: Payment Method Analysis (Left Column)
        with chart_col1:
            if 'payment_method' in df.columns and PRICE_COL in df.columns:
                payment_sales = df.groupby('payment_method')[PRICE_COL].sum().reset_index()
                payment_sales.columns = ['Payment Method', 'Total Sales']
                
                st.subheader("Total Sales by Payment Method")
                
                bar_chart = alt.Chart(payment_sales).mark_bar(color='#D70F64').encode(
                    x=alt.X('Total Sales:Q', title='Total Revenue ($)'),
                    y=alt.Y('Payment Method:N', title='Payment Method', sort='-x'),
                    tooltip=['Payment Method', alt.Tooltip('Total Sales', format='$,.0f')]
                ).properties(
                    height=300
                ).interactive()
                st.altair_chart(bar_chart, use_container_width=True)
            else:
                st.info("Cannot show Payment Method chart. Missing 'payment_method' column.")


        # 2. Pie Chart: Age Distribution (Right Column) - REMOVED ALL LABELS
        with chart_col2:
            if AGE_GROUP_COL in df.columns and CUST_COL in df.columns:
                
                customer_age = df[[CUST_COL, AGE_GROUP_COL]].drop_duplicates(subset=[CUST_COL]).dropna(subset=[AGE_GROUP_COL])
                
                if not customer_age.empty:
                    
                    age_counts = customer_age.groupby(AGE_GROUP_COL)[CUST_COL].count().reset_index()
                    age_counts.columns = ['Age Group', 'Customer Count']
                    
                    # Calculate Percentage
                    total_customers_in_chart = age_counts['Customer Count'].sum()
                    age_counts['Percentage'] = (age_counts['Customer Count'] / total_customers_in_chart) * 100
                    
                    st.subheader("Customer Distribution by Age Group")

                    pie_chart = alt.Chart(age_counts).encode(
                        theta=alt.Theta("Customer Count", stack=True)
                    ) 
                    
                    color_scale = alt.Scale(range=['#D70F64', '#FF5A93', '#FF8CC6', '#6A053F', '#9C0A52'])

                    # Draw the arcs (pie slices) - relying on tooltips/legend
                    arc = pie_chart.mark_arc(outerRadius=140, innerRadius=30).encode(
                        color=alt.Color("Age Group:N", scale=color_scale),
                        order=alt.Order("Customer Count", sort="descending"),
                        tooltip=[
                            "Age Group", 
                            "Customer Count", 
                            alt.Tooltip('Percentage', format='.2f', title='Contribution (%)') 
                        ] 
                    )
                    
                    final_pie = arc
                    
                    st.altair_chart(final_pie, use_container_width=True)
                    
                else:
                    st.info(f"Age Group data is missing for unique customers.")
            else:
                st.info(f"Cannot show Age Distribution chart. Missing '{AGE_GROUP_COL}' or '{CUST_COL}' column.")
        
        st.write("---") 
    else:
        st.warning("Customer KPIs cannot be calculated. Ensure 'customer_id', 'sales', and 'order_date' columns exist.")


def show_product_overview(df):
    """Generates the content for the Product Overview tab based on provided KPIs."""
    
    ITEM_COL = 'item_name'
    CATEGORY_COL = 'category'
    RESTAURANT_COL = 'restaurant_name'
    QTY_COL = 'quantity'
    SALES_COL = 'sales'
    RATING_COL = 'rating'
    ISSUES_COL = 'delivery_issues' 

    st.title("Product & Restaurant Overview Dashboard 🍔")
    st.write("---")

    # Check for required columns before proceeding
    required_cols = [ITEM_COL, CATEGORY_COL, RESTAURANT_COL, QTY_COL, SALES_COL]
    if not all(col in df.columns for col in required_cols):
        st.warning(f"Missing required columns for Product Overview: {', '.join([c for c in required_cols if c not in df.columns])}")
        return

    # ----------------------------------------------------
    #  --- Sales Visualization Section (Restaurant & Dish) ---
    # ----------------------------------------------------
    st.header("Sales Performance Visualizations 📈")
    col_rest_sales, col_dish_sales = st.columns(2)

    # 1. Bar Chart: Restaurant Sales (All Restaurants - Top 20)
    with col_rest_sales:
        st.subheader("Top 20 Restaurant Sales Ranking")
        restaurant_sales = df.groupby(RESTAURANT_COL)[SALES_COL].sum().reset_index()
        restaurant_sales.columns = ['Restaurant Name', 'Total Sales']
        
        # Sort and select top 20 for a cleaner chart
        top_n_rest_sales = restaurant_sales.sort_values('Total Sales', ascending=False).head(20)

        chart_rest = alt.Chart(top_n_rest_sales).mark_bar(color='#D70F64').encode(
            x=alt.X('Total Sales:Q', title='Total Revenue ($)'),
            y=alt.Y('Restaurant Name:N', sort='-x', title=''),
            tooltip=['Restaurant Name', alt.Tooltip('Total Sales', format='$,.0f')]
        ).properties(
            title='Top 20 Restaurants by Sales'
        ).interactive()
        
        st.altair_chart(chart_rest, use_container_width=True)


    # 2. Bar Chart: Top Dish Sales (Top 15 Dishes)
    with col_dish_sales:
        st.subheader("Top 15 Dishes by Sales Revenue")
        dish_sales = df.groupby(ITEM_COL)[SALES_COL].sum().nlargest(15).reset_index()
        dish_sales.columns = ['Dish Name', 'Total Sales']

        chart_dish = alt.Chart(dish_sales).mark_bar(color='#FF5A93').encode(
            x=alt.X('Total Sales:Q', title='Total Revenue ($)'),
            y=alt.Y('Dish Name:N', sort='-x', title=''),
            tooltip=['Dish Name', alt.Tooltip('Total Sales', format='$,.0f')]
        ).properties(
            title='Top 15 Dishes by Revenue'
        ).interactive()

        st.altair_chart(chart_dish, use_container_width=True)
        
    st.write("---")

    # --- 1. Top Sellers Section (Original Top Sellers by Quantity/Revenue) ---
    st.header("Top Sellers (Quantity vs. Revenue)")
    col_qty, col_rev = st.columns(2)

    # 1A. Most Sold Dishes (by quantity)
    with col_qty:
        st.subheader("🥇 Most Sold Dishes (by Quantity)")
        top_qty = df.groupby(ITEM_COL)[QTY_COL].sum().nlargest(10).reset_index()
        top_qty.columns = ['Item Name', 'Total Quantity Sold']
        
        # Create Bar Chart
        chart_qty = alt.Chart(top_qty).mark_bar(color='#D70F64').encode(
            x=alt.X('Total Quantity Sold:Q', title='Quantity Sold'),
            y=alt.Y('Item Name:N', sort='-x', title=''),
            tooltip=['Item Name', alt.Tooltip('Total Quantity Sold', format=',')]
        ).properties(height=350)
        st.altair_chart(chart_qty, use_container_width=True)
        st.dataframe(top_qty, use_container_width=True, hide_index=True)

    # 1B. Most Revenue-Generating Dishes (by price × quantity)
    with col_rev:
        st.subheader("💰 Top Revenue-Generating Dishes")
        top_rev = df.groupby(ITEM_COL)[SALES_COL].sum().nlargest(10).reset_index()
        top_rev.columns = ['Item Name', 'Total Revenue']

        # Create Bar Chart
        chart_rev = alt.Chart(top_rev).mark_bar(color='#FF5A93').encode(
            x=alt.X('Total Revenue:Q', title='Total Revenue ($)'),
            y=alt.Y('Item Name:N', sort='-x', title=''),
            tooltip=['Item Name', alt.Tooltip('Total Revenue', format='$,.2f')]
        ).properties(height=350)
        st.altair_chart(chart_rev, use_container_width=True)
        st.dataframe(top_rev, use_container_width=True, hide_index=True)

    st.write("---")

    # --- 2. Category Insights Section ---
    st.header("Category Insights")
    
    # Check if 'rating' column exists for Category aggregation
    if RATING_COL in df.columns:
        category_summary = df.groupby(CATEGORY_COL).agg(
            Total_Sales=(SALES_COL, 'sum'),
            Total_Orders=('order_id', 'nunique'),
            Avg_Rating=(RATING_COL, 'mean')
        ).reset_index()
        category_summary['Avg_Rating'] = category_summary['Avg_Rating'].round(2)
    else:
        # Fallback if 'rating' is missing
        category_summary = df.groupby(CATEGORY_COL).agg(
            Total_Sales=(SALES_COL, 'sum'),
            Total_Orders=('order_id', 'nunique')
        ).reset_index()
        category_summary['Average Rating'] = np.nan # Add NaN column to maintain structure
        
    # Calculate Total Sales for Percentage
    total_sales_overall = category_summary['Total_Sales'].sum()
    category_summary['Sales_Share'] = (category_summary['Total_Sales'] / total_sales_overall) 
    
    # Calculate Category-wise AOV
    category_summary['AOV'] = category_summary['Total_Sales'] / category_summary['Total_Orders']
    category_summary['AOV'] = category_summary['AOV'].round(2)
    
    
    category_summary = category_summary.rename(columns={
        'Total_Sales': 'Total Sales', 
        'Total_Orders': 'Total Orders',
        'Sales_Share': 'Sales Share',
        'Avg_Rating': 'Average Rating'
    })

    col_share, col_aov, col_rating = st.columns(3)

    # 2A. Category Share of Sales (Donut Chart)
    with col_share:
        st.subheader("📊 Category Share of Sales")
        
        chart_share = alt.Chart(category_summary).encode(
            theta=alt.Theta("Total Sales", stack=True)
        )
        
        color_scale = alt.Scale(range=['#D70F64', '#FF5A93', '#FF8CC6', '#6A053F', '#9C0A52', '#333333'])

        arc_share = chart_share.mark_arc(outerRadius=120, innerRadius=60).encode(
            color=alt.Color(CATEGORY_COL, scale=color_scale),
            order=alt.Order("Total Sales", sort="descending"),
            tooltip=[
                CATEGORY_COL, 
                alt.Tooltip('Total Sales', format='$,.2f', title='Revenue'), 
                alt.Tooltip('Sales Share', format='.1%', title='Share (%)') 
            ] 
        ).properties(height=350)
        
        st.altair_chart(arc_share, use_container_width=True)

    # 2B. Category-wise AOV (Bar Chart)
    with col_aov:
        st.subheader("💸 Category Average Order Value (AOV)")
        
        chart_aov = alt.Chart(category_summary).mark_bar(color='#D70F64').encode(
            x=alt.X('AOV:Q', title='AOV ($)'),
            y=alt.Y(CATEGORY_COL + ':N', sort='-x', title=''),
            tooltip=[CATEGORY_COL, alt.Tooltip('AOV', format='$,.2f')]
        ).properties(height=350)
        
        st.altair_chart(chart_aov, use_container_width=True)

    # 2C. Category-wise Ratings (Bar Chart)
    with col_rating:
        st.subheader("⭐ Category Average Rating")
        
        if 'Average Rating' in category_summary.columns and not category_summary['Average Rating'].isna().all():
            # Determine rating scale min/max for better visualization
            valid_ratings = category_summary['Average Rating'].dropna()
            rating_scale_min = valid_ratings.min() * 0.9 if not valid_ratings.empty else 1
            rating_scale_max = valid_ratings.max() * 1.1 if not valid_ratings.empty else 5

            chart_rating = alt.Chart(category_summary).mark_bar(color='#FF5A93').encode(
                x=alt.X('Average Rating:Q', title='Average Rating', scale=alt.Scale(domain=[rating_scale_min, rating_scale_max])),
                y=alt.Y(CATEGORY_COL + ':N', sort=alt.EncodingSortField(field='Average Rating', order='descending'), title=''),
                tooltip=[CATEGORY_COL, alt.Tooltip('Average Rating', format='.2f')]
            ).properties(height=350)
            
            st.altair_chart(chart_rating, use_container_width=True)
        else:
             st.info("Average Rating data is not available in the dataset.")


    st.write("---")

    # --- 3. Restaurant Insights Section ---
    st.header("Restaurant Insights")

    # Aggregate Restaurant Data (SIMPLIFIED to only Total Sales to resolve KeyError)
    restaurant_summary = df.groupby(RESTAURANT_COL).agg(
        Total_Sales=(SALES_COL, 'sum'),
        # Avg_Rating=(RATING_COL, 'mean'), # Removed due to potential KeyError
        # Delivery_Issues_Count=(ISSUES_COL, 'sum') # Removed due to potential KeyError
    ).reset_index()
    
    # KPIs (Simplified to only Highest Sales)
    highest_sales_rest = restaurant_summary.loc[restaurant_summary['Total_Sales'].idxmax()]
    
    kpi_r1 = st.columns(1)[0] # Use a single column for the single KPI

    with kpi_r1:
        st.metric(
            label="🏆 Highest Sales Restaurant", 
            value=f"{highest_sales_rest[RESTAURANT_COL]}",
            delta=f"${highest_sales_rest['Total_Sales']:,.0f}"
        )
    
    st.write("---")
    
    # Top 10 Restaurant Sales Table (Simplified columns)
    st.subheader("Top 10 Restaurants by Sales (Table View)")
    top_rest_sales = restaurant_summary.sort_values('Total_Sales', ascending=False).head(10).rename(
        columns={'Total_Sales': 'Total Sales ($)'}
    )
    st.dataframe(top_rest_sales.style.format({
        'Total Sales ($)': '$,.0f',
    }), use_container_width=True, hide_index=True)


# -------------------------
# Main Dashboard Function
# -------------------------
def main_dashboard():
    # Reset background theme for the main dashboard content area
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: white !important; 
            color: #333333 !important;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(215, 15, 100, 0.8) !important;
        }
        
        /* FIX OVERRIDE: Input Labels inside the white dashboard content area must be dark for visibility */
        .stApp .stTextInput > label {
            color: #333333 !important; /* Overrides the white label color set in the global CSS */
        }
        
        </style>
        """, unsafe_allow_html=True)
    
    df = load_data() 
    if df.empty:
        # If data load failed, display the error message from load_data and stop execution
        return

    # --- Sidebar Setup ---
    st.sidebar.title("Dashboard Menu")
    st.sidebar.markdown(f"**Welcome, {st.session_state['username']}**")
    
    # Logout Button
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.clear() 
        st.rerun() 
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    
    # --- Tab Buttons ---
    TAB_NAMES = ["Sales Overview", "Customer Overview", "Product Overview"]
    current_tab = st.session_state["current_tab"]
    
    def nav_button(label, current_tab):
        if st.sidebar.button(label, use_container_width=True, key=f"nav_{label}"):
            st.session_state["current_tab"] = label
            st.rerun()
            
        if current_tab == label:
            st.sidebar.markdown(
                f"""
                <style>
                    [data-testid="stSidebar"] button[kind="secondary"][key="nav_{label}"] {{
                        background-color: white !important;
                        color: #D70F64 !important;
                        border: 2px solid white !important;
                        font-weight: bold;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

    for tab in TAB_NAMES:
        nav_button(tab, current_tab)


    # --- Content Routing ---
    if st.session_state["current_tab"] == "Sales Overview":
        show_sales_overview(df)
    elif st.session_state["current_tab"] == "Customer Overview":
        show_customer_overview(df)
    elif st.session_state["current_tab"] == "Product Overview":
        show_product_overview(df)


# -------------------------
# App routing
# -------------------------
def main():
    if not st.session_state.get("logged_in", False):
        login()
    else:
        main_dashboard()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    main()

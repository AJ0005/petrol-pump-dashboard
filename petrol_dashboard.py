import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import os

# Set page config
st.set_page_config(layout="wide", page_title="Petrol Pump Dashboard", page_icon="⛽")

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 5px; padding: 8px 16px;}
    .stButton>button:hover {background-color: #45a049;}
    .metric-box {border: 1px solid #ddd; border-radius: 8px; padding: 10px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .metric-label {font-size: 14px; color: #555;}
    .metric-value {font-size: 20px; font-weight: bold;}
    .sidebar .sidebar-content {background-color: #e8ecef;}
    .stTabs [data-baseweb="tab"] {background-color: #ffffff; border-radius: 5px; margin: 5px;}
    .stTabs [data-baseweb="tab"]:hover {background-color: #e0e7ff;}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif;}
    h2 {color: #34495e; font-family: 'Arial', sans-serif;}
    .stExpander {background-color: #ffffff; border: 1px solid #ddd; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# File paths for CSV storage
SALES_DATA_PATH = "petrol_pump_sales_data.csv"
CREDIT_DEBIT_PATH = "petrol_pump_credit_debit.csv"
OWNER_TRANSACTIONS_PATH = "petrol_pump_owner_transactions.csv"
EMPLOYEE_SHORTAGES_PATH = "petrol_pump_employee_shortages.csv"

# Initialize CSV files with headers if they don’t exist
def init_csv_files():
    if not os.path.exists(SALES_DATA_PATH):
        columns = [
            "id", "date", "petrol_c3_open", "petrol_c3_close", "petrol_c3_sales",
            "petrol_c4_open", "petrol_c4_close", "petrol_c4_sales",
            "petrol_a1_open", "petrol_a1_close", "petrol_a1_sales",
            "petrol_a2_open", "petrol_a2_close", "petrol_a2_sales",
            "hsd_c1_open", "hsd_c1_close", "hsd_c1_sales",
            "hsd_c2_open", "hsd_c2_close", "hsd_c2_sales",
            "hsd_b1_open", "hsd_b1_close", "hsd_b1_sales",
            "hsd_b2_open", "hsd_b2_close", "hsd_b2_sales",
            "xp_b3_open", "xp_b3_close", "xp_b3_sales",
            "xp_b4_open", "xp_b4_close", "xp_b4_sales",
            "test_b1", "test_b2", "test_b3", "test_b4",
            "petrol_rate", "hsd_rate", "xp_rate",
            "petrol_amount", "hsd_amount", "xp_amount",
            "gross_sales_amount", "total_sales_amount",
            "paytm_amount", "icici_amount", "fleet_card_amount",
            "pump_expenses", "pump_expenses_remark"
        ]
        pd.DataFrame(columns=columns).to_csv(SALES_DATA_PATH, index=False)

    if not os.path.exists(CREDIT_DEBIT_PATH):
        pd.DataFrame(columns=["id", "date", "party", "type", "amount"]).to_csv(CREDIT_DEBIT_PATH, index=False)

    if not os.path.exists(OWNER_TRANSACTIONS_PATH):
        pd.DataFrame(columns=["id", "date", "owner_name", "type", "mode", "amount", "remark"]).to_csv(OWNER_TRANSACTIONS_PATH, index=False)

    if not os.path.exists(EMPLOYEE_SHORTAGES_PATH):
        pd.DataFrame(columns=["id", "date", "employee_name", "shortage_amount"]).to_csv(EMPLOYEE_SHORTAGES_PATH, index=False)

# Initialize CSV files
init_csv_files()

# Title
st.markdown("<h1>⛽ Petrol Pump Daily Sales Dashboard</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h2 style='color: #2c3e50;'>📊 Data Input</h2>", unsafe_allow_html=True)
today = date.today()
selected_date = st.sidebar.date_input("📅 Select Date", value=today)

# Petrol Meter Readings
st.sidebar.subheader("⛽ Petrol Meter Readings (Liters)")
petrol_c3_open = st.sidebar.number_input("C3 Opening", min_value=0.0, step=0.1, key="c3_open")
petrol_c3_close = st.sidebar.number_input("C3 Closing", min_value=petrol_c3_open, step=0.1, key="c3_close")
petrol_c4_open = st.sidebar.number_input("C4 Opening", min_value=0.0, step=0.1, key="c4_open")
petrol_c4_close = st.sidebar.number_input("C4 Closing", min_value=petrol_c4_open, step=0.1, key="c4_close")
petrol_a1_open = st.sidebar.number_input("A1 Opening", min_value=0.0, step=0.1, key="a1_open")
petrol_a1_close = st.sidebar.number_input("A1 Closing", min_value=petrol_a1_open, step=0.1, key="a1_close")
petrol_a2_open = st.sidebar.number_input("A2 Opening", min_value=0.0, step=0.1, key="a2_open")
petrol_a2_close = st.sidebar.number_input("A2 Closing", min_value=petrol_a2_open, step=0.1, key="a2_close")
petrol_rate = st.sidebar.number_input("💰 Petrol Rate (per Liter)", min_value=0.0, step=0.01, value=104.62)

# HSD Meter Readings
st.sidebar.subheader("⛽ HSD Meter Readings (Liters)")
hsd_c1_open = st.sidebar.number_input("C1 Opening", min_value=0.0, step=0.1, key="c1_open")
hsd_c1_close = st.sidebar.number_input("C1 Closing", min_value=hsd_c1_open, step=0.1, key="c1_close")
hsd_c2_open = st.sidebar.number_input("C2 Opening", min_value=0.0, step=0.1, key="c2_open")
hsd_c2_close = st.sidebar.number_input("C2 Closing", min_value=hsd_c2_open, step=0.1, key="c2_close")
hsd_b1_open = st.sidebar.number_input("B1 Opening", min_value=0.0, step=0.1, key="b1_open")
hsd_b1_close = st.sidebar.number_input("B1 Closing", min_value=hsd_b1_open, step=0.1, key="b1_close")
hsd_b2_open = st.sidebar.number_input("B2 Opening", min_value=0.0, step=0.1, key="b2_open")
hsd_b2_close = st.sidebar.number_input("B2 Closing", min_value=hsd_b2_open, step=0.1, key="b2_close")
hsd_rate = st.sidebar.number_input("💰 HSD Rate (per Liter)", min_value=0.0, step=0.01, value=91.16)

# Petrol XP Meter Readings
st.sidebar.subheader("⛽ Petrol XP Meter Readings (Liters)")
xp_b3_open = st.sidebar.number_input("B3 Opening", min_value=0.0, step=0.1, key="b3_open")
xp_b3_close = st.sidebar.number_input("B3 Closing", min_value=xp_b3_open, step=0.1, key="b3_close")
xp_b4_open = st.sidebar.number_input("B4 Opening", min_value=0.0, step=0.1, key="b4_open")
xp_b4_close = st.sidebar.number_input("B4 Closing", min_value=xp_b4_open, step=0.1, key="b4_close")
xp_rate = st.sidebar.number_input("💰 XP Rate (per Liter)", min_value=0.0, step=0.01, value=111.57)

# Testing Amounts
st.sidebar.subheader("🧪 Testing (Liters)")
test_b1 = st.sidebar.number_input("Testing B1 (HSD)", min_value=0.0, max_value=(hsd_b1_close - hsd_b1_open), step=0.1)
test_b2 = st.sidebar.number_input("Testing B2 (HSD)", min_value=0.0, max_value=(hsd_b2_close - hsd_b2_open), step=0.1)
test_b3 = st.sidebar.number_input("Testing B3 (XP)", min_value=0.0, max_value=(xp_b3_close - xp_b3_open), step=0.1)
test_b4 = st.sidebar.number_input("Testing B4 (XP)", min_value=0.0, max_value=(xp_b4_close - xp_b4_open), step=0.1)

# Payment Transactions
st.sidebar.subheader("💳 Payment Transactions (₹)")
paytm_amount = st.sidebar.number_input("Paytm Amount", min_value=0.0, step=0.1, value=0.0)
icici_amount = st.sidebar.number_input("ICICI Amount", min_value=0.0, step=0.1, value=0.0)
fleet_card_amount = st.sidebar.number_input("Fleet Card Amount", min_value=0.0, step=0.1, value=0.0)

# Pump Expenses
st.sidebar.subheader("🛠️ Pump Expenses (₹)")
pump_expenses = st.sidebar.number_input("Pump Expenses", min_value=0.0, step=0.1, value=0.0)
pump_expenses_remark = st.sidebar.text_input("📝 Expenses Remark", value="")

# Employee-wise Shortage
st.sidebar.subheader("👨‍💼 Employee-wise Shortage (₹)")
num_employees = st.sidebar.number_input("Number of Employees", min_value=0, max_value=10, value=1, step=1)
employee_shortages = {}
for i in range(num_employees):
    with st.sidebar.expander(f"Employee {i+1}"):
        employee_name = st.text_input(f"Employee Name {i+1}", key=f"emp_name_{i}")
        shortage_amount = st.number_input(f"Shortage Amount {i+1} (₹)", min_value=0.0, step=0.1, key=f"emp_shortage_{i}")
        if employee_name and shortage_amount >= 0:
            employee_shortages[employee_name] = shortage_amount
total_employee_shortage = sum(employee_shortages.values())

# Owner's Transactions
st.sidebar.subheader("👑 Owner's Transactions (₹)")
num_owner_transactions = st.sidebar.number_input("Number of Owner Transactions", min_value=0, max_value=10, value=1, step=1)
owner_transactions = []
for i in range(num_owner_transactions):
    with st.sidebar.expander(f"Owner Transaction {i+1}"):
        owner_name = st.text_input(f"Owner Name {i+1}", key=f"owner_name_{i}")
        transaction_type = st.selectbox(f"Type {i+1}", ["Debit", "Credit"], key=f"owner_type_{i}")
        mode = st.selectbox(f"Mode {i+1}", ["Online", "Cheque", "Cash"], key=f"owner_mode_{i}")
        amount = st.number_input(f"Amount {i+1} (₹)", min_value=0.0, step=0.1, key=f"owner_amount_{i}")
        remark = st.text_input(f"Remark {i+1}", key=f"owner_remark_{i}")
        if owner_name and amount > 0:
            owner_transactions.append({
                "Date": selected_date, 
                "Owner_Name": owner_name, 
                "Type": transaction_type, 
                "Mode": mode, 
                "Amount": amount, 
                "Remark": remark
            })

# Calculate Sales
petrol_c3_sales = petrol_c3_close - petrol_c3_open
petrol_c4_sales = petrol_c4_close - petrol_c4_open
petrol_a1_sales = petrol_a1_close - petrol_a1_open
petrol_a2_sales = petrol_a2_close - petrol_a2_open
hsd_c1_sales = hsd_c1_close - hsd_c1_open
hsd_c2_sales = hsd_c2_close - hsd_c2_open
hsd_b1_sales = (hsd_b1_close - hsd_b1_open) - test_b1
hsd_b2_sales = (hsd_b2_close - hsd_b2_open) - test_b2
xp_b3_sales = (xp_b3_close - xp_b3_open) - test_b3
xp_b4_sales = (xp_b4_close - xp_b4_open) - test_b4

total_petrol = petrol_c3_sales + petrol_c4_sales + petrol_a1_sales + petrol_a2_sales
total_hsd = hsd_c1_sales + hsd_c2_sales + hsd_b1_sales + hsd_b2_sales
total_xp = xp_b3_sales + xp_b4_sales
petrol_amount = total_petrol * petrol_rate
hsd_amount = total_hsd * hsd_rate
xp_amount = total_xp * xp_rate
gross_sales_amount = petrol_amount + hsd_amount + xp_amount
total_sales_amount = gross_sales_amount - total_employee_shortage

# Party-wise Credit/Debit
st.sidebar.subheader("🤝 Party-wise Credit/Debit (₹)")
num_transactions = st.sidebar.number_input("Number of Transactions", min_value=0, max_value=10, value=1, step=1)
transactions = []
for i in range(num_transactions):
    with st.sidebar.expander(f"Transaction {i+1}"):
        party_name = st.text_input(f"Party Name {i+1}", key=f"party_{i}")
        transaction_type = st.selectbox(f"Type {i+1}", ["Credit", "Debit"], key=f"type_{i}")
        amount = st.number_input(f"Amount {i+1} (₹)", min_value=0.0, step=0.1, key=f"amount_{i}")
        if party_name and amount > 0:
            transactions.append({"Date": selected_date, "Party": party_name, "Type": transaction_type, "Amount": amount})

# Save Functions
def save_sales_data():
    df = pd.read_csv(SALES_DATA_PATH)
    new_id = df["id"].max() + 1 if not df.empty else 1
    data = {
        "id": new_id,
        "date": str(selected_date),
        "petrol_c3_open": petrol_c3_open, "petrol_c3_close": petrol_c3_close, "petrol_c3_sales": petrol_c3_sales,
        "petrol_c4_open": petrol_c4_open, "petrol_c4_close": petrol_c4_close, "petrol_c4_sales": petrol_c4_sales,
        "petrol_a1_open": petrol_a1_open, "petrol_a1_close": petrol_a1_close, "petrol_a1_sales": petrol_a1_sales,
        "petrol_a2_open": petrol_a2_open, "petrol_a2_close": petrol_a2_close, "petrol_a2_sales": petrol_a2_sales,
        "hsd_c1_open": hsd_c1_open, "hsd_c1_close": hsd_c1_close, "hsd_c1_sales": hsd_c1_sales,
        "hsd_c2_open": hsd_c2_open, "hsd_c2_close": hsd_c2_close, "hsd_c2_sales": hsd_c2_sales,
        "hsd_b1_open": hsd_b1_open, "hsd_b1_close": hsd_b1_close, "hsd_b1_sales": hsd_b1_sales,
        "hsd_b2_open": hsd_b2_open, "hsd_b2_close": hsd_b2_close, "hsd_b2_sales": hsd_b2_sales,
        "xp_b3_open": xp_b3_open, "xp_b3_close": xp_b3_close, "xp_b3_sales": xp_b3_sales,
        "xp_b4_open": xp_b4_open, "xp_b4_close": xp_b4_close, "xp_b4_sales": xp_b4_sales,
        "test_b1": test_b1, "test_b2": test_b2, "test_b3": test_b3, "test_b4": test_b4,
        "petrol_rate": petrol_rate, "hsd_rate": hsd_rate, "xp_rate": xp_rate,
        "petrol_amount": petrol_amount, "hsd_amount": hsd_amount, "xp_amount": xp_amount,
        "gross_sales_amount": gross_sales_amount, "total_sales_amount": total_sales_amount,
        "paytm_amount": paytm_amount, "icici_amount": icici_amount, "fleet_card_amount": fleet_card_amount,
        "pump_expenses": pump_expenses, "pump_expenses_remark": pump_expenses_remark
    }
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(SALES_DATA_PATH, index=False)

    # Save employee shortages
    emp_df = pd.read_csv(EMPLOYEE_SHORTAGES_PATH)
    new_emp_id = emp_df["id"].max() + 1 if not emp_df.empty else 1
    for emp_name, shortage in employee_shortages.items():
        emp_data = {"id": new_emp_id, "date": str(selected_date), "employee_name": emp_name, "shortage_amount": shortage}
        emp_df = pd.concat([emp_df, pd.DataFrame([emp_data])], ignore_index=True)
        new_emp_id += 1
    emp_df.to_csv(EMPLOYEE_SHORTAGES_PATH, index=False)

    st.sidebar.success("Sales data saved successfully!")

def save_credit_debit_data():
    df = pd.read_csv(CREDIT_DEBIT_PATH)
    new_id = df["id"].max() + 1 if not df.empty else 1
    for t in transactions:
        data = {"id": new_id, "date": str(t["Date"]), "party": t["Party"], "type": t["Type"], "amount": t["Amount"]}
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        new_id += 1
    df.to_csv(CREDIT_DEBIT_PATH, index=False)
    st.sidebar.success("Credit/Debit data saved successfully!")

def save_owner_transactions():
    df = pd.read_csv(OWNER_TRANSACTIONS_PATH)
    new_id = df["id"].max() + 1 if not df.empty else 1
    for t in owner_transactions:
        data = {
            "id": new_id, "date": str(t["Date"]), "owner_name": t["Owner_Name"],
            "type": t["Type"], "mode": t["Mode"], "amount": t["Amount"], "remark": t["Remark"]
        }
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        new_id += 1
    df.to_csv(OWNER_TRANSACTIONS_PATH, index=False)
    st.sidebar.success("Owner transactions saved successfully!")

# Save Buttons
if st.sidebar.button("💾 Save Sales Data"):
    save_sales_data()
if st.sidebar.button("💾 Save Credit/Debit Data") and transactions:
    save_credit_debit_data()
if st.sidebar.button("💾 Save Owner Transactions") and owner_transactions:
    save_owner_transactions()

# Delete Data
st.sidebar.subheader("🗑️ Delete Saved Data")
delete_date = st.sidebar.date_input("📅 Select Date to Delete", value=today)
delete_option = st.sidebar.selectbox("Data to Delete", ["Sales Data", "Credit/Debit Data", "Owner Transactions", "Employee Shortages", "All"])
if st.sidebar.button("🗑️ Delete Selected Data"):
    delete_date_str = str(delete_date)
    
    if delete_option in ["Sales Data", "All"]:
        df = pd.read_csv(SALES_DATA_PATH)
        df = df[df["date"] != delete_date_str]
        df.to_csv(SALES_DATA_PATH, index=False)
    if delete_option in ["Credit/Debit Data", "All"]:
        df = pd.read_csv(CREDIT_DEBIT_PATH)
        df = df[df["date"] != delete_date_str]
        df.to_csv(CREDIT_DEBIT_PATH, index=False)
    if delete_option in ["Owner Transactions", "All"]:
        df = pd.read_csv(OWNER_TRANSACTIONS_PATH)
        df = df[df["date"] != delete_date_str]
        df.to_csv(OWNER_TRANSACTIONS_PATH, index=False)
    if delete_option in ["Employee Shortages", "All"]:
        df = pd.read_csv(EMPLOYEE_SHORTAGES_PATH)
        df = df[df["date"] != delete_date_str]
        df.to_csv(EMPLOYEE_SHORTAGES_PATH, index=False)
    
    st.sidebar.success(f"{delete_option} for {delete_date} deleted!")

# Load Data
def load_data():
    df = pd.read_csv(SALES_DATA_PATH)
    cd_df = pd.read_csv(CREDIT_DEBIT_PATH)
    owner_df = pd.read_csv(OWNER_TRANSACTIONS_PATH)
    emp_short_df = pd.read_csv(EMPLOYEE_SHORTAGES_PATH)
    
    df["Date"] = pd.to_datetime(df["date"])
    cd_df["Date"] = pd.to_datetime(cd_df["date"])
    owner_df["Date"] = pd.to_datetime(owner_df["date"])
    emp_short_df["Date"] = pd.to_datetime(emp_short_df["date"])
    
    return df.drop(columns=["date"]), cd_df.drop(columns=["date"]), owner_df.drop(columns=["date"]), emp_short_df.drop(columns=["date"])

# Dashboard
try:
    df, cd_df, owner_df, emp_short_df = load_data()
    
    # Filters
    st.sidebar.subheader("🔍 Dashboard Filters")
    date_range = st.sidebar.date_input("📅 Date Range", value=selected_date)
    if isinstance(date_range, tuple) and len(date_range) == 2 and date_range[0] != date_range[1]:
        mask = (df["Date"].dt.date >= date_range[0]) & (df["Date"].dt.date <= date_range[1])
        cd_mask = (cd_df["Date"].dt.date >= date_range[0]) & (cd_df["Date"].dt.date <= date_range[1])
        owner_mask = (owner_df["Date"].dt.date >= date_range[0]) & (owner_df["Date"].dt.date <= date_range[1])
        emp_mask = (emp_short_df["Date"].dt.date >= date_range[0]) & (emp_short_df["Date"].dt.date <= date_range[1])
        title_suffix = f" ({date_range[0]} to {date_range[1]})"
    else:
        mask = (df["Date"].dt.date == selected_date)
        cd_mask = (cd_df["Date"].dt.date == selected_date)
        owner_mask = (owner_df["Date"].dt.date == selected_date)
        emp_mask = (emp_short_df["Date"].dt.date == selected_date)
        title_suffix = f" ({selected_date})"
    
    filtered_df = df.loc[mask]
    filtered_cd_df = cd_df.loc[cd_mask]
    filtered_owner_df = owner_df.loc[owner_mask]
    filtered_emp_short_df = emp_short_df.loc[emp_mask]

    # Calculate Totals
    total_credit = filtered_cd_df[filtered_cd_df["type"] == "Credit"]["amount"].sum() if not filtered_cd_df.empty else 0
    total_debit = filtered_cd_df[filtered_cd_df["type"] == "Debit"]["amount"].sum() if not filtered_cd_df.empty else 0
    total_paytm = filtered_df["paytm_amount"].sum() if not filtered_df.empty else 0
    total_icici = filtered_df["icici_amount"].sum() if not filtered_df.empty else 0
    total_fleet_card = filtered_df["fleet_card_amount"].sum() if not filtered_df.empty else 0
    total_pump_expenses = filtered_df["pump_expenses"].sum() if not filtered_df.empty else 0
    total_employee_shortage = filtered_emp_short_df["shortage_amount"].sum() if not filtered_emp_short_df.empty else 0
    total_owner_debits = filtered_owner_df[filtered_owner_df["type"] == "Debit"]["amount"].sum() if not filtered_owner_df.empty else 0
    total_owner_credits = filtered_owner_df[filtered_owner_df["type"] == "Credit"]["amount"].sum() if not filtered_owner_df.empty else 0
    
    net_sales = filtered_df["total_sales_amount"].sum() + total_credit - total_debit
    net_cash = net_sales - total_paytm - total_icici - total_fleet_card - total_pump_expenses

    # Key Metrics
    st.markdown(f"<h2>📈 Key Metrics{title_suffix}</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        petrol_total = filtered_df[["petrol_c3_sales", "petrol_c4_sales", "petrol_a1_sales", "petrol_a2_sales"]].sum().sum()
        st.markdown(f"<div class='metric-box'><span class='metric-label'>⛽ Petrol Sold (L)</span><br><span class='metric-value' style='color: #e74c3c;'>{petrol_total:.2f}</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💰 Petrol Sales (₹)</span><br><span class='metric-value' style='color: #e74c3c;'>₹{filtered_df['petrol_amount'].sum():.2f}</span></div>", unsafe_allow_html=True)
    with col3:
        hsd_total = filtered_df[["hsd_c1_sales", "hsd_c2_sales", "hsd_b1_sales", "hsd_b2_sales"]].sum().sum()
        st.markdown(f"<div class='metric-box'><span class='metric-label'>⛽ HSD Sold (L)</span><br><span class='metric-value' style='color: #3498db;'>{hsd_total:.2f}</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💰 HSD Sales (₹)</span><br><span class='metric-value' style='color: #3498db;'>₹{filtered_df['hsd_amount'].sum():.2f}</span></div>", unsafe_allow_html=True)
    with col5:
        xp_total = filtered_df[["xp_b3_sales", "xp_b4_sales"]].sum().sum()
        st.markdown(f"<div class='metric-box'><span class='metric-label'>⛽ XP Sold (L)</span><br><span class='metric-value' style='color: #2ecc71;'>{xp_total:.2f}</span></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💰 XP Sales (₹)</span><br><span class='metric-value' style='color: #2ecc71;'>₹{filtered_df['xp_amount'].sum():.2f}</span></div>", unsafe_allow_html=True)

    col7, col8, col9, col10, col11, col12, col13, col14, col15 = st.columns(9)
    with col7:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💵 Gross Sales (₹)</span><br><span class='metric-value' style='color: #8e44ad;'>₹{filtered_df['gross_sales_amount'].sum():.2f}</span></div>", unsafe_allow_html=True)
    with col8:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>📉 Creditors (₹)</span><br><span class='metric-value' style='color: #e67e22;'>₹{total_credit:.2f}</span></div>", unsafe_allow_html=True)
    with col9:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>📈 Debtors (₹)</span><br><span class='metric-value' style='color: #27ae60;'>₹{total_debit:.2f}</span></div>", unsafe_allow_html=True)
    with col10:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💵 Net Sales (₹)</span><br><span class='metric-value' style='color: #8e44ad;'>₹{net_sales:.2f}</span></div>", unsafe_allow_html=True)
    with col11:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💳 Paytm (₹)</span><br><span class='metric-value' style='color: #f1c40f;'>₹{total_paytm:.2f}</span></div>", unsafe_allow_html=True)
    with col12:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💳 ICICI (₹)</span><br><span class='metric-value' style='color: #d35400;'>₹{total_icici:.2f}</span></div>", unsafe_allow_html=True)
    with col13:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>💳 Fleet Card (₹)</span><br><span class='metric-value' style='color: #16a085;'>₹{total_fleet_card:.2f}</span></div>", unsafe_allow_html=True)
    with col14:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>🛠️ Expenses (₹)</span><br><span class='metric-value' style='color: #c0392b;'>₹{total_pump_expenses:.2f}</span></div>", unsafe_allow_html=True)
    with col15:
        st.markdown(f"<div class='metric-box'><span class='metric-label'>👨‍💼 Shortage (₹)</span><br><span class='metric-value' style='color: #e74c3c;'>₹{total_employee_shortage:.2f}</span></div>", unsafe_allow_html=True)

    # Net Cash
    st.markdown(f"<h2>💰 Cash Flow{title_suffix}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-box'><span class='metric-label'>Net Cash Balance (₹)</span><br><span class='metric-value' style='color: #2980b9;'>₹{net_cash:.2f}</span></div>", unsafe_allow_html=True)

    # Owner's Transactions Summary
    with st.expander(f"👑 Owner's Transactions Summary{title_suffix}", expanded=False):
        if not filtered_owner_df.empty:
            owner_summary = filtered_owner_df.groupby(["owner_name", "type"])["amount"].sum().unstack(fill_value=0).reset_index()
            owner_summary["Net"] = owner_summary.get("Credit", 0) - owner_summary.get("Debit", 0)

            st.subheader("🔍 Filter Owner Transactions")
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            with col_filter1:
                owner_filter = st.text_input("Filter by Owner Name", "")
            with col_filter2:
                mode_filter = st.multiselect("Filter by Mode", ["Online", "Cheque", "Cash"], default=["Online", "Cheque", "Cash"])
            with col_filter3:
                type_filter = st.multiselect("Filter by Type", ["Debit", "Credit"], default=["Debit", "Credit"])

            filtered_owner_display = filtered_owner_df.copy()
            if owner_filter:
                filtered_owner_display = filtered_owner_display[filtered_owner_display["owner_name"].str.contains(owner_filter, case=False, na=False)]
            if mode_filter:
                filtered_owner_display = filtered_owner_display[filtered_owner_display["mode"].isin(mode_filter)]
            if type_filter:
                filtered_owner_display = filtered_owner_display[filtered_owner_display["type"].isin(type_filter)]

            st.dataframe(
                filtered_owner_display.style.format({"amount": "₹{:.2f}"})
                .set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd', 'text-align': 'center', 'color': '#2c3e50'}),
                use_container_width=True
            )
            st.write("Summary by Owner:")
            st.dataframe(
                owner_summary.style.format({"Debit": "₹{:.2f}", "Credit": "₹{:.2f}", "Net": "₹{:.2f}"})
                .set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd', 'text-align': 'center', 'color': '#2c3e50'}),
                use_container_width=True
            )
            st.markdown(f"<div class='metric-box'><span class='metric-label'>👑 Total Owner Balance (₹)</span><br><span class='metric-value' style='color: #9b59b6;'>₹{total_owner_credits - total_owner_debits:.2f}</span></div>", unsafe_allow_html=True)
        else:
            st.write("No owner transactions available.")

    # Employee-wise Shortage Breakdown
    with st.expander(f"👨‍💼 Employee-wise Shortage Breakdown", expanded=False):
        if not filtered_emp_short_df.empty:
            st.subheader("📅 Select Month for Shortage Analysis")
            col_month, col_year = st.columns(2)
            with col_month:
                month = st.selectbox("Month", list(range(1, 13)), index=today.month-1, format_func=lambda x: datetime(2000, x, 1).strftime("%B"))
            with col_year:
                year = st.number_input("Year", min_value=2000, max_value=today.year, value=today.year, step=1)

            monthly_mask = (emp_short_df["Date"].dt.month == month) & (emp_short_df["Date"].dt.year == year)
            monthly_df = emp_short_df.loc[monthly_mask]
            if not monthly_df.empty:
                shortage_data = monthly_df.groupby("employee_name")["shortage_amount"].sum().reset_index()
                shortage_df = pd.DataFrame(shortage_data, columns=["employee_name", "shortage_amount"]).rename(columns={"employee_name": "Employee", "shortage_amount": "Shortage (₹)"})

                st.subheader("🔍 Filter Employee Shortage Data")
                col_filter1, col_filter2, col_filter3 = st.columns(3)
                with col_filter1:
                    emp_filter = st.text_input("Filter by Employee Name", "")
                with col_filter2:
                    shortage_min = st.number_input("Min Shortage (₹)", value=None, placeholder="Leave blank for no min")
                with col_filter3:
                    shortage_max = st.number_input("Max Shortage (₹)", value=None, placeholder="Leave blank for no max")

                filtered_shortage_df = shortage_df.copy()
                if emp_filter:
                    filtered_shortage_df = filtered_shortage_df[filtered_shortage_df["Employee"].str.contains(emp_filter, case=False, na=False)]
                if shortage_min is not None:
                    filtered_shortage_df = filtered_shortage_df[filtered_shortage_df["Shortage (₹)"] >= shortage_min]
                if shortage_max is not None:
                    filtered_shortage_df = filtered_shortage_df[filtered_shortage_df["Shortage (₹)"] <= shortage_max]

                st.markdown(f"### Total Shortages for {datetime(2000, month, 1).strftime('%B')} {year}")
                st.dataframe(
                    filtered_shortage_df.style.format({"Shortage (₹)": "₹{:.2f}"})
                    .set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd', 'text-align': 'center', 'color': '#2c3e50'}),
                    use_container_width=True
                )
            else:
                st.write(f"No shortage data available for {datetime(2000, month, 1).strftime('%B')} {year}.")
        else:
            st.write("No employee-wise shortage data available.")

    # Party-wise Credit/Debit Summary
    with st.expander(f"🤝 Party-wise Credit/Debit Summary{title_suffix}", expanded=False):
        if not filtered_cd_df.empty:
            party_summary = filtered_cd_df.groupby(["party", "type"])["amount"].sum().unstack(fill_value=0)
            party_summary["Net"] = party_summary.get("Credit", 0) - party_summary.get("Debit", 0)
            party_summary = party_summary.reset_index()

            st.subheader("🔍 Filter Party Data")
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
            with col_filter1:
                party_filter = st.text_input("Filter by Party Name", "")
            with col_filter2:
                credit_min = st.number_input("Min Credit (₹)", value=None, placeholder="Leave blank for no min")
                credit_max = st.number_input("Max Credit (₹)", value=None, placeholder="Leave blank for no max")
            with col_filter3:
                debit_min = st.number_input("Min Debit (₹)", value=None, placeholder="Leave blank for no min")
                debit_max = st.number_input("Max Debit (₹)", value=None, placeholder="Leave blank for no max")
            with col_filter4:
                net_min = st.number_input("Min Net (₹)", value=None, placeholder="Leave blank for no min")
                net_max = st.number_input("Max Net (₹)", value=None, placeholder="Leave blank for no max")

            filtered_party_summary = party_summary.copy()
            if party_filter:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["party"].str.contains(party_filter, case=False, na=False)]
            if credit_min is not None:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["Credit"] >= credit_min]
            if credit_max is not None:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["Credit"] <= credit_max]
            if debit_min is not None:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["Debit"] >= debit_min]
            if debit_max is not None:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["Debit"] <= debit_max]
            if net_min is not None:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["Net"] >= net_min]
            if net_max is not None:
                filtered_party_summary = filtered_party_summary[filtered_party_summary["Net"] <= net_max]

            st.dataframe(
                filtered_party_summary.style.format({"Credit": "₹{:.2f}", "Debit": "₹{:.2f}", "Net": "₹{:.2f}"})
                .set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd', 'text-align': 'center', 'color': '#2c3e50'}),
                use_container_width=True
            )
        else:
            st.write("No party-wise credit/debit data available.")

    # Visualizations
    st.markdown(f"<h2>📊 Visualizations{title_suffix}</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 Sales Trend", "🚗 Nozzle Breakdown", "🍰 Fuel Distribution", 
                                                        "💳 Credit/Debit Trend", "🤝 Party-wise Credit/Debit", 
                                                        "👨‍💼 Shortage Breakdown", "👑 Owner Transactions"])

    with tab1:
        if len(filtered_df) > 1:
            chart_data = filtered_df.groupby("Date")[["petrol_amount", "hsd_amount", "xp_amount"]].sum()
            fig_trend = px.line(chart_data, title=f"Daily Sales Trend{title_suffix}", labels={"value": "Amount (₹)", "Date": "Date"},
                                color_discrete_map={"petrol_amount": "#e74c3c", "hsd_amount": "#3498db", "xp_amount": "#2ecc71"})
            fig_trend.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.write(f"No trend available for single day {selected_date}.")

    with tab2:
        nozzle_data = pd.DataFrame({
            "Nozzle": ["C3", "C4", "A1", "A2", "C1", "C2", "B1", "B2", "B3", "B4"],
            "Sales": [filtered_df[f"petrol_{n.lower()}_sales"].sum() if n in ["C3", "C4", "A1", "A2"] else 
                      filtered_df[f"hsd_{n.lower()}_sales"].sum() if n in ["C1", "C2", "B1", "B2"] else 
                      filtered_df[f"xp_{n.lower()}_sales"].sum() for n in ["C3", "C4", "A1", "A2", "C1", "C2", "B1", "B2", "B3", "B4"]],
            "Fuel": ["Petrol"]*4 + ["HSD"]*4 + ["XP"]*2
        })
        fig_nozzle = px.bar(nozzle_data, x="Nozzle", y="Sales", color="Fuel", title=f"Sales by Nozzle{title_suffix}",
                            color_discrete_map={"Petrol": "#e74c3c", "HSD": "#3498db", "XP": "#2ecc71"})
        fig_nozzle.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
        st.plotly_chart(fig_nozzle, use_container_width=True)

    with tab3:
        fuel_dist = [filtered_df["petrol_amount"].sum(), filtered_df["hsd_amount"].sum(), filtered_df["xp_amount"].sum()]
        fig_dist = px.pie(values=fuel_dist, names=["Petrol", "HSD", "XP"], title=f"Revenue Distribution{title_suffix}",
                          color_discrete_map={"Petrol": "#e74c3c", "HSD": "#3498db", "XP": "#2ecc71"})
        fig_dist.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
        st.plotly_chart(fig_dist, use_container_width=True)

    with tab4:
        if not filtered_cd_df.empty and len(filtered_cd_df) > 1:
            credit_debit_data = filtered_cd_df.groupby("Date")[["amount"]].sum().rename(columns={"amount": "Total"})
            credit_debit_data["Credit"] = filtered_cd_df[filtered_cd_df["type"] == "Credit"].groupby("Date")["amount"].sum()
            credit_debit_data["Debit"] = filtered_cd_df[filtered_cd_df["type"] == "Debit"].groupby("Date")["amount"].sum()
            credit_debit_data.fillna(0, inplace=True)
            fig_cd = px.line(credit_debit_data, title=f"Credit/Debit Trend{title_suffix}", labels={"value": "Amount (₹)", "Date": "Date"},
                             color_discrete_map={"Total": "#8e44ad", "Credit": "#e67e22", "Debit": "#27ae60"})
            fig_cd.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
            st.plotly_chart(fig_cd, use_container_width=True)
        else:
            st.write(f"No credit/debit trend available for {selected_date}.")

    with tab5:
        if not filtered_cd_df.empty:
            party_summary = filtered_cd_df.groupby(["party", "type"])["amount"].sum().unstack(fill_value=0)
            party_summary["Net"] = party_summary.get("Credit", 0) - party_summary.get("Debit", 0)
            fig_party = px.bar(party_summary.reset_index(), x="party", y=["Credit", "Debit"], barmode="group",
                               title=f"Party-wise Credit vs Debit{title_suffix}",
                               color_discrete_map={"Credit": "#e67e22", "Debit": "#27ae60"})
            fig_party.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
            st.plotly_chart(fig_party, use_container_width=True)
        else:
            st.write(f"No party-wise credit/debit data available for {selected_date}.")

    with tab6:
        if not filtered_emp_short_df.empty:
            monthly_mask = (emp_short_df["Date"].dt.month == month) & (emp_short_df["Date"].dt.year == year)
            monthly_df = emp_short_df.loc[monthly_mask]
            if not monthly_df.empty:
                shortage_data = monthly_df.groupby("employee_name")["shortage_amount"].sum().reset_index()
                shortage_df = pd.DataFrame(shortage_data, columns=["employee_name", "shortage_amount"]).rename(columns={"employee_name": "Employee", "shortage_amount": "Shortage (₹)"})
                filtered_shortage_df = shortage_df.copy()
                if emp_filter:
                    filtered_shortage_df = filtered_shortage_df[filtered_shortage_df["Employee"].str.contains(emp_filter, case=False, na=False)]
                if shortage_min is not None:
                    filtered_shortage_df = filtered_shortage_df[filtered_shortage_df["Shortage (₹)"] >= shortage_min]
                if shortage_max is not None:
                    filtered_shortage_df = filtered_shortage_df[filtered_shortage_df["Shortage (₹)"] <= shortage_max]
                
                fig_shortage = px.bar(
                    filtered_shortage_df, x="Employee", y="Shortage (₹)", 
                    title=f"Employee-wise Shortage Breakdown for {datetime(2000, month, 1).strftime('%B')} {year}",
                    color_discrete_sequence=["#e74c3c"]
                )
                fig_shortage.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
                st.plotly_chart(fig_shortage, use_container_width=True)
            else:
                st.write(f"No shortage data available for {datetime(2000, month, 1).strftime('%B')} {year}.")
        else:
            st.write("No employee-wise shortage data available.")

    with tab7:
        if not filtered_owner_df.empty:
            fig_owner = px.bar(
                filtered_owner_df, x="Date", y="amount", color="type", facet_col="mode",
                title=f"Owner's Transactions{title_suffix}",
                color_discrete_map={"Debit": "#9b59b6", "Credit": "#1abc9c"},
                text=filtered_owner_df["owner_name"] + " (" + filtered_owner_df["remark"] + ")"
            )
            fig_owner.update_traces(textposition='auto')
            fig_owner.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(size=12, color="#2c3e50"))
            st.plotly_chart(fig_owner, use_container_width=True)
        else:
            st.write(f"No owner transactions available for {selected_date}.")

    # Detailed Data
    st.markdown(f"<h2>📋 Detailed Records{title_suffix}</h2>", unsafe_allow_html=True)
    st.subheader("Sales Records")
    st.dataframe(filtered_df.style.set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd'}))
    st.subheader("Credit/Debit Records")
    st.dataframe(filtered_cd_df.style.set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd'}))
    st.subheader("Owner Transactions")
    st.dataframe(filtered_owner_df.style.set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd'}))
    st.subheader("Employee Shortages")
    st.dataframe(filtered_emp_short_df.style.set_properties(**{'background-color': '#ffffff', 'border': '1px solid #ddd'}))

    # Download Buttons
    col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
    with col_dl1:
        st.download_button(label="📥 Download Sales Data", data=filtered_df.to_csv(index=False), file_name=f"sales_data_{selected_date}.csv", mime="text/csv")
    with col_dl2:
        st.download_button(label="📥 Download Credit/Debit Data", data=filtered_cd_df.to_csv(index=False), file_name=f"credit_debit_data_{selected_date}.csv", mime="text/csv")
    with col_dl3:
        st.download_button(label="📥 Download Owner Transactions", data=filtered_owner_df.to_csv(index=False), file_name=f"owner_transactions_{selected_date}.csv", mime="text/csv")
    with col_dl4:
        st.download_button(label="📥 Download Employee Shortages", data=filtered_emp_short_df.to_csv(index=False), file_name=f"employee_shortages_{selected_date}.csv", mime="text/csv")

except Exception as e:
    st.warning(f"No data available yet or error occurred: {str(e)}. Please enter data using the sidebar.")

# Footer
st.markdown("<hr><p style='text-align: center; color: #7f8c8d;'>Powered by xAI | Designed for Petrol Pump Management</p>", unsafe_allow_html=True)

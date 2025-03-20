import streamlit as st
import pandas as pd
from datetime import date
import os
import time

# Set page config
st.set_page_config(layout="wide", page_title="Petrol Pump Dashboard", page_icon="⛽")

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #f8f9fa; padding: 20px;}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif; font-size: 2.5rem; text-align: center;}
    h2 {color: #34495e; font-family: 'Arial', sans-serif; font-size: 1.8rem;}
    .stButton>button {
        background-color: #4CAF50; color: white; border-radius: 8px; padding: 10px 20px; font-size: 1rem;
        border: none; cursor: pointer; transition: background-color 0.3s;
    }
    .stButton>button:hover {background-color: #45a049;}
    .delete-button {background-color: #e74c3c !important;}
    .delete-button:hover {background-color: #c0392b !important;}
    .metric-box {
        border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 10px 0; text-align: center;
    }
    .metric-label {font-size: 1rem; color: #666; font-weight: 500;}
    .metric-value {font-size: 1.8rem; font-weight: bold; margin-top: 5px;}
    </style>
""", unsafe_allow_html=True)

# File paths
SALES_DATA_PATH = "petrol_sales.csv"
PARTY_LEDGER_PATH = "party_ledger.csv"
EMPLOYEE_SHORTAGE_PATH = "employee_shortage.csv"
OWNERS_TRANSACTION_PATH = "owners_transaction.csv"

# Initialize CSVs
def init_csv():
    if not os.path.exists(SALES_DATA_PATH):
        pd.DataFrame(columns=[
            "id", "date",
            "petrol_c3_open", "petrol_c3_close", "petrol_c3_sales",
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
            "pump_expenses", "pump_expenses_remark",
            "cash_in", "cash_out", "net_cash", "credit_balance"
        ]).to_csv(SALES_DATA_PATH, index=False)
    if not os.path.exists(PARTY_LEDGER_PATH):
        pd.DataFrame(columns=["id", "date", "party_name", "credit_amount", "debit_amount"]).to_csv(PARTY_LEDGER_PATH, index=False)
    if not os.path.exists(EMPLOYEE_SHORTAGE_PATH):
        pd.DataFrame(columns=["id", "date", "employee_name", "shortage_amount"]).to_csv(EMPLOYEE_SHORTAGE_PATH, index=False)
    if not os.path.exists(OWNERS_TRANSACTION_PATH):
        pd.DataFrame(columns=["id", "date", "owner_name", "amount", "mode", "type"]).to_csv(OWNERS_TRANSACTION_PATH, index=False)

init_csv()

# Load Sales Data
def load_sales_data():
    try:
        df = pd.read_csv(SALES_DATA_PATH)
        df["Date"] = pd.to_datetime(df["date"], errors='coerce')
        required_columns = ["cash_in", "cash_out", "net_cash", "credit_balance"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0.0
        st.sidebar.write(f"Loaded {SALES_DATA_PATH} - Rows: {len(df)}")
        return df
    except Exception as e:
        st.error(f"Sales Load Error: {str(e)}")
        return pd.DataFrame(columns=[
            "id", "date",
            "petrol_c3_open", "petrol_c3_close", "petrol_c3_sales",
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
            "pump_expenses", "pump_expenses_remark",
            "cash_in", "cash_out", "net_cash", "credit_balance", "Date"
        ])

# Load Party Ledger
def load_party_ledger():
    try:
        df = pd.read_csv(PARTY_LEDGER_PATH)
        df["Date"] = pd.to_datetime(df["date"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Party Ledger Load Error: {str(e)}")
        return pd.DataFrame(columns=["id", "date", "party_name", "credit_amount", "debit_amount", "Date"])

# Load Employee Shortage
def load_employee_shortage():
    try:
        df = pd.read_csv(EMPLOYEE_SHORTAGE_PATH)
        df["Date"] = pd.to_datetime(df["date"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Employee Shortage Load Error: {str(e)}")
        return pd.DataFrame(columns=["id", "date", "employee_name", "shortage_amount", "Date"])

# Load Owner's Transactions
def load_owners_transactions():
    try:
        df = pd.read_csv(OWNERS_TRANSACTION_PATH)
        df["Date"] = pd.to_datetime(df["date"], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Owner's Transaction Load Error: {str(e)}")
        return pd.DataFrame(columns=["id", "date", "owner_name", "amount", "mode", "type", "Date"])

# Save Sales Data
def save_sales_data(selected_date, data_dict):
    df = load_sales_data()
    new_id = df["id"].max() + 1 if not df.empty else 1
    
    petrol_c3_sales = data_dict["petrol_c3_close"] - data_dict["petrol_c3_open"]
    petrol_c4_sales = data_dict["petrol_c4_close"] - data_dict["petrol_c4_open"]
    petrol_a1_sales = data_dict["petrol_a1_close"] - data_dict["petrol_a1_open"]
    petrol_a2_sales = data_dict["petrol_a2_close"] - data_dict["petrol_a2_open"]
    hsd_c1_sales = data_dict["hsd_c1_close"] - data_dict["hsd_c1_open"]
    hsd_c2_sales = data_dict["hsd_c2_close"] - data_dict["hsd_c2_open"]
    hsd_b1_sales = data_dict["hsd_b1_close"] - data_dict["hsd_b1_open"]
    hsd_b2_sales = data_dict["hsd_b2_close"] - data_dict["hsd_b2_open"]
    xp_b3_sales = data_dict["xp_b3_close"] - data_dict["xp_b3_open"]
    xp_b4_sales = data_dict["xp_b4_close"] - data_dict["xp_b4_open"]
    
    petrol_amount = (petrol_c3_sales + petrol_c4_sales + petrol_a1_sales + petrol_a2_sales) * data_dict["petrol_rate"]
    hsd_amount = (hsd_c1_sales + hsd_c2_sales + hsd_b1_sales + hsd_b2_sales) * data_dict["hsd_rate"]
    xp_amount = (xp_b3_sales + xp_b4_sales) * data_dict["xp_rate"]
    
    gross_sales_amount = petrol_amount + hsd_amount + xp_amount
    total_sales_amount = gross_sales_amount - (data_dict["paytm_amount"] + data_dict["icici_amount"] + data_dict["fleet_card_amount"] + data_dict["pump_expenses"])
    
    cash_in = data_dict["paytm_amount"] + data_dict["icici_amount"] + data_dict["fleet_card_amount"]
    cash_out = data_dict["pump_expenses"]
    net_cash = cash_in - cash_out
    credit_balance = total_sales_amount - cash_in
    
    new_row = pd.DataFrame({
        "id": [new_id], "date": [str(selected_date)],
        "petrol_c3_open": [data_dict["petrol_c3_open"]], "petrol_c3_close": [data_dict["petrol_c3_close"]], "petrol_c3_sales": [petrol_c3_sales],
        "petrol_c4_open": [data_dict["petrol_c4_open"]], "petrol_c4_close": [data_dict["petrol_c4_close"]], "petrol_c4_sales": [petrol_c4_sales],
        "petrol_a1_open": [data_dict["petrol_a1_open"]], "petrol_a1_close": [data_dict["petrol_a1_close"]], "petrol_a1_sales": [petrol_a1_sales],
        "petrol_a2_open": [data_dict["petrol_a2_open"]], "petrol_a2_close": [data_dict["petrol_a2_close"]], "petrol_a2_sales": [petrol_a2_sales],
        "hsd_c1_open": [data_dict["hsd_c1_open"]], "hsd_c1_close": [data_dict["hsd_c1_close"]], "hsd_c1_sales": [hsd_c1_sales],
        "hsd_c2_open": [data_dict["hsd_c2_open"]], "hsd_c2_close": [data_dict["hsd_c2_close"]], "hsd_c2_sales": [hsd_c2_sales],
        "hsd_b1_open": [data_dict["hsd_b1_open"]], "hsd_b1_close": [data_dict["hsd_b1_close"]], "hsd_b1_sales": [hsd_b1_sales],
        "hsd_b2_open": [data_dict["hsd_b2_open"]], "hsd_b2_close": [data_dict["hsd_b2_close"]], "hsd_b2_sales": [hsd_b2_sales],
        "xp_b3_open": [data_dict["xp_b3_open"]], "xp_b3_close": [data_dict["xp_b3_close"]], "xp_b3_sales": [xp_b3_sales],
        "xp_b4_open": [data_dict["xp_b4_open"]], "xp_b4_close": [data_dict["xp_b4_close"]], "xp_b4_sales": [xp_b4_sales],
        "test_b1": [data_dict["test_b1"]], "test_b2": [data_dict["test_b2"]],
        "test_b3": [data_dict["test_b3"]], "test_b4": [data_dict["test_b4"]],
        "petrol_rate": [data_dict["petrol_rate"]], "hsd_rate": [data_dict["hsd_rate"]], "xp_rate": [data_dict["xp_rate"]],
        "petrol_amount": [petrol_amount], "hsd_amount": [hsd_amount], "xp_amount": [xp_amount],
        "gross_sales_amount": [gross_sales_amount], "total_sales_amount": [total_sales_amount],
        "paytm_amount": [data_dict["paytm_amount"]], "icici_amount": [data_dict["icici_amount"]],
        "fleet_card_amount": [data_dict["fleet_card_amount"]], "pump_expenses": [data_dict["pump_expenses"]],
        "pump_expenses_remark": [data_dict["pump_expenses_remark"]],
        "cash_in": [cash_in], "cash_out": [cash_out], "net_cash": [net_cash], "credit_balance": [credit_balance]
    })
    df = pd.concat([df.drop(columns=["Date"]), new_row], ignore_index=True)
    df.to_csv(SALES_DATA_PATH, index=False)
    st.sidebar.success(f"Saved Sales! Rows now: {len(df)}")
    st.rerun()

# Save Party Ledger Entry
def save_party_ledger(selected_date, party_name, credit_amount, debit_amount):
    df = load_party_ledger()
    new_id = df["id"].max() + 1 if not df.empty else 1
    new_row = pd.DataFrame({
        "id": [new_id], "date": [str(selected_date)],
        "party_name": [party_name], "credit_amount": [credit_amount], "debit_amount": [debit_amount]
    })
    df = pd.concat([df.drop(columns=["Date"]), new_row], ignore_index=True)
    df.to_csv(PARTY_LEDGER_PATH, index=False)
    st.sidebar.success(f"Saved Party Ledger! Rows now: {len(df)}")
    st.rerun()

# Save Employee Shortage
def save_employee_shortage(selected_date, employee_name, shortage_amount):
    df = load_employee_shortage()
    new_id = df["id"].max() + 1 if not df.empty else 1
    new_row = pd.DataFrame({
        "id": [new_id], "date": [str(selected_date)],
        "employee_name": [employee_name], "shortage_amount": [shortage_amount]
    })
    df = pd.concat([df.drop(columns=["Date"]), new_row], ignore_index=True)
    df.to_csv(EMPLOYEE_SHORTAGE_PATH, index=False)
    st.sidebar.success(f"Saved Employee Shortage! Rows now: {len(df)}")
    st.rerun()

# Save Owner's Transaction
def save_owners_transaction(selected_date, owner_name, amount, mode, transaction_type):
    df = load_owners_transactions()
    new_id = df["id"].max() + 1 if not df.empty else 1
    new_row = pd.DataFrame({
        "id": [new_id], "date": [str(selected_date)],
        "owner_name": [owner_name], "amount": [amount], "mode": [mode], "type": [transaction_type]
    })
    df = pd.concat([df.drop(columns=["Date"]), new_row], ignore_index=True)
    df.to_csv(OWNERS_TRANSACTION_PATH, index=False)
    st.sidebar.success(f"Saved Owner's Transaction! Rows now: {len(df)}")
    st.rerun()

# Delete Sales Data
def delete_sales_data(start_date, end_date):
    try:
        df = pd.read_csv(SALES_DATA_PATH)
        if df.empty:
            st.sidebar.write("No sales data to delete")
            return 0
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
        st.sidebar.write(f"Before deletion - Rows: {len(df)}")
        mask = (df["date"].dt.date < start_date) | (df["date"].dt.date > end_date)
        updated_df = df[mask]
        st.sidebar.write(f"After filter (deleting {start_date} to {end_date}) - Rows: {len(updated_df)}")
        updated_df.to_csv(SALES_DATA_PATH, index=False)
        return len(df) - len(updated_df)
    except Exception as e:
        st.sidebar.error(f"Delete Error: {str(e)}")
        return 0

# Title
st.markdown("<h1>⛽ Petrol Pump Dashboard</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Data Entry")
today = date.today()
selected_date = st.sidebar.date_input("📅 Select Date", value=today)

st.sidebar.subheader("⛽ Petrol Meter Readings (Liters)")
petrol_c3_open = st.sidebar.number_input("C3 Opening", min_value=0.0, step=0.1)
petrol_c3_close = st.sidebar.number_input("C3 Closing", min_value=petrol_c3_open, step=0.1)
petrol_c4_open = st.sidebar.number_input("C4 Opening", min_value=0.0, step=0.1)
petrol_c4_close = st.sidebar.number_input("C4 Closing", min_value=petrol_c4_open, step=0.1)
petrol_a1_open = st.sidebar.number_input("A1 Opening", min_value=0.0, step=0.1)
petrol_a1_close = st.sidebar.number_input("A1 Closing", min_value=petrol_a1_open, step=0.1)
petrol_a2_open = st.sidebar.number_input("A2 Opening", min_value=0.0, step=0.1)
petrol_a2_close = st.sidebar.number_input("A2 Closing", min_value=petrol_a2_open, step=0.1)

st.sidebar.subheader("🚛 HSD Meter Readings (Liters)")
hsd_c1_open = st.sidebar.number_input("C1 Opening (HSD)", min_value=0.0, step=0.1)
hsd_c1_close = st.sidebar.number_input("C1 Closing (HSD)", min_value=hsd_c1_open, step=0.1)
hsd_c2_open = st.sidebar.number_input("C2 Opening (HSD)", min_value=0.0, step=0.1)
hsd_c2_close = st.sidebar.number_input("C2 Closing (HSD)", min_value=hsd_c2_open, step=0.1)
hsd_b1_open = st.sidebar.number_input("B1 Opening (HSD)", min_value=0.0, step=0.1)
hsd_b1_close = st.sidebar.number_input("B1 Closing (HSD)", min_value=hsd_b1_open, step=0.1)
hsd_b2_open = st.sidebar.number_input("B2 Opening (HSD)", min_value=0.0, step=0.1)
hsd_b2_close = st.sidebar.number_input("B2 Closing (HSD)", min_value=hsd_b2_open, step=0.1)

st.sidebar.subheader("⚡ XP Meter Readings (Liters)")
xp_b3_open = st.sidebar.number_input("B3 Opening (XP)", min_value=0.0, step=0.1)
xp_b3_close = st.sidebar.number_input("B3 Closing (XP)", min_value=xp_b3_open, step=0.1)
xp_b4_open = st.sidebar.number_input("B4 Opening (XP)", min_value=0.0, step=0.1)
xp_b4_close = st.sidebar.number_input("B4 Closing (XP)", min_value=xp_b4_open, step=0.1)

st.sidebar.subheader("🛢️ Oil Sales (Liters)")
test_b1 = st.sidebar.number_input("Test B1", min_value=0.0, step=0.1, value=0.0)
test_b2 = st.sidebar.number_input("Test B2", min_value=0.0, step=0.1, value=0.0)
test_b3 = st.sidebar.number_input("Test B3", min_value=0.0, step=0.1, value=0.0)
test_b4 = st.sidebar.number_input("Test B4", min_value=0.0, step=0.1, value=0.0)

st.sidebar.subheader("💰 Rates (₹/L)")
petrol_rate = st.sidebar.number_input("Petrol Rate", min_value=0.0, step=0.01, value=104.62)
hsd_rate = st.sidebar.number_input("HSD Rate", min_value=0.0, step=0.01, value=91.16)
xp_rate = st.sidebar.number_input("XP Rate", min_value=0.0, step=0.01, value=111.57)

st.sidebar.subheader("💳 Payment Transactions (₹)")
paytm_amount = st.sidebar.number_input("Paytm Amount", min_value=0.0, step=0.1, value=0.0)
icici_amount = st.sidebar.number_input("ICICI Amount", min_value=0.0, step=0.1, value=0.0)
fleet_card_amount = st.sidebar.number_input("Fleet Card Amount", min_value=0.0, step=0.1, value=0.0)

st.sidebar.subheader("🛠️ Pump Expenses (₹)")
pump_expenses = st.sidebar.number_input("Pump Expenses", min_value=0.0, step=0.1, value=0.0)
pump_expenses_remark = st.sidebar.text_input("Expenses Remark", value="")

if st.sidebar.button("💾 Save Sales"):
    data_dict = {
        "petrol_c3_open": petrol_c3_open, "petrol_c3_close": petrol_c3_close,
        "petrol_c4_open": petrol_c4_open, "petrol_c4_close": petrol_c4_close,
        "petrol_a1_open": petrol_a1_open, "petrol_a1_close": petrol_a1_close,
        "petrol_a2_open": petrol_a2_open, "petrol_a2_close": petrol_a2_close,
        "hsd_c1_open": hsd_c1_open, "hsd_c1_close": hsd_c1_close,
        "hsd_c2_open": hsd_c2_open, "hsd_c2_close": hsd_c2_close,
        "hsd_b1_open": hsd_b1_open, "hsd_b1_close": hsd_b1_close,
        "hsd_b2_open": hsd_b2_open, "hsd_b2_close": hsd_b2_close,
        "xp_b3_open": xp_b3_open, "xp_b3_close": xp_b3_close,
        "xp_b4_open": xp_b4_open, "xp_b4_close": xp_b4_close,
        "test_b1": test_b1, "test_b2": test_b2, "test_b3": test_b3, "test_b4": test_b4,
        "petrol_rate": petrol_rate, "hsd_rate": hsd_rate, "xp_rate": xp_rate,
        "paytm_amount": paytm_amount, "icici_amount": icici_amount,
        "fleet_card_amount": fleet_card_amount, "pump_expenses": pump_expenses,
        "pump_expenses_remark": pump_expenses_remark
    }
    save_sales_data(selected_date, data_dict)

# Party Ledger Entry
st.sidebar.subheader("📒 Party Ledger")
party_name = st.sidebar.text_input("Party Name")
party_credit = st.sidebar.number_input("Credit Amount (₹)", min_value=0.0, step=0.1, value=0.0)
party_debit = st.sidebar.number_input("Debit Amount (₹)", min_value=0.0, step=0.1, value=0.0)
if st.sidebar.button("💾 Save Party Transaction"):
    save_party_ledger(selected_date, party_name, party_credit, party_debit)

# Employee Shortage Entry
st.sidebar.subheader("👷 Employee Shortage")
employee_name = st.sidebar.text_input("Employee Name")
shortage_amount = st.sidebar.number_input("Shortage Amount (₹)", min_value=0.0, step=0.1, value=0.0)
if st.sidebar.button("💾 Save Shortage"):
    save_employee_shortage(selected_date, employee_name, shortage_amount)

# Owner's Transaction Entry
st.sidebar.subheader("👑 Owner’s Transaction")
owner_name = st.sidebar.text_input("Owner Name")
owner_amount = st.sidebar.number_input("Amount (₹)", min_value=0.0, step=0.1, value=0.0)
owner_mode = st.sidebar.selectbox("Mode of Transaction", ["Online", "Cheque", "Cash"])
owner_type = st.sidebar.selectbox("Type", ["Credit", "Debit"])
if st.sidebar.button("💾 Save Owner Transaction"):
    save_owners_transaction(selected_date, owner_name, owner_amount, owner_mode, owner_type)

# Delete Section
st.sidebar.subheader("🗑️ Delete Sales Data")
delete_range = st.sidebar.date_input("📅 Delete Range", value=[today, today], key="delete_range")
if len(delete_range) == 2:
    start_date, end_date = delete_range
    confirm_delete = st.sidebar.checkbox("Confirm Deletion", value=False)
    if st.sidebar.button("🗑️ Delete", type="primary"):
        if confirm_delete:
            deleted_rows = delete_sales_data(start_date, end_date)
            st.sidebar.success(f"Deleted {deleted_rows} rows!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.sidebar.write("Please check 'Confirm Deletion' to proceed.")

# Load and Display Data
sales_df = load_sales_data()
party_df = load_party_ledger()
shortage_df = load_employee_shortage()
owners_df = load_owners_transactions()

if sales_df.empty and party_df.empty and shortage_df.empty and owners_df.empty:
    st.warning("No data available.")
else:
    # Filter Data
    date_range = st.sidebar.date_input("📅 Filter Range", value=[today, today], key="filter_range")
    if len(date_range) == 2:
        start_date, end_date = date_range
        sales_mask = (sales_df["Date"].dt.date >= start_date) & (sales_df["Date"].dt.date <= end_date)
        party_mask = (party_df["Date"].dt.date >= start_date) & (party_df["Date"].dt.date <= end_date)
        shortage_mask = (shortage_df["Date"].dt.date >= start_date) & (shortage_df["Date"].dt.date <= end_date)
        owners_mask = (owners_df["Date"].dt.date >= start_date) & (owners_df["Date"].dt.date <= end_date)
        title_suffix = f" ({start_date} to {end_date})"
    else:
        start_date = today
        sales_mask = (sales_df["Date"].dt.date == start_date)
        party_mask = (party_df["Date"].dt.date == start_date)
        shortage_mask = (shortage_df["Date"].dt.date == start_date)
        owners_mask = (owners_df["Date"].dt.date == start_date)
        title_suffix = f" ({start_date})"
    
    filtered_sales_df = sales_df.loc[sales_mask]
    filtered_party_df = party_df.loc[party_mask]
    filtered_shortage_df = shortage_df.loc[shortage_mask]
    filtered_owners_df = owners_df.loc[owners_mask]

    if filtered_sales_df.empty:
        st.warning("No sales data in selected range.")
    else:
        # Sales Metrics
        st.markdown(f"<h2>📈 Key Metrics{title_suffix}</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            petrol_sales_l = filtered_sales_df[["petrol_c3_sales", "petrol_c4_sales", "petrol_a1_sales", "petrol_a2_sales"]].sum().sum()
            petrol_sales_r = filtered_sales_df["petrol_amount"].sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>⛽ Petrol Sales</span><br><span class='metric-value' style='color: #e74c3c;'>{petrol_sales_l:.2f} L<br>₹{petrol_sales_r:.2f}</span></div>", unsafe_allow_html=True)
        with col2:
            hsd_sales_l = filtered_sales_df[["hsd_c1_sales", "hsd_c2_sales", "hsd_b1_sales", "hsd_b2_sales"]].sum().sum()
            hsd_sales_r = filtered_sales_df["hsd_amount"].sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>🚛 Diesel Sales</span><br><span class='metric-value' style='color: #e67e22;'>{hsd_sales_l:.2f} L<br>₹{hsd_sales_r:.2f}</span></div>", unsafe_allow_html=True)
        with col3:
            xp_sales_l = filtered_sales_df[["xp_b3_sales", "xp_b4_sales"]].sum().sum()
            xp_sales_r = filtered_sales_df["xp_amount"].sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>⚡ XP Sales</span><br><span class='metric-value' style='color: #8e44ad;'>{xp_sales_l:.2f} L<br>₹{xp_sales_r:.2f}</span></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-box'><span class='metric-label'>💵 Total Sales (₹)</span><br><span class='metric-value' style='color: #2980b9;'>₹{filtered_sales_df['total_sales_amount'].sum():.2f}</span></div>", unsafe_allow_html=True)

        # Cash Flow Metrics
        st.markdown(f"<h2>💰 Cash Flow{title_suffix}</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_payments = filtered_sales_df[["paytm_amount", "icici_amount", "fleet_card_amount"]].sum().sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>💳 Total Payments Received (₹)</span><br><span class='metric-value' style='color: #27ae60;'>{total_payments:.2f}</span></div>", unsafe_allow_html=True)
        with col2:
            total_expenses = filtered_sales_df["pump_expenses"].sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>🛠️ Pump Expenses (₹)</span><br><span class='metric-value' style='color: #e67e22;'>{total_expenses:.2f}</span></div>", unsafe_allow_html=True)
        with col3:
            total_shortage = filtered_shortage_df["shortage_amount"].sum() if not filtered_shortage_df.empty else 0.0
            st.markdown(f"<div class='metric-box'><span class='metric-label'>👷 Total Shortage (₹)</span><br><span class='metric-value' style='color: #e74c3c;'>{total_shortage:.2f}</span></div>", unsafe_allow_html=True)
        with col4:
            net_sales = filtered_sales_df["credit_balance"].sum()
            adjusted_net_sales = net_sales - total_shortage
            color = "#c0392b" if adjusted_net_sales > 0 else "#27ae60"
            st.markdown(f"<div class='metric-box'><span class='metric-label'>📊 Net Sales (₹)</span><br><span class='metric-value' style='color: {color};'>{adjusted_net_sales:.2f}</span></div>", unsafe_allow_html=True)

        # Visualizations
        st.markdown(f"<h2>📊 Visualizations{title_suffix}</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Fuel Sales by Type (Liters)")
            sales_data = pd.DataFrame({
                "Fuel Type": ["Petrol", "Diesel", "XP"],
                "Sales (L)": [petrol_sales_l, hsd_sales_l, xp_sales_l]
            })
            st.bar_chart(sales_data.set_index("Fuel Type"))
        with col2:
            st.subheader("Payment Breakdown (₹)")
            payment_data = pd.DataFrame({
                "Payment Type": ["Paytm", "ICICI", "Fleet Card", "Expenses"],
                "Amount (₹)": [
                    filtered_sales_df["paytm_amount"].sum(),
                    filtered_sales_df["icici_amount"].sum(),
                    filtered_sales_df["fleet_card_amount"].sum(),
                    filtered_sales_df["pump_expenses"].sum()
                ]
            })
            st.bar_chart(payment_data.set_index("Payment Type"))

        # Sales Data Table
        st.subheader("📋 Sales Data")
        display_sales_df = filtered_sales_df[[
            "Date", "petrol_c3_sales", "petrol_c4_sales", "petrol_a1_sales", "petrol_a2_sales",
            "hsd_c1_sales", "hsd_c2_sales", "hsd_b1_sales", "hsd_b2_sales",
            "xp_b3_sales", "xp_b4_sales", "test_b1", "test_b2", "test_b3", "test_b4",
            "petrol_amount", "hsd_amount", "xp_amount", "gross_sales_amount", "total_sales_amount",
            "paytm_amount", "icici_amount", "fleet_card_amount", "pump_expenses", "pump_expenses_remark",
            "cash_in", "cash_out", "net_cash", "credit_balance"
        ]]
        st.dataframe(display_sales_df)

    # Party Ledger Section
    if not filtered_party_df.empty:
        st.markdown(f"<h2>📒 Party Ledger{title_suffix}</h2>", unsafe_allow_html=True)
        party_summary = filtered_party_df.groupby("party_name").agg({
            "credit_amount": "sum",
            "debit_amount": "sum"
        }).reset_index()
        party_summary["Net Balance"] = party_summary["credit_amount"] - party_summary["debit_amount"]
        
        col1, col2 = st.columns(2)
        with col1:
            total_credit = party_summary["credit_amount"].sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>📈 Total Credit (₹)</span><br><span class='metric-value' style='color: #27ae60;'>{total_credit:.2f}</span></div>", unsafe_allow_html=True)
        with col2:
            total_debit = party_summary["debit_amount"].sum()
            st.markdown(f"<div class='metric-box'><span class='metric-label'>📉 Total Debit (₹)</span><br><span class='metric-value' style='color: #e74c3c;'>{total_debit:.2f}</span></div>", unsafe_allow_html=True)

        st.subheader("Party Balances")
        st.dataframe(party_summary)

        st.subheader("Party Net Balance (₹)")
        party_chart_data = party_summary[["party_name", "Net Balance"]].set_index("party_name")
        st.bar_chart(party_chart_data)

    # Employee Shortage Section
    if not filtered_shortage_df.empty:
        st.markdown(f"<h2>👷 Employee Shortage{title_suffix}</h2>", unsafe_allow_html=True)
        shortage_summary = filtered_shortage_df.groupby("employee_name").agg({
            "shortage_amount": "sum"
        }).reset_index()
        
        st.subheader("Employee Shortages")
        st.dataframe(shortage_summary)

        st.subheader("Shortage by Employee (₹)")
        shortage_chart_data = shortage_summary[["employee_name", "shortage_amount"]].set_index("employee_name")
        st.bar_chart(shortage_chart_data)

    # Owner's Transaction Section
    if not filtered_owners_df.empty:
        st.markdown(f"<h2>👑 Owner’s Transactions{title_suffix}</h2>", unsafe_allow_html=True)
        owners_credit = filtered_owners_df[filtered_owners_df["type"] == "Credit"]["amount"].sum()
        owners_debit = filtered_owners_df[filtered_owners_df["type"] == "Debit"]["amount"].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-box'><span class='metric-label'>📈 Total Owner’s Credit (₹)</span><br><span class='metric-value' style='color: #27ae60;'>{owners_credit:.2f}</span></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><span class='metric-label'>📉 Total Owner’s Debit (₹)</span><br><span class='metric-value' style='color: #e74c3c;'>{owners_debit:.2f}</span></div>", unsafe_allow_html=True)

        st.subheader("Owner’s Transaction Summary")
        owners_summary = filtered_owners_df.groupby(["owner_name", "mode", "type"]).agg({"amount": "sum"}).reset_index()
        st.dataframe(owners_summary)

        st.subheader("Owner’s Credit vs Debit by Owner (₹)")
        owners_chart_data = filtered_owners_df.pivot_table(index="owner_name", columns="type", values="amount", aggfunc="sum", fill_value=0)
        st.bar_chart(owners_chart_data)

    # Downloads
    if not filtered_sales_df.empty:
        sales_csv = filtered_sales_df.to_csv(index=False)
        st.download_button("📥 Download Sales Data", data=sales_csv, file_name=f"sales_{start_date}_to_{end_date}.csv", mime="text/csv")
    if not filtered_party_df.empty:
        party_csv = filtered_party_df.to_csv(index=False)
        st.download_button("📥 Download Party Ledger", data=party_csv, file_name=f"party_ledger_{start_date}_to_{end_date}.csv", mime="text/csv")
    if not filtered_shortage_df.empty:
        shortage_csv = filtered_shortage_df.to_csv(index=False)
        st.download_button("📥 Download Employee Shortage", data=shortage_csv, file_name=f"shortage_{start_date}_to_{end_date}.csv", mime="text/csv")
    if not filtered_owners_df.empty:
        owners_csv = filtered_owners_df.to_csv(index=False)
        st.download_button("📥 Download Owner’s Transactions", data=owners_csv, file_name=f"owners_transactions_{start_date}_to_{end_date}.csv", mime="text/csv")

# Footer
st.markdown("<hr><p style='text-align: center; color: #7f8c8d;'>Chhatrapati Petroleum</p>", unsafe_allow_html=True)

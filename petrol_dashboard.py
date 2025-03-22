import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
import time
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

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
    .login-container {max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px; background-color: #ffffff;}
    </style>
""", unsafe_allow_html=True)

# Hardcoded credentials (for simplicity)
VALID_CREDENTIALS = {
    "admin": "password123",
    "user": "petrol2025"
}

# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login function
def check_login(username, password):
    return username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password

# Login form
def show_login_page():
    st.markdown("<h1>🔒 Login to Petrol Pump Dashboard</h1>", unsafe_allow_html=True)
    with st.form(key="login_form", clear_on_submit=True):
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit_button:
            if check_login(username, password):
                st.session_state.authenticated = True
                st.success(f"Welcome, {username}!")
                time.sleep(1)  # Brief delay for user feedback
                st.rerun()  # Refresh to show dashboard
            else:
                st.error("Invalid username or password")

# File paths
SALES_DATA_PATH = "petrol_sales.csv"
PARTY_LEDGER_PATH = "party_ledger.csv"
EMPLOYEE_SHORTAGE_PATH = "employee_shortage.csv"
OWNERS_TRANSACTION_PATH = "owners_transaction.csv"
CSV_FILES = [SALES_DATA_PATH, PARTY_LEDGER_PATH, EMPLOYEE_SHORTAGE_PATH, OWNERS_TRANSACTION_PATH]

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
            "oil_products", "oil_amounts", "total_oil_amount",
            "gross_sales_amount", "total_sales_amount",
            "paytm_amount", "icici_amount", "fleet_card_amount",
            "pump_expenses", "pump_expenses_remark",
            "cash_in", "cash_out", "net_cash", "credit_balance"
        ]).to_csv(SALES_DATA_PATH, index=False)
    if not os.path.exists(PARTY_LEDGER_PATH):
        pd.DataFrame(columns=["id", "date", "party_name", "credit_amount", "debit_amount", "remark"]).to_csv(PARTY_LEDGER_PATH, index=False)
    if not os.path.exists(EMPLOYEE_SHORTAGE_PATH):
        pd.DataFrame(columns=["id", "date", "employee_name", "shortage_amount"]).to_csv(EMPLOYEE_SHORTAGE_PATH, index=False)
    if not os.path.exists(OWNERS_TRANSACTION_PATH):
        pd.DataFrame(columns=["id", "date", "owner_name", "amount", "mode", "type"]).to_csv(OWNERS_TRANSACTION_PATH, index=False)

# Load Sales Data
def load_sales_data():
    try:
        df = pd.read_csv(SALES_DATA_PATH)
        df["Date"] = pd.to_datetime(df["date"], errors='coerce')
        required_columns = ["cash_in", "cash_out", "net_cash", "credit_balance", "oil_products", "oil_amounts", "total_oil_amount"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = "" if col in ["oil_products", "oil_amounts"] else 0.0
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
            "oil_products", "oil_amounts", "total_oil_amount",
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
        if "remark" not in df.columns:
            df["remark"] = ""
        return df
    except Exception as e:
        st.error(f"Party Ledger Load Error: {str(e)}")
        return pd.DataFrame(columns=["id", "date", "party_name", "credit_amount", "debit_amount", "remark", "Date"])

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
    
    oil_products = ";".join(data_dict["oil_products"]) if data_dict["oil_products"] else ""
    oil_amounts = ";".join([str(amt) for amt in data_dict["oil_amounts"]]) if data_dict["oil_amounts"] else ""
    total_oil_amount = sum(data_dict["oil_amounts"]) if data_dict["oil_amounts"] else 0.0
    
    gross_sales_amount = petrol_amount + hsd_amount + xp_amount + total_oil_amount
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
        "oil_products": [oil_products], "oil_amounts": [oil_amounts], "total_oil_amount": [total_oil_amount],
        "gross_sales_amount": [gross_sales_amount], "total_sales_amount": [total_sales_amount],
        "paytm_amount": [data_dict["paytm_amount"]], "icici_amount": [data_dict["icici_amount"]],
        "fleet_card_amount": [data_dict["fleet_card_amount"]], "pump_expenses": [data_dict["pump_expenses"]],
        "pump_expenses_remark": [data_dict["pump_expenses_remark"]],
        "cash_in": [cash_in], "cash_out": [cash_out], "net_cash": [net_cash], "credit_balance": [credit_balance]
    })
    df = pd.concat([df.drop(columns=["Date"]), new_row], ignore_index=True)
    df.to_csv(SALES_DATA_PATH, index=False)
    st.sidebar.success(f"Saved Sales for {selected_date}! Rows now: {len(df)}")

# Save Party Ledger Entry
def save_party_ledger(selected_date, party_name, credit_amount, debit_amount, remark):
    df = load_party_ledger()
    new_id = df["id"].max() + 1 if not df.empty else 1
    new_row = pd.DataFrame({
        "id": [new_id], "date": [str(selected_date)],
        "party_name": [party_name], "credit_amount": [credit_amount], "debit_amount": [debit_amount], "remark": [remark]
    })
    df = pd.concat([df.drop(columns=["Date"]), new_row], ignore_index=True)
    df.to_csv(PARTY_LEDGER_PATH, index=False)
    st.sidebar.success(f"Saved Party Ledger for {selected_date}! Rows now: {len(df)}")

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
    st.sidebar.success(f"Saved Employee Shortage for {selected_date}! Rows now: {len(df)}")

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
    st.sidebar.success(f"Saved Owner's Transaction for {selected_date}! Rows now: {len(df)}")

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

# Reset All Data
def reset_all_data():
    for file in CSV_FILES:
        if os.path.exists(file):
            os.remove(file)
    init_csv()
    st.sidebar.success("All data reset successfully!")
    time.sleep(0.5)
    st.rerun()

# Backup Data
def backup_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"petrol_data_backup_{timestamp}.zip"
    with zipfile.ZipFile(backup_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in CSV_FILES:
            if os.path.exists(file):
                zipf.write(file)
    return backup_filename

# Restore Data
def restore_data(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as zipf:
        zipf.extractall()
    st.sidebar.success("Data restored successfully!")
    time.sleep(0.5)
    st.rerun()

# Generate PDF
def generate_pdf(title, data_df, columns, totals=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Header
    elements.append(Paragraph(f"{title}", styles['Title']))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Table
    data = [columns] + data_df[columns].values.tolist()
    if totals:
        total_row = ["Total"] + [""] * (len(columns) - 1)
        for col in totals:
            if col in columns:
                col_idx = columns.index(col)
                total_row[col_idx] = f"₹{totals[col]:.2f}"
        data.append(total_row)
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table)
    
    # Footer
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Chhatrapati Petroleum", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Load and filter data
def load_and_filter_data(display_start_date, display_end_date):
    sales_df = load_sales_data()
    party_df = load_party_ledger()
    shortage_df = load_employee_shortage()
    owners_df = load_owners_transactions()

    st.sidebar.write(f"Displaying from {display_start_date} to {display_end_date}")
    if not sales_df.empty:
        st.sidebar.write("Raw Sales Dates:", sales_df["date"].tolist())

    sales_mask = (sales_df["Date"].dt.date >= display_start_date) & (sales_df["Date"].dt.date <= display_end_date)
    party_mask = (party_df["Date"].dt.date >= display_start_date) & (party_df["Date"].dt.date <= display_end_date)
    shortage_mask = (shortage_df["Date"].dt.date >= display_start_date) & (shortage_df["Date"].dt.date <= display_end_date)
    owners_mask = (owners_df["Date"].dt.date >= display_start_date) & (owners_df["Date"].dt.date <= display_end_date)

    filtered_sales_df = sales_df.loc[sales_mask]
    filtered_party_df = party_df.loc[party_mask]
    filtered_shortage_df = shortage_df.loc[shortage_mask]
    filtered_owners_df = owners_df.loc[owners_mask]

    st.sidebar.write(f"Filtered Sales Rows: {len(filtered_sales_df)}")
    st.sidebar.write(f"Filtered Party Rows: {len(filtered_party_df)}")
    st.sidebar.write(f"Filtered Shortage Rows: {len(filtered_shortage_df)}")
    st.sidebar.write(f"Filtered Owners Rows: {len(filtered_owners_df)}")

    return filtered_sales_df, filtered_party_df, filtered_shortage_df, filtered_owners_df, f" ({display_start_date} to {display_end_date})"

# Main app logic (only shown if authenticated)
if not st.session_state.authenticated:
    show_login_page()
else:
    init_csv()  # Initialize CSVs only after login
    
    # Title
    st.markdown("<h1>⛽ Petrol Pump Dashboard</h1>", unsafe_allow_html=True)

    # Logout button in sidebar
    st.sidebar.header("🔑 User Session")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # Sidebar
    st.sidebar.header("📊 Data Entry")
    today = date.today()
    selected_date = st.sidebar.date_input("📅 Select Date for Entry", value=today)
    st.sidebar.write(f"Entering data for: {selected_date}")

    # Tabs for Data Entry Sections
    sales_tab, party_tab, shortage_tab, owner_tab = st.sidebar.tabs(["Sales", "Party Ledger", "Shortage", "Owner’s Transaction"])

    # Sales Tab
    with sales_tab:
        st.subheader("⛽ Petrol Meter Readings (Liters)")
        petrol_c3_open = st.number_input("C3 Opening", min_value=0.0, step=0.1, key="sales_c3_open")
        petrol_c3_close = st.number_input("C3 Closing", min_value=petrol_c3_open, step=0.1, key="sales_c3_close")
        petrol_c4_open = st.number_input("C4 Opening", min_value=0.0, step=0.1, key="sales_c4_open")
        petrol_c4_close = st.number_input("C4 Closing", min_value=petrol_c4_open, step=0.1, key="sales_c4_close")
        petrol_a1_open = st.number_input("A1 Opening", min_value=0.0, step=0.1, key="sales_a1_open")
        petrol_a1_close = st.number_input("A1 Closing", min_value=petrol_a1_open, step=0.1, key="sales_a1_close")
        petrol_a2_open = st.number_input("A2 Opening", min_value=0.0, step=0.1, key="sales_a2_open")
        petrol_a2_close = st.number_input("A2 Closing", min_value=petrol_a2_open, step=0.1, key="sales_a2_close")

        st.subheader("🚛 HSD Meter Readings (Liters)")
        hsd_c1_open = st.number_input("C1 Opening (HSD)", min_value=0.0, step=0.1, key="sales_hsd_c1_open")
        hsd_c1_close = st.number_input("C1 Closing (HSD)", min_value=hsd_c1_open, step=0.1, key="sales_hsd_c1_close")
        hsd_c2_open = st.number_input("C2 Opening (HSD)", min_value=0.0, step=0.1, key="sales_hsd_c2_open")
        hsd_c2_close = st.number_input("C2 Closing (HSD)", min_value=hsd_c2_open, step=0.1, key="sales_hsd_c2_close")
        hsd_b1_open = st.number_input("B1 Opening (HSD)", min_value=0.0, step=0.1, key="sales_hsd_b1_open")
        hsd_b1_close = st.number_input("B1 Closing (HSD)", min_value=hsd_b1_open, step=0.1, key="sales_hsd_b1_close")
        hsd_b2_open = st.number_input("B2 Opening (HSD)", min_value=0.0, step=0.1, key="sales_hsd_b2_open")
        hsd_b2_close = st.number_input("B2 Closing (HSD)", min_value=hsd_b2_open, step=0.1, key="sales_hsd_b2_close")

        st.subheader("⚡ XP Meter Readings (Liters)")
        xp_b3_open = st.number_input("B3 Opening (XP)", min_value=0.0, step=0.1, key="sales_xp_b3_open")
        xp_b3_close = st.number_input("B3 Closing (XP)", min_value=xp_b3_open, step=0.1, key="sales_xp_b3_close")
        xp_b4_open = st.number_input("B4 Opening (XP)", min_value=0.0, step=0.1, key="sales_xp_b4_open")
        xp_b4_close = st.number_input("B4 Closing (XP)", min_value=xp_b4_open, step=0.1, key="sales_xp_b4_close")

        st.subheader("🧪 Testing (Liters)")
        test_b1 = st.number_input("Test B1", min_value=0.0, step=0.1, value=0.0, key="sales_test_b1")
        test_b2 = st.number_input("Test B2", min_value=0.0, step=0.1, value=0.0, key="sales_test_b2")
        test_b3 = st.number_input("Test B3", min_value=0.0, step=0.1, value=0.0, key="sales_test_b3")
        test_b4 = st.number_input("Test B4", min_value=0.0, step=0.1, value=0.0, key="sales_test_b4")

        st.subheader("💰 Rates (₹/L)")
        petrol_rate = st.number_input("Petrol Rate", min_value=0.0, step=0.01, value=104.62, key="sales_petrol_rate")
        hsd_rate = st.number_input("HSD Rate", min_value=0.0, step=0.01, value=91.16, key="sales_hsd_rate")
        xp_rate = st.number_input("XP Rate", min_value=0.0, step=0.01, value=111.57, key="sales_xp_rate")

        st.subheader("🛢️ Oil Sales (₹)")
        num_oil_products = st.number_input("Number of Oil Products", min_value=0, max_value=10, value=0, step=1, key="sales_num_oil")
        oil_products = []
        oil_amounts = []
        for i in range(num_oil_products):
            col1, col2 = st.columns(2)
            with col1:
                product_name = st.text_input(f"Oil Product {i+1} Name", key=f"sales_oil_product_{i}")
            with col2:
                amount = st.number_input(f"Oil Product {i+1} Amount (₹)", min_value=0.0, step=0.1, key=f"sales_oil_amount_{i}")
            oil_products.append(product_name)
            oil_amounts.append(amount)

        st.subheader("💳 Payment Transactions (₹)")
        paytm_amount = st.number_input("Paytm Amount", min_value=0.0, step=0.1, value=0.0, key="sales_paytm")
        icici_amount = st.number_input("ICICI Amount", min_value=0.0, step=0.1, value=0.0, key="sales_icici")
        fleet_card_amount = st.number_input("Fleet Card Amount", min_value=0.0, step=0.1, value=0.0, key="sales_fleet")

        st.subheader("🛠️ Pump Expenses (₹)")
        pump_expenses = st.number_input("Pump Expenses", min_value=0.0, step=0.1, value=0.0, key="sales_expenses")
        pump_expenses_remark = st.text_input("Expenses Remark", value="", key="sales_expenses_remark")

        if st.button("💾 Save Sales", key="save_sales"):
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
                "oil_products": oil_products, "oil_amounts": oil_amounts,
                "paytm_amount": paytm_amount, "icici_amount": icici_amount,
                "fleet_card_amount": fleet_card_amount, "pump_expenses": pump_expenses,
                "pump_expenses_remark": pump_expenses_remark
            }
            save_sales_data(selected_date, data_dict)

    # Party Ledger Tab
    with party_tab:
        st.subheader("📒 Party Ledger")
        party_name = st.text_input("Party Name", key="party_name")
        party_credit = st.number_input("Credit Amount (₹)", min_value=0.0, step=0.1, value=0.0, key="party_credit")
        party_debit = st.number_input("Debit Amount (₹)", min_value=0.0, step=0.1, value=0.0, key="party_debit")
        party_remark = st.text_input("Remark", value="", key="party_remark")
        if st.button("💾 Save Party Transaction", key="save_party"):
            save_party_ledger(selected_date, party_name, party_credit, party_debit, party_remark)

    # Employee Shortage Tab
    with shortage_tab:
        st.subheader("👷 Employee Shortage")
        employee_name = st.text_input("Employee Name", key="shortage_employee")
        shortage_amount = st.number_input("Shortage Amount (₹)", min_value=0.0, step=0.1, value=0.0, key="shortage_amount")
        if st.button("💾 Save Shortage", key="save_shortage"):
            save_employee_shortage(selected_date, employee_name, shortage_amount)

    # Owner’s Transaction Tab
    with owner_tab:
        st.subheader("👑 Owner’s Transaction")
        owner_name = st.text_input("Owner Name", key="owner_name")
        owner_amount = st.number_input("Amount (₹)", min_value=0.0, step=0.1, value=0.0, key="owner_amount")
        owner_mode = st.selectbox("Mode of Transaction", ["Online", "Cheque", "Cash"], key="owner_mode")
        owner_type = st.selectbox("Type", ["Credit", "Debit"], key="owner_type")
        if st.button("💾 Save Owner Transaction", key="save_owner"):
            save_owners_transaction(selected_date, owner_name, owner_amount, owner_mode, owner_type)

    # Remaining Sidebar Sections (Outside Tabs)
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

    st.sidebar.subheader("🔄 Reset All Data")
    confirm_reset = st.sidebar.checkbox("Confirm Reset (This will delete all data permanently)", value=False)
    if st.sidebar.button("🔄 Reset All Data", type="primary"):
        if confirm_reset:
            reset_all_data()
        else:
            st.sidebar.write("Please check 'Confirm Reset' to proceed.")

    st.sidebar.subheader("💾 Backup & Restore")
    if st.sidebar.button("📥 Backup Data"):
        backup_file = backup_data()
        with open(backup_file, "rb") as f:
            st.sidebar.download_button("Download Backup", f, file_name=backup_file, mime="application/zip")

    uploaded_file = st.sidebar.file_uploader("Upload Backup ZIP", type="zip")
    if uploaded_file and st.sidebar.button("📤 Restore Data"):
        restore_data(uploaded_file)

    st.sidebar.subheader("📅 Filter Dashboard Data (Optional)")
    date_range = st.sidebar.date_input("Select Date Range for Display", value=[selected_date, selected_date], key="filter_range")
    if len(date_range) == 2:
        display_start_date, display_end_date = date_range
    else:
        display_start_date, display_end_date = selected_date, selected_date

    # Load and filter data
    filtered_sales_df, filtered_party_df, filtered_shortage_df, filtered_owners_df, title_suffix = load_and_filter_data(display_start_date, display_end_date)

    # Display Dashboard
    if filtered_sales_df.empty and filtered_party_df.empty and filtered_shortage_df.empty and filtered_owners_df.empty:
        st.warning(f"No data available for the selected range{title_suffix}.")
    else:
        if not filtered_sales_df.empty:
            # Sales Metrics
            st.markdown(f"<h2>📈 Key Metrics{title_suffix}</h2>", unsafe_allow_html=True)
            col1, col2, col3, col4, col5 = st.columns(5)
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
                oil_sales_r = filtered_sales_df["total_oil_amount"].sum()
                st.markdown(f"<div class='metric-box'><span class='metric-label'>🛢️ Oil Sales</span><br><span class='metric-value' style='color: #16a085;'>₹{oil_sales_r:.2f}</span></div>", unsafe_allow_html=True)
            with col5:
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
                party_net_balance = filtered_party_df["credit_amount"].sum() - filtered_party_df["debit_amount"].sum()
                adjusted_net_sales = net_sales + party_net_balance - total_shortage
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
                st.subheader("Sales Breakdown (₹)")
                payment_data = pd.DataFrame({
                    "Type": ["Petrol", "Diesel", "XP", "Oil", "Expenses"],
                    "Amount (₹)": [
                        petrol_sales_r,
                        hsd_sales_r,
                        xp_sales_r,
                        oil_sales_r,
                        total_expenses
                    ]
                })
                st.bar_chart(payment_data.set_index("Type"))

            # Sales Data Table
            st.subheader("📋 Sales Data")
            display_sales_df = filtered_sales_df[[
                "Date", "petrol_c3_sales", "petrol_c4_sales", "petrol_a1_sales", "petrol_a2_sales",
                "hsd_c1_sales", "hsd_c2_sales", "hsd_b1_sales", "hsd_b2_sales",
                "xp_b3_sales", "xp_b4_sales", "test_b1", "test_b2", "test_b3", "test_b4",
                "petrol_amount", "hsd_amount", "xp_amount", "oil_products", "oil_amounts", "total_oil_amount",
                "gross_sales_amount", "total_sales_amount",
                "paytm_amount", "icici_amount", "fleet_card_amount", "pump_expenses", "pump_expenses_remark",
                "cash_in", "cash_out", "net_cash", "credit_balance"
            ]]
            st.dataframe(display_sales_df)
            
            # PDF Download for Sales
            sales_pdf = generate_pdf(
                f"Sales Report{title_suffix}",
                display_sales_df,
                ["Date", "petrol_amount", "hsd_amount", "xp_amount", "total_oil_amount", "total_sales_amount"],
                {"total_sales_amount": filtered_sales_df["total_sales_amount"].sum()}
            )
            st.download_button("📜 Download Sales PDF", sales_pdf, f"sales_report_{display_start_date}_to_{display_end_date}.pdf", "application/pdf")

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

            st.subheader("Party Balances Summary")
            st.dataframe(party_summary)

            st.subheader("Party Net Balance (₹)")
            party_chart_data = party_summary[["party_name", "Net Balance"]].set_index("party_name")
            st.bar_chart(party_chart_data)

            # Detailed Party Ledger
            st.subheader("Detailed Party Ledger")
            for party in party_summary["party_name"].unique():
                with st.expander(f"Ledger for {party}"):
                    party_transactions = filtered_party_df[filtered_party_df["party_name"] == party][["Date", "credit_amount", "debit_amount", "remark"]]
                    st.dataframe(party_transactions)
                    net_balance = party_summary[party_summary["party_name"] == party]["Net Balance"].values[0]
                    color = "#27ae60" if net_balance >= 0 else "#e74c3c"
                    st.markdown(f"<p style='font-weight: bold; color: {color};'>Net Balance: ₹{net_balance:.2f}</p>", unsafe_allow_html=True)
                    
                    # PDF Download for Party
                    party_pdf = generate_pdf(
                        f"Party Ledger - {party}{title_suffix}",
                        party_transactions,
                        ["Date", "credit_amount", "debit_amount", "remark"],
                        {"credit_amount": party_transactions["credit_amount"].sum(), "debit_amount": party_transactions["debit_amount"].sum()}
                    )
                    st.download_button(f"📜 Download {party} Ledger PDF", party_pdf, f"party_ledger_{party}_{display_start_date}_to_{display_end_date}.pdf", "application/pdf")

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
            
            # PDF Download for Employee Shortage
            shortage_pdf = generate_pdf(
                f"Employee Shortage Report{title_suffix}",
                filtered_shortage_df,
                ["Date", "employee_name", "shortage_amount"],
                {"shortage_amount": filtered_shortage_df["shortage_amount"].sum()}
            )
            st.download_button("📜 Download Shortage PDF", shortage_pdf, f"shortage_report_{display_start_date}_to_{display_end_date}.pdf", "application/pdf")

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
            
            # PDF Download for Owner’s Transactions
            owners_pdf = generate_pdf(
                f"Owner’s Transactions Report{title_suffix}",
                filtered_owners_df,
                ["Date", "owner_name", "amount", "mode", "type"],
                {"amount": filtered_owners_df["amount"].sum()}
            )
            st.download_button("📜 Download Owner’s Transactions PDF", owners_pdf, f"owners_transactions_{display_start_date}_to_{display_end_date}.pdf", "application/pdf")

        # Downloads for CSV
        if not filtered_sales_df.empty:
            sales_csv = filtered_sales_df.to_csv(index=False)
            st.download_button("📥 Download Sales CSV", data=sales_csv, file_name=f"sales_{display_start_date}_to_{display_end_date}.csv", mime="text/csv")
        if not filtered_party_df.empty:
            party_csv = filtered_party_df.to_csv(index=False)
            st.download_button("📥 Download Party Ledger CSV", data=party_csv, file_name=f"party_ledger_{display_start_date}_to_{display_end_date}.csv", mime="text/csv")
        if not filtered_shortage_df.empty:
            shortage_csv = filtered_shortage_df.to_csv(index=False)
            st.download_button("📥 Download Employee Shortage CSV", data=shortage_csv, file_name=f"shortage_{display_start_date}_to_{display_end_date}.csv", mime="text/csv")
        if not filtered_owners_df.empty:
            owners_csv = filtered_owners_df.to_csv(index=False)
            st.download_button("📥 Download Owner’s Transactions CSV", data=owners_csv, file_name=f"owners_transactions_{display_start_date}_to_{display_end_date}.csv", mime="text/csv")

    # Footer
    st.markdown("<hr><p style='text-align: center; color: #7f8c8d;'>Chhatrapati Petroleum</p>", unsafe_allow_html=True)

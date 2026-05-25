import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Spend",
    page_icon="💰",
    layout="wide"
)

# ================= LIGHT THEME CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    color: #111;
}

.main-title {
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    color: #1f77b4;
}

.card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    border: 1px solid #ddd;
}

[data-testid="metric-container"] {
    background: white;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}

.stDataFrame {
    background-color: white;
}

</style>
""", unsafe_allow_html=True)

# ================= DATA INIT =================
if "expense" not in st.session_state:
    st.session_state.expense = pd.DataFrame(
        columns=["Date", "Category", "Amount", "Description"]
    )

# ================= FUNCTIONS =================
def add_expense(date, category, amount, description):
    new = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.expense.columns
    )
    st.session_state.expense = pd.concat(
        [st.session_state.expense, new],
        ignore_index=True
    )

def save_data():
    st.session_state.expense.to_csv("expense.csv", index=False)
    st.success("Saved Successfully!")

def load_data(file):
    if file:
        st.session_state.expense = pd.read_csv(file)
        st.session_state.expense["Date"] = pd.to_datetime(
            st.session_state.expense["Date"],
            errors="coerce"
        ).dt.date
        st.success("Loaded Successfully!")

# ================= CATEGORY PIE CHART =================
def visualize():
    if st.session_state.expense.empty:
        st.warning("No data found!")
        return

    df = st.session_state.expense.copy()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    data = df.groupby("Category")["Amount"].sum()

    colors = ["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0"]

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(
        data,
        labels=data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors
    )
    ax.set_title("Expense Distribution")
    st.pyplot(fig)

# ================= MONTHLY VISUALIZATION =================
def monthly_visualize():
    if st.session_state.expense.empty:
        st.warning("No data found!")
        return

    df = st.session_state.expense.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    df["Month"] = df["Date"].dt.to_period("M")

    monthly_data = df.groupby("Month")["Amount"].sum()
    monthly_data.index = monthly_data.index.astype(str)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(monthly_data.index, monthly_data.values, marker="o")

    ax.set_title("Monthly Expense Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spend")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)

# ================= HEADER =================
st.markdown('<div class="main-title">💰 Smart Spend Dashboard</div>', unsafe_allow_html=True)
st.markdown("### Track your money easily 📊")
st.markdown("---")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("➕ Add Expense")

    date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Entertainment", "Utilities", "Other"]
    )
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")

    if st.button("Add Expense"):
        add_expense(date, category, amount, description)
        st.success("Added Successfully!")

    st.markdown("---")

    st.header("📂 Data")

    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        load_data(file)

    if st.button("Save Data"):
        save_data()

# ================= METRICS =================
if not st.session_state.expense.empty:
    df = st.session_state.expense.copy()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    total = df["Amount"].sum()
    count = len(df)
    avg = df["Amount"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Spend", f"${total:.2f}")
    col2.metric("🧾 Transactions", count)
    col3.metric("📊 Average", f"${avg:.2f}")

st.markdown("---")

# ================= TABLE =================
st.subheader("💳 Transaction History")

if st.session_state.expense.empty:
    st.info("No transactions yet.")
else:
    st.dataframe(st.session_state.expense, use_container_width=True)

# ================= VISUALS =================
st.subheader("📊 Category Visualization")

if st.button("Show Category Chart"):
    visualize()

st.subheader("📅 Monthly Visualization")

if st.button("Show Monthly Trend"):
    monthly_visualize()
import streamlit as st
import pandas as pd
import time
from advanced_logic import get_layout_insights, plot_affinity_network, calculate_batches, plot_delivery_map, check_expiry_risk

st.set_page_config(layout="wide", page_title="Fulfillment Optimization Suite")

# Load Databases
try:
    df_trans = pd.read_csv('transactions.csv')
    df_orders = pd.read_csv('orders.csv')
    df_inv = pd.read_csv('inventory.csv')
except FileNotFoundError:
    st.error("Run 'python data_setup.py' to initialize database!")
    st.stop()

st.sidebar.title("⚡ Live Ops Control")

# --- LIVE SIMULATION SIDEBAR ---
sim_mode = st.sidebar.selectbox("Simulate Action:", ["Incoming Order", "Add Transaction", "Update Stock"])

if sim_mode == "Incoming Order":
    with st.sidebar.form("new_order"):
        oid = f"ORD-{len(df_orders)+101}"
        x = st.slider("Location X", -10, 10, 5)
        y = st.slider("Location Y", -10, 10, 5)
        sla = st.number_input("SLA (Mins Left)", 5, 60, 20)
        if st.form_submit_button("Inject Order"):
            new_row = pd.DataFrame([{'id': oid, 'x': x, 'y': y, 'sla': sla, 'status': 'Pending'}])
            df_orders = pd.concat([df_orders, new_row], ignore_index=True)
            df_orders.to_csv('orders.csv', index=False)
            st.success(f"Order {oid} received!")
            time.sleep(1)
            st.rerun()

elif sim_mode == "Add Transaction":
    with st.sidebar.form("new_trans"):
        item = st.selectbox("Item Sold", df_inv['sku'].unique())
        if st.form_submit_button("Log Sale"):
            new_id = df_trans['transaction_id'].max() + 1
            new_row = pd.DataFrame([{'transaction_id': new_id, 'item': item}])
            df_trans = pd.concat([df_trans, new_row], ignore_index=True)
            df_trans.to_csv('transactions.csv', index=False)
            st.success("Transaction Logged!")
            st.rerun()

# --- MAIN DASHBOARD ---
module = st.radio("Select Module:", ["1. Warehouse (Layout)", "2. Logistics (Batching)", "3. Inventory (Expiry)"], horizontal=True)
st.divider()

if module == "1. Warehouse (Layout)":
    st.title("🏭 Dynamic Warehouse Slotting")
    c1, c2 = st.columns([1, 2])
    
    rules = get_layout_insights(df_trans)
    
    with c1:
        st.subheader("Affinity Rules")
        st.dataframe(rules[['antecedents', 'consequents', 'lift']].head(5), hide_index=True)
        st.info("💡 Higher Lift = Stronger correlation. Place these items adjacent.")
        
    with c2:
        st.subheader("Interactive Layout Map")
        fig = plot_affinity_network(rules)
        st.plotly_chart(fig, use_container_width=True)

elif module == "2. Logistics (Batching)":
    st.title("🛵 Real-Time Batching Engine")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Live Fleet Map")
        fig = plot_delivery_map(df_orders)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("Optimized Batches")
        batches = calculate_batches(df_orders)
        st.dataframe(batches, hide_index=True)
        
        savings = len(batches[batches['Type'] == 'BATCH']) * 40
        st.metric("Real-Time Savings", f"₹{savings}", "Fuel & Time")

elif module == "3. Inventory (Expiry)":
    st.title("📉 Expiry & Waste Management")
    
    analyzed_inv = check_expiry_risk(df_inv)
    
    # Metrics
    risk_items = len(analyzed_inv[analyzed_inv['Action'] != 'No Action'])
    st.metric("SKUs at Risk", risk_items, delta="High Priority", delta_color="inverse")
    
    st.subheader("Action Board")
    # styled dataframe
    def highlight_risk(s):
        return ['background-color: #ffcccb' if v == '⚡ FLASH SALE' else '' for v in s]
    
    st.dataframe(analyzed_inv.style.apply(highlight_risk, subset=['Action']), use_container_width=True)
    
    if risk_items > 0:
        if st.button("🚀 Trigger Auto-Markdown Campaign"):
            st.toast("Push Notifications sent to 4,500 users nearby!", icon="✅")
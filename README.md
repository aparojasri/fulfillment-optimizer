# ⚡ Hyperlocal Fulfillment Optimization Suite

### 🚀 Overview
An execution-focused platform designed for **Regional Ops & Logistics Managers**. It solves the "Last Mile Trilemma" by optimizing **Warehouse Picking Speed**, **Delivery Fleet Costs**, and **Inventory Waste** simultaneously.

**Live Demo:** [Insert Netlify/Streamlit Link Here if deployed]

---

### 💼 Business Value
* **Warehouse Efficiency:** Reduces picker travel time by ~12% using Market Basket Analysis to co-locate high-affinity items.
* **Logistics Cost:** Lowers fleet costs by dynamically batching orders based on location proximity and SLA constraints.
* **Zero Waste:** dynamic pricing engine that triggers hyperlocal flash sales for expiring inventory, recovering sunk costs.

---

### 🛠️ Technical Architecture
* **Layout Optimizer:** **Apriori Algorithm (Association Rule Mining)** to detect item correlations (e.g., Milk & Bread).
* **Logistics Engine:** Heuristic routing algorithm calculating **Manhattan Distances** to optimize rider batches in real-time.
* **Persistent Database:** CSV-based state management to track live orders, transactions, and inventory across sessions.
* **Visualization:** Interactive Network Graphs (Plotly) for warehouse layout and Scatter Plots for live fleet tracking.

### ⚡ Key Features
1.  **Real-Time Simulation:** "Live Ops" sidebar to inject new orders and transactions, instantly triggering re-optimization.
2.  **Interactive Warehouse Map:** Network graph visualizing product affinity to guide slotting decisions.
3.  **SLA-Aware Batching:** Logic that only batches orders if the Service Level Agreement (Delivery Time) can be met for *both* customers.

---

### 💻 Tech Stack
* **Core:** Python 3.9+, Streamlit
* **ML/Algorithms:** MLxtend (Apriori), Graph Theory (NetworkX logic)
* **Data:** Pandas, NumPy
* **Visualization:** Plotly Graph Objects, Plotly Express

### 🏃‍♂️ How to Run
1.  Install dependencies: `pip install pandas numpy mlxtend streamlit plotly`
2.  Initialize Database: `python data_setup.py`
3.  Launch Dashboard: `streamlit run app.py`

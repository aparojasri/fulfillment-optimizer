import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px
import plotly.graph_objects as go

# --- MODULE 1: LAYOUT OPTIMIZER ---
def get_layout_insights(df_trans):
    # One-hot encode
    basket = pd.get_dummies(df_trans['item']).groupby(df_trans['transaction_id']).sum()
    basket[basket > 0] = 1
    
    # Apriori
    frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
    rules = rules.sort_values(by='lift', ascending=False).head(10)
    
    # Convert frozen sets to strings for display
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0])
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x)[0])
    
    return rules

def plot_affinity_network(rules):
    # Create a visual Network Graph using Scatter Plot
    # This simulates a "Warehouse Map"
    
    # Simple positioning logic for visualization
    items = list(set(rules['antecedents']).union(set(rules['consequents'])))
    pos = {item: (np.random.uniform(0, 10), np.random.uniform(0, 10)) for item in items}
    
    edge_x = []
    edge_y = []
    for _, row in rules.iterrows():
        x0, y0 = pos[row['antecedents']]
        x1, y1 = pos[row['consequents']]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), hoverinfo='none', mode='lines')

    node_x = [pos[item][0] for item in items]
    node_y = [pos[item][1] for item in items]

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        text=items, textposition="top center",
        marker=dict(showscale=True, colorscale='YlGnBu', size=20, color=[10]*len(items)),
        hoverinfo='text'
    )
    
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<b>Optimal Product Co-Location Map</b>',
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="Aisle Layout X"),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="Aisle Layout Y"))
             )
    return fig

# --- MODULE 2: BATCHING ---
def calculate_batches(df_orders):
    batches = []
    processed = []
    
    for i, a in df_orders.iterrows():
        if a['id'] in processed: continue
        best_match = None
        min_dist = 100
        
        for j, b in df_orders.iterrows():
            if a['id'] == b['id'] or b['id'] in processed: continue
            
            dist = abs(a['x'] - b['x']) + abs(a['y'] - b['y'])
            
            # SLA Constraint: Can we do both?
            time_needed = (dist * 2) + 5
            if dist < 4 and time_needed < a['sla'] and time_needed < b['sla']:
                if dist < min_dist:
                    min_dist = dist
                    best_match = b
        
        if best_match is not None:
            batches.append({'Type': 'BATCH', 'IDs': f"{a['id']} + {best_match['id']}", 'Savings': '₹40 (1 Rider)'})
            processed.extend([a['id'], best_match['id']])
        else:
            batches.append({'Type': 'SINGLE', 'IDs': a['id'], 'Savings': '-'})
            processed.append(a['id'])
            
    return pd.DataFrame(batches)

def plot_delivery_map(df_orders):
    fig = px.scatter(df_orders, x='x', y='y', text='id', color='sla', size='sla',
                     title="<b>Live Delivery Fleet Map</b>",
                     labels={'sla': 'Mins Remaining', 'x': 'Zone Longitude', 'y': 'Zone Latitude'},
                     color_continuous_scale='RdYlGn')
    fig.update_traces(textposition='top center')
    fig.add_scatter(x=[0], y=[0], mode='markers', marker=dict(size=25, color='Black'), name='Dark Store Hub')
    return fig

# --- MODULE 3: EXPIRY ---
def check_expiry_risk(df_inv):
    df_inv['Action'] = 'No Action'
    
    # Logic: Expiry < 3 days AND Stock > 10
    mask = (df_inv['days_to_expiry'] <= 3) & (df_inv['stock'] > 10)
    df_inv.loc[mask, 'Action'] = '⚡ FLASH SALE'
    
    return df_inv
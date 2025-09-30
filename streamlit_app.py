# polished_streamlit_app.py
import streamlit as st
import pickle
from collections import defaultdict
from itertools import combinations
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Market Basket Recommender", layout="wide")

# -------------------------
# Load artifacts
# -------------------------
@st.cache_data
def load_artifacts():
    with open('artifacts/rules_df.pkl', 'rb') as f:
        rules_df = pickle.load(f)
    with open('artifacts/prod_mappings.pkl', 'rb') as f:
        prod_maps = pickle.load(f)
    with open('artifacts/neighbors.pkl', 'rb') as f:
        neighbors = pickle.load(f)
    return rules_df, prod_maps, neighbors

rules_df, prod_maps, neighbors = load_artifacts()

prod_id_to_idx = prod_maps['prod_id_to_idx']
idx_to_prod_id = prod_maps['idx_to_prod_id']
idx_to_name = prod_maps['idx_to_name']
name_to_idx = prod_maps['name_to_idx']

# -------------------------
# Helper functions
# -------------------------
def idxs_to_names(idxs):
    return [idx_to_name[i] for i in idxs]

# Build rule lookup
rule_lookup = defaultdict(list)
for _, row in rules_df.iterrows():
    ant = tuple(sorted(row['antecedent']))
    cons = tuple(sorted(row['consequent']))
    rule_lookup[ant].append({
        'consequents': cons,
        'support': float(row['support']),
        'confidence': float(row['confidence']),
        'lift': float(row['lift'])
    })

# Hybrid recommendation function
def get_recommendations_from_cart(cart_item_names, top_n=12, alpha=0.7):
    cart_idxs = [name_to_idx[n] for n in cart_item_names if n in name_to_idx]
    cart_set = set(cart_idxs)
    candidate_scores = defaultdict(float)
    candidate_reasons = {}
    candidate_types = {}

    cart_sorted = tuple(sorted(cart_set))
    # Exact rules
    if cart_sorted in rule_lookup:
        for r in rule_lookup[cart_sorted]:
            for c in r['consequents']:
                if c in cart_set:
                    continue
                score = r['confidence'] * r['lift']
                candidate_scores[c] += score
                candidate_reasons[c] = f"rule: {', '.join(idxs_to_names(cart_sorted))} → {idx_to_name[c]}"
                candidate_types[c] = 'Rule-based'

    # Subset rules
    max_subset = min(2, len(cart_sorted))
    for k in range(1, max_subset+1):
        for comb in combinations(cart_sorted, k):
            if comb in rule_lookup:
                for r in rule_lookup[comb]:
                    for c in r['consequents']:
                        if c in cart_set:
                            continue
                        score = (r['confidence'] * r['lift']) * (1.0/(k))
                        candidate_scores[c] += score
                        if c not in candidate_reasons:
                            candidate_reasons[c] = f"rule: {', '.join(idxs_to_names(comb))} → {idx_to_name[c]}"
                            candidate_types[c] = 'Rule-based'

    # Similarity neighbors
    for i in cart_set:
        for nbr, sim in neighbors.get(i, []):
            if nbr in cart_set:
                continue
            candidate_scores[nbr] += alpha * sim
            if nbr not in candidate_reasons:
                candidate_reasons[nbr] = f"similarity to {idx_to_name[i]} (sim={sim:.3f})"
                candidate_types[nbr] = 'Similarity-based'

    # Sort and pick top-N
    cand_list = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for idx, score in cand_list[:top_n]:
        results.append({
            'Product': idx_to_name[idx],
            'Score': round(float(score), 4),
            'Reason': candidate_reasons.get(idx, 'hybrid'),
            'Type': candidate_types.get(idx, 'Hybrid')
        })
    return results

# -------------------------
# Streamlit UI
# -------------------------
st.title("🛒 Market Basket Recommender")

st.markdown("""
Select items in your cart and get **top-N recommended products** with explanations.  
- **Green** = Rule-based recommendation  
- **Blue** = Similarity-based recommendation
""")

# Product selection
all_products = list(idx_to_name.values())
cart_items = st.multiselect("Select products in your cart:", options=all_products)

if st.button("Get Recommendations") and cart_items:
    recommendations = get_recommendations_from_cart(cart_items, top_n=12)
    if recommendations:
        # Display in DataFrame
        df = pd.DataFrame(recommendations)
        
        # Color-code by type
        def highlight_row(row):
            color = ''
            if row['Type'] == 'Rule-based':
                color = 'background-color: #d4edda'  # greenish
            elif row['Type'] == 'Similarity-based':
                color = 'background-color: #d1ecf1'  # blueish
            return [color]*len(row)
        
        st.subheader("Recommended Products")
        st.dataframe(df.style.apply(highlight_row, axis=1))
        
        # Download CSV button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Recommendations CSV", data=csv, file_name='recommendations.csv', mime='text/csv')
        
    else:
        st.info("No recommendations found for this combination of products.")

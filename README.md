🛒 Market Basket Recommender

An interactive hybrid recommendation system for online grocery shopping.
Recommends products based on what’s already in the user’s cart using association rules and item similarity. Built with Python, pandas, and Streamlit.

🔹 Project Overview

Market Basket Analysis (MBA) is a popular technique in retail analytics that uncovers patterns in customer purchases:

“People who buy X also buy Y”

This project builds a hybrid recommender system that:

Generates association rules from real transaction data using Apriori.

Computes item-item similarity from co-occurrence data.

Combines both approaches to provide explainable product recommendations.

Features an interactive Streamlit app for users to select products in their cart and get top-N recommendations with explanations.

🔹 Dataset

Source: Instacart Online Grocery Shopping Dataset on Kaggle

Files used:

products.csv – Product IDs, names, aisles, departments

orders.csv – Orders history

order_products__train.csv / order_products__prior.csv – Order-product mapping

aisles.csv / departments.csv – Product metadata

Data Stats from preprocessing:

Metric	Value
Total products considered	5,000 top products
Total transactions	~3,050,000
Sampled transactions for rule mining	300,000
Number of rules discovered	450+
🔹 Features

Hybrid Recommendation Engine

Combines rule-based and similarity-based recommendations for better coverage.

Rule-based recommendations prioritize strong co-purchases.

Similarity handles rare/unseen combinations.

Explainable Recommendations

Users see why a product is recommended:

Rule-based → shows the antecedent and consequent

Similarity-based → shows which cart item it is similar to

Interactive Streamlit App

Multi-select input for cart items

Top-N recommendations displayed in color-coded table:

Green → Rule-based

Blue → Similarity-based

Downloadable CSV & PDF of recommendations

Memory-efficient

Uses precomputed artifacts (rules_df.pkl, neighbors.pkl, prod_mappings.pkl)

Avoids computing large one-hot matrices at runtime

🔹 How It Works
1. Preprocessing

Filtered top 5,000 products by popularity

Sampled 300k transactions for memory efficiency

Generated product index mappings for fast lookup

2. Association Rule Mining

Used Apriori algorithm (efficient_apriori)

Rules computed with support, confidence, and lift thresholds

Top 450 rules selected

3. Co-occurrence Similarity

Built item-item co-occurrence matrix

Calculated similarity scores for each product pair

Stored top neighbors for hybrid recommendation

4. Hybrid Recommendations

Combines rule scores + similarity scores

Sorted top-N products displayed with Score, Type, and Reason

5. Evaluation

Hit rates on test set (expected due to sparse retail data):

Top-1 Hit Rate: 1.82%

Top-3 Hit Rate: 3.77%

Top-5 Hit Rate: 5.21%

Top-10 Hit Rate: 8.31%

🔹 Streamlit App

Features:

Select multiple products in your cart

View top recommended products

Recommendations include score, type, and reasoning

Download CSV or PDF for offline use

Screenshots: (Add images here after running the app locally)

🔹 Installation
# Clone repository
git clone https://github.com/WhiteFang04/Market-Basket-Recommender.git
cd Market-Basket-Recommender

# Install dependencies
pip install -r requirements.txt

🔹 Run the App
streamlit run polished_streamlit_app.py

🔹 Future Enhancements

Real-time dynamic recommendations without button click

Include product images in the recommendations

Deploy as API service for e-commerce platforms

Update rules and similarities periodically to capture trending products

🔹 References

Instacart Market Basket Analysis Dataset

efficient-apriori Python library

Streamlit Documentation

Author: Your Name
GitHub: https://github.com/WhiteFang04

If you want, I can also write a concise, eye-catching one-paragraph description for the GitHub repo main page, so visitors immediately understand the project without scrolling.

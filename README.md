# Uber Eats Operational & Customer Intelligence System

## 1. Project Overview & Business Problem
In a three-sided food delivery marketplace (Customers, Delivery Partners, and Restaurants), efficiency and customer retention depend heavily on data-informed decision-making. The objective of this project is to build an end-to-end Machine Learning intelligence system using synthetic operational data to address key logistical bottlenecks and customer friction points:
* **Customer & Restaurant Segmentation:** Group high-value diners and identify struggling restaurant partners to enable targeted marketing and operational interventions.
* **Customer Sentiment Analysis:** Process unstructured review text to isolate primary dissatisfaction themes and drivers.
* **Delivery Tip Prediction:** Model courier tip behavior to understand non-linear earning drivers across distance, order volume, and weather variables.
* **Hourly & Daily Demand Forecasting:** Project platform order demand across 7-to-14 day windows to assist in dynamic courier dispatching and capacity allocation.

---

## 2. Repository & Folder Structure
```text
uber-eats-capstone/
├── data/
│   ├── customers.csv
│   ├── deliveries.csv
│   ├── drivers.csv
│   ├── orders.csv
│   ├── payments.csv
│   └── reviews.csv
├── docs/
│   ├── data_dictionary.md
│   └── business_insights.md
├── notebooks/
│   ├── eda_and_data_generation.ipynb
│   ├── customer_restaurant_segmentation.ipynb
│   ├── nlp_sentiment_analysis.ipynb
│   ├── regression_modeling.ipynb
│   └── time_series_forecasting.ipynb
├── scripts/
│   └── generate_data.py
├── .gitignore
└── README.md
```

## 3. Tech Stack & Environment Setup
* **Language & Core Analytics:** Python 3.9+, Pandas, and NumPy for data manipulation and tabular transformations.
* **Machine Learning & Preprocessing:** Scikit-learn for K-Means, DBSCAN, PCA, Linear Regression, Ridge, Lasso, and Random Forest modeling.
* **Natural Language Processing:** NLTK and VADER for text preprocessing, tokenization, lemmatization, and sentiment extraction.
* **Time-Series Analysis:** Statsmodels for stationarity diagnostics (ADF), seasonal decomposition, and ARIMA modeling, alongside Prophet for holiday and cycle-aware forecasting.
* **Visualization & Version Control:** Matplotlib and Seaborn for diagnostic charts, managed entirely through Git and GitHub.

## 4. End-to-End Workflow & Module Breakdown
* **Data Generation & Git:** Schema architecture, prompt engineering for realistic synthetic multi-table datasets, and feature branch versioning.
* **Segmentation:** Feature scaling via StandardScaler, K-Means clustering tuned by Elbow and Silhouette metrics, DBSCAN noise detection, and PCA 2D visualization.
* **NLP Sentiment:** Review cleaning (tokenization, stop-word removal, lemmatization), TF-IDF feature extraction, Naive Bayes classification, and VADER lexicon scoring.
* **Supervised Regression:** Relational dataset merging, feature encoding, and benchmarked tip prediction using Linear, Ridge, Lasso, and Random Forest models.
* **Time-Series Forecasting:** Daily order aggregation, ADF stationarity testing, additive seasonal decomposition, and comparative 14-day projections via ARIMA and Prophet.

## 5. Model Performance Summary
* **Segmentation:** K-Means achieved the highest cluster separation score, cleanly identifying key segments like "Premium Frequent Diners".
* **NLP Sentiment:** VADER delivered superior classification on short, informal reviews by capturing punctuation, capitalization, and emoji sentiment weights.
* **Supervised Regression:** Random Forest Regressor outperformed Linear, Ridge, and Lasso baselines, minimizing MAE and RMSE by capturing non-linear feature interactions.
* **Demand Forecasting:** Prophet outperformed ARIMA on out-of-sample RMSE, demonstrating better handling of 7-day cyclical patterns and business trends.

## 6. Strategic Business Insights & Recommendations
* **Dynamic Courier Allocation:** Deploy additional driver incentives during recurring weekend dinner spikes (6:00 PM – 9:00 PM) to minimize delivery delays.
* **High-Value Loyalty Programs:** Provide targeted subscription perks and fee waivers for the "Premium Frequent Diners" cohort to increase customer lifetime value.
* **Vendor Operations Auditing:** Implement performance interventions for restaurant clusters exhibiting prolonged kitchen prep times and elevated cancellation rates.
* **Proactive ETA Communication:** Leverage weather and traffic variables directly in dispatch calculations to maintain accurate customer expectations and reduce negative reviews.

## 7. Model Limitations & Future Scope
* **Synthetic Constraints:** Generated data cannot replicate all edge cases, unusual human behaviors, or operational anomalies found in real-world platforms.
* **Time-Series Horizon:** Baseline statistical forecasting assumes trend stability and requires retraining during major macroeconomic shocks.
* **Deep Learning Expansion:** Future iterations can implement Transformer models (e.g., BERT) to detect complex semantic sentiment and sarcasm in customer reviews.
* **Production Deployment:** Future scope involves containerizing the pipeline with Docker and exposing endpoints via FastAPI for real-time inference.

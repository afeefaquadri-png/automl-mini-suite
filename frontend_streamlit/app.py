import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, SVC
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

st.set_page_config(page_title="AutoML Suite", layout="wide")
st.title("🤖 AutoML Mini Suite")

# Tabs for Train and Predict
tab1, tab2 = st.tabs(["Train Model", "Predict"])

# ------------------- TRAIN TAB -------------------
with tab1:
    st.header("Train a New Model")

    train_file = st.file_uploader("Upload your training CSV file", type=["csv"], key="train")

    if train_file:
        df = pd.read_csv(train_file)
        st.success("Training file uploaded!")
        st.dataframe(df.head())

        target_col = st.selectbox("Select Target Column", df.columns)

        if st.button("Train Model"):
            X = df.drop(columns=[target_col])
            y = df[target_col]

            # Handle missing values
            X = X.fillna(0)
            y = y.fillna(0)

            # Encode categorical features
            X_encoded = pd.get_dummies(X)

            # Encode target if categorical
            le = None
            if y.dtype == "object":
                le = LabelEncoder()
                y = le.fit_transform(y)
                model_type = "Classification"
                model_choice = st.selectbox("Select Classification Model", ["Logistic Regression", "SVM"])
                model = LogisticRegression(max_iter=1000) if model_choice == "Logistic Regression" else SVC()
            else:
                model_type = "Regression"
                model_choice = st.selectbox("Select Regression Model", ["Linear Regression", "SVR"])
                model = LinearRegression() if model_choice == "Linear Regression" else SVR()

            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=0.2, random_state=42
            )

            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            st.subheader("📊 Results")
            st.write("Model Type:", model_type)
            st.write("Selected Model:", model_choice)

            if model_type == "Regression":
                rmse = np.sqrt(mean_squared_error(y_test, preds))
                st.success(f"RMSE: {rmse:.4f}")
            else:
                acc = accuracy_score(y_test, preds)
                st.success(f"Accuracy: {acc:.4f}")

            # Save model package
            model_package = {
                "model": model,
                "feature_columns": X_encoded.columns.tolist(),
                "label_encoder": le
            }
            joblib.dump(model_package, "best_model.joblib")
            st.success("✅ Model saved as 'best_model.joblib'")
            st.download_button(
                label="Download Model",
                data=open("best_model.joblib", "rb").read(),
                file_name="best_model.joblib"
            )

# ------------------- PREDICT TAB -------------------
with tab2:
    st.header("Make Predictions with Saved Model")

    uploaded_model = st.file_uploader("Upload saved model (.joblib)", type=["joblib"], key="model")
    pred_file = st.file_uploader("Upload CSV for prediction", type=["csv"], key="predict")

    if uploaded_model and pred_file:
        model_package = joblib.load(uploaded_model)
        model = model_package["model"]
        feature_columns = model_package["feature_columns"]
        le = model_package["label_encoder"]

        df_pred = pd.read_csv(pred_file)
        st.subheader("Prediction Data Preview")
        st.dataframe(df_pred.head())

        # Encode categorical features same as training
        df_encoded = pd.get_dummies(df_pred)
        # Add missing columns if necessary
        for col in feature_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[feature_columns]  # Ensure same column order

        predictions = model.predict(df_encoded)

        # If classification with label encoder
        if le:
            predictions = le.inverse_transform(predictions.astype(int))

        st.subheader("Predictions")
        st.dataframe(pd.DataFrame(predictions, columns=["Prediction"]))

        # Allow download
        pred_df = df_pred.copy()
        pred_df["Prediction"] = predictions
        st.download_button(
            label="Download Predictions",
            data=pred_df.to_csv(index=False).encode("utf-8"),
            file_name="predictions.csv"
        )


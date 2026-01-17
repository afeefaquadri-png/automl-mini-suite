import streamlit as st
import pandas as pd
import numpy as np
import joblib
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, SVC
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="AutoML Mini Suite", layout="wide")
st.title("🤖 AutoML Mini Suite")

tab1, tab2 = st.tabs(["Train Model", "Predict"])

# ======================= TRAIN TAB =======================
with tab1:
    st.header("Train a New Model")

    train_file = st.file_uploader(
        "Upload training CSV file",
        type=["csv"]
    )

    if train_file:
        df = pd.read_csv(train_file)
        st.dataframe(df.head())

        target_col = st.selectbox(
            "Select target column",
            df.columns
        )

        y_sample = df[target_col]
        is_classification = y_sample.dtype == "object"

        if is_classification:
            model_choice = st.selectbox(
                "Select Classification Model",
                ["Logistic Regression", "SVM"]
            )
        else:
            model_choice = st.selectbox(
                "Select Regression Model",
                ["Linear Regression", "SVR"]
            )

        @st.cache_resource
        def train_model(df, target_col, model_choice):
            X = df.drop(columns=[target_col]).fillna(0)
            y = df[target_col].fillna(0)
            X = pd.get_dummies(X)

            label_encoder = None
            if y.dtype == "object":
                label_encoder = LabelEncoder()
                y = label_encoder.fit_transform(y)
                model = LogisticRegression(max_iter=1000) if model_choice == "Logistic Regression" else SVC()
            else:
                model = LinearRegression() if model_choice == "Linear Regression" else SVR()

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            metrics = {}
            if label_encoder:
                metrics["Accuracy"] = accuracy_score(y_test, preds)
            else:
                metrics["RMSE"] = np.sqrt(mean_squared_error(y_test, preds))

            return {
                "model": model,
                "feature_columns": X.columns.tolist(),
                "label_encoder": label_encoder,
                "metrics": metrics
            }

        if st.button("Train Model"):
            with st.spinner("Training model..."):
                result = train_model(df, target_col, model_choice)

            st.success("Training completed!")

            for k, v in result["metrics"].items():
                st.metric(k, f"{v:.4f}")

            buffer = BytesIO()
            joblib.dump(result, buffer)
            buffer_bytes = buffer.getvalue()

            st.download_button(
                "Download Model",
                data=buffer_bytes,
                file_name="best_model.joblib",
                mime="application/octet-stream"
            )

# ======================= PREDICT TAB =======================
with tab2:
    st.header("Make Predictions")

    uploaded_model = st.file_uploader("Upload saved model (.joblib)", type=["joblib"])
    pred_file = st.file_uploader("Upload CSV for prediction", type=["csv"])

    if uploaded_model and pred_file:
        model_package = joblib.load(uploaded_model)

        model = model_package["model"]
        feature_columns = model_package["feature_columns"]
        label_encoder = model_package["label_encoder"]

        df_pred = pd.read_csv(pred_file)
        st.dataframe(df_pred.head())

        df_encoded = pd.get_dummies(df_pred)

        for col in feature_columns:
            if col not in df_encoded:
                df_encoded[col] = 0

        df_encoded = df_encoded[feature_columns]

        predictions = model.predict(df_encoded)

        if label_encoder:
            predictions = label_encoder.inverse_transform(predictions.astype(int))

        result_df = df_pred.copy()
        result_df["Prediction"] = predictions

        st.dataframe(result_df)
        st.download_button(
            "Download Predictions",
            data=result_df.to_csv(index=False),
            file_name="predictions.csv"
        )


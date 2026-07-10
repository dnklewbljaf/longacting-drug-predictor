import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Long-Acting Drug Predictor",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("website_predictions.csv")

df = load_data()

st.title("Long-Acting Drug Predictor")

st.write(
    """
    Search for a drug or compound to view:
    - Long-acting prediction
    - Model confidence
    - Physicochemical properties
    - Key factors influencing the prediction
    """
)

drug_name = st.text_input("Drug Name")

if drug_name:

    result = df[
        df["name"].astype(str).str.upper()
        ==
        drug_name.upper()
    ]

    if result.empty:

        st.error("Compound not found.")

    else:

        row = result.iloc[0]

        st.header("Prediction")

        if row["Prediction"] == "Likely Long-Acting":
            st.success(row["Prediction"])
        else:
            st.warning(row["Prediction"])

        st.metric(
            "Model Confidence",
            f"{row['Probability']:.1%}"
        )

        st.header("Why the Model Predicted This")

        reasons = []

        if row["MolecularWeight_g_mol_Combined_Avg_Percentile"] > 0.75:
            reasons.append("High molecular weight")

        if row["PolarSurfaceArea_A2_Combined_Avg_Percentile"] > 0.75:
            reasons.append("High polar surface area")

        if row["LogP_Combined_Avg_Percentile"] > 0.75:
            reasons.append("High lipophilicity (LogP)")

        if row["Solubility_g_L_Combined_Avg_Percentile"] < 0.25:
            reasons.append("Low aqueous solubility")

        if row["MeltingPoint_C_Combined_Avg_Percentile"] > 0.75:
            reasons.append("High melting point")

        if row["FractionUnionized_Base_pH7_4_Combined_Avg_Percentile"] < 0.25:
            reasons.append("Low fraction unionized base")

        if reasons:
            for reason in reasons:
                st.write("✅", reason)
        else:
            st.write("No dominant factors identified.")

        st.header("Physicochemical Properties")

        properties = pd.DataFrame({
            "Property": [
                "Molecular Weight",
                "Polar Surface Area",
                "LogP",
                "Solubility",
                "Acidic pKa",
                "Basic pKa",
                "

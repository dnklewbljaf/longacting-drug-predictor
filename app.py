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

def get_interpretation(probability):

    if probability >= 0.50:
        return "Likely a Very Strong Candidate"

    elif probability >= 0.20:
        return "Likely a Strong Candidate"

    elif probability >= 0.05:
        return "Likely a Moderate Candidate"

    elif probability >= 0.01:
        return "Likely a Challenging Candidate"

    else:
        return "Likely a Very Challenging Candidate"

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

        probability = row["Probability"]

        st.metric(
            "Model Confidence",
            f"{probability:.2%}"
        )

        st.info(
            f"Interpretation: {get_interpretation(probability)}"
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
                "Fraction Unionized Acid",
                "Fraction Unionized Base",
                "H-Bond Ratio",
                "Melting Point"
            ],
            "Value": [
                row["MolecularWeight_g_mol_Combined_Avg"],
                row["PolarSurfaceArea_A2_Combined_Avg"],
                row["LogP_Combined_Avg"],
                row["Solubility_g_L_Combined_Avg"],
                row["Acidic_pKa_Combined_Avg"],
                row["Basic_pKa_Combined_Avg"],
                row["FractionUnionized_Acid_pH7_4_Combined_Avg"],
                row["FractionUnionized_Base_pH7_4_Combined_Avg"],
                row["HBondRatio_Donor_Acceptor_Combined_Avg"],
                row["MeltingPoint_C_Combined_Avg"]
            ]
        })

        st.dataframe(
            properties,
            use_container_width=True
        )
st.subheader("How It Works")

st.markdown("""
- A machine learning model was trained on physicochemical property data from long-acting and non-long-acting FDA-approved small-molecule drugs.
- The model uses patterns in FDA-approved drugs to predict whether a molecule might be long-acting based on its physicochemical properties.
- The model's threshold between predicted non-long-acting and predicted long-acting is **0.05 (5%)**.
- **Model Confidence Interpretation**
    - **≥ 50%:** Likely a Very Strong Candidate
    - **20–50%:** Likely a Strong Candidate
    - **5–20%:** Likely a Moderate Candidate
    - **1–5% (not including exactly 5%):** Likely a Challenging Candidate
    - **< 1%:** Likely a Very Challenging Candidate
""")

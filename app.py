import streamlit as st
import pandas as pd

from autogluon.tabular import TabularPredictor

# ====================================
# LOAD MODEL
# ====================================

predictor = TabularPredictor.load(
    "ag-20260708_232811"
)

THRESHOLD = 0.05

# ====================================
# LOAD DATA
# ====================================

df = pd.read_csv(
    "website_prediction_dataset.csv"
)

# ====================================
# PAGE TITLE
# ====================================

st.title(
    "Long-Acting Drug Predictor"
)

st.write(
    "Enter the name of a compound."
)

# ====================================
# INPUT
# ====================================

drug_name = st.text_input(
    "Drug Name"
)

# ====================================
# SEARCH
# ====================================

if drug_name:

    matches = df[
        df["Name"]
        .astype(str)
        .str.upper()
        ==
        drug_name.upper()
    ]

    if len(matches) == 0:

        st.error(
            "Compound not found."
        )

    else:

        row = matches.iloc[[0]]

        model_inputs = row[
        [
            "PolarSurfaceArea_A2_Combined_Avg",
            "Solubility_g_L_Combined_Avg",
            "FractionUnionized_Acid_pH7_4_Combined_Avg",
            "FractionUnionized_Base_pH7_4_Combined_Avg",
            "MolecularWeight_g_mol_Combined_Avg",
            "Acidic_pKa_Combined_Avg",
            "Basic_pKa_Combined_Avg",
            "LogP_Combined_Avg",
            "HBondRatio_Donor_Acceptor_Combined_Avg"
        ]
        ]

        probability = predictor.predict_proba(
            model_inputs
        )[1].iloc[0]

        prediction = (
            probability >= THRESHOLD
        )

        st.header(
            "Prediction"
        )

        if prediction:

            st.success(
                "Predicted Long-Acting"
            )

        else:

            st.warning(
                "Predicted Not Long-Acting"
            )

        st.metric(
            "Probability",
            f"{probability:.1%}"
        )

        st.header(
            "Physicochemical Properties"
        )

        st.dataframe(
            model_inputs.T
        )

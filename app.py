import streamlit as st
import pickle
import matplotlib.pyplot as plt

# ------------------ Data Mappings ------------------
d1 = {'Comprehensive': 0,'Zero Dep': 1,'Third Party': 3,'Third Party insurance': 2,'Not Available': 4}
d2 = {'First Owner': 1,'Second Owner': 2,'Third Owner': 3,'Fourth Owner': 4, 'Fifth Owner': 5}
d3 = {'Petrol': 0,'Diesel': 1,'CNG': 2}
d4 = {'Manual': 0,'Automatic': 1}

# ------------------ Load Model ------------------
final_model = pickle.load(open('Final_model.pkl', 'rb'))

# ------------------ Page Config ------------------
st.set_page_config(page_title="Car Price Predictor", layout="centered")

# ------------------ Dark Theme ------------------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
.block-container {
    max-width: 700px;
    margin: auto;
}

/* Center button */
.stButton>button {
    width: 100%;
    height: 45px;
    font-size: 16px;
    background-color: black;
    color: white;
}

/* Result box */
.result-box {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title(" Car Price Predictor")
st.markdown("### Predict your car price")

# ------------------ INPUT FORM ------------------
insurance_validity = st.selectbox("Insurance Validity", list(d1.keys()))
ownership = st.selectbox("Ownership", list(d2.keys()))
fuel_type = st.selectbox("Fuel Type", list(d3.keys()))
transmission = st.selectbox("Transmission", list(d4.keys()))
kms_driven = st.slider("Kms Driven", 0, 200000, 50000)

predict_btn = st.button("Predict Price")

# ------------------ OUTPUT (BOTTOM CENTER) ------------------
if predict_btn:
    try:
        iv = d1[insurance_validity]
        own = d2[ownership]
        fuel = d3[fuel_type]
        trans = d4[transmission]

        test = [[iv, own, fuel, kms_driven, trans]]
        yp = int(final_model.predict(test)[0])

        # ---- RESULT BOX ----
        st.markdown(f"""
        <div class="result-box">
            <h2>💰 Estimated Price</h2>
            <h1>₹ {yp} Lakhs</h1>
        </div>
        """, unsafe_allow_html=True)

        # ---- SMALL HISTOGRAM ----
        factors = ['Ins', 'Own', 'Fuel', 'Kms', 'Trans']
        values = [iv, own, fuel, kms_driven/10000, trans]

        fig, ax = plt.subplots(figsize=(4,2))  # 👈 small size
        ax.bar(factors, values)
        ax.set_title("Impact", fontsize=10)

        st.pyplot(fig)

    except:
        st.error("Please enter valid input!")
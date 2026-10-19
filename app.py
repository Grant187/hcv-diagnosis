import streamlit as st
import pandas as pd
import joblib
 
st.set_page_config(page_title="HCV Diagnosis", layout="centered")
 
@st.cache_resource
def load_model():
    return joblib.load("hcv_model.joblib")
 
model = load_model()
 
st.title("Chan doan benh gan do viem gan C")
st.caption("Cong cu ho tro sang loc cho bai tap, KHONG thay the chan doan cua bac si.")
 
# bo so mau de demo nhanh (thay bang so ban in ra o Buoc 13)
SAMPLES = {
    "Nhap tay": None,
    "Mau KHOE": dict(Age=59, Sex="Nam", ALB=43.8, ALP=46.6, ALT=28.3, AST=27.4,
                     BIL=6.1, CHE=10.56, CHOL=5.47, CREA=83.0, GGT=20.3, PROT=78.5),
    "Mau BENH": dict(Age=61, Sex="Nữ", ALB=50.0, ALP=34.4, ALT=27.4, AST=114.4,
                     BIL=22.0, CHE=9.48, CHOL=4.62, CREA=61.9, GGT=169.8, PROT=86.0),
}
choice = st.selectbox("Chon du lieu mau", list(SAMPLES.keys()))
s = SAMPLES[choice] or dict(Age=45, Sex="Nam", ALB=42.0, ALP=65.0, ALT=23.0, AST=25.0,
                            BIL=7.0, CHE=8.4, CHOL=5.4, CREA=78.0, GGT=21.0, PROT=72.0)
 
c1, c2 = st.columns(2)
age  = c1.number_input("Tuoi (nam)", 18, 100, int(s["Age"]))
sex  = c2.selectbox("Gioi tinh", ["Nam", "Nu"], index=0 if s["Sex"] == "Nam" else 1)
alb  = c1.number_input("ALB - Albumin (g/L)", 0.0, 100.0, float(s["ALB"]))
alp  = c2.number_input("ALP (U/L)", 0.0, 500.0, float(s["ALP"]))
alt  = c1.number_input("ALT (U/L)", 0.0, 500.0, float(s["ALT"]))
ast  = c2.number_input("AST (U/L)", 0.0, 800.0, float(s["AST"]))
bil  = c1.number_input("BIL - Bilirubin (umol/L)", 0.0, 500.0, float(s["BIL"]))
che  = c2.number_input("CHE (kU/L)", 0.0, 30.0, float(s["CHE"]))
chol = c1.number_input("CHOL (mmol/L)", 0.0, 20.0, float(s["CHOL"]))
crea = c2.number_input("CREA (umol/L)", 0.0, 1500.0, float(s["CREA"]))
ggt  = c1.number_input("GGT (U/L)", 0.0, 1000.0, float(s["GGT"]))
prot = c2.number_input("PROT (g/L)", 0.0, 120.0, float(s["PROT"]))
 
if st.button("Du doan"):
    X = pd.DataFrame([{
        "Age": age, "Sex": 1 if sex == "Nam" else 0, "ALB": alb, "ALP": alp,
        "ALT": alt, "AST": ast, "BIL": bil, "CHE": che, "CHOL": chol,
        "CREA": crea, "GGT": ggt, "PROT": prot}])
    p = model.predict_proba(X)[0, 1]
    st.progress(float(p))
    st.metric("Xac suat co benh gan do HCV", f"{p:.1%}")
    if p >= 0.5:
        st.error("Mo hinh du doan: CO NGUY CO benh. Nen di kham bac si.")
    else:
        st.success("Mo hinh du doan: it co nguy co benh.")
    st.caption("Day chi la ket qua tham khao tu mo hinh hoc may.")

import streamlit as st
import pandas as pd
import category_encoders as ce

# Web ilova sarlavhasi
st.title("📊 Kategorikal Encoding Web Ilovasi")

# Excel faylni yuklash
uploaded_file = st.file_uploader("📥 Excel faylni yuklang (.xls yoki .xlsx)", type=["xls", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("🔍 **Yuklangan ma'lumotlar:**", df.head())

    # Kategorik ustunlarni aniqlash
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    if not categorical_columns:
        st.warning("❌ Jadvalda kategorik ustunlar topilmadi!")
    else:
        # Foydalanuvchidan ustunlarni tanlash
        columns_to_encode = st.multiselect("📌 Kodlanishi kerak bo'lgan ustunlarni tanlang:", categorical_columns)

        if columns_to_encode:
            # Encoding usullarini tanlash
            encoding_methods = {
                "One-Hot Encoding": ce.OneHotEncoder,
                "Label Encoding": ce.OrdinalEncoder,
                "Target Encoding": ce.TargetEncoder,
                "Frequency Encoding": "custom_frequency",
                "Ordinal Encoding": ce.OrdinalEncoder,
                "Dummy Encoding": ce.OneHotEncoder,
                "Count Encoding": "custom_count",
                "Leave-One-Out Encoding": ce.LeaveOneOutEncoder,
                "Binary Encoding": ce.BinaryEncoder,
                "Effect Encoding": ce.SumEncoder,
                "Base-N Encoding": ce.BaseNEncoder,
                "Gray Encoding": ce.BaseNEncoder,
                "Hash Encoding": ce.HashingEncoder,
                "Mean Encoding": "custom_mean",
                "Helmert Encoding": ce.HelmertEncoder
            }

            encoding_choice = st.selectbox("🔢 Qaysi encoding usulini tanlaysiz?", list(encoding_methods.keys()))

            if st.button("🚀 Kodlashni boshlash"):
                df_encoded = df.copy()

                # Maxsus encoding usullari
                if encoding_choice in ["Frequency Encoding", "Count Encoding", "Mean Encoding"]:
                    if encoding_choice == "Frequency Encoding":
                        for col in columns_to_encode:
                            df_encoded[col + "_freq"] = df_encoded[col].map(df_encoded[col].value_counts(normalize=True))
                    elif encoding_choice == "Count Encoding":
                        for col in columns_to_encode:
                            df_encoded[col + "_count"] = df_encoded[col].map(df_encoded[col].value_counts())
                    elif encoding_choice == "Mean Encoding":
                        target_col = st.text_input("🎯 Maqsad ustunini kiriting (target encoding uchun): ")
                        if target_col in df.columns:
                            for col in columns_to_encode:
                                df_encoded[col + "_mean"] = df_encoded.groupby(col)[target_col].transform('mean')
                        else:
                            st.warning("❌ Noto‘g‘ri target ustuni nomi!")
                else:
                    if encoding_choice == "Target Encoding" or encoding_choice == "Leave-One-Out Encoding":
                        target_col = st.text_input("🎯 Maqsad ustunini kiriting (target encoding uchun): ")
                        if target_col in df.columns:
                            encoder = encoding_methods[encoding_choice](cols=columns_to_encode)
                            df_encoded = encoder.fit_transform(df_encoded[columns_to_encode], df[target_col])
                        else:
                            st.warning("❌ Noto‘g‘ri target ustuni nomi!")
                    else:
                        encoder = encoding_methods[encoding_choice](cols=columns_to_encode)
                        df_encoded = encoder.fit_transform(df_encoded)

                st.success("✅ Kodlash bajarildi!")
                st.write("📊 **Kodlangan ma'lumotlar:**", df_encoded.head())

                 # Natijani yuklab olish
                st.download_button(
                    label="📥 Kodlangan faylni yuklab olish",
                    data=df_encoded.to_csv(index=False).encode('utf-8'),
                    file_name="encoded_data.csv",
                    mime="text/csv"
                )
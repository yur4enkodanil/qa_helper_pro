import streamlit as st
import base64
from modules.i18n import get_text

def render_base64_lab():
    t = get_text

    st.subheader(t("base64_header"))

    col1, col2 = st.columns(2)

    # --- КОЛОНКА КОДИРОВАНИЯ ---
    with col1:
        st.markdown(f"#### {t('base64_encode_header')}")
        
        encode_input = st.text_area(
            t("base64_input_label"), 
            height=200, 
            key="b64_encode_in",
            placeholder="Hello, World!"
        )

        if st.button(t("base64_button_encode"), use_container_width=True, key="b64_encode_btn"):
            if encode_input:
                try:
                    encoded_bytes = base64.b64encode(encode_input.encode('utf-8'))
                    encoded_str = encoded_bytes.decode('utf-8')
                    st.code(encoded_str, language="text")
                except Exception as e:
                    st.error(e)

    # --- КОЛОНКА ДЕКОДИРОВАНИЯ ---
    with col2:
        st.markdown(f"#### {t('base64_decode_header')}")

        decode_input = st.text_area(
            t("base64_input_label"), 
            height=200, 
            key="b64_decode_in",
            placeholder="SGVsbG8sIFdvcmxkIQ=="
        )

        if st.button(t("base64_button_decode"), use_container_width=True, key="b64_decode_btn"):
            if decode_input:
                try:
                    # Добавляем padding, если его не хватает
                    missing_padding = len(decode_input) % 4
                    if missing_padding:
                        decode_input += '=' * (4 - missing_padding)
                    
                    decoded_bytes = base64.b64decode(decode_input)
                    decoded_str = decoded_bytes.decode('utf-8')
                    st.code(decoded_str, language="text")
                except Exception:
                    st.error(t("base64_decode_error"))

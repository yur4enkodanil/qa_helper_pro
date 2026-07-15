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
            height=150, 
            key="b64_encode_in",
            placeholder="Hello, World!"
        )

        uploaded_file = st.file_uploader(t("base64_file_uploader_label"), key="b64_file_up")

        if st.button(t("base64_button_encode"), key="b64_encode_btn", width='stretch'):
            source_bytes = None
            if uploaded_file is not None:
                source_bytes = uploaded_file.getvalue()
            elif encode_input:
                source_bytes = encode_input.encode('utf-8')

            if source_bytes is not None:
                try:
                    encoded_bytes = base64.b64encode(source_bytes)
                    encoded_str = encoded_bytes.decode('utf-8')
                    st.text_area(t("base64_result_label"), value=encoded_str, height=150, key="b64_encode_out")
                except Exception:
                    st.error(t("base64_encode_error"))

    # --- КОЛОНКА ДЕКОДИРОВАНИЯ ---
    with col2:
        st.markdown(f"#### {t('base64_decode_header')}")

        decode_input = st.text_area(
            t("base64_input_label"), 
            height=200, 
            key="b64_decode_in",
            placeholder="SGVsbG8sIFdvcmxkIQ=="
        )

        if st.button(t("base64_button_decode"), key="b64_decode_btn", width='stretch'):
            if decode_input:
                try:
                    # Убираем пробелы и переносы строк, которые могут мешать
                    clean_input = "".join(decode_input.split())

                    # Добавляем padding, если его не хватает
                    missing_padding = len(clean_input) % 4
                    if missing_padding:
                        clean_input += '=' * (4 - missing_padding)
                    
                    decoded_bytes = base64.b64decode(clean_input)
                    
                    # Пытаемся декодировать как текст
                    try:
                        decoded_str = decoded_bytes.decode('utf-8')
                        st.code(decoded_str, language="text")
                    except UnicodeDecodeError:
                        # Если не получилось - это бинарные данные
                        st.warning(t("base64_decode_binary_warning"))
                        st.download_button(
                            label=t("base64_download_binary_button"),
                            data=decoded_bytes,
                            file_name="decoded.bin",
                            mime="application/octet-stream"
                        )
                except (base64.binascii.Error, ValueError):
                    st.error(t("base64_decode_error"))

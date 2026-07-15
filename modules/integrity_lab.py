import streamlit as st
import hashlib
from modules.i18n import get_text

def get_bytes_hash(file_bytes, algo="sha256"):
    """Calculates hash from bytes for various algorithms."""
    if algo == "md5":
        hash_func = hashlib.md5()
    elif algo == "sha1":
        hash_func = hashlib.sha1()
    elif algo == "sha512":
        hash_func = hashlib.sha512()
    else:  # default to sha256
        hash_func = hashlib.sha256()

    hash_func.update(file_bytes)
    return hash_func.hexdigest()

def render_integrity_lab():
    t = get_text
    st.subheader(t("hash_header"))

    # 1. File Uploader
    uploaded_file = st.file_uploader(t("hash_upload_label"), type=None, key="hash_file_uploader")

    # 2. Algorithm and Expected Hash inputs
    col1, col2 = st.columns(2)
    with col1:
        # Adding more algorithms
        algo = st.selectbox(
            t("hash_algo_label"),
            ["sha256", "md5", "sha1", "sha512"],
            index=0
        )
    with col2:
        expected_hash = st.text_input(
            t("hash_expected_label"),
            placeholder=t("hash_expected_placeholder")
        ).strip().lower()

    # 3. Automatic calculation and comparison
    if uploaded_file is not None:
        with st.spinner(t("hash_spinner")):
            try:
                file_bytes = uploaded_file.getvalue()
                calculated_hash = get_bytes_hash(file_bytes, algo)

                st.success(t("hash_success"))
                st.code(calculated_hash, language="text")

                # Comparison logic
                if expected_hash:
                    if calculated_hash == expected_hash:
                        st.success(t("hash_match"))
                    else:
                        st.error(t("hash_mismatch"))

            except Exception as e:
                st.error(f"{t('hash_error_read')}: {e}")
    else:
        st.info(t("hash_warn_no_file"))
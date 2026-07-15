import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs
from modules.i18n import get_text

def highlight_last_row(row):
    """Applies a style to the last row of a DataFrame."""
    if row.name == len(row.index) -1 : # Check if it's the last row
        return ['background-color: #2E4A2E; font-weight: bold'] * len(row)
    return [''] * len(row)

def render_link_lab():
    t = get_text
    st.subheader(t("link_lab_header"))
    
    url_input = st.text_input(
        t("link_lab_url_label"), 
        placeholder="https://example.com/promo?utm_source=tg&utm_medium=post"
    )

    if url_input:
        # Простейшая валидация протокола
        if not url_input.startswith(("http://", "https://")):
            st.error("⚠️ URL must start with http:// or https://")
            return

        # --- LIVE PARAMETER PARSING ---
        st.markdown(f"#### {t('link_lab_params_header')}")
        parsed_url = urlparse(url_input)
        params = parse_qs(parsed_url.query)
        
        st.markdown(f"{t('link_lab_base_url')} `{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}`")
        
        if params:
            param_data = [{t("link_lab_params_table_param"): k, t("link_lab_params_table_value"): v[0]} for k, v in params.items()]
            st.dataframe(pd.DataFrame(param_data), use_container_width=True, hide_index=True)
            
            has_utm = any(p.startswith("utm_") for p in params.keys())
            if has_utm:
                st.info(t("link_lab_utm_info"))
        else:
            st.write(t("link_lab_no_params"))

        st.divider()

        # --- REDIRECT TRACING ---
        st.markdown(f"#### {t('link_lab_redirects_header')}")
        if st.button(t("link_lab_button_trace")):
            try:
                with st.spinner(t("link_lab_spinner_text")):
                    response = requests.get(url_input, allow_redirects=True, timeout=10)
                    
                    chain = []
                    for resp in response.history:
                        chain.append({
                            t("link_lab_table_status"): resp.status_code,
                            t("link_lab_table_url"): resp.url,
                            t("link_lab_table_type"): t("link_lab_redirect_type_redirect"),
                            t("link_lab_table_time"): f"{resp.elapsed.total_seconds() * 1000:.0f} ms"
                        })
                    
                    chain.append({
                        t("link_lab_table_status"): response.status_code,
                        t("link_lab_table_url"): response.url,
                        t("link_lab_table_type"): t("link_lab_redirect_type_final"),
                        t("link_lab_table_time"): f"{response.elapsed.total_seconds() * 1000:.0f} ms"
                    })
                    
                    df = pd.DataFrame(chain)
                    
                    # Apply styling to highlight the last row
                    st.dataframe(df.style.apply(highlight_last_row, axis=1), use_container_width=True, hide_index=True)
                    
                    if len(response.history) == 0:
                        st.success(t("link_lab_no_redirects"))
            except Exception as e:
                st.error(t("link_lab_error_request").format(e=e))


    st.divider()
    with st.expander(t("link_lab_guide_header")):
        st.markdown(t("link_lab_guide_content"))
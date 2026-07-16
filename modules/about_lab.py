import streamlit as st
from modules.i18n import get_text
import json
import os

def render_about_lab():
    t = get_text
    
    st.header(t("about_header"))
    st.subheader(t("about_subheader"))
    st.markdown(t("about_desc"))
    st.divider()

    st.markdown(f"### {t('about_modules_header')}")

    # Dynamically create the list of modules from the tools_config.json file
    module_keys = []
    try:
        # Correctly locate tools_config.json from the project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(project_root, "tools_config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            tools_config = json.load(f)
        # Get description keys, filtering out any entries that might not have one
        module_keys = [tool['desc_key'] for tool in tools_config if 'desc_key' in tool]
    except Exception as e:
        st.error(f"Could not load module descriptions: {e}")
    
    module_list_md = "\n".join([f"* {t(key)}" for key in module_keys])
    st.markdown(module_list_md)

    st.divider()

    st.markdown(f"### {t('about_author_header')}")
    st.markdown(t("about_author_desc"))
    st.write(f"**Email:** {t('about_author_email')}")
    st.write(f"**Telegram:** {t('about_author_telegram')}")

    app_version = st.session_state.get("app_version", "2.2.1")
    st.divider()
    st.caption(f"v{app_version} Stable | Created with passion for Quality Assurance")
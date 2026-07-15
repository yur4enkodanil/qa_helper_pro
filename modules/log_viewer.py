import streamlit as st
import os
from modules.i18n import get_text

def render_log_viewer():
    """
    Отображает содержимое файла логов и позволяет его очистить, обновить и скачать.
    """
    t = get_text

    st.subheader(t("log_viewer_header"))
    st.info(t("log_viewer_info"))

    # Путь к лог-файлу в корневой папке проекта
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    log_file_path = os.path.join(project_root, "qa_helper_pro.log")

    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r", encoding="utf-8") as f:
                log_content = f.read()
            
            # Отображение контента лога
            if log_content:
                st.code(log_content, language="log")
            else:
                st.success(t("log_viewer_no_errors"))

            # Кнопки действий
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(t("log_viewer_refresh_button"), width='stretch'):
                    st.rerun()
            
            with col2:
                # Кнопка скачивания активна, только если есть что скачивать
                st.download_button(
                    label=t("log_viewer_download_button"),
                    data=log_content.encode('utf-8'),
                    file_name="qa_helper_pro.log",
                    mime="text/plain",
                    width='stretch',
                    disabled=not log_content
                )

            with col3:
                if st.button(t("log_viewer_clear_button"), width='stretch', type="secondary"):
                    with open(log_file_path, "w", encoding="utf-8") as f:
                        f.write("")
                    st.rerun()

        except Exception as e:
            st.error(f"{t('log_viewer_read_error')}{e}")
    else:
        st.success(t("log_viewer_not_created"))
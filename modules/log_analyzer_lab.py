import streamlit as st
import re
from modules.i18n import get_text

def highlight_text(text, query):
    """Подсвечивает поисковый запрос в тексте, игнорируя регистр."""
    if not query:
        return text
    try:
        # Используем re.sub для регистронезависимой замены и подсветки
        highlighted_text = re.sub(f'({re.escape(query)})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
        return highlighted_text
    except re.error:
        # Возврат к обычному тексту, если в запросе некорректное регулярное выражение
        return text

def _process_log_content(log_content):
    """Хелпер для анализа контента и обновления состояния."""
    t = get_text
    with st.spinner(t("log_analyzer_processing")):
        lines = log_content.splitlines()
        st.session_state.log_lines = lines
        
        # Расчет статистики
        stats = {
            'total': len(lines),
            'error': len([l for l in lines if 'error' in l.lower()]),
            'warn': len([l for l in lines if 'warn' in l.lower()]),
            'info': len([l for l in lines if 'info' in l.lower()]),
            'debug': len([l for l in lines if 'debug' in l.lower()]),
        }
        st.session_state.log_stats = stats
    st.rerun()

def render_log_analyzer_lab():
    t = get_text
    st.subheader(t("log_analyzer_header"))

    # --- Инициализация состояния ---
    if 'log_lines' not in st.session_state:
        st.session_state.log_lines = []
    if 'log_stats' not in st.session_state:
        st.session_state.log_stats = {}

    # --- UI для загрузки логов ---
    tab_upload, tab_paste = st.tabs([t("log_analyzer_tab_upload"), t("log_analyzer_tab_paste")])

    with tab_upload:
        uploaded_file = st.file_uploader(t("log_analyzer_upload_label"), type=['log', 'txt'])
        if st.button(t("log_analyzer_button_file"), use_container_width=True, key="log_analyze_file"):
            if uploaded_file is not None:
                log_content = uploaded_file.getvalue().decode("utf-8", errors='ignore')
                _process_log_content(log_content)
            else:
                st.warning(t("log_analyzer_warn_no_file"))

    with tab_paste:
        pasted_text = st.text_area(t("log_analyzer_paste_label"), height=200)
        if st.button(t("log_analyzer_button_text"), use_container_width=True, key="log_analyze_text"):
            if pasted_text:
                _process_log_content(pasted_text)
            else:
                st.warning(t("log_analyzer_warn_no_text"))

    # --- Отображение, если логи загружены ---
    if st.session_state.log_lines:
        st.divider()
        
        # --- Блок статистики ---
        stats = st.session_state.log_stats
        st.markdown(f"#### {t('log_analyzer_stats_header')}")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric(t('log_analyzer_total_lines'), stats['total'])
        s2.metric("ERROR", stats['error'], delta_color="inverse" if stats['error'] > 0 else "off")
        s3.metric("WARN", stats['warn'], delta_color="inverse" if stats['warn'] > 0 else "off")
        s4.metric("INFO", stats['info'])
        s5.metric("DEBUG", stats['debug'])

        # --- Блок фильтров ---
        st.markdown(f"#### {t('log_analyzer_filters_header')}")
        search_query = st.text_input(t('log_analyzer_search_label'), placeholder=t('log_analyzer_search_placeholder'))
        selected_levels = st.multiselect(t('log_analyzer_levels_label'), options=['ERROR', 'WARN', 'INFO', 'DEBUG'])

        # --- Применение фильтров ---
        filtered_lines = [line for line in st.session_state.log_lines if (not search_query or search_query.lower() in line.lower()) and (not selected_levels or any(level.lower() in line.lower() for level in selected_levels))]

        # --- Отображение отфильтрованных логов ---
        st.info(t('log_analyzer_results_info').format(count=len(filtered_lines)))
        log_display_container = st.container(height=500, border=True)
        with log_display_container:
            for line in filtered_lines:
                color = "#ff4b4b" if 'error' in line.lower() else "#ffc400" if 'warn' in line.lower() else "#888888"
                st.markdown(f'<p style="color:{color}; font-family: monospace; white-space: pre; margin: 0;">{highlight_text(line, search_query)}</p>', unsafe_allow_html=True)
    else:
        st.info(t("log_analyzer_welcome_info"))

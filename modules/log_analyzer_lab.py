import streamlit as st
import re
from modules.i18n import get_text

def highlight_text(text, query, use_regex=False, case_sensitive=False):
    """Подсвечивает поисковый запрос в тексте с учетом опций."""
    if not query:
        return text
    try:
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = query if use_regex else re.escape(query)
        highlighted_text = re.sub(f'({pattern})', r'<mark>\1</mark>', text, flags=flags)
        return highlighted_text
    except re.error:
        st.error(f"Invalid Regex: {query}")
        return text

def get_log_level(line):
    """Определяет уровень лога в строке с помощью RegEx."""
    line_lower = line.lower()
    if re.search(r'\berror\b', line_lower): return 'error'
    if re.search(r'\bwarn(ing)?\b', line_lower): return 'warn'
    if re.search(r'\binfo\b', line_lower): return 'info'
    if re.search(r'\bdebug\b', line_lower): return 'debug'
    return 'unknown'

def _process_log_content(log_content, source):
    """Анализирует контент и обновляет состояние, избегая лишних rerun."""
    t = get_text
    with st.spinner(t("log_analyzer_processing")):
        lines = log_content.splitlines()
        st.session_state.log_lines = list(enumerate(lines, 1))

        stats = {
            'total': len(lines),
            'error': 0, 'warn': 0, 'info': 0, 'debug': 0, 'unknown': 0
        }
        for _, line in st.session_state.log_lines:
            level = get_log_level(line)
            stats[level] += 1

        st.session_state.log_stats = stats
        st.session_state.log_source_id = source # Отмечаем, что контент обработан

def render_log_analyzer_lab():
    t = get_text
    st.subheader(t("log_analyzer_header"))

    # --- Инициализация состояния ---
    for key, default in [('log_lines', []), ('log_stats', {}), ('log_pasted_text', ''), ('log_source_id', None)]:
        if key not in st.session_state:
            st.session_state[key] = default

    # --- UI для загрузки логов ---
    tab_upload, tab_paste = st.tabs([t("log_analyzer_tab_upload"), t("log_analyzer_tab_paste")])

    with tab_upload:
        uploaded_file = st.file_uploader(t("log_analyzer_upload_label"), type=['log', 'txt'], key="log_file_uploader")
        # Автоматический анализ при загрузке нового файла
        if uploaded_file is not None and uploaded_file.file_id != st.session_state.log_source_id:
            log_content = uploaded_file.getvalue().decode("utf-8", errors='ignore')
            _process_log_content(log_content, uploaded_file.file_id)
            st.rerun()

    with tab_paste:
        st.text_area(t("log_analyzer_paste_label"), height=200, key="log_pasted_text")
        # Автоматический анализ при изменении текста
        if st.session_state.log_pasted_text and hash(st.session_state.log_pasted_text) != st.session_state.log_source_id:
            _process_log_content(st.session_state.log_pasted_text, hash(st.session_state.log_pasted_text))
            st.rerun()

    # --- Отображение, если логи загружены ---
    if st.session_state.log_lines:
        st.divider()

        # --- Блок статистики ---
        stats = st.session_state.log_stats
        total = stats['total']
        st.markdown(f"#### {t('log_analyzer_stats_header')}")
        s1, s2, s3, s4, s5, s_clear = st.columns(6)
        s1.metric(t('log_analyzer_total_lines'), total)
        s2.metric(t('log_level_error'), stats['error'], f"{(stats['error']/total*100):.1f}%" if total > 0 else "0%", delta_color="inverse" if stats['error'] > 0 else "off")
        s3.metric(t('log_level_warn'), stats['warn'], f"{(stats['warn']/total*100):.1f}%" if total > 0 else "0%", delta_color="inverse" if stats['warn'] > 0 else "off")
        s4.metric(t('log_level_info'), stats['info'], f"{(stats['info']/total*100):.1f}%" if total > 0 else "0%")
        s5.metric(t('log_level_debug'), stats['debug'], f"{(stats['debug']/total*100):.1f}%" if total > 0 else "0%")
        with s_clear:
            st.write("") # Spacer
            if st.button(t("log_analyzer_clear_button"), width='stretch'):
                # Сбрасываем все связанные состояния
                for key in ['log_lines', 'log_stats', 'log_pasted_text', 'log_source_id', 'log_file_uploader']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        # --- Блок фильтров ---
        st.markdown(f"#### {t('log_analyzer_filters_header')}")
        f1, f2 = st.columns(2)
        search_query = f1.text_input(t('log_analyzer_search_label'), placeholder=t('log_analyzer_search_placeholder'))
        selected_levels = f2.multiselect(t('log_analyzer_levels_label'), options=['error', 'warn', 'info', 'debug'])

        c1, c2, c3 = st.columns(3)
        use_regex = c1.checkbox(t("log_analyzer_search_regex"), key="log_search_use_regex")
        case_sensitive = c2.checkbox(t("log_analyzer_search_case_sensitive"), key="log_search_case_sensitive")
        context_lines = c3.number_input(t("log_analyzer_context_lines"), min_value=0, max_value=50, value=0, help=t("log_analyzer_context_lines_help"))

        # --- Применение фильтров ---
        all_lines = st.session_state.log_lines
        matched_line_nums = set()
        lines_to_display_nums = set()

        # 1. Находим строки, соответствующие фильтрам
        if search_query or selected_levels:
            try:
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = search_query if use_regex else re.escape(search_query)
                
                for num, line in all_lines:
                    level = get_log_level(line)
                    level_match = not selected_levels or level in selected_levels
                    text_match = not search_query or re.search(pattern, line, flags)
                    
                    if level_match and text_match:
                        matched_line_nums.add(num)
            except re.error:
                # Ошибка уже обработана в highlight_text, здесь просто пропускаем
                pass

        # 2. Формируем список строк для отображения (с контекстом)
        if not search_query and not selected_levels:
            # Если фильтров нет, показываем все
            lines_to_display = all_lines
        else:
            for num in sorted(list(matched_line_nums)):
                start = max(1, num - context_lines)
                end = min(len(all_lines), num + context_lines)
                for i in range(start, end + 1):
                    lines_to_display_nums.add(i)
            
            lines_to_display = [line for num, line in all_lines if num in lines_to_display_nums]

        # --- Отображение отфильтрованных логов ---
        st.info(t('log_analyzer_results_info').format(count=len(lines_to_display)))
        log_display_container = st.container(height=500, border=True)
        with log_display_container:
            # Преобразуем обратно в список с кортежами для отображения
            display_data = [(num, line_text) for num, line_text in all_lines if num in lines_to_display_nums]

            for num, line in display_data:
                level = get_log_level(line)
                color_map = {'error': '#ff4b4b', 'warn': '#ffc400', 'info': '#fafafa', 'debug': '#888888', 'unknown': '#888888'}
                color = color_map[level]
                
                is_match = num in matched_line_nums
                opacity = 1.0 if is_match else 0.7
                
                line_num_html = f'<span style="color:#555; user-select: none; opacity: {opacity};">{num:>5}: </span>'
                
                # Подсвечиваем только строки, которые совпали с поиском
                display_line = highlight_text(line, search_query, use_regex, case_sensitive) if is_match else line
                
                st.markdown(f'<p style="color:{color}; font-family: monospace; white-space: pre; margin: 0; opacity: {opacity};">{line_num_html}{display_line}</p>', unsafe_allow_html=True)
    else:
        st.info(t("log_analyzer_auto_analysis_info"))

import streamlit as st
import json
import pandas as pd
import re
from modules.i18n import get_text

def fix_json(bad_json):
    if not bad_json: return ""
    # Удаляем комментарии, которые занимают всю строку (с учетом отступов)
    # Это безопаснее, чем удалять `//` везде, т.к. не затронет URL
    res = re.sub(r'^\s*//.*$', '', bad_json, flags=re.MULTILINE)
    # Заменяем одинарные кавычки на двойные, если они используются для ключей/строк
    res = res.replace("'", '"')
    # Удаляем висячие запятые
    res = re.sub(r',\s*([\]}])', r'\1', res)
    return res.strip()

def render_json_lab():
    logger = st.session_state.get('logger')
    t = get_text
    st.subheader(t("json_lab_header"))

    # Инициализируем версию виджета, чтобы "сбрасывать" его при фиксе
    if "json_widget_version" not in st.session_state:
        st.session_state["json_widget_version"] = 0
    if "json_content" not in st.session_state:
        st.session_state["json_content"] = ""
    
    # --- UI для загрузки/вставки ---
    tab_paste, tab_upload = st.tabs([t("json_lab_tab_paste"), t("json_lab_tab_upload")])

    with tab_upload:
        uploaded_file = st.file_uploader(t("json_lab_upload_label"), type=['json', 'txt'])
        if uploaded_file:
            try:
                content = uploaded_file.getvalue().decode("utf-8")
                st.session_state["json_content"] = content
                st.session_state["json_widget_version"] += 1
                st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}")

    with tab_paste:
        # Кнопки действий
        col_fix, col_clear, _ = st.columns([1, 1, 2])
        if col_fix.button(t("json_lab_button_fix"), width='stretch'):
            current_raw = st.session_state.get(f"json_area_{st.session_state['json_widget_version']}", "")
            fixed = fix_json(current_raw)
            st.session_state["json_content"] = fixed
            st.session_state["json_widget_version"] += 1
            if logger: logger("JSON Lab: Text fixed and updated")
            st.rerun()
        
        if col_clear.button(t("json_lab_button_clear"), width='stretch'):
            st.session_state["json_content"] = ""
            st.session_state["json_widget_version"] += 1
            st.rerun()

        # Текстовое поле с динамическим ключом
        json_input = st.text_area(
            t("json_lab_paste_label"), 
            value=st.session_state["json_content"],
            height=300, 
            key=f"json_area_{st.session_state['json_widget_version']}"
        )
        st.session_state["json_content"] = json_input

    if json_input:
        try:
            parsed_data = json.loads(json_input)
            st.success(t("json_lab_valid"))
            
            # --- РЕЖИМЫ ПРОСМОТРА ---
            c1, c2, c3 = st.columns(3)
            view_mode = c1.selectbox(t("json_lab_view_mode"), [t("json_lab_mode_tree"), t("json_lab_mode_pretty"), t("json_lab_mode_table")])
            sort_keys = c2.checkbox(t("json_lab_sort_keys"))
            
            if c3.button(t("json_lab_button_log"), width='stretch'):
                if logger: logger(f"JSON Lab: {view_mode} logged")

            st.divider()

            if view_mode == t("json_lab_mode_tree"):
                st.json(parsed_data, expanded=True)
            
            elif view_mode == t("json_lab_mode_pretty"):
                pretty_json = json.dumps(parsed_data, indent=4, ensure_ascii=False, sort_keys=sort_keys)
                st.code(pretty_json, language="json")

            elif view_mode == t("json_lab_mode_table"):
                try:
                    # json_normalize отлично справляется с вложенными структурами
                    df = pd.json_normalize(parsed_data)
                    st.dataframe(df, use_container_width=True)
                except:
                    # Если структура не подходит для normalize, пробуем обычный конструктор
                    df = pd.DataFrame(parsed_data)
                    st.dataframe(df, use_container_width=True)

        except json.JSONDecodeError as e:
            st.error(f"{t('json_lab_error_prefix')}: {str(e)}")
            st.info(t("json_lab_error_tip"))
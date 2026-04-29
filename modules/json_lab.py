import streamlit as st
import json
import pandas as pd
import re

def fix_json(bad_json):
    if not bad_json: return ""
    # Удаляем комментарии
    res = re.sub(r'//.*', '', bad_json)
    # Заменяем кавычки
    res = res.replace("'", '"')
    # Удаляем висячие запятые
    res = re.sub(r',\s*([\]}])', r'\1', res)
    return res.strip()

def render_json_lab():
    logger = st.session_state.get('logger')
    st.subheader("📦 JSON Formatter & Validator")

    # Инициализируем версию виджета, чтобы "сбрасывать" его при фиксе
    if "json_widget_version" not in st.session_state:
        st.session_state["json_widget_version"] = 0
    if "json_content" not in st.session_state:
        st.session_state["json_content"] = ""

    col_actions, _ = st.columns([1, 2])
    
    # Кнопка починки
    if col_actions.button("🔧 Попробовать починить (Auto-fix)", use_container_width=True):
        # Берем данные напрямую из текущего состояния виджета
        current_raw = st.session_state.get(f"json_area_{st.session_state['json_widget_version']}", "")
        fixed = fix_json(current_raw)
        st.session_state["json_content"] = fixed
        # Меняем версию, чтобы создать "новый" виджет с новым текстом
        st.session_state["json_widget_version"] += 1
        if logger: logger("JSON Lab: Текст исправлен и обновлен")
        st.rerun()

    # Текстовое поле с динамическим ключом
    json_input = st.text_area(
        "Вставьте сырой JSON сюда:", 
        value=st.session_state["json_content"],
        height=300, 
        key=f"json_area_{st.session_state['json_widget_version']}"
    )
    
    # Обновляем контент в памяти для других функций
    st.session_state["json_content"] = json_input

    if json_input:
        try:
            parsed_data = json.loads(json_input)
            st.success("✅ JSON валиден!")
            
            # --- РЕЖИМЫ ПРОСМОТРА ---
            c1, c2, c3 = st.columns(3)
            view_mode = c1.selectbox("Режим просмотра:", ["Дерево", "Текст (Pretty)", "Таблица"])
            sort_keys = c2.checkbox("Сортировать ключи")
            
            if c3.button("📋 В лог", use_container_width=True):
                if logger: logger(f"JSON Lab: {view_mode} залоггирован")

            st.divider()

            if view_mode == "Дерево":
                st.json(parsed_data, expanded=True)
            
            elif view_mode == "Текст (Pretty)":
                pretty_json = json.dumps(parsed_data, indent=4, ensure_ascii=False, sort_keys=sort_keys)
                st.code(pretty_json, language="json")

            elif view_mode == "Таблица":
                try:
                    # json_normalize отлично справляется с вложенными структурами
                    df = pd.json_normalize(parsed_data)
                    st.dataframe(df, use_container_width=True)
                except:
                    # Если совсем всё плохо, пробуем обычный конструктор
                    df = pd.DataFrame(parsed_data)
                    st.dataframe(df, use_container_width=True)

        except json.JSONDecodeError as e:
            st.error(f"❌ Ошибка: {str(e)}")
            st.info("💡 Совет: Используйте двойные кавычки. Комментарии и лишние запятые запрещены.")
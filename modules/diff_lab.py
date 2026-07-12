import streamlit as st
import difflib
import json

def highlight_diff(text1, text2):
    """Функция для детальной подсветки различий внутри строк"""
    result1, result2 = [], []
    s = difflib.SequenceMatcher(None, text1, text2)
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            result1.append(text1[i1:i2])
            result2.append(text2[j1:j2])
        elif tag == 'replace':
            # Подсвечиваем замененную часть
            result1.append(f'<span style="background-color: #7d2a2a; color: white;">{text1[i1:i2]}</span>')
            result2.append(f'<span style="background-color: #2a7d2a; color: white;">{text2[j1:j2]}</span>')
        elif tag == 'delete':
            result1.append(f'<span style="background-color: #7d2a2a; color: white;">{text1[i1:i2]}</span>')
        elif tag == 'insert':
            result2.append(f'<span style="background-color: #2a7d2a; color: white;">{text2[j1:j2]}</span>')
            
    return "".join(result1), "".join(result2)

def render_diff_lab():
    logger = st.session_state.get('logger')
    st.subheader("🧮 Smart Data Diff")

    col_input1, col_input2 = st.columns(2)
    text_a = col_input1.text_area("Оригинал (A):", height=200, key="diff_a")
    text_b = col_input2.text_area("Измененный (B):", height=200, key="diff_b")

    if text_a or text_b:
        c1, c2, _ = st.columns([1, 1, 2])
        is_json = c1.checkbox("Как JSON (Pretty)", value=True)
        
        if st.button("🔍 Найти точные различия", use_container_width=True):
            # Подготовка строк
            lines_a = text_a.splitlines()
            lines_b = text_b.splitlines()

            if is_json:
                try:
                    lines_a = json.dumps(json.loads(text_a), indent=4, ensure_ascii=False, sort_keys=True).splitlines()
                    lines_b = json.dumps(json.loads(text_b), indent=4, ensure_ascii=False, sort_keys=True).splitlines()
                except:
                    st.warning("Ошибка парсинга JSON, сравниваю как текст.")

            st.write("### Результат сравнения:")
            
            html_output = []
            
            # Используем SequenceMatcher для каждой пары измененных строк
            matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
            
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == 'equal':
                    for i in range(i1, i2):
                        html_output.append(f'<div style="color: #888; font-family: monospace; white-space: pre;">  {lines_a[i]}</div>')
                elif tag == 'replace':
                    # Сравниваем строки внутри блока замены для посимвольной подсветки
                    for i, j in zip(range(i1, i2), range(j1, j2)):
                        h1, h2 = highlight_diff(lines_a[i], lines_b[j])
                        html_output.append(f'<div style="background-color: #3d1b1b; color: #ff4b4b; font-family: monospace; white-space: pre;">- {h1}</div>')
                        html_output.append(f'<div style="background-color: #1b3d1b; color: #00ff00; font-family: monospace; white-space: pre;">+ {h2}</div>')
                elif tag == 'delete':
                    for i in range(i1, i2):
                        html_output.append(f'<div style="background-color: #3d1b1b; color: #ff4b4b; font-family: monospace; white-space: pre;">- {lines_a[i]}</div>')
                elif tag == 'insert':
                    for j in range(j1, j2):
                        html_output.append(f'<div style="background-color: #1b3d1b; color: #00ff00; font-family: monospace; white-space: pre;">+ {lines_b[j]}</div>')

            st.markdown(f"""
                <div style="background-color: #0e1117; padding: 15px; border-radius: 10px; border: 1px solid #333; height: 500px; overflow-y: auto;">
                    {"".join(html_output)}
                </div>
            """, unsafe_allow_html=True)
            
            if logger: logger("Diff Lab: Проведен глубокий анализ различий")
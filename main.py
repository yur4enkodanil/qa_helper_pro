import streamlit as st
import os
import shutil

# --- ИМПОРТЫ МОДУЛЕЙ ---
from modules.file_lab import render_file_lab
from modules.logic_lab import render_logic_lab
from modules.matrix_lab import render_matrix_lab
from modules.visual_diff_lab import render_visual_diff_lab
from modules.data_generator import render_data_generator
from modules.visual_lab import render_visual_lab
from modules.integrity_lab import render_integrity_lab
from modules.json_lab import render_json_lab
from modules.diff_lab import render_diff_lab
from modules.about_lab import render_about_lab
from modules.notes_lab import render_notes_lab
from modules.negative_lab import render_negative_lab
from modules.viewport_lab import render_viewport_lab
from modules.link_lab import render_link_lab

# Настройка страницы
st.set_page_config(page_title="QA Helper Pro", layout="wide", page_icon="🚀")

if 'nav_index' not in st.session_state:
    st.session_state.nav_index = 0

current_menu = [
    "🏠 Главная", "📊 Матрица тестов", "📸 Сравнение скриншотов", 
    "📁 Файловый цех", "🧪 Генератор данных", "💀 Негативные сценарии (beta)",
    "🖥️ Эмулятор экранов", "🔗 Анализатор ссылок", "🧠 Тест-дизайн", 
    "📦 JSON Lab", "🧮 Сравнение текста", "🛡️ Проверить хеш", 
    "👁️ Визуальная проверка", "📝 Заметки", "ℹ️ О программе"
]

# --- ФУНКЦИЯ ГЛУБОКОЙ ОЧИСТКИ ---
def deep_clear_all():
    # 1. Сброс оперативной памяти (Session State)
    keys_to_reset = [
        'matrix_params', 'matrix_input_editor', 'matrix_result_viewer', 
        'log_history', 'user_notes', 'json_input', 'text_diff_a', 'text_diff_b'
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

    # 2. Очистка физических папок
    folders_to_clean = ['generated_files', 'test_tree'] # 
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                # Удаляем все содержимое папки
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path) # Удаление файла [cite: 2, 3]
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path) # Удаление подпапок 
            except Exception as e:
                st.error(f"Ошибка при очистке {folder}: {e}")

    st.toast("Система полностью очищена!")

def on_nav_change():
    if st.session_state.nav_selection in current_menu:
        st.session_state.nav_index = current_menu.index(st.session_state.nav_selection)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 QA Helper Pro")
    st.divider()
    
    st.radio("📍 Навигация", current_menu, index=st.session_state.nav_index,
             key="nav_selection", on_change=on_nav_change)

    st.divider()
    
    # Кнопка очистки
    if st.button("🗑️ Полная очистка", use_container_width=True, help="Удалить все нагенеренные файлы и сбросить таблицы"):
        deep_clear_all()
        st.rerun()

    st.caption("v2.0 Stable | yur4enko.danil.18@gmail.com")

# --- РОУТИНГ ---
nav_idx = st.session_state.nav_index

if nav_idx == 0:
    st.title("🚀 Панель управления")
    st.write("---")
    tools = current_menu[1:] 
    cols = st.columns(3)
    for i, tool_name in enumerate(tools):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(tool_name)
                st.write("Инструментарий для профессионального QA.") # [cite: 4]

elif nav_idx == 1: render_matrix_lab() # [cite: 5, 7]
elif nav_idx == 2: render_visual_diff_lab()
elif nav_idx == 3: render_file_lab()
elif nav_idx == 4: render_data_generator()
elif nav_idx == 5: render_negative_lab()
elif nav_idx == 6: render_viewport_lab()
elif nav_idx == 7: render_link_lab()
elif nav_idx == 8: render_logic_lab()
elif nav_idx == 9: render_json_lab()
elif nav_idx == 10: render_diff_lab()
elif nav_idx == 11: render_integrity_lab()
elif nav_idx == 12: render_visual_lab()
elif nav_idx == 13: render_notes_lab()
elif nav_idx == 14: render_about_lab()
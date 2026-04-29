import streamlit as st
import os
import hashlib
import tkinter as tk
from tkinter import filedialog

def get_file_hash(file_path, algo="sha256"):
    """Чтение файла по чанкам для поддержки гигантских файлов."""
    hash_func = hashlib.sha256() if algo == "sha256" else hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def render_integrity_lab():
    logger = st.session_state.get('logger')
    st.subheader("🔒 Целостность и Хеширование")
    st.info("Выберите файл, чтобы получить его отпечаток (Checksum).")
    
    # Инициализация состояния для фикса бага обновления пути
    if 'hash_upd' not in st.session_state:
        st.session_state.hash_upd = 0
    if 'hash_path_state' not in st.session_state:
        st.session_state['hash_path_state'] = ""

    with st.container(border=True):
        col_p, col_b = st.columns([3, 1])
        
        with col_b:
            st.write("")
            if st.button("📂 Обзор...", key="hash_browse"):
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True) # Теперь здесь нет лишнего текста
                selected_file = filedialog.askopenfilename(master=root)
                root.destroy()
                if selected_file:
                    st.session_state['hash_path_state'] = selected_file
                    st.session_state.hash_upd += 1  # Смена ключа для обновления виджета
                    if logger: logger(f"Integrity: Выбран файл {os.path.basename(selected_file)}")
                    st.rerun()  # Принудительная перерисовка страницы

        with col_p:
            # Динамический ключ гарантирует отображение нового пути после выбора
            path_input = st.text_input(
                "Путь к файлу:", 
                value=st.session_state['hash_path_state'], 
                key=f"hash_input_dyn_{st.session_state.hash_upd}"
            )
            st.session_state['hash_path_state'] = path_input
        
        algo = st.selectbox("Алгоритм хеширования:", ["sha256", "md5"], index=0)
    
    if st.button("🔢 Рассчитать хеш", use_container_width=True):
        if os.path.exists(path_input) and os.path.isfile(path_input):
            if logger: logger(f"Integrity: Расчет {algo} для {os.path.basename(path_input)}")
            
            with st.spinner("Выполняется расчет..."):
                try:
                    result = get_file_hash(path_input, algo)
                    st.success("Хеш успешно рассчитан!")
                    st.code(result, language="text")
                    
                    if logger: logger(f"Integrity: Хеш готов ({result[:10]}...)")
                    
                except Exception as e:
                    if logger: logger(f"Integrity ERROR: {str(e)}")
                    st.error(f"Ошибка при чтении файла: {e}")
        else:
            st.error("Файл не найден. Проверьте правильность пути.")
            if logger: logger("Integrity: Ошибка — файл не найден")
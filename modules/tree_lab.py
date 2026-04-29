import streamlit as st
import os
import random
import tkinter as tk
from tkinter import filedialog
from utils.helpers import fill_raw_bytes, get_multiplier

# Полный список расширений
ALL_EXTENSIONS = [
    'docx', 'xlsx', 'pptx', 'pdf', 'csv', 'xls', 'doc', 'ppt', 'txt',
    'png', 'jpg', 'jpeg', 'bmp', 'gif', 'svg', 'tif', 'tiff',
    'mp4', 'ogg', 'ogv', 'webm',
    'zip', '7z', 'rar',
    'grd', 'shp', 'las', 'dlis', 'seg-y', 'lis', 'cst', 'roff',
    'unrst', 'egrid', 'geo-tiff',
    'bin', 'dat', 'tmp', 'log', 'exe'
]

def render_tree_lab():
    logger = st.session_state.get('logger')
    st.subheader("🌳 Генератор сложных структур")
    
    # --- БЛОК ФИКСА ПУТИ ---
    if 'tree_upd' not in st.session_state:
        st.session_state.tree_upd = 0
    if 'tree_path_state' not in st.session_state:
        st.session_state['tree_path_state'] = os.path.join(os.getcwd(), "test_tree")

    with st.container(border=True):
        col_p, col_b = st.columns([3, 1])
     
        with col_b:
            st.write("") 
            if st.button("📂 Обзор...", key="tree_browse"):
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                selected_dir = filedialog.askdirectory(master=root)
                root.destroy()
                if selected_dir:
                    st.session_state['tree_path_state'] = selected_dir
                    st.session_state.tree_upd += 1  # Увеличиваем счетчик для смены ключа
                    st.rerun()  # Мгновенно перерисовываем интерфейс

        with col_p:
            # Динамический ключ заставляет Streamlit обновить значение в поле
            path_tree = st.text_input(
                "Путь для дерева:", 
                value=st.session_state['tree_path_state'], 
                key=f"tree_input_{st.session_state.tree_upd}"
            )
            # Синхронизируем ручной ввод с состоянием
            st.session_state['tree_path_state'] = path_tree

        c1, c2, c3 = st.columns([1, 1, 2])
        with c1: unit = st.selectbox("Вес в:", ["MB", "GB", "KB"], key="tree_unit")
        with c2: min_v = st.number_input("Мин:", value=1.0, key="tree_min")
        with c3: max_v = st.number_input("Макс:", value=2.0, key="tree_max")

    # --- ОСТАЛЬНАЯ ЛОГИКА ---
    use_all = st.checkbox("🔓 Все доступные форматы", value=False, help="Выбрать сразу все расширения из списка")

    with st.expander("⚙️ Настройка форматов и вложенности", expanded=True):
        selected_exts = []
        if use_all:
            selected_exts = ALL_EXTENSIONS
            st.info(f"Выбрано форматов: {len(ALL_EXTENSIONS)}")
        else:
            st.write("Выберите нужные расширения (сетка):")
            cols = st.columns(6)
            for i, ext in enumerate(ALL_EXTENSIONS):
                with cols[i % 6]:
                    is_default = ext in ['bin', 'dat', 'txt']
                    if st.checkbox(ext, value=is_default, key=f"tree_chk_{ext}"):
                        selected_exts.append(ext)
        
        st.divider()
        ca, cb = st.columns(2)
        f_count = ca.number_input("Кол-во папок:", min_value=1, max_value=500, value=5)
        files_count = cb.number_input("Кол-во файлов:", min_value=1, max_value=5000, value=20)

    if st.button("🚀 Вырастить дерево", use_container_width=True):
        if not selected_exts:
            st.error("Выберите хотя бы один формат!")
            return

        if logger: logger(f"TreeLab: Старт генерации {files_count} файлов")
        
        progress_bar = st.progress(0, text="Подготовка структуры...")
        try:
            target_bytes = int(random.uniform(min_v, max_v) * get_multiplier(unit))
            bytes_per_file = target_bytes // files_count
            
            os.makedirs(path_tree, exist_ok=True)
            folders = [path_tree]
            
            # 1. Создаем структуру папок
            for i in range(f_count):
                parent = random.choice(folders)
                new_dir = os.path.join(parent, f"dir_{i+1}")
                os.makedirs(new_dir, exist_ok=True)
                folders.append(new_dir)
            
            # 2. Наполняем файлами
            for i in range(files_count):
                folder = random.choice(folders)
                ext = random.choice(selected_exts)
                fp = os.path.join(folder, f"file_{i+1}.{ext}")
                
                with open(fp, "wb") as f:
                    fill_raw_bytes(f, bytes_per_file)
                
                pct = int(((i + 1) / files_count) * 100)
                progress_bar.progress(pct, text=f"Создание файлов: {i+1}/{files_count}")
            
            st.success(f"✅ Структура успешно создана в {path_tree}!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Ошибка: {e}")
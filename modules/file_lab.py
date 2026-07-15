import streamlit as st
import os
import shutil
import random
import string
from utils.helpers import get_multiplier, fill_raw_bytes
from modules.tree_lab import render_tree_lab
from modules.i18n import get_text
from utils.ui_helpers import open_file_picker
from utils.file_content import VALID_FILE_CONTENT
from utils.file_formats import MAGIC_BYTES, ALL_EXTENSIONS

def render_file_lab():
    # Создаем папки если их нет
    for d in ['generated_files', 'test_tree']:
        if not os.path.exists(d): os.makedirs(d)

    # Инициализация счетчиков для обновления виджетов (решает проблему отображения пути)
    # Эти счетчики нужны для хака с обновлением text_input после выбора файла через диалог
    if 'upd_gen' not in st.session_state: st.session_state.upd_gen = 0
    if 'upd_repl_f' not in st.session_state: st.session_state.upd_repl_f = 0
    if 'upd_repl_d' not in st.session_state: st.session_state.upd_repl_d = 0
    
    t = get_text

    # Возвращаем структуру с тремя вкладками для объединения функционала
    tab1, tab2, tab3 = st.tabs([t("file_lab_tab_single"), t("file_lab_tab_tree"), t("file_lab_tab_replicator")])

    with tab1:
        render_generator_ui(t)
    with tab2:
        render_tree_lab()
    with tab3:
        render_replicator_ui(t)

def render_generator_ui(t):
    st.subheader(t("file_gen_header"))
    st.warning(t("file_lab_tkinter_warning"), icon="⚠️")

    with st.container(border=True):
        if 'file_gen_path' not in st.session_state:
            st.session_state['file_gen_path'] = os.path.join(os.getcwd(), "generated_files")

        c1, c2 = st.columns([3, 1])
        with c2:
            st.write("")
            if st.button(t("file_gen_browse_button"), key="btn_gen_path"):
                res = open_file_picker("folder")
                if res:
                    st.session_state['file_gen_path'] = res
                    st.session_state.upd_gen += 1
                    st.rerun()

        # Динамический ключ гарантирует, что путь из проводника появится в поле
        current_path = c1.text_input(t("file_gen_save_path"), 
                                     value=st.session_state['file_gen_path'], 
                                     key=f"path_gen_input_{st.session_state.upd_gen}")
        
        # Важно: обновляем сохраненный путь при ручном вводе
        st.session_state['file_gen_path'] = current_path

        c1, c2, c3, c4 = st.columns(4)
        ext = c1.selectbox(t("file_gen_format"), ALL_EXTENSIONS, index=ALL_EXTENSIONS.index('bin') if 'bin' in ALL_EXTENSIONS else 0)
        unit = c2.selectbox(t("file_gen_weight_in"), ["MB", "GB", "KB"])
        size = c3.number_input(t("file_gen_size"), min_value=0.1, value=1.0)
        count = c4.number_input(t("file_gen_count"), min_value=1, value=1)
        
        fill_type = st.radio(
            t("file_gen_fill_type"), 
            [
                t("file_gen_fill_valid"),
                t("file_gen_fill_random"),
                t("file_gen_fill_text"),
                t("file_gen_fill_null")
            ], 
            horizontal=False
        )

        # Показываем подсказку с доступными форматами, если выбран режим генерации по шаблону
        if fill_type == t("file_gen_fill_valid"):
            with st.expander(t("file_gen_supported_formats_expander")):
                # Получаем список ключей из словаря с шаблонами
                supported_formats = sorted(list(VALID_FILE_CONTENT.keys()))
                st.info(f"**{t('file_gen_available_formats')}:**\n\n`{', '.join(supported_formats)}`")
                st.caption(t("file_gen_unsupported_formats_caption"))

    if st.button(t("file_gen_start_button"), width='stretch'):
        target_dir = st.session_state['file_gen_path']
        os.makedirs(target_dir, exist_ok=True)
        
        t_bytes = int(size * get_multiplier(unit))
        pb = st.progress(0)
        
        for i in range(int(count)):
            f_path = os.path.join(target_dir, f"test_{i+1}_{os.urandom(4).hex()}.{ext}")
            with open(f_path, "wb") as f:
                if fill_type == t("file_gen_fill_valid"):
                    # Используем валидный шаблон
                    template_content = VALID_FILE_CONTENT.get(ext, b'')
                    f.write(template_content)
                    # Добиваем до нужного размера, если требуется
                    remaining_bytes = max(0, t_bytes - len(template_content))
                    if remaining_bytes > 0:
                        fill_raw_bytes(f, remaining_bytes)
                else:
                    # Старая логика для остальных типов
                    h = MAGIC_BYTES.get(ext, b'')
                    f.write(h)
                    rem = max(0, t_bytes - len(h))
                    if fill_type == t("file_gen_fill_random"):
                        fill_raw_bytes(f, rem)
                    elif fill_type == t("file_gen_fill_text"):
                        chunk_size = 1024 * 1024
                        written = 0
                        chars = (string.ascii_letters + string.digits + " \n\t.,;()[]{}").encode('utf-8')
                        while written < rem:
                            curr = min(chunk_size, rem - written)
                            f.write(bytes(random.choices(chars, k=curr)))
                            written += curr
                    else: # Null bytes
                        chunk_size = 1024 * 1024
                        null_chunk = b'\x00' * chunk_size
                        written = 0
                        while written < rem:
                            bytes_to_write = min(chunk_size, rem - written)
                            f.write(null_chunk[:bytes_to_write])
                            written += bytes_to_write
            pb.progress((i + 1) / count)
        st.success(t("file_gen_success").format(count=count, target_dir=target_dir))

def render_replicator_ui(t):
    st.subheader(t("replicator_header"))
    st.warning(t("file_lab_tkinter_warning"), icon="⚠️")

    with st.container(border=True):
        # ВЫБОР ФАЙЛА
        if 'repl_file' not in st.session_state: st.session_state['repl_file'] = ""
        cf1, cf2 = st.columns([3, 1])
        with cf2:
            st.write("")
            if st.button(t("replicator_select_file_button"), key="btn_repl_f"):
                res = open_file_picker("file")
                if res:
                    st.session_state['repl_file'] = res
                    st.session_state.upd_repl_f += 1
                    st.rerun()
        
        source_path = cf1.text_input(t("replicator_source_file"), value=st.session_state['repl_file'], key=f"f_repl_{st.session_state.upd_repl_f}")
        st.session_state['repl_file'] = source_path

        # ВЫБОР ПАПКИ
        if 'repl_dest' not in st.session_state:
            st.session_state['repl_dest'] = os.path.join(os.getcwd(), "generated_files")
        cd1, cd2 = st.columns([3, 1])
        with cd2:
            st.write("")
            if st.button(t("replicator_select_dest_button"), key="btn_repl_d"):
                res = open_file_picker("folder")
                if res:
                    st.session_state['repl_dest'] = res
                    st.session_state.upd_repl_d += 1
                    st.rerun()

        dest_dir = cd1.text_input(t("replicator_dest_folder"), value=st.session_state['repl_dest'], key=f"d_repl_{st.session_state.upd_repl_d}")
        st.session_state['repl_dest'] = dest_dir
        
        copies = st.number_input(t("replicator_copies_count"), min_value=1, max_value=2000, value=10)

    if st.button(t("replicator_start_button"), width='stretch'):
        if not source_path or not os.path.exists(source_path):
            st.error(t("replicator_error_no_file"))
            return
        os.makedirs(dest_dir, exist_ok=True)
        fname = os.path.basename(source_path)
        pb = st.progress(0)
        for i in range(copies):
            shutil.copy2(source_path, os.path.join(dest_dir, f"copy_{i+1}_{fname}"))
            pb.progress((i + 1) / copies)
        st.success(t("replicator_success").format(copies=copies, dest_dir=dest_dir))
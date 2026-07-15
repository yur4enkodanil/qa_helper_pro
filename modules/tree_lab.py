import streamlit as st
import os
import random
from modules.i18n import get_text
from utils.helpers import fill_raw_bytes, get_multiplier
from utils.ui_helpers import open_file_picker
from utils.file_formats import ALL_EXTENSIONS, MAGIC_BYTES
from utils.file_content import VALID_FILE_CONTENT


def render_tree_lab():
    t = get_text
    logger = st.session_state.get("logger")
    st.subheader(t("tree_lab_header"))
    st.warning(t("file_lab_tkinter_warning"), icon="⚠️")

    # --- БЛОК ФИКСА ПУТИ ---
    if "tree_upd" not in st.session_state:
        st.session_state.tree_upd = 0
    if "tree_path_state" not in st.session_state:
        st.session_state["tree_path_state"] = os.path.join(os.getcwd(), "test_tree")

    with st.container(border=True):
        col_p, col_b = st.columns([3, 1])

        with col_b:
            st.write("")
            if st.button(t("file_gen_browse_button"), key="tree_browse"):
                selected_dir = open_file_picker("folder")
                if selected_dir: 
                    st.session_state["tree_path_state"] = selected_dir
                    st.session_state.tree_upd += (
                        1  # Увеличиваем счетчик для смены ключа
                    )
                    st.rerun()  # Мгновенно перерисовываем интерфейс

        with col_p:
            # Динамический ключ заставляет Streamlit обновить значение в поле
            path_tree = st.text_input(
                t("tree_lab_path"),
                value=st.session_state["tree_path_state"],
                key=f"tree_input_{st.session_state.tree_upd}",
            )
            # Синхронизируем ручной ввод с состоянием
            st.session_state["tree_path_state"] = path_tree

        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            unit = st.selectbox(
                t("file_gen_weight_in"),
                ["MB", "GB", "KB"],
                key="tree_unit",
            )
        with c2:
            min_v = st.number_input(
                t("tree_lab_min_size"), value=1.0, key="tree_min"
            )
        with c3:
            max_v = st.number_input(
                t("tree_lab_max_size"), value=2.0, key="tree_max"
            )

    # --- ОСТАЛЬНАЯ ЛОГИКА ---
    use_all = st.checkbox(
        t("tree_lab_all_formats"),
        value=False,
        help=t("tree_lab_all_formats_help"),
    )

    with st.expander(
        t("tree_lab_settings_expander"),
        expanded=True,
    ):
        selected_exts = []
        if use_all:
            selected_exts = ALL_EXTENSIONS
            st.info(t("tree_lab_formats_selected").format(count=len(ALL_EXTENSIONS)))
        else:
            st.write(t("tree_lab_select_extensions"))
            cols = st.columns(6)
            for i, ext in enumerate(ALL_EXTENSIONS):
                with cols[i % 6]:
                    is_default = ext in ["bin", "dat", "txt"]
                    if st.checkbox(ext, value=is_default, key=f"tree_chk_{ext}"):
                        selected_exts.append(ext)

        st.divider()
        ca, cb = st.columns(2)
        f_count = ca.number_input(
            t("tree_lab_folders_count"),
            min_value=1,
            max_value=500,
            value=5,
        )
        files_count = cb.number_input(
            t("tree_lab_files_count"),
            min_value=1,
            max_value=5000,
            value=20,
        )
        
        fill_type_tree = st.radio(
            t("file_gen_fill_type"),
            [t("file_gen_fill_valid"), t("file_gen_fill_random")],
            horizontal=True, key="tree_fill_type"
        )

    if st.button(
        t("tree_lab_start_button"),
        width='stretch',
    ):
        if not selected_exts:
            st.error(t("tree_lab_error_no_formats"))
            return

        if logger:
            logger(f"TreeLab: Старт генерации {files_count} файлов")

        progress_bar = st.progress(
            0,
            text=t("tree_lab_progress_prepare"),
        )
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
                    if fill_type_tree == t("file_gen_fill_valid"):
                        template_content = VALID_FILE_CONTENT.get(ext, b'')
                        f.write(template_content)
                        remaining_bytes = max(0, bytes_per_file - len(template_content))
                        if remaining_bytes > 0:
                            fill_raw_bytes(f, remaining_bytes)
                    else: # Случайные байты
                        header = MAGIC_BYTES.get(ext, b'')
                        f.write(header)
                        remaining_bytes = max(0, bytes_per_file - len(header))
                        fill_raw_bytes(f, remaining_bytes)
                pct = int(((i + 1) / files_count) * 100)
                progress_bar.progress(pct, text=t("tree_lab_progress_creating").format(current=i+1, total=files_count))

            st.success(t("tree_lab_success").format(path=path_tree))
            st.balloons()

        except Exception as e:
            st.error(f"{t('tree_lab_error_generic')}: {e}")

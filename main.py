import streamlit as st
import os
import shutil
import importlib
import sys
import json

# Добавляем корневую папку проекта в sys.path, чтобы все модули могли найти друг друга.
# Это решает проблемы с импортами вида `from utils.helpers...` из подмодулей.
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
from modules.i18n import get_text

# --- ВЕРСИЯ ПРИЛОЖЕНИЯ ---
APP_VERSION = "2.1.2"

# --- ЛОГИРОВАНИЕ ОШИБОК В ФАЙЛ ---
LOG_FILE = os.path.join(project_root, "qa_helper_pro.log")

# Очищаем лог-файл при каждом запуске, чтобы хранить только актуальную сессию
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("")

class StderrTee:
    """Перехватывает поток ошибок (stderr) и дублирует его в файл и в консоль."""
    def __init__(self, original_stderr, log_file):
        self.original_stderr = original_stderr
        self.log_file = log_file

    def write(self, message):
        # Пишем в оригинальный stderr (консоль)
        self.original_stderr.write(message)
        # Дописываем в файл
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message)
        except Exception as e:
            # Если запись в лог не удалась, выводим ошибку в консоль, чтобы не уйти в рекурсию
            self.original_stderr.write(f"FATAL: Could not write to log file {self.log_file}: {e}\n")

    def flush(self):
        self.original_stderr.flush()

# Перенаправляем stderr. Все ошибки print(..., file=sys.stderr) и исключения пойдут сюда.
if not isinstance(sys.stderr, StderrTee):
    sys.stderr = StderrTee(sys.stderr, LOG_FILE)

# Настройка страницы
st.set_page_config(page_title="QA Helper Pro", layout="wide", page_icon="🚀")

# --- ИНЖЕКЦИЯ СОВРЕМЕННЫХ СТИЛЕЙ ---
st.markdown("""
<style>
    html {
        font-size: 95%; /* Уменьшаем масштаб всего приложения для большей компактности */
    }

    /* Стилизация таблиц (st.table) */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background-color: #2a3950; /* Темно-синий фон для заголовков */
        color: #e0e0e0;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #232323; /* Чередование цвета строк для читаемости */
    }
    td, th {
        border: 1px solid #4A4A4A;
    }
<style>
    /* Стиль для контейнеров, созданных через st.container(border=True) */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1E1E1E; /* Темный фон для карточки */
        border: 1px solid #4A4A4A; /* Более заметная рамка */
        border-radius: 0.75rem; /* Более скругленные углы */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Легкая тень для объема */
        transition: box-shadow 0.3s ease-in-out, border-color 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #6C6C6C;
    }
</style>
""", unsafe_allow_html=True)

if "nav_index" not in st.session_state:
    st.session_state.nav_index = 0

if "lang" not in st.session_state:
    st.session_state.lang = "RU"
st.session_state.app_version = APP_VERSION


def load_tool(module_name, func_name):
    """Безопасная загрузка модулей. Спасает приложение от падения, если файл поврежден или удален."""
    try:
        # Сначала пытаемся загрузить из стандартной папки modules
        module = importlib.import_module(f"modules.{module_name}")
        return getattr(module, func_name)
    except ImportError:
        try:
            # Если не получилось, пробуем загрузить из корня проекта (для обратной совместимости)
            module = importlib.import_module(module_name)
            return getattr(module, func_name)
        except Exception as e:
            print(
                f"[QA Helper] Модуль '{module_name}' пропущен из-за ошибки: {e}",
                file=sys.stderr,
            )
            return None


def load_tools_from_config():
    """Загружает и валидирует конфигурацию инструментов из JSON."""
    config_path = os.path.join(project_root, "tools_config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            raw_tools = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error(f"Критическая ошибка: не удалось загрузить `tools_config.json`: {e}")
        return []
    return raw_tools


# --- КОНФИГУРАЦИЯ ИНСТРУМЕНТОВ ---
TOOLS_CONFIG = []
for tool in load_tools_from_config():
    loaded_func = load_tool(tool["mod"], tool["func"])
    if loaded_func:
        tool["func"] = loaded_func
        TOOLS_CONFIG.append(tool)

lang = st.session_state.lang
lang_key = lang.lower()

current_menu = [tool[lang_key] for tool in TOOLS_CONFIG]

# Защита от сбоя индексации, если количество инструментов изменилось
if st.session_state.nav_index >= len(current_menu):
    st.session_state.nav_index = 0


# --- ФУНКЦИЯ ГЛУБОКОЙ ОЧИСТКИ ---
def deep_clear_all(current_lang="RU"):
    # 1. Сброс оперативной памяти (Session State)
    # Группируем ключи для лучшей читаемости и поддержки
    keys_to_reset = [
        # matrix_lab
        "matrix_params", "matrix_editor_widget", "matrix_input_editor", "matrix_result_viewer", "matrix_df",
        # log_analyzer_lab
        "log_lines", "log_stats",
        # notes_lab
        "user_notes",
        # json_lab
        "json_input", "json_content", "json_widget_version",
        # diff_lab
        "text_diff_a", "text_diff_b",
        # visual_lab, integrity_lab, file_lab
        "v_ref", "v_cur", "hash_path_state", "hash_upd", "file_gen_path", "upd_gen",
        "tree_path_state", "tree_upd", "repl_file", "repl_dest",
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    print("[QA Helper] Session state cleared.", file=sys.stderr)

    # 2. Очистка физических папок
    # Добавляем папки от заметок и визуального регресса
    folders_to_clean = ["generated_files", "test_tree", "qa_notes_storage", "reference_storage"]

    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                # Удаляем все содержимое папки
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Удаление файла [cite: 2, 3]
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Удаление подпапок
                print(f"[QA Helper] Folder '{folder}' cleaned.", file=sys.stderr)
            except Exception as e:
                st.error(f"Ошибка при очистке {folder}: {e}")
                print(f"[QA Helper] ERROR cleaning folder '{folder}': {e}", file=sys.stderr)

    msg = (
        "Система полностью очищена!"
        if current_lang == "RU"
        else "System completely cleared!"
    )
    st.toast(msg)
    print(f"[QA Helper] {msg}", file=sys.stderr)


# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 QA Helper Pro")

    st.radio("🌐 Язык / Language", ["RU", "EN"], key="lang", horizontal=True)

    st.divider()

    nav_label = "📍 Навигация" if lang == "RU" else "📍 Navigation"
    nav_idx = st.radio(
        nav_label,
        options=range(len(current_menu)),
        format_func=lambda i: current_menu[i],
        index=st.session_state.nav_index,
    )
    st.session_state.nav_index = nav_idx

    st.divider()

    clear_btn = "🗑️ Полная очистка" if lang == "RU" else "🗑️ Clear All"
    clear_help = (
        "Удалить все нагенеренные файлы и сбросить таблицы"
        if lang == "RU"
        else "Delete all generated files and reset tables"
    )
    # Кнопка очистки
    if st.button(
        clear_btn,
        use_container_width=True,
        help=clear_help,
    ):
        deep_clear_all(lang)
        st.rerun()

    st.caption(f"v{APP_VERSION} Stable | yur4enko.danil.18@gmail.com")

# --- РОУТИНГ ---
# Вызываем функцию рендера для выбранного в сайдбаре инструмента
selected_tool_data = TOOLS_CONFIG[nav_idx]
if selected_tool_data and "func" in selected_tool_data:
    # Вызываем функцию из ключа 'func'
    selected_tool_data["func"]()

import streamlit as st
import os
import shutil
import importlib
import sys
import json
from io import BytesIO
import base64

# Добавляем корневую папку проекта в sys.path, чтобы все модули могли найти друг друга.
# Это решает проблемы с импортами вида `from utils.helpers...` из подмодулей.
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# --- NEW: DLL PATH FIX FOR PYZBAR ON WINDOWS ---
def add_dll_path():
    """Adds the bundled 'dlls' directory to the search path for libraries."""
    if sys.platform == "win32":
        dll_path = os.path.join(project_root, "dlls")
        if os.path.isdir(dll_path):
            # For Python 3.8+ on Windows, this is the recommended way
            if hasattr(os, 'add_dll_directory'):
                try:
                    os.add_dll_directory(dll_path)
                    print(f"[QA Helper] Registered DLL path: {dll_path}", file=sys.stderr)
                except Exception as e:
                    print(f"[QA Helper] Failed to use os.add_dll_directory(): {e}", file=sys.stderr)
            # Fallback for older Python versions
            if dll_path not in os.environ['PATH']:
                os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']
                print(f"[QA Helper] Added to PATH for DLLs: {dll_path}", file=sys.stderr)

# Call the function at the start, before any other imports that might need it
add_dll_path()
# --- END OF FIX ---

from modules.i18n import get_text

# --- ВЕРСИЯ ПРИЛОЖЕНИЯ ---
APP_VERSION = "2.2.1"

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
    section[data-testid="stAppViewContainer"] {
        font-size: 80%; /* Уменьшаем масштаб основного контента, не затрагивая сайдбар */
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
    except ImportError as first_error:
        try:
            # Если не получилось, пробуем загрузить из корня проекта (для обратной совместимости)
            module = importlib.import_module(module_name)
            return getattr(module, func_name)
        except Exception as second_error:
            print(
                f"[QA Helper] Модуль '{module_name}' пропущен. Основная ошибка: {first_error}. Дополнительная ошибка: {second_error}",
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

# --- NEW: Категоризация инструментов для улучшенной навигации ---
CATEGORIES_RU = {
    "Система": ["Журнал ошибок", "О программе"],
    "Инструменты для Веб": ["Эмулятор экранов", "Анализатор ссылок", "Frontend Анализатор", "UI Инспектор", "Сравнение скриншотов"],
    "Инструменты для API и Данных": ["API Клиент", "Повторитель запросов", "Генератор данных", "JSON Lab", "Base64 Кодер"],
    "Инструменты для Файлов": ["Файловый цех", "Анализатор логов", "Проверить хеш", "Визуальная проверка"],
    "Общие утилиты": ["Матрица тестов", "Тест-дизайн", "Негативные сценарии", "Сравнение текста", "Заметки"],
    "Мобильная лаборатория": ["Мобильная лаборатория"]
}

CATEGORIES_EN = {
    "System": ["Журнал ошибок", "О программе"],
    "Web Tools": ["Эмулятор экранов", "Анализатор ссылок", "Frontend Анализатор", "UI Инспектор", "Сравнение скриншотов"],
    "API & Data Tools": ["API Клиент", "Повторитель запросов", "Генератор данных", "JSON Lab", "Base64 Кодер"],
    "File Tools": ["Файловый цех", "Анализатор логов", "Проверить хеш", "Визуальная проверка"],
    "General Utilities": ["Матрица тестов", "Тест-дизайн", "Негативные сценарии", "Сравнение текста", "Заметки"],
    "Mobile Lab": ["Мобильная лаборатория"]
}

lang = st.session_state.lang
lang_key = lang.lower()

current_menu = [tool[lang_key] for tool in TOOLS_CONFIG]

# Защита от сбоя индексации, если количество инструментов изменилось
if st.session_state.nav_index >= len(current_menu):
    st.session_state.nav_index = 0


# --- ФУНКЦИЯ ГЛУБОКОЙ ОЧИСТКИ ---
def deep_clear_all(current_lang="RU"):
    # 1. Сброс оперативной памяти (Session State)
    # Сохраняем ключи, которые не нужно сбрасывать
    preserved_keys = ["lang", "nav_index", "app_version"]
    # Исключаем ключи заметок (начинаются с 'content_')
    keys_to_delete = [
        k
        for k in st.session_state.keys()
        if k not in preserved_keys and not k.startswith("content_")
    ]
    
    for key in keys_to_delete:
        del st.session_state[key]
    print("[QA Helper] Session state cleared (notes preserved).", file=sys.stderr)

    # 2. Очистка физических папок (кроме заметок)
    folders_to_clean = ["generated_files", "test_tree", "reference_storage"]

    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                # Для остальных папок удаляем все и пересоздаем
                shutil.rmtree(folder)
                os.makedirs(folder, exist_ok=True)
                print(
                    f"[QA Helper] Folder '{folder}' fully cleared and recreated.",
                    file=sys.stderr,
                )
            except Exception as e:
                st.error(f"Ошибка при очистке {folder}: {e}")
                print(
                    f"[QA Helper] ERROR cleaning folder '{folder}': {e}", file=sys.stderr
                )

    # 3. Очистка кеша Streamlit
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
        print("[QA Helper] Streamlit caches cleared.", file=sys.stderr)
    except Exception as e:
        print(f"[QA Helper] ERROR clearing Streamlit caches: {e}", file=sys.stderr)

    msg = (
        "Система очищена (заметки сохранены)!"
        if current_lang == "RU"
        else "System cleared (notes preserved)!"
    )
    st.toast(msg)
    print(f"[QA Helper] {msg}", file=sys.stderr)


# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 QA Helper Pro")

    st.radio("🌐 Язык / Language", ["RU", "EN"], key="lang", horizontal=True)

    st.divider()

    # --- NEW: Навигация с поиском и категориями ---
    search_query = st.text_input(
        "🔍 " + ("Поиск по модулям..." if lang == "RU" else "Search modules..."),
        key="nav_search"
    ).lower()

    # Фильтруем меню на основе поиска
    filtered_menu = {
        name: idx for idx, name in enumerate(current_menu)
        if search_query in name.lower()
    }

    categories = CATEGORIES_RU if lang == "RU" else CATEGORIES_EN

    # Создаем карту из текущего языка в русский для сопоставления с категориями
    # Категории определены через русские названия, которые выступают как ID
    name_to_ru_map = {tool[lang_key]: tool['ru'] for tool in TOOLS_CONFIG}

    def get_clean_ru_name(display_name):
        """Helper to get the Russian tool name without emoji for category matching."""
        ru_name_with_emoji = name_to_ru_map.get(display_name)
        if not ru_name_with_emoji:
            return ""
        # Assuming format is "emoji name"
        parts = ru_name_with_emoji.split(' ', 1)
        return parts[-1]

    for category, tools_in_cat in categories.items():
        # Показываем категорию, только если в ней есть инструменты, соответствующие поиску
        category_tools = {
            name: idx for name, idx in filtered_menu.items()
            if get_clean_ru_name(name) in tools_in_cat
        }
        if category_tools or not search_query:
            st.markdown(f"**{category}**")
            
            # Если есть поиск, показываем только отфильтрованные
            if search_query:
                display_tools = category_tools
            else:
                display_tools = {
                    name: i for i, name in enumerate(current_menu) if get_clean_ru_name(name) in tools_in_cat
                }
            
            for name, idx in display_tools.items():
                # Используем кастомные кнопки вместо st.radio
                is_selected = (st.session_state.nav_index == idx)
                button_type = "primary" if is_selected else "secondary"
                if st.button(name, key=f"nav_{idx}", type=button_type, width='stretch'):
                    st.session_state.nav_index = idx
                    st.rerun()

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
        help=clear_help,
        width='stretch'
    ):
        deep_clear_all(lang)
        st.rerun()

    st.caption(f"v{APP_VERSION} Stable | yur4enko.danil.18@gmail.com")

# --- РОУТИНГ ---
# Вызываем функцию рендера для выбранного в сайдбаре инструмента
selected_tool_data = TOOLS_CONFIG[st.session_state.nav_index]
if selected_tool_data and "func" in selected_tool_data:
    # Вызываем функцию из ключа 'func'
    selected_tool_data["func"]()

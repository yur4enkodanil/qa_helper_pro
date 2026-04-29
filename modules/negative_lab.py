import streamlit as st
import os
import pandas as pd
import json
import random
from utils.helpers import fill_raw_bytes

def render_negative_lab():
    lang = st.session_state.get('lang', 'RU')
    title = "💀 Негативные сценарии" if lang == "RU" else "💀 Negative Scenarios"
    st.subheader(f"{title} :orange[(beta)]")
    
    tabs = st.tabs([
        "🚀 " + ("Конструктор атак" if lang == "RU" else "Attack Constructor"),
        "💣 " + ("Файлы-ловушки" if lang == "RU" else "File Traps"),
        "📊 " + ("Наборы данных" if lang == "RU" else "Data Sets"),
        "💡 " + ("Гайд по проверкам" if lang == "RU" else "Testing Guide")
    ])

    with tabs[0]: render_attack_constructor(lang)
    with tabs[1]: render_file_bombs(lang)
    with tabs[2]: render_data_sets(lang)
    with tabs[3]: render_testing_guide(lang)

def render_attack_constructor(lang):
    st.markdown("### 📝 " + ("Ультимативный конструктор атак" if lang == "RU" else "Ultimate Attack Constructor"))
    
    # Визуализация спецсимволов
    special_chars_map = {
        "[SPACE] (Пробел)": " ",
        "[TAB] (Табуляция)": "\t",
        "[NEWLINE] (Перенос строки)": "\n",
        "[NULL BYTE] (Нулевой байт)": "\0",
        "[ZERO WIDTH SPACE] (Невидимый разделитель)": "\u200B",
        "[RLO] (Разворот текста)": "\u202E",
        "[BOM] (Byte Order Mark)": "\xef\xbb\xbf"
    }

    # Граничные значения (Лимит 2000 символов)
    boundary_map = {
        "1 символ (Минимум)": "A",
        "255 символов (Лимит VARCHAR)": "A" * 255,
        "256 символов (Превышение лимита)": "A" * 256,
        "1000 символов (Длинный текст)": "A" * 1000,
        "2000 символов (Максимальный предел)": "A" * 2000,
        "Макс. Int 32-bit (2147483647)": "2147483647",
        "Макс. Int 64-bit (9223372036854775807)": "9223372036854775807"
    }

    attacks = {
        "XSS (Скрипты)": ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "<svg onload=alert(1)>", "javascript:alert(1)"],
        "SQLi (Инъекции БД)": ["' OR 1=1 --", "'; DROP TABLE users; --", "admin' #", "' UNION SELECT NULL--"],
        "NoSQL и Команды": ['{"$gt": ""}', '{"$ne": null}', "; rm -rf /", "&& whoami", "| ping 127.0.0.1"],
        "Пути (Path Traversal)": ["../../etc/passwd", "..\\..\\windows\\win.ini", "%2e%2e%2f%2e%2e%2fconfig.php"],
        "Спецсимволы / Пробелы": list(special_chars_map.keys()),
        "Граничные значения": list(boundary_map.keys()),
        "Кодировки / Unicode": ["🔥🚀☢️", "你好", "Ω∑∆", "﷽", "русский текст", "السلام"],
        "Логика API (JSON)": ['{"id": -1}', '{"amount": "NaN"}', '{"count": 9999999999}', '{"price": -0.01}']
    }
    
    col1, col2 = st.columns([1, 2])
    with col1:
        type_a = st.selectbox(("Категория" if lang == "RU" else "Category"), list(attacks.keys()))
    with col2:
        selected_option = st.selectbox(("Вариант" if lang == "RU" else "Variant"), attacks[type_a])
    
    # Определяем Payload
    if type_a == "Спецсимволы / Пробелы": val = special_chars_map[selected_option]
    elif type_a == "Граничные значения": val = boundary_map[selected_option]
    else: val = selected_option
    
    st.markdown("---")
    st.info(("Результат (Кнопка копирования справа вверху):" if lang == "RU" else "Result:"))
    
    if type_a == "Спецсимволы / Пробелы":
        st.caption(f"Технический вид: `{repr(val)}`")
    
    # Кнопка копирования встроена в st.code
    st.code(val, language="javascript")
    
    if st.button("📋 " + ("Экспорт набора в JSON" if lang == "RU" else "Export to JSON")):
        if type_a == "Спецсимволы / Пробелы": export_p = list(special_chars_map.values())
        elif type_a == "Граничные значения": export_p = list(boundary_map.values())
        else: export_p = attacks[type_a]
        st.json(export_p)

def render_file_bombs(lang):
    st.markdown("### 💣 " + ("Файлы-ловушки" if lang == "RU" else "File Traps"))
    
    traps = {
        "EICAR (Virus Test)": "Тестовая сигнатура вируса для проверки антивируса на сервере.",
        "Zero-Byte (0 KB)": "Файл нулевого размера для проверки обработки пустых данных.",
        "Broken Header": "Файл с неверным магическим числом (JPG с мусором внутри).",
        "Double Extension": "Маскировка исполняемого файла под картинку (photo.jpg.exe).",
        "BOM CSV": "CSV файл со скрытыми байтами BOM в начале (ломает импорт)."
    }

    with st.container(border=True):
        f_type = st.selectbox(("Тип ловушки" if lang == "RU" else "Type"), list(traps.keys()))
        st.caption(f"ℹ️ {traps[f_type]}")
        
        if st.button("🚀 " + ("Сгенерировать" if lang == "RU" else "Create")):
            fname, content = "trap.txt", b"test"
            if "EICAR" in f_type: fname, content = "eicar.com", b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
            elif "Zero-Byte" in f_type: fname, content = "empty.pdf", b""
            elif "Broken" in f_type: fname, content = "broken.jpg", b"\xFF\xD8\xFF\xE0" + b"\x00" * 10
            elif "BOM" in f_type: fname, content = "test.csv", b'\xef\xbb\xbfID,Name\n1,Test'
            
            st.download_button(("📥 Скачать" if lang == "RU" else "Download"), content, file_name=fname)

def render_data_sets(lang):
    st.markdown("### 📊 " + ("Массовая генерация (Chaos CSV)" if lang == "RU" else "Mass Chaos"))
    count = st.slider(("Строк:" if lang == "RU" else "Rows:"), 5, 500, 50)
    
    if st.button("⚡ " + ("Создать таблицу" if lang == "RU" else "Generate")):
        bad = ["<script>alert(1)</script>", "NaN", "null", "\0", "' OR 1=1", "   "]
        data = [{"id": i+1, "field": random.choice(bad), "num": random.choice([-1, 0, 2147483647])} for i in range(count)]
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8-sig'), "chaos.csv")

def render_testing_guide(lang):
    """Подробный гайд по кейсам"""
    st.markdown("""
    ### 🧠 Гайд по негативному тестированию (Middle QA Edition)

    #### 1. Конструктор атак (Поля ввода)
    * **Кейс XSS:** Вставьте скрипт в поле "Имя профиля".
        * **Как проверить:** Сохраните и обновите страницу. Если появилось окно `alert` — уязвимость найдена. 
    * **Кейс Нулевой байт (`\0`):** Вставьте в поле поиска.
        * **Как проверить:** Посмотрите логи бэкенда. Если запрос обрезался на этом символе, сервер неправильно обрабатывает строки (C-style strings).
    * **Кейс Границы (2000 симв.):** Вставьте в описание товара.
        * **Как проверить:** Если БД упала с ошибкой `Data too long`, значит на бэкенде отсутствует валидация длины перед записью.

    #### 2. Файлы-ловушки (Uploads)
    * **Кейс EICAR:** Загрузите файл как "Аватар".
        * **Как проверить:** Система **обязана** выдать ошибку (400 или "Virus detected"). Если файл загрузился — на сервере нет антивирусного сканера.
    * **Кейс Broken Header:** Загрузите "битый" JPG.
        * **Как проверить:** Бэкенд должен проверить MIME-тип (Magic bytes), а не только расширение. Ожидаем ошибку валидации формата.

    #### 3. Наборы данных (Импорты)
    * **Кейс Chaos CSV:** Скачайте CSV и загрузите в модуль импорта пользователей.
        * **Как проверить:** Ищем "эффект домино". Если одна плохая строка (`NaN` или `null`) роняет весь процесс импорта 1000 строк — это критический баг обработки исключений.

    #### 📋 Чек-лист Middle QA:
    1.  **400/422 Bad Request:** Идеально (валидация сработала).
    2.  **200 OK (Текст как есть):** Безопасно (данные экранированы).
    3.  **500 Internal Error:** **Bug.** Необработанное исключение.
    4.  **Скрипт выполнился:** **Critical Security Bug.**
    """)
import streamlit as st
import os
import pandas as pd
import json
import random
from utils.helpers import fill_raw_bytes


def render_negative_lab():
    lang = st.session_state.get("lang", "RU")
    title = "💀 Негативные сценарии" if lang == "RU" else "💀 Negative Scenarios"
    st.subheader(f"{title} :orange[(beta)]")

    tabs = st.tabs(
        [
            "🚀 " + ("Конструктор атак" if lang == "RU" else "Attack Constructor"),
            "💣 " + ("Файлы-ловушки" if lang == "RU" else "File Traps"),
            "📊 " + ("Наборы данных" if lang == "RU" else "Data Sets"),
            "💡 " + ("Гайд по проверкам" if lang == "RU" else "Testing Guide"),
        ]
    )

    with tabs[0]:
        render_attack_constructor(lang)
    with tabs[1]:
        render_file_bombs(lang)
    with tabs[2]:
        render_data_sets(lang)
    with tabs[3]:
        render_testing_guide(lang)


def render_attack_constructor(lang):
    st.markdown(
        "### 📝 "
        + (
            "Ультимативный конструктор атак"
            if lang == "RU"
            else "Ultimate Attack Constructor"
        )
    )

    # Визуализация спецсимволов
    special_chars_map = {
        "[SPACE]" if lang == "EN" else "[SPACE] (Пробел)": " ",
        "[TAB]" if lang == "EN" else "[TAB] (Табуляция)": "\t",
        "[NEWLINE]" if lang == "EN" else "[NEWLINE] (Перенос строки)": "\n",
        "[NULL BYTE]" if lang == "EN" else "[NULL BYTE] (Нулевой байт)": "\0",
        (
            "[ZERO WIDTH SPACE]"
            if lang == "EN"
            else "[ZERO WIDTH SPACE] (Невидимый разделитель)"
        ): "\u200b",
        "[RLO]" if lang == "EN" else "[RLO] (Разворот текста)": "\u202e",
        "[BOM]" if lang == "EN" else "[BOM] (Byte Order Mark)": "\xef\xbb\xbf",
    }

    # Граничные значения (Лимит 2000 символов)
    boundary_map = {
        "1 char (Min)" if lang == "EN" else "1 символ (Минимум)": "A",
        (
            "255 chars (VARCHAR Limit)"
            if lang == "EN"
            else "255 символов (Лимит VARCHAR)"
        ): "A"
        * 255,
        (
            "256 chars (Over Limit)"
            if lang == "EN"
            else "256 символов (Превышение лимита)"
        ): "A"
        * 256,
        (
            "1000 chars (Long text)"
            if lang == "EN"
            else "1000 символов (Длинный текст)"
        ): "A"
        * 1000,
        (
            "2000 chars (Max Limit)" if lang == "EN" else "2000 символов (Макс. предел)"
        ): "A"
        * 2000,
        "Max Int 32-bit (2147483647)": "2147483647",
        "Max Int 64-bit (9223372036854775807)": "9223372036854775807",
    }

    k_xss = "XSS (Scripts)" if lang == "EN" else "XSS (Скрипты)"
    k_sql = "SQLi (DB Injections)" if lang == "EN" else "SQLi (Инъекции БД)"
    k_nosql = "NoSQL & Commands" if lang == "EN" else "NoSQL и Команды"
    k_path = "Path Traversal" if lang == "EN" else "Пути (Path Traversal)"
    k_chars = "Special / Whitespaces" if lang == "EN" else "Спецсимволы / Пробелы"
    k_bound = "Boundaries" if lang == "EN" else "Граничные значения"
    k_enc = "Encoding / Unicode" if lang == "EN" else "Кодировки / Unicode"
    k_api = "API Logic (JSON)" if lang == "EN" else "Логика API (JSON)"

    attacks = {
        k_xss: [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "javascript:alert(1)",
        ],
        k_sql: [
            "' OR 1=1 --",
            "'; DROP TABLE users; --",
            "admin' #",
            "' UNION SELECT NULL--",
        ],
        k_nosql: [
            '{"$gt": ""}',
            '{"$ne": null}',
            "; rm -rf /",
            "&& whoami",
            "| ping 127.0.0.1",
        ],
        k_path: [
            "../../etc/passwd",
            "..\\..\\windows\\win.ini",
            "%2e%2e%2f%2e%2e%2fconfig.php",
        ],
        k_chars: list(special_chars_map.keys()),
        k_bound: list(boundary_map.keys()),
        k_enc: ["🔥🚀☢️", "你好", "Ω∑∆", "﷽", "русский текст", "السلام"],
        k_api: [
            '{"id": -1}',
            '{"amount": "NaN"}',
            '{"count": 9999999999}',
            '{"price": -0.01}',
        ],
    }

    col1, col2 = st.columns([1, 2])
    with col1:
        type_a = st.selectbox(
            ("Категория" if lang == "RU" else "Category"), list(attacks.keys())
        )
    with col2:
        selected_option = st.selectbox(
            ("Вариант" if lang == "RU" else "Variant"), attacks[type_a]
        )

    # Определяем Payload
    if type_a == k_chars:
        val = special_chars_map[selected_option]
    elif type_a == k_bound:
        val = boundary_map[selected_option]
    else:
        val = selected_option

    st.markdown("---")
    st.info(
        ("Результат (Кнопка копирования справа вверху):" if lang == "RU" else "Result:")
    )

    if type_a == k_chars:
        st.caption(f"Технический вид: `{repr(val)}`")

    # Кнопка копирования встроена в st.code
    st.code(val, language="javascript")

    if st.button(
        "📋 " + ("Экспорт набора в JSON" if lang == "RU" else "Export to JSON")
    ):
        if type_a == k_chars:
            export_p = list(special_chars_map.values())
        elif type_a == k_bound:
            export_p = list(boundary_map.values())
        else:
            export_p = attacks[type_a]
        st.json(export_p)


def render_file_bombs(lang):
    st.markdown("### 💣 " + ("Файлы-ловушки" if lang == "RU" else "File Traps"))

    if lang == "RU":
        desc_eicar = "Тестовая сигнатура вируса для проверки антивируса на сервере."
        desc_zero = "Файл нулевого размера для проверки обработки пустых данных."
        desc_broken = "Файл с неверным магическим числом (JPG с мусором внутри)."
        desc_ext = "Маскировка исполняемого файла под картинку (photo.jpg.exe)."
        desc_bom = "CSV файл со скрытыми байтами BOM в начале (ломает импорт)."
    else:
        desc_eicar = "Test virus signature to check server antivirus."
        desc_zero = "Zero-size file to test empty data handling."
        desc_broken = "File with invalid magic bytes (JPG with garbage inside)."
        desc_ext = "Executable masked as an image (photo.jpg.exe)."
        desc_bom = "CSV file with hidden BOM bytes at start (breaks imports)."

    traps = {
        "EICAR (Virus Test)": desc_eicar,
        "Zero-Byte (0 KB)": desc_zero,
        "Broken Header": desc_broken,
        "Double Extension": desc_ext,
        "BOM CSV": desc_bom,
    }

    with st.container(border=True):
        f_type = st.selectbox(
            ("Тип ловушки" if lang == "RU" else "Type"), list(traps.keys())
        )
        st.caption(f"ℹ️ {traps[f_type]}")

        if st.button("🚀 " + ("Сгенерировать" if lang == "RU" else "Create")):
            fname, content = "trap.txt", b"test"
            if "EICAR" in f_type:
                fname, content = (
                    "eicar.com",
                    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*",
                )
            elif "Zero-Byte" in f_type:
                fname, content = "empty.pdf", b""
            elif "Broken" in f_type:
                fname, content = "broken.jpg", b"\xff\xd8\xff\xe0" + b"\x00" * 10
            elif "BOM" in f_type:
                fname, content = "test.csv", b"\xef\xbb\xbfID,Name\n1,Test"

            st.download_button(
                ("📥 Скачать" if lang == "RU" else "Download"), content, file_name=fname
            )


def render_data_sets(lang):
    st.markdown(
        "### 📊 " + ("Массовая генерация (Chaos CSV)" if lang == "RU" else "Mass Chaos")
    )
    count = st.slider(("Строк:" if lang == "RU" else "Rows:"), 5, 500, 50)

    if st.button("⚡ " + ("Создать таблицу" if lang == "RU" else "Generate")):
        bad = ["<script>alert(1)</script>", "NaN", "null", "\0", "' OR 1=1", "   "]
        data = [
            {
                "id": i + 1,
                "field": random.choice(bad),
                "num": random.choice([-1, 0, 2147483647]),
            }
            for i in range(count)
        ]
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "📥 Export CSV", df.to_csv(index=False).encode("utf-8-sig"), "chaos.csv"
        )


def render_testing_guide(lang):
    if lang == "RU":
        st.markdown("""
        ### 🧠 Гайд по негативному тестированию (Middle QA Edition)

        #### 1. Конструктор атак (Поля ввода)
        * **Кейс XSS:** Вставьте скрипт в поле "Имя профиля".
            * **Как проверить:** Сохраните и обновите страницу. Если появилось окно `alert` — уязвимость найдена. 
        * **Кейс Нулевой байт (`\0`):** Вставьте в поле поиска.
            * **Как проверить:** Посмотрите логи бэкенда. Если запрос обрезался на этом символе, сервер неправильно обрабатывает строки.
        * **Кейс Границы (2000 симв.):** Вставьте в описание товара.
            * **Как проверить:** Если БД упала с ошибкой `Data too long`, значит на бэкенде отсутствует валидация длины перед записью.

        #### 2. Файлы-ловушки (Uploads)
        * **Кейс EICAR:** Загрузите файл как "Аватар".
            * **Как проверить:** Система **обязана** выдать ошибку (400 или "Virus detected"). Если файл загрузился — на сервере нет антивирусного сканера.
        * **Кейс Broken Header:** Загрузите "битый" JPG.
            * **Как проверить:** Бэкенд должен проверить MIME-тип (Magic bytes). Ожидаем ошибку валидации формата.

        #### 📋 Чек-лист Middle QA:
        1.  **400/422 Bad Request:** Идеально (валидация сработала).
        2.  **200 OK (Текст как есть):** Безопасно (данные экранированы).
        3.  **500 Internal Error:** **Bug.** Необработанное исключение.
        4.  **Скрипт выполнился:** **Critical Security Bug.**
        """)
    else:
        st.markdown("""
        ### 🧠 Negative Testing Guide (Middle QA Edition)

        #### 1. Attack Constructor (Inputs)
        * **XSS Case:** Insert a script into the "Profile Name" field.
            * **Validation:** Save and refresh. If an `alert` box pops up — vulnerability found.
        * **Null Byte Case (`\0`):** Insert into the search field.
            * **Validation:** Check backend logs. If the query gets truncated at this symbol, strings are handled improperly (C-style).
        * **Boundaries Case (2000 chars):** Insert into product description.
            * **Validation:** If the DB crashes with `Data too long`, backend length validation is missing.

        #### 2. File Traps (Uploads)
        * **EICAR Case:** Upload the file as an "Avatar".
            * **Validation:** The system **must** return an error (400 or "Virus detected"). If uploaded, there's no AV scanner.
        * **Broken Header Case:** Upload a "broken" JPG.
            * **Validation:** Backend must check the MIME type (Magic bytes). Expecting format validation error.

        #### 📋 Middle QA Checklist:
        1.  **400/422 Bad Request:** Perfect (Validation triggered).
        2.  **200 OK (Text as is):** Safe (Data is escaped).
        3.  **500 Internal Error:** **Bug.** Unhandled exception.
        4.  **Script executed:** **Critical Security Bug.**
        """)

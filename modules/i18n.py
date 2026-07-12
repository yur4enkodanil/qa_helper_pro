import streamlit as st

# Словарь с переводами
TRANSLATIONS = {
    "RU": {
        # about_lab
        "about_header": "🚀 QA Helper Pro",
        "about_subheader": "Ультимативный комбайн для Middle QA инженера",
        "about_desc": """
        **QA Helper Pro** — это экосистема инструментов, созданная для автоматизации рутинных задач тестирования, 
        проверки безопасности и анализа производительности веб-приложений. 
        Разработано тестировщиком для тестировщиков.
        """,
        "about_modules_header": "📚 Функциональные модули:",
        "about_module_matrix": "**📊 Матрица тестов:** Генерация комбинаций проверок методами Pairwise и Full Combinatorial. Экономит время на планировании.",
        "about_module_screenshot": "**📸 Сравнение скриншотов:** Pixel Perfect анализ визуальных регрессий. Сравнивайте эталон и текущий результат.",
        "about_module_file_lab": "**📁 Файловый цех:** Генерация файлов любого веса (от КБ до ГБ) и формата для проверки лимитов загрузки.",
        "about_module_data_gen": "**🧪 Генератор данных:** Мгновенное создание реалистичных ФИО, ИНН, адресов и данных банковских карт.",
        "about_module_negative": "**💀 Негативные сценарии:** Библиотека хаоса для проверки безопасности (XSS, SQLi, Null-байты) и файлов-ловушек.",
        "about_module_emulator": "**🖥️ Эмулятор экранов:** Проверка адаптивности под любые мониторы (от 1024x768 до 2K) и мобильные устройства.",
        "about_module_links": "**🔗 Анализатор ссылок:** Трассировка цепочек редиректов и детальный разбор UTM-меток для проверки маркетинга.",
        "about_module_test_design": "**🧠 Тест-дизайн:** Калькулятор для расчета граничных значений и классов эквивалентности.",
        "about_module_json": "**📦 JSON Lab:** Валидация, форматирование и \"причесывание\" сложных JSON структур.",
        "about_module_diff": "**🧮 Сравнение текста:** Дифф-инструмент для анализа логов, конфигураций и больших текстовых массивов.",
        "about_module_hash": "**🛡️ Проверить хеш:** Быстрый расчет контрольных сумм MD5 и SHA-256 для контроля целостности файлов.",
        "about_module_visual": "**👁️ Визуальная проверка:** Анализ метаданных (EXIF) и глубокая проверка свойств изображений.",
        "about_module_repeater": "**🕹️ Повторитель запросов:** Отправка множества запросов к API для базового стресс-тестирования по количеству или времени.",
        "about_module_log_analyzer": "**📜 Анализатор логов:** Фильтрация и анализ больших лог-файлов, поиск ошибок и статистика.",
        "about_module_base64": "**🧬 Base64 Кодер:** Кодирование и декодирование данных в формат Base64 для работы с API и токенами.",
        "about_module_api_client": "**📡 API Клиент:** Отправка HTTP-запросов (GET, POST и др.) и анализ ответов сервера.",
        "about_module_notes": "**📝 Заметки:** Временный буфер для хранения данных сессии, которые не должны потеряться.",
        "about_module_logs": "**🪲 Журнал ошибок:** Просмотр системных логов и ошибок, возникших во время работы.",
        "about_module_about": "**ℹ️ О программе:** Информация о версии, авторе и использованных технологиях.",
        "about_author_header": "👨‍💻 Автор проекта",
        "about_author_desc": "Если у вас есть идеи по улучшению софта или вы нашли баг — пишите!",
        "about_author_email": "yur4enko.danil.18@gmail.com",

        # log_analyzer_lab
        "log_analyzer_header": "📜 Анализатор логов",
        "log_analyzer_tab_upload": "Загрузить файл",
        "log_analyzer_tab_paste": "Вставить текст",
        "log_analyzer_upload_label": "Выберите .log или .txt файл для анализа:",
        "log_analyzer_paste_label": "Или вставьте сырой текст лога сюда:",
        "log_analyzer_processing": "Анализирую строки...",
        "log_analyzer_button_file": "🔬 Проанализировать файл",
        "log_analyzer_button_text": "🔬 Проанализировать текст",
        "log_analyzer_stats_header": "Статистика по уровням",
        "log_analyzer_total_lines": "Всего строк",
        "log_analyzer_filters_header": "Фильтры и поиск",
        "log_analyzer_search_label": "Поиск по тексту (регистр не важен):",
        "log_analyzer_search_placeholder": "Например: payment failed или user_id=123",
        "log_analyzer_levels_label": "Фильтр по уровням:",
        "log_analyzer_results_info": "Найдено строк: {count}",
        "log_analyzer_warn_no_file": "Сначала выберите файл для загрузки.",
        "log_analyzer_warn_no_text": "Сначала вставьте текст в поле.",
        "log_analyzer_welcome_info": "Загрузите или вставьте лог, чтобы начать анализ.",

        # base64_lab
        "base64_header": "🧬 Base64 Кодер / Декодер",
        "base64_encode_header": "Кодировать в Base64",
        "base64_decode_header": "Декодировать из Base64",
        "base64_input_label": "Входные данные:",
        "base64_decode_error": "Ошибка декодирования! Проверьте входные данные.",
        "base64_button_encode": "Кодировать",
        "base64_button_decode": "Декодировать",

        # api_client_lab
        "history_header": "История запросов",
        "history_clear": "Очистить историю",
        "history_empty": "История пуста",
        "history_replay": "Повторить",
        "history_delete": "Удалить",
        "curl_expander": "🌀 Импорт из cURL",
        "curl_label": "Вставьте cURL команду:",
        "curl_button": "Разобрать и вставить",
        "curl_error": "Не удалось разобрать cURL. Проверьте команду.",
        "guide_header": "💡 Как использовать API Клиент?",
        "send_button": "🚀 Отправить",
        "params_tab": "Параметры",
        "headers_tab": "Заголовки",
        "body_tab": "Тело",
        "response_header": "Ответ сервера",
        "response_status": "Статус",
        "response_time": "Время",
        "response_size": "Размер",
        "response_body_tab": "Тело ответа",
        "response_headers_tab": "Заголовки ответа",
        "api_client_guide_content": "1.  **Отправка запроса:** Заполните поля и нажмите \"Отправить\". Результат появится ниже.\n2.  **История:** Каждый запрос сохраняется справа. Используйте \"Повторить\", чтобы загрузить его параметры, или \"Удалить\" для очистки.\n3.  **Импорт из cURL:** Скопируйте cURL-команду (например, из DevTools браузера), вставьте в поле \"Импорт из cURL\" и нажмите \"Разобрать\".",

        # viewport_lab
        "viewport_header": "🖥️ Эмулятор экранов",
        "viewport_info": "Открывает целевой URL в отдельном окне с точными размерами монитора или смартфона.",
        "viewport_url_label": "Введите URL страницы:",
        "viewport_cat_desktop": "--- ДЕСКТОП (Мониторы) ---",
        "viewport_cat_tablet": "--- ПЛАНШЕТЫ ---",
        "viewport_cat_mobile": "--- МОБИЛЬНЫЕ ---",
        "viewport_res_1": "1024x768 (XGA / Старый офис)",
        "viewport_res_2": "1280x1024 (SXGA / Квадрат)",
        "viewport_res_3": "1366x768 (HD / Ноутбуки)",
        "viewport_res_4": "1440x900 (WXGA+ / Мониторы)",
        "viewport_presets_label": "Предустановки разрешения:",
        "viewport_current_size": "**Текущий размер:** {width}x{height}",
        "viewport_custom_size": "Свой размер",
        "viewport_button_open": "🚀 Открыть в новом окне",
        "viewport_error_url": "Укажите ссылку!",
        "viewport_guide_header": "📝 Гайд по использованию и кроссбраузерности",
        "viewport_guide_content": """
            ### 🛠 Как эффективно тестировать верстку:
            
            * **Кроссбраузерность:** * Чтобы проверить сайт в другом браузере (например, в Safari или Edge), откройте **этот инструмент (QA Helper)** в нужном браузере. 
                * Все окна, которые вы откроете через кнопку, будут запускаться в том же браузере.
            * **Авторизация:**
                * Окна используют общие куки с текущим браузером. Если вы залогинены здесь — вы будете залогинены и в эмуляторе.
                * Если нужна "чистая" сессия без кук — запустите QA Helper в режиме **Инкогнито**.
            * **Офисные мониторы:**
                * Тестируйте `1024x768` и `1280x1024`. На них чаще всего "съезжают" кнопки в футере и боковые панели.
            * **Pop-up блокировщик:**
                * Если окно не открылось — посмотрите в правую часть адресной строки. Нажмите на иконку с красным крестиком и выберите **"Разрешить всплывающие окна"**.
        """
    },
    "EN": {
        # about_lab
        "about_header": "🚀 QA Helper Pro",
        "about_subheader": "Ultimate Toolbox for Middle QA Engineers",
        "about_desc": """
        **QA Helper Pro** is an ecosystem of tools designed to automate routine testing tasks, 
        security checks, and performance analysis.
        """,
        "about_modules_header": "📚 Module Overview:",
        "about_module_matrix": "**📊 Test Matrix:** Pairwise & Full Combinatorial test generation.",
        "about_module_screenshot": "**📸 Screenshot Diff:** Pixel-perfect visual regression analysis.",
        "about_module_file_lab": "**📁 File Lab:** Generate files of any size and format for upload testing.",
        "about_module_data_gen": "**🧪 Data Generator:** Mock realistic data (Names, IDs, Cards).",
        "about_module_negative": "**💀 Negative Lab:** Chaos library for security and negative testing.",
        "about_module_emulator": "**🖥️ Screen Emulator:** Viewport testing for various monitors and devices.",
        "about_module_repeater": "**🕹️ Request Repeater:** Send multiple requests to an API for basic stress testing by count or duration.",
        "about_module_log_analyzer": "**📜 Log Analyzer:** Filter and analyze large log files, find errors, and view statistics.",
        "about_module_base64": "**🧬 Base64 Coder:** Encode and decode data to/from Base64 format for API and token handling.",
        "about_module_logs": "**🪲 Error Log:** View system logs and errors that occurred during runtime.",
        "about_module_about": "**ℹ️ About:** Information about the version, author, and technologies used.",
        "about_module_links": "**🔗 Link Tracker:** Redirect chain analysis and UTM parsing.",
        "about_author_header": "👨‍💻 Contact Me",
        "about_author_desc": "", # No equivalent in the original EN version
        "about_author_email": "yur4enko.danil.18@gmail.com",

        # log_analyzer_lab
        "log_analyzer_header": "📜 Log Analyzer",
        "log_analyzer_tab_upload": "Upload File",
        "log_analyzer_tab_paste": "Paste Text",
        "log_analyzer_upload_label": "Select a .log or .txt file to analyze:",
        "log_analyzer_paste_label": "Or paste raw log text here:",
        "log_analyzer_processing": "Processing lines...",
        "log_analyzer_button_file": "🔬 Analyze File",
        "log_analyzer_button_text": "🔬 Analyze Text",
        "log_analyzer_stats_header": "Stats by Level",
        "log_analyzer_total_lines": "Total Lines",
        "log_analyzer_filters_header": "Filters & Search",
        "log_analyzer_search_label": "Search text (case-insensitive):",
        "log_analyzer_search_placeholder": "e.g., payment failed or user_id=123",
        "log_analyzer_levels_label": "Filter by levels:",
        "log_analyzer_results_info": "Found lines: {count}",
        "log_analyzer_warn_no_file": "Please select a file to upload first.",
        "log_analyzer_warn_no_text": "Please paste text into the field first.",
        "log_analyzer_welcome_info": "Upload or paste a log to begin analysis.",

        # base64_lab
        "base64_header": "🧬 Base64 Coder / Decoder",
        "base64_encode_header": "Encode to Base64",
        "base64_decode_header": "Decode from Base64",
        "base64_input_label": "Input data:",
        "base64_decode_error": "Decoding error! Check the input.",
        "base64_button_encode": "Encode",
        "base64_button_decode": "Decode",

        # api_client_lab
        "history_header": "Request History",
        "history_clear": "Clear History",
        "history_empty": "History is empty",
        "history_replay": "Replay",
        "history_delete": "Delete",
        "curl_expander": "🌀 Import from cURL",
        "curl_label": "Paste cURL command:",
        "curl_button": "Parse and Insert",
        "curl_error": "Failed to parse cURL. Check the command.",
        "guide_header": "💡 How to use the API Client?",
        "send_button": "🚀 Send",
        "params_tab": "Params",
        "headers_tab": "Headers",
        "body_tab": "Body",
        "response_header": "Server Response",
        "response_status": "Status",
        "response_time": "Time",
        "response_size": "Size",
        "response_body_tab": "Response Body",
        "response_headers_tab": "Response Headers",
        "api_client_guide_content": "1.  **Send Request:** Fill in the fields and click \"Send\". The result will appear below.\n2.  **History:** Each request is saved on the right. Use \"Replay\" to load its parameters or \"Delete\" to clean up.\n3.  **Import from cURL:** Copy a cURL command (e.g., from browser DevTools), paste it into the \"Import from cURL\" field, and click \"Parse\".",
        
        # viewport_lab
        "viewport_header": "🖥️ Screen Emulator",
        "viewport_info": "Opens target URL in a separate window with precise dimensions.",
        "viewport_url_label": "Enter Page URL:",
        "viewport_cat_desktop": "--- DESKTOP (Monitors) ---",
        "viewport_cat_tablet": "--- TABLETS ---",
        "viewport_cat_mobile": "--- MOBILE ---",
        "viewport_res_1": "1024x768 (XGA / Legacy Office)",
        "viewport_res_2": "1280x1024 (SXGA / Square)",
        "viewport_res_3": "1366x768 (HD / Laptops)",
        "viewport_res_4": "1440x900 (WXGA+ / Monitors)",
        "viewport_presets_label": "Resolution Presets:",
        "viewport_current_size": "**Current size:** {width}x{height}",
        "viewport_custom_size": "Custom size",
        "viewport_button_open": "🚀 Open in New Window",
        "viewport_error_url": "URL missing!",
        "viewport_guide_header": "📝 Usage & Cross-browser Guide",
        "viewport_guide_content": """
            ### 🛠 How to test layouts effectively:
            
            * **Cross-browser:** * To check the site in a different browser (e.g., Safari or Edge), open **this tool (QA Helper)** in that specific browser. 
                * All windows you launch via the button will open in the same browser context.
            * **Authorization:**
                * The windows share cookies with the current browser. If you are logged in here, you'll be logged in the emulator.
                * If you need a "clean" session without cookies — run QA Helper in **Incognito mode**.
            * **Office Monitors:**
                * Be sure to test `1024x768` and `1280x1024`. Footer buttons and sidebars frequently break on these resolutions.
            * **Pop-up Blocker:**
                * If the window didn't open — check the right side of the address bar. Click the red cross icon and select **"Allow pop-ups"**.
        """
    }
}

# Дополняем английский словарь ключами из русского, если их нет, чтобы избежать ошибок
for key in TRANSLATIONS["RU"]:
    if key not in TRANSLATIONS["EN"]:
        TRANSLATIONS["EN"][key] = key.replace("_", " ").title()

def get_text(key):
    """
    Возвращает текст для текущего языка из словаря TRANSLATIONS.
    """
    lang = st.session_state.get('lang', 'RU')
    # Возвращаем ключ, если перевод не найден, чтобы было легче отлаживать
    return TRANSLATIONS.get(lang, {}).get(key, key)
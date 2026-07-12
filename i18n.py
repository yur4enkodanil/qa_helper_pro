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
        "about_module_notes": "**📝 Заметки:** Временный буфер для хранения данных сессии, которые не должны потеряться.",
        "about_author_header": "👨‍💻 Автор проекта",
        "about_author_desc": "Если у вас есть идеи по улучшению софта или вы нашли баг — пишите!",
        "about_author_email": "[yur4enko.danil.18@gmail.com](mailto:yur4enko.danil.18@gmail.com)",

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
        "about_module_links": "**🔗 Link Tracker:** Redirect chain analysis and UTM parsing.",
        "about_author_header": "👨‍💻 Contact Me",
        "about_author_desc": "", # No equivalent in the original EN version
        "about_author_email": "yur4enko.danil.18@gmail.com",

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
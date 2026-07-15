import streamlit as st

def render_about_lab():
    lang = st.session_state.get('lang', 'RU')
    
    if lang == "RU":
        st.header("🚀 QA Helper Pro")
        st.subheader("Ультимативный комбайн для Middle QA инженера")
        
        st.markdown("""
        **QA Helper Pro** — это экосистема инструментов, созданная для автоматизации рутинных задач тестирования, 
        проверки безопасности и анализа производительности веб-приложений. 
        Разработано тестировщиком для тестировщиков.
        
        ---
        
        ### 📚 Функциональные модули:
        
        * **📊 Матрица тестов:** Генерация комбинаций проверок методами Pairwise и Full Combinatorial. Экономит время на планировании.
        * **📸 Сравнение скриншотов:** Pixel Perfect анализ визуальных регрессий. Сравнивайте эталон и текущий результат.
        * **📁 Файловый цех:** Генерация файлов любого веса (от КБ до ГБ) и формата для проверки лимитов загрузки.
        * **🧪 Генератор данных:** Мгновенное создание реалистичных ФИО, ИНН, адресов и данных банковских карт.
        * **💀 Негативные сценарии:** Библиотека хаоса для проверки безопасности (XSS, SQLi, Null-байты) и файлов-ловушек.
        * **🖥️ Эмулятор экранов:** Проверка адаптивности под любые мониторы (от 1024x768 до 2K) и мобильные устройства.
        * **🔗 Анализатор ссылок:** Трассировка цепочек редиректов и детальный разбор UTM-меток для проверки маркетинга.
        * **📱 Мобильная лаборатория:** Набор утилит для тестирования мобильных приложений: QR-коды, облачный буфер, анализатор локализации и другие.
        * **🎨 Frontend Анализатор:** Проверка доступности (Accessibility) и поиск битых ссылок на сайте.
        * **🕵️ UI Инспектор:** Визуальный анализ UI: распознавание текста (OCR), симулятор "челок", инспектор шрифтов, анализ GIF и линейка.
        * **️ Повторитель запросов:** Отправка множества запросов к API для базового стресс-тестирования.
        * **🧠 Тест-дизайн:** Калькулятор для расчета граничных значений и классов эквивалентности.
        * **📦 JSON Lab:** Валидация, форматирование и "причесывание" сложных JSON структур.
        * **🧮 Сравнение текста:** Дифф-инструмент для анализа логов, конфигураций и больших текстовых массивов.
        * **🛡️ Проверить хеш:** Быстрый расчет контрольных сумм MD5 и SHA-256 для контроля целостности файлов.
        * **👁️ Визуальная проверка:** Анализ метаданных (EXIF) и глубокая проверка свойств изображений.
        * **📜 Анализатор логов:** Фильтрация и анализ больших лог-файлов, поиск ошибок и статистика.
        * **🧬 Base64 Кодер:** Кодирование и декодирование данных для работы с API и токенами.
        * **📡 API Клиент:** Отправка HTTP-запросов (GET, POST и др.) и анализ ответов сервера.
        * **📝 Заметки:** Временный буфер для хранения данных сессии, которые не должны потеряться.
        
        ---
        
        ### 👨‍💻 Автор проекта
        Если у вас есть идеи по улучшению софта или вы нашли баг — пишите!
        
        **Email:** [yur4enko.danil.18@gmail.com](mailto:yur4enko.danil.18@gmail.com)
        """)
        
    else:
        st.header("🚀 QA Helper Pro")
        st.subheader("Ultimate Toolbox for Middle QA Engineers")
        
        st.markdown("""
        **QA Helper Pro** is an ecosystem of tools designed to automate routine testing tasks, 
        security checks, and performance analysis.
        
        ---
        
        ### 📚 Module Overview:
        
        * **📊 Test Matrix:** Pairwise & Full Combinatorial test generation.
        * **📸 Screenshot Diff:** Pixel-perfect visual regression analysis.
        * **📁 File Lab:** Generate files of any size and format for upload testing.
        * **🧪 Data Generator:** Mock realistic data (Names, IDs, Cards).
        * **💀 Negative Lab:** Chaos library for security and negative testing.
        * **🖥️ Screen Emulator:** Viewport testing for various monitors and devices.
        * **🔗 Link Tracker:** Redirect chain analysis and UTM parsing.
        * **📱 Mobile Lab:** A suite of utilities for mobile app testing: QR codes, cloud clipboard, localization analyzer, and more.
        * **🎨 Frontend Analyzer:** Accessibility (a11y) checks and broken link crawling.
        * **🕵️ UI Inspector:** Visual UI analysis: text recognition (OCR), notch simulator, font inspector, GIF analysis, and ruler.
        * **🕹️ Request Repeater:** Basic stress testing by sending multiple requests.
        * **🧠 Test Design:** Boundary Value Analysis (BVA) calculator.
        * **📦 JSON Lab:** Validate, format, and pretty-print complex JSON structures.
        * **🧮 Text Diff:** A diff tool for logs, configs, and large text blocks.
        * **🛡️ Hash Checker:** Quick MD5 & SHA-256 checksum calculation.
        * **👁️ Visual Check:** Image metadata (EXIF) analysis.
        * **📜 Log Analyzer:** Filter and analyze large log files for errors and stats.
        * **🧬 Base64 Coder:** Encode and decode data for API and token handling.
        * **📡 API Client:** Send HTTP requests (GET, POST, etc.) and analyze server responses.
        * **📝 Notes:** A temporary buffer to store session data.
        
        ---
        
        ### 👨‍💻 Contact Me
        **Email:** [yur4enko.danil.18@gmail.com](mailto:yur4enko.danil.18@gmail.com)
        """)

    app_version = st.session_state.get("app_version", "2.2.1")
    st.divider()
    st.caption(f"v{app_version} Stable | Created with passion for Quality Assurance")
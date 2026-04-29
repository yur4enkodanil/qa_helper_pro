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
        * **🧠 Тест-дизайн:** Калькулятор для расчета граничных значений и классов эквивалентности.
        * **📦 JSON Lab:** Валидация, форматирование и "причесывание" сложных JSON структур.
        * **🧮 Сравнение текста:** Дифф-инструмент для анализа логов, конфигураций и больших текстовых массивов.
        * **🛡️ Проверить хеш:** Быстрый расчет контрольных сумм MD5 и SHA-256 для контроля целостности файлов.
        * **👁️ Визуальная проверка:** Анализ метаданных (EXIF) и глубокая проверка свойств изображений.
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
        
        ---
        
        ### 👨‍💻 Contact Me
        **Email:** [yur4enko.danil.18@gmail.com](mailto:yur4enko.danil.18@gmail.com)
        """)

    st.divider()
    st.caption("v1.5 Stable | Created with passion for Quality Assurance")
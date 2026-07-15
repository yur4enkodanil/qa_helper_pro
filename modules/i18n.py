import streamlit as st

# Словарь с переводами
TRANSLATIONS = {
    "RU": {
        # about_lab
        "about_header": "🚀 QA Helper Pro",
        "about_subheader": "Ваш швейцарский нож в мире тестирования",
        "about_desc": """
        **QA Helper Pro** — это набор утилит, созданный для ускорения и упрощения повседневных задач QA-инженера. 
        От генерации тестовых данных до анализа UI — все необходимое в одном месте.
        """,
        "about_modules_header": "📚 Функциональные модули:",
        "about_module_api_client": "**📡 API Клиент:** Позволяет отправлять HTTP-запросы (GET, POST и др.), импортировать cURL и анализировать ответы сервера.",
        "about_module_repeater": "**🕹️ Повторитель запросов:** Инструмент для базового нагрузочного тестирования путем многократной отправки одного и того же запроса.",
        "about_module_mobile": "**📱 Мобильная лаборатория:** Набор утилит для мобильного тестирования: генератор QR-кодов, облачный буфер, гайды по разрешениям ОС и тестер диплинков.",
        "about_module_ui_inspector": "**🕵️ UI Инспектор:** Набор инструментов для визуального анализа: распознавание текста (OCR), симулятор \"челок\", инспектор шрифтов, анализ GIF и линейка.",
        "about_module_screenshot": "**📸 Сравнение скриншотов:** Позволяет найти визуальные различия между двумя изображениями, подсвечивая несовпадающие пиксели.",
        "about_module_emulator": "**🖥️ Эмулятор экранов:** Проверяет адаптивность верстки, открывая сайт в окне с разрешением популярных десктопных и мобильных устройств.",
        "about_module_frontend": "**🎨 Frontend Анализатор:** Автоматически сканирует страницу на предмет проблем с доступностью (WCAG) и ищет битые ссылки.",
        "about_module_file_lab": "**📁 Файловый цех:** Генерирует файлы заданного размера и формата для тестирования загрузок, а также создает сложные структуры папок.",
        "about_module_data_gen": "**🧪 Генератор данных:** Создает реалистичные тестовые данные: ФИО, адреса, номера карт, ИНН и многое другое.",
        "about_module_negative": "**💀 Негативные сценарии:** Библиотека готовых векторов атак (XSS, SQLi) и файлов-ловушек для базовых проверок безопасности.",
        "about_module_matrix": "**📊 Матрица тестов:** Помогает сократить количество тест-кейсов, генерируя комбинации проверок методами Pairwise и Full Combinatorial.",
        "about_module_test_design": "**🧠 Тест-дизайн:** Калькулятор для быстрого определения граничных значений (BVA) и классов эквивалентности.",
        "about_module_json": "**📦 JSON Lab:** Валидатор и форматер для JSON. Умеет исправлять мелкие синтаксические ошибки и отображать данные в виде дерева или таблицы.",
        "about_module_diff": "**🧮 Сравнение текста:** Находит и подсвечивает различия между двумя блоками текста, идеально для сравнения логов или конфигураций.",
        "about_module_log_analyzer": "**📜 Анализатор логов:** Позволяет фильтровать и искать нужную информацию в больших лог-файлах, а также показывает статистику по уровням логирования.",
        "about_module_hash": "**🛡️ Проверить хеш:** Рассчитывает контрольные суммы (MD5, SHA-256) для проверки целостности файлов.",
        "about_module_visual": "**👁️ Визуальная проверка:** Позволяет управлять базой эталонных скриншотов и сравнивать их с актуальными для поиска визуальных регрессий.",
        "about_module_base64": "**🧬 Base64 Кодер:** Инструмент для кодирования и декодирования данных в формат Base64.",
        "about_module_links": "**🔗 Анализатор ссылок:** Отслеживает цепочки редиректов и разбирает URL на компоненты, включая UTM-метки.",
        "about_module_notes": "**📝 Заметки:** Простой блокнот для временного хранения текста, который сохраняется между сессиями.",
        "about_module_logs": "**🪲 Журнал ошибок:** Просмотр системных логов и ошибок, возникших во время работы.",
        "about_module_about": "**ℹ️ О программе:** Информация о версии, авторе и использованных технологиях.",
        "about_author_header": "👨‍💻 Автор проекта",
        "about_author_desc": "Если у вас есть идеи по улучшению софта или вы нашли баг — пишите!",
        "about_author_email": "[yur4enko.danil.18@gmail.com](mailto:yur4enko.danil.18@gmail.com)",
        "about_author_telegram": "[@DanilYurc](https://t.me/DanilYurc)",

        # data_generator
        "data_gen_header": "🧪 Генератор данных",
        "data_gen_fields_expander": "⚙️ Выбор полей для генерации",
        "data_gen_cat_personal": "Личные данные",
        "data_gen_cat_location": "Локация/Работа",
        "data_gen_cat_tech": "IT/Технические",
        "data_gen_cat_finance": "Финансы/Прочее",
        "data_gen_field_full_name": "ФИО",
        "data_gen_field_phone": "Телефон",
        "data_gen_field_email": "Email",
        "data_gen_field_birthdate": "Дата рождения",
        "data_gen_field_inn": "ИНН",
        "data_gen_field_snils": "СНИЛС",
        "data_gen_field_address": "Адрес",
        "data_gen_field_company": "Компания",
        "data_gen_field_job": "Профессия",
        "data_gen_field_country_city": "Страна/Город",
        "data_gen_field_coordinates": "Координаты",
        "data_gen_field_ipv4": "IPv4 адрес",
        "data_gen_field_uuid4": "UUID v4",
        "data_gen_field_user_agent": "User Agent",
        "data_gen_field_mac_address": "MAC адрес",
        "data_gen_field_login": "Логин",
        "data_gen_field_password": "Пароль",
        "data_gen_field_card_number": "Номер карты",
        "data_gen_field_iban": "IBAN",
        "data_gen_field_hex_color": "HEX Цвет",
        "data_gen_field_sentence": "Текст (предложение)",
        "data_gen_rows_label": "Количество строк:",
        "data_gen_format_label": "Формат:",
        "data_gen_format_table": "Таблица",
        "data_gen_button_generate": "🚀 Сгенерировать данные",
        "data_gen_error_no_fields": "Выберите хотя бы одно поле!",
        "data_gen_spinner": "Генерирую данные...",
        "data_gen_button_download": "📥 Скачать результат (CSV)",

        # json_lab
        "json_lab_header": "📦 JSON Lab: Валидатор и Форматер",
        "json_lab_tab_paste": "Вставить текст",
        "json_lab_tab_upload": "Загрузить файл",
        "json_lab_upload_label": "Выберите .json или .txt файл:",
        "json_lab_paste_label": "Вставьте сырой JSON сюда:",
        "json_lab_button_fix": "🔧 Починить JSON",
        "json_lab_button_clear": "🧹 Очистить",
        "json_lab_valid": "✅ JSON валиден!",
        "json_lab_view_mode": "Режим просмотра:",
        "json_lab_mode_tree": "Дерево",
        "json_lab_mode_pretty": "Текст (Pretty)",
        "json_lab_mode_table": "Таблица",
        "json_lab_sort_keys": "Сортировать ключи",
        "json_lab_button_log": "📋 В лог",
        "json_lab_error_prefix": "❌ Ошибка",
        "json_lab_error_tip": "💡 Совет: Используйте двойные кавычки. Комментарии и лишние запятые запрещены.",

        # chat_log_lab
        "chat_log_header": "📋 Журнал чата",
        "chat_log_info": "Место для сохранения истории общения с ассистентом. Просто скопируйте и вставьте сюда диалог, чтобы вернуться к нему позже.",
        "chat_log_initial_title": "История чата",
        "chat_log_editor_label": "Содержимое журнала:",
        "chat_log_saved_toast": "Журнал сохранен!",

        "about_github_link": "⭐ Проект на GitHub",
        "about_tech_header": "⚙️ Технологии",
        "about_tech_content": """
- **Python 3.10+**
- **Streamlit** — для создания интерактивного веб-интерфейса.
- **Pandas** — для обработки данных и таблиц.
- **Playwright** — для автоматизации браузера в модуле "Frontend Анализатор".
- **Pillow (PIL)** — для работы с изображениями.
- **Requests** — для выполнения HTTP-запросов.
- **EasyOCR** — для распознавания текста на скриншотах.""",

        # link_lab
        "link_lab_header": "🔗 Анализатор ссылок",
        "link_lab_url_label": "Введите URL для анализа:",
        "link_lab_button_trace": "🛰️ Проверить редиректы",
        "link_lab_spinner_text": "Анализирую переходы...",
        "link_lab_no_redirects": "Редиректов не обнаружено (Прямая ссылка)",
        "link_lab_error_request": "Ошибка запроса: {e}",
        "link_lab_params_header": "📊 Разбор параметров",
        "link_lab_base_url": "**Base URL:**",
        "link_lab_utm_info": "ℹ️ В ссылке присутствуют UTM-метки для аналитики",
        "link_lab_no_params": "Параметры (query strings) не найдены.",
        "link_lab_redirects_header": "🛰️ Цепочка редиректов",
        "link_lab_table_status": "Статус",
        "link_lab_table_url": "URL",
        "link_lab_table_type": "Тип",
        "link_lab_table_time": "Время ответа",
        "link_lab_redirect_type_redirect": "Редирект",
        "link_lab_redirect_type_final": "Конечный URL",
        "link_lab_params_table_param": "Параметр",
        "link_lab_params_table_value": "Значение",
        "link_lab_guide_header": "💡 Как использовать этот инструмент?",
        "link_lab_guide_content": """
        1. **Проверка сокращателей:** Вставьте ссылку из `bit.ly` или `vk.cc`, чтобы увидеть реальный адрес назначения.
        2. **Проверка меток:** Убедитесь, что при редиректе с лендинга на основной сайт не «отвалились» `utm_source` или `client_id`.
        3. **Статус-коды:** Следите, чтобы редиректы были `301` (постоянные) или `302` (временные), а не падали в `404`.
        """,

        # log_viewer
        "log_viewer_header": "🪲 Журнал ошибок",
        "log_viewer_info": "Здесь отображаются технические ошибки, которые произошли во время работы приложения. Если что-то пошло не так, скопируйте этот текст и приложите к сообщению об ошибке.",
        "log_viewer_read_error": "Не удалось прочитать файл логов: ",
        "log_viewer_no_errors": "🎉 Ошибок не найдено. Журнал пуст.",
        "log_viewer_clear_button": "🗑️ Очистить журнал",
        "log_viewer_refresh_button": "🔄 Обновить",
        "log_viewer_download_button": "📥 Скачать лог",
        "log_viewer_not_created": "🎉 Файл логов еще не создан. Ошибок не было.",

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
        "log_analyzer_clear_button": "Очистить",
        "log_level_error": "ERROR",
        "log_level_warn": "WARN",
        "log_level_info": "INFO",
        "log_level_debug": "DEBUG",
        "log_analyzer_welcome_info": "Загрузите или вставьте лог, чтобы начать анализ.",
        "log_analyzer_search_regex": "Искать как RegEx",
        "log_analyzer_search_case_sensitive": "Учитывать регистр",
        "log_analyzer_context_lines": "Контекст (строк до/после)",
        "log_analyzer_context_lines_help": "Показать N строк до и после найденной строки. 0 - отключить.",
        "log_analyzer_auto_analysis_info": "Анализ запускается автоматически при изменении текста или загрузке файла.",

        # visual_lab
        "visual_header": "👁️ Визуальная проверка",
        "visual_ref_header": "1. Эталон (Reference)",
        "visual_ref_source_label": "Источник эталона:",
        "visual_ref_source_upload": "Загрузить новый",
        "visual_ref_source_db": "Выбрать из базы",
        "visual_ref_upload_label": "Загрузить эталонный скриншот",
        "visual_ref_db_empty": "База эталонов пуста.",
        "visual_ref_gallery_header": "Галерея эталонов",
        "visual_ref_load_button": "Сравнить",
        "visual_ref_delete_button": "Удалить",
        "visual_ref_delete_success": "Эталон {filename} удален.",
        "visual_ref_delete_error": "Ошибка при удалении: {e}",
        "visual_actual_header": "2. Актуальный результат",
        "visual_actual_upload_label": "Загрузить актуальный скриншот",
        "visual_save_expander": "💾 Сохранить текущий эталон в базу",
        "visual_save_filename_label": "Имя файла (без .png):",
        "visual_save_button": "Подтвердить сохранение",
        "visual_save_spinner": "Выполняется сохранение...",
        "visual_save_success": "Эталон {filename} сохранен!",
        "visual_save_error": "Ошибка сохранения: {e}",
        "visual_save_warn_name": "⚠️ Введите имя файла!",
        "visual_compare_button": "🚀 НАЧАТЬ СРАВНЕНИЕ",
        "visual_compare_error_size": "❌ Ошибка: Изображения должны быть одинакового размера для сравнения!",
        "visual_compare_info_size": "Эталон: {w1}x{h1} | Актуальный: {w2}x{h2}",
        "visual_compare_similarity": "Сходство",
        "visual_compare_identical": "✅ Изображения полностью идентичны!",
        "visual_compare_diffmap_caption": "Карта различий (Красный цвет = расхождения)",
        "visual_info_no_images": "Загрузите эталонное и актуальное изображения, чтобы начать.",
        "visual_caption_ref": "Эталон",
        "visual_caption_actual": "Актуальный",

        # base64_lab
        "base64_header": "🧬 Base64 Кодер / Декодер",
        "base64_encode_header": "Кодировать в Base64",
        "base64_decode_header": "Декодировать из Base64",
        "base64_input_label": "Входные данные:",
        "base64_result_label": "Результат:",
        "base64_file_uploader_label": "Или загрузите файл для кодирования:",
        "base64_decode_error": "Ошибка декодирования! Проверьте входные данные.",
        "base64_encode_error": "Ошибка кодирования!",
        "base64_button_encode": "Кодировать",
        "base64_button_decode": "Декодировать",
        "base64_decode_binary_warning": "⚠️ Декодированные данные не являются текстом (UTF-8). Возможно, это бинарный файл.",
        "base64_download_binary_button": "📥 Скачать бинарный файл",

        # frontend_lab
        "frontend_lab_header": "🎨 Frontend Анализатор",
        "frontend_lab_tab_accessibility": "Доступность (a11y)",
        "frontend_lab_tab_links": "Битые ссылки",
        "frontend_url_label": "URL для анализа:",
        "frontend_button_check": "🔍 Проверить",
        "frontend_button_crawl": "🕷️ Начать поиск",
        "frontend_accessibility_running": "Запускаю браузер и анализирую страницу...",
        "frontend_accessibility_results": "Результаты анализа доступности",
        "frontend_accessibility_no_violations": "✅ Нарушений доступности не найдено!",
        "frontend_accessibility_violations_found": "Найдено нарушений: {count}",
        "frontend_accessibility_impact": "Критичность",
        "frontend_accessibility_help": "Как исправить",
        "frontend_accessibility_nodes": "Проблемные элементы",
        "frontend_links_running": "Обхожу сайт в поисках ссылок...",
        "frontend_links_results": "Результаты поиска битых ссылок",
        "frontend_links_no_broken": "✅ Битых ссылок не найдено!",
        "frontend_links_broken_found": "Найдено битых ссылок: {count}",
        "frontend_links_table_url": "Битый URL",
        "frontend_links_table_status": "Статус",
        "frontend_links_table_source": "Найдено на странице",
        "frontend_lab_error_url": "Пожалуйста, введите URL.",
        "frontend_lab_error_generic": "Произошла ошибка: {error}",
        "frontend_lab_button_clear_cache": "Очистить кеш",
        "frontend_lab_crawl_depth_label": "Глубина обхода:",
        "frontend_lab_crawling_page": "Сканирую: {url}",

        # mobile_lab
        "mobile_lab_header": "📱 Мобильная лаборатория",
        "mobile_lab_tab_qr": "QR-код Хаб",
        "mobile_lab_tab_clipboard": "Облачный буфер",        
        "mobile_lab_tab_test_data_qr": "QR с тест-данными",
        "mobile_lab_tab_permissions": "Гайд по разрешениям", 
        "mobile_lab_tab_l10n": "Анализатор локализации",
        "mobile_lab_tab_deeplink": "Тестер Deep Link",
        "mobile_lab_tab_contrast": "Анализатор контраста (A11y)",
        "mobile_lab_guide_header": "💡 Как это использовать?",
        
        "qr_hub_guide": "1. **Генератор:** Введите любой текст или ссылку, чтобы мгновенно получить QR-код. Полезно для быстрой передачи URL на телефон.\n2. **Сканер:** Нажмите 'Начать сканирование', чтобы активировать камеру. Поднесите QR-код к камере, и его содержимое отобразится ниже.",
        "qr_hub_clipboard_caption": "Отсканируйте, чтобы открыть текст в браузере для копирования",
        "qr_hub_text_too_long": "Текст очень длинный. QR-код может быть сложным для сканирования.",


        "qr_hub_generator_header": "Генератор QR-кодов",
        "qr_hub_scanner_header": "Сканер QR-кодов",
        "qr_hub_input_label": "Текст или ссылка для кодирования:",
        "qr_hub_scan_button": "📷 Начать сканирование",
        "qr_hub_scan_stop": "⏹️ Остановить",
        "qr_hub_scan_result": "Результат сканирования:",
        "qr_hub_no_camera": "Камера не найдена или доступ запрещен.",
        "qr_hub_generate_button": "Генерировать QR-код",
        "qr_hub_uploader_label": "Или загрузите изображение:",
        "qr_hub_no_qr_found": "QR-код не найден на изображении.",

        "clipboard_guide": "Введите любой текст (токен, URL, кусок кода) в поле ниже. Инструмент сгенерирует QR-код, содержащий специальную HTML-страницу с вашим текстом. Отсканируйте код телефоном: в открывшемся браузере текст будет готов к копированию.",
        "clipboard_input_label": "Текст для передачи на телефон:",
        "clipboard_button": "📲 Создать QR-код для копирования",

        "test_data_qr_guide": "Выберите готовый набор тестовых данных из списка, чтобы сгенерировать QR-код. Это позволяет быстро вставлять сложные строки в поля ввода на мобильном устройстве.",
        "test_data_qr_select_label": "Выберите тип данных:",
        "test_data_qr_payload_header": "Полезная нагрузка (Payload):",
        "test_data_qr_generate_button": "Генерировать QR",

        "permissions_guide_guide": "Этот справочник содержит краткую информацию о ключевых изменениях в системе разрешений для разных версий ОС.",
        "permissions_guide_select_os": "Выберите версию ОС для просмотра гайда:",
        "permissions_guide_android14_header": "Ключевые изменения в Android 14 (API 34)",
        "permissions_guide_android14_content": """
        *   **Частичный доступ к фото/видео:** Пользователь может выбрать конкретные файлы, к которым приложение получит доступ.
            *   **Тест-кейс:** При запросе доступа к галерее выбрать "Выбрать фото". Убедиться, что приложение видит только выбранные файлы.
        *   **Ограничение на полноэкранные уведомления:** Только звонилки и будильники могут по умолчанию использовать `USE_FULL_SCREEN_INTENT`.
            *   **Тест-кейс:** Если ваше приложение не относится к этой категории, его полноэкранные уведомления должны отображаться как обычные.
        *   **Типы сервисов переднего плана (Foreground):** Приложения обязаны объявлять тип сервиса (например, `location`, `camera`).
            *   **Тест-кейс:** Проверить, что при работе сервиса в шторке уведомлений отображается корректная информация и приложение не падает.
        """,
        "permissions_guide_android13_header": "Ключевые изменения в Android 13 (API 33)",
        "permissions_guide_android13_content": """
        *   **Уведомления (POST_NOTIFICATIONS):** Приложения теперь должны явно запрашивать у пользователя разрешение на отправку push-уведомлений.
            *   **Тест-кейс:** При первом запуске или при действии, требующем уведомлений, должен появляться системный диалог запроса разрешения.
            *   **Тест-кейс (негативный):** Если пользователь запретил уведомления, приложение не должно их отправлять. Проверить в настройках, что переключатель выключен.
        *   **Гранулярный доступ к медиафайлам:** `READ_EXTERNAL_STORAGE` разделен на `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_MEDIA_AUDIO`.
            *   **Тест-кейс:** Приложение должно запрашивать доступ только к тому типу контента, который ему нужен (например, только к фото, а не ко всем файлам).
        """,
        "permissions_guide_android12_header": "Ключевые изменения в Android 12 (API 31)",
        "permissions_guide_android12_content": """
        *   **Приблизительная геолокация:** Пользователь может выбрать, давать ли приложению точные (`FINE`) или приблизительные (`COARSE`) координаты.
            *   **Тест-кейс:** Выдать приложению приблизительную геолокацию. Проверить, что карты и зависимые от гео функции работают корректно (например, показывают погоду для города, а не для точного адреса).
        *   **Индикаторы камеры и микрофона:** В статус-баре появляется зеленый значок, когда приложение использует камеру или микрофон.
            *   **Тест-кейс:** Запустить запись видео/аудио в приложении. Убедиться, что индикатор появился. Смахнуть шторку и проверить, что там указано ваше приложение.
        *   **Новые разрешения Bluetooth:** `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, `BLUETOOTH_ADVERTISE` заменяют старые. Для сканирования больше не нужен доступ к геолокации.
            *   **Тест-кейс:** Проверить, что приложение может найти Bluetooth-устройства, не запрашивая доступ к гео.
        """,
        "permissions_guide_android11_header": "Ключевые изменения в Android 11 (API 30)",
        "permissions_guide_android11_content": """
        *   **Одноразовые разрешения:** Пользователь может дать разрешение только на текущую сессию.
            *   **Тест-кейс:** Запросить доступ (камера, гео), выбрать "Только в этот раз". Свернуть и развернуть приложение — доступ сохраняется. Убить процесс и запустить заново — приложение снова запрашивает разрешение.
        *   **Автосброс разрешений:** Система отзывает разрешения у приложений, которыми долго не пользовались.
            *   **Тест-кейс:** Выдать разрешения. Перевести дату на 3 месяца вперед. Зайти в приложение — оно должно снова запросить разрешения (или использовать ADB для симуляции).
        *   **Scoped Storage (Принудительно):** Ограниченный доступ к файловой системе.
            *   **Тест-кейс:** Проверить, что приложение не может получить доступ к произвольным папкам, но может работать со своими файлами и медиатекой.
        """,
        "permissions_guide_ios17_header": "Ключевые изменения в iOS 17+",
        "permissions_guide_ios17_content": """
        *   **Расширенный доступ к фото:** Приложения могут запрашивать разрешение на добавление фото в библиотеку, не получая полного доступа к ней.
            *   **Тест-кейс:** При попытке сохранить изображение из приложения должен появиться системный диалог с опцией "Добавить фото".
        """,
        "permissions_guide_ios16_header": "Ключевые изменения в iOS 16+",
        "permissions_guide_ios16_content": """
        *   **Доступ к буферу обмена:** Приложения должны запрашивать разрешение перед доступом к буферу обмена.
            *   **Тест-кейс:** При попытке вставить текст из буфера обмена (например, код подтверждения) появляется системный запрос "Разрешить вставку?".
        *   **Live Activities:** Для запуска Live Activity (виджет на экране блокировки) требуется явное разрешение пользователя.
        """,
        "permissions_guide_ios15_header": "Ключевые изменения в iOS 15+",
        "permissions_guide_ios15_content": """
        *   **Private Relay (iCloud+):** Скрывает IP-адрес и DNS-запросы пользователя.
            *   **Тест-кейс:** Если логика приложения зависит от IP-адреса (например, определение страны), проверить его работу с включенной и выключенной функцией Private Relay.
        *   **Mail Privacy Protection:** Скрывает, открыл ли пользователь письмо, отправленное из приложения.
            *   **Тест-кейс:** Метрики Open Rate для email-рассылок из приложения становятся ненадежными.
        """,
        "permissions_guide_ios14_header": "Ключевые изменения в iOS 14+",
        "permissions_guide_ios14_content": """
        *   **Ограниченный доступ к фото:** Пользователь может дать доступ не ко всей галерее, а только к выбранным фото.
            *   **Тест-кейс:** При запросе доступа к галерее выбрать "Выбрать фото...". Убедиться, что приложение видит только выбранные изображения.
        *   **Приблизительная геолокация:** Пользователь может отключить "Точную геопозицию" при запросе.
            *   **Тест-кейс:** Отключить точную геопозицию. Проверить, что приложение корректно работает с приблизительными координатами (например, показывает погоду для города).
        *   **Доступ к локальной сети:** Приложения должны запрашивать разрешение на сканирование устройств в локальной сети.
            *   **Тест-кейс:** При активации функции поиска устройств в Wi-Fi (напр. Chromecast) должен появиться системный запрос.
        """,

        "l10n_guide": "1. Загрузите базовый файл локализации (например, английский).\n2. Загрузите один или несколько файлов с переводами.\n3. Инструмент автоматически сравнит их и покажет проблемы: отсутствующие ключи, несовпадение плейсхолдеров (`%s`, `%d`) или HTML-тегов, а также строки, перевод которых слишком длинный и может 'сломать' верстку.",
        "l10n_base_file_label": "1. Загрузите базовый файл локализации (напр. en.xml)",
        "l10n_translated_files_label": "2. Загрузите файлы с переводами (напр. de.xml, fr.xml)",
        "l10n_analyze_button": "🔍 Проанализировать файлы",
        "l10n_results_header": "Результаты анализа",
        "l10n_error_parsing": "Ошибка парсинга файла",
        "l10n_column_key": "Ключ",
        "l10n_column_issue": "Проблема",
        "l10n_column_base": "Базовое значение",
        "l10n_column_translated": "Перевод",

        "deeplink_guide": "Этот инструмент генерирует QR-код из введенного URI (например, `myapp://user/123` или `https://example.com/products`). Отсканируйте его на мобильном устройстве, чтобы проверить, корректно ли ваше приложение обрабатывает диплинки или универсальные/app ссылки.",
        "deeplink_uri_label": "Введите Deep Link / Universal Link:",
        "deeplink_generate_button": "🔗 Сгенерировать QR для ссылки",

        "contrast_guide": "Этот инструмент проверяет соответствие цветов текста и фона стандартам доступности WCAG. Контраст важен для людей с нарушениями зрения. \n- **AA (Минимальный):** Коэффициент ≥ 4.5:1. Обычный текст должен соответствовать. \n- **AAA (Повышенный):** Коэффициент ≥ 7:1. Идеальный уровень для максимальной читаемости.",
        "contrast_fg_label": "Цвет текста (Foreground)",
        "contrast_bg_label": "Цвет фона (Background)",
        "contrast_ratio_label": "Коэффициент контрастности",
        "contrast_result_aaa": "✅ AAA (Отлично)",
        "contrast_result_aa": "✅ AA (Хорошо)",
        "contrast_result_fail": "❌ Fail (Плохо)",
        "contrast_demo_text": "Пример текста для оценки",

        # file_lab & tree_lab
        "file_lab_tab_single": "📄 Одиночные (Генерация)",
        "file_lab_tab_tree": "🌳 Дерево папок",
        "file_lab_tab_replicator": "👯 Тиражирование",
        "file_lab_tkinter_warning": "Выбор папки работает только при локальном запуске приложения. В веб-версии используйте ручной ввод пути.",
        "file_gen_header": "Генератор файлов",
        "file_gen_save_path": "Путь сохранения:",
        "file_gen_browse_button": "📂 Обзор...",
        "file_gen_format": "Формат:",
        "file_gen_weight_in": "Вес в:",
        "file_gen_size": "Размер:",
        "file_gen_count": "Кол-во:",
        "file_gen_fill_type": "Тип заполнения:",
        "file_gen_fill_valid": "Валидное содержимое (по шаблону)",
        "file_gen_fill_random": "Случайные байты (Бинарный мусор)",
        "file_gen_fill_text": "Текстовый (Читаемые символы)",
        "file_gen_fill_null": "Пустой (NULL-байты)",
        "file_gen_supported_formats_expander": "ℹ️ Поддерживаемые форматы для валидного содержимого",
        "file_gen_available_formats": "Доступные форматы",
        "file_gen_unsupported_formats_caption": "Для остальных форматов будет создан файл с корректным расширением, но без валидного содержимого (0 байт).",
        "file_gen_start_button": "🚀 Начать генерацию",
        "file_gen_success": "Готово! {count} файлов создано в {target_dir}",
        "replicator_header": "Массовое копирование",
        "replicator_select_file_button": "📂 Выбрать файл...",
        "replicator_source_file": "Файл-источник:",
        "replicator_select_dest_button": "📂 Куда копировать...",
        "replicator_dest_folder": "Папка назначения:",
        "replicator_copies_count": "Количество копий:",
        "replicator_start_button": "👯 Запустить тиражирование",
        "replicator_error_no_file": "Файл не выбран или не существует!",
        "replicator_success": "Скопировано {copies} раз в {dest_dir}",
        "tree_lab_header": "🌳 Генератор сложных структур",
        "tree_lab_path": "Путь для дерева:",
        "tree_lab_min_size": "Мин:",
        "tree_lab_max_size": "Макс:",
        "tree_lab_all_formats": "🔓 Все доступные форматы",
        "tree_lab_all_formats_help": "Выбрать сразу все расширения из списка",
        "tree_lab_settings_expander": "⚙️ Настройка форматов и вложенности",
        "tree_lab_formats_selected": "Выбрано форматов: {count}",
        "tree_lab_select_extensions": "Выберите нужные расширения (сетка):",
        "tree_lab_folders_count": "Кол-во папок:",
        "tree_lab_files_count": "Кол-во файлов:",
        "tree_lab_start_button": "🚀 Вырастить дерево",
        "tree_lab_error_no_formats": "Выберите хотя бы один формат!",
        "tree_lab_progress_prepare": "Подготовка структуры...",
        "tree_lab_progress_creating": "Создание файлов: {current}/{total}",
        "tree_lab_success": "✅ Структура успешно создана в {path}!",
        "tree_lab_error_generic": "Ошибка",

        # integrity_lab
        "hash_header": "🛡️ Проверка целостности файла (Хеш)",
        "hash_upload_label": "1. Загрузите файл для проверки:",
        "hash_algo_label": "2. Выберите алгоритм хеширования:",
        "hash_expected_label": "3. (Опционально) Вставьте эталонный хеш для сравнения:",
        "hash_expected_placeholder": "Например: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "hash_calculate_button": "🔢 Рассчитать и сравнить",
        "hash_spinner": "Выполняется расчет...",
        "hash_success": "Хеш успешно рассчитан!",
        "hash_match": "✅ СОВПАДАЕТ! Файл не был изменен.",
        "hash_mismatch": "❌ НЕ СОВПАДАЕТ! Файл поврежден или изменен.",
        "hash_error_read": "Ошибка при чтении файла",
        "hash_warn_no_file": "Пожалуйста, загрузите файл.",

        # ui_inspector_lab
        "ui_inspector_header": "🕵️ UI Инспектор",
        "ui_inspector_tab_ocr": "Распознавание текста (OCR)",
        "ui_inspector_tab_notch": "Симулятор \"челок\"",
        "ui_inspector_tab_font_inspector": "Инспектор шрифтов",
        "ui_inspector_tab_gif_inspector": "Инспектор GIF",
        "ui_inspector_tab_ruler": "Линейка и сетка",
        "ui_inspector_ocr_guide": "Загрузите скриншот, и инструмент извлечет из него весь текст. Полезно для копирования сообщений об ошибках или ID, которые нельзя выделить в приложении.",
        "ui_inspector_ocr_upload": "Загрузите скриншот:",
        "ui_inspector_ocr_processing": "Распознаю текст...",
        "ui_inspector_ocr_result": "Распознанный текст:",
        "ui_inspector_notch_guide": "Загрузите скриншот, чтобы проверить, как он будет выглядеть на устройствах с разными вырезами на экране. Это помогает найти проблемы, когда важные элементы UI перекрываются \"челкой\".",
        "ui_inspector_notch_upload": "Загрузите скриншот:",
        "ui_inspector_notch_select": "Выберите тип выреза:",
        "ui_inspector_notch_classic": "Классическая \"чёлка\" (iPhone X)",
        "ui_inspector_notch_dynamic_island": "Островной вырез (iPhone 14 Pro)",
        "ui_inspector_notch_teardrop": "Каплевидный вырез",
        "ui_inspector_notch_center_hole": "Центральное отверстие (Android)",
        "ui_inspector_notch_corner_hole": "Угловое отверстие (Android)",
        "ui_inspector_font_guide": "Загрузите скриншот и выделите прямоугольником область с текстом. Инструмент попытается определить примерную высоту шрифта в пикселях.",
        "ui_inspector_font_upload": "Загрузите скриншот для анализа шрифта:",
        "ui_inspector_font_result": "Примерная высота шрифта:",
        "ui_inspector_font_tip": "Выделите прямоугольник вокруг одной строки текста для более точного результата.",
        "ui_inspector_gif_guide": "Загрузите GIF-анимацию, чтобы разложить ее на кадры. Это позволяет пошагово проанализировать анимацию, проверить ее плавность и найти визуальные артефакты.",
        "ui_inspector_gif_upload": "Загрузите GIF-файл:",
        "ui_inspector_gif_info_header": "Информация о файле",
        "ui_inspector_gif_frames": "Количество кадров:",
        "ui_inspector_gif_duration": "Длительность кадра (мс):",
        "ui_inspector_gif_download_frame": "📥 Скачать кадр",
        "ui_inspector_gif_select_frame": "Выберите кадр для просмотра:",
        "ui_inspector_ruler_guide": "Загрузите скриншот для pixel-perfect анализа. Вы можете наложить сетку 8x8 пикселей и измерить расстояние между элементами с помощью инструмента 'Линия'.",
        "ui_inspector_ruler_upload": "Загрузите скриншот для измерений:",
        "ui_inspector_ruler_grid": "Показать сетку 8x8 px",
        "ui_inspector_ocr_button_run": "🔍 Распознать текст",
        "ui_inspector_ruler_clear_button": "Очистить линии",
        "ui_inspector_ruler_distance": "Длина последней линии:",


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
        "api_client_header": "📡 API Клиент",
        "api_client_url_label": "URL запроса:",
        "api_client_method_label": "Метод:",
        "api_client_add_param_button": "Добавить параметр",
        "api_client_add_header_button": "Добавить заголовок",
        "api_client_key_placeholder": "Ключ (напр. 'limit')",
        "api_client_value_placeholder": "Значение (напр. '10')",
        "api_client_body_label": "Тело запроса (e.g. JSON):",
        "api_client_url_error": "❌ URL не может быть пустым!",
        "api_client_cookies_tab": "🍪 Cookies",
        "api_client_request_error": "❌ Ошибка выполнения запроса: {e}",
        "curl_parse_success": "✅ cURL команда успешно разобрана!",
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
        "viewport_res_1024_768_desc": "XGA / Старый офис",
        "viewport_res_1280_1024_desc": "SXGA / Квадрат",
        "viewport_res_1366_768_desc": "HD / Ноутбуки",
        "viewport_res_fullhd": "Full HD",
        "viewport_res_2k": "QHD / 2K",
        "viewport_preset_ipad_mini": "iPad Mini",
        "viewport_preset_ipad_air": "iPad Air",
        "viewport_preset_samsung_tab_s8": "Samsung Tab S8",
        "viewport_preset_iphone_se": "iPhone SE",
        "viewport_preset_iphone_14_pro": "iPhone 14 Pro",
        "viewport_preset_iphone_14_pro_max": "iPhone 14 Pro Max",
        "viewport_preset_samsung_s22": "Samsung Galaxy S22",
        "viewport_preset_pixel_7": "Google Pixel 7",
        "viewport_preset_samsung_a54": "Samsung Galaxy A54",
        "viewport_preset_xiaomi_redmi_12": "Xiaomi Redmi Note 12",
        "viewport_presets_label": "Предустановки разрешения:",
        "viewport_current_size": "**Текущий размер:** {width}x{height}",
        "viewport_custom_size": "Свой размер",
        "viewport_rotate_label": "Повернуть (Альбомная)",
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
        ,
        # visual_diff_lab
        "visual_diff_header": "Сравнение скриншотов",
        "visual_diff_info": "Загрузите эталонное и актуальное изображения для поиска визуальных различий. Изображения должны быть одинакового размера для точного анализа.",
        "visual_diff_expected_label": "Ожидаемое изображение (Эталон)",
        "visual_diff_actual_label": "Фактическое изображение",
        "visual_diff_warn_upload": "Пожалуйста, загрузите оба изображения для начала сравнения.",
        "visual_diff_button_compare": "Сравнить изображения",
        "visual_diff_warning_size": "Внимание: Размеры изображений отличаются! Эталон: {size1}, Фактическое: {size2}. Результат может быть неточным.",
        "visual_diff_result_similarity": "Процент сходства",
        "visual_diff_result_identical": "Изображения абсолютно идентичны!",
        "visual_diff_result_caption": "Карта различий (подсвечено красным)",
        "visual_diff_error_process": "Ошибка при обработке изображений: {e}"
        ,
        # repeater_lab
        "repeater_header": "🕹️ Повторитель запросов",
        "repeater_url_label": "URL эндпоинта:",
        "repeater_method_label": "Метод:",
        "repeater_concurrency_label": "Параллельных потоков:",
        "repeater_headers_label": "Заголовки (JSON):",
        "repeater_body_label": "Тело запроса (для POST/PUT/PATCH):",
        "repeater_mode_label": "Режим работы:",
        "repeater_mode_count": "По количеству запросов",
        "repeater_mode_duration": "По длительности",
        "repeater_req_count_label": "Количество запросов:",
        "repeater_duration_label": "Длительность теста:",
        "repeater_duration_unit_seconds": "Секунды",
        "repeater_duration_unit_minutes": "Минуты",
        "repeater_duration_unit_hours": "Часы",
        "repeater_start_button": "🚀 Начать отправку",
        "repeater_clear_button": "🧹 Очистить результаты",
        "repeater_live_results_header": "📈 Промежуточные результаты",
        "repeater_response_time_chart_header": "График времени ответа",
        "repeater_request_number_label": "Номер запроса",
        "repeater_response_time_ms_label": "Время ответа (мс)",
        "repeater_response_time_chart_title": "Время ответа по запросам",
        "repeater_stop_button": "⏹️ Остановить",
        "repeater_json_error_headers": "Ошибка в формате JSON для заголовков!",
        "repeater_json_error_body": "Ошибка в формате JSON для тела запроса!",
        "repeater_status_preparing": "Подготовка...",
        "repeater_status_running_count": "Выполняется: {done}/{total} | Потоков: {threads}",
        "repeater_status_running_duration": "Выполняется: {elapsed} / {total} сек. | Запросов: {req_count}",
        "repeater_results_header": "📊 Результаты",
        "repeater_no_requests_made": "Запросы не были выполнены.",
        "repeater_total_reqs": "Всего запросов",
        "repeater_success_reqs": "Успешно (2xx)",
        "repeater_client_errors": "Ошибки клиента (4xx)",
        "repeater_server_errors": "Ошибки сервера (5xx)",
        "repeater_other_errors": "Другие ошибки",
        "repeater_avg_time": "Среднее время",
        "repeater_min_time": "Мин. время",
        "repeater_max_time": "Макс. время",
        "repeater_ms": "мс",
        "repeater_status_codes_header": "Распределение по статусам:",
        "repeater_status_code": "Код ответа",
        "repeater_description": "Описание",
        "repeater_count": "Количество",
        "repeater_response_body": "Тело ответа / Ошибка",
        "repeater_url_empty_error": "URL не может быть пустым!",
        "repeater_guide_header": "💡 Как использовать Повторитель запросов?",
        "repeater_guide_content": """
        1.  **URL и Метод:** Укажите адрес эндпоинта и HTTP-метод.
        2.  **Заголовки и Тело:** Если необходимо, добавьте заголовки и тело запроса в формате JSON.
        3.  **Режим работы:**
            *   **По количеству запросов:** Укажите общее число запросов и количество параллельных потоков.
            *   **По длительности:** Задайте время, в течение которого будут отправляться запросы, и количество потоков.
        4.  **Начать отправку:** Нажмите кнопку, чтобы запустить тест. Вы увидите прогресс и результаты.
        5.  **Остановить:** В любой момент можно остановить выполнение теста кнопкой "Остановить".
        6.  **Результаты:** После завершения теста будет показана сводная статистика: общее количество запросов, успешные/неуспешные, среднее/минимальное/максимальное время ответа и распределение по статус-кодам.
        """
    },
    "EN": {
        # about_lab
        "about_header": "🚀 QA Helper Pro",
        "about_subheader": "Your Swiss Army Knife in the World of Testing",
        "about_desc": """
        **QA Helper Pro** is a suite of utilities designed to speed up and simplify the daily tasks of a QA engineer. 
        From test data generation to UI analysis - everything you need in one place.
        """,
        "about_modules_header": "📚 Module Overview:",
        "about_module_api_client": "**📡 API Client:** Allows sending HTTP requests (GET, POST, etc.), importing cURL, and analyzing server responses.",
        "about_module_repeater": "**🕹️ Request Repeater:** A tool for basic load testing by repeatedly sending the same request.",
        "about_module_mobile": "**📱 Mobile Lab:** A set of utilities for mobile testing: QR code generator, cloud clipboard, OS permission guides, and a deeplink tester.",
        "about_module_ui_inspector": "**🕵️ UI Inspector:** A set of tools for visual analysis: text recognition (OCR), notch simulator, font inspector, GIF analysis, and ruler.",
        "about_module_screenshot": "**📸 Screenshot Diff:** Allows finding visual differences between two images by highlighting mismatched pixels.",
        "about_module_emulator": "**🖥️ Screen Emulator:** Checks layout responsiveness by opening a site in a window with resolutions of popular desktop and mobile devices.",
        "about_module_frontend": "**🎨 Frontend Analyzer:** Automatically scans a page for accessibility issues (WCAG) and finds broken links.",
        "about_module_file_lab": "**📁 File Lab:** Generates files of a specified size and format for upload testing, and creates complex folder structures.",
        "about_module_data_gen": "**🧪 Data Generator:** Creates realistic test data: names, addresses, card numbers, tax IDs, and more.",
        "about_module_negative": "**💀 Negative Scenarios:** A library of ready-made attack vectors (XSS, SQLi) and file traps for basic security checks.",
        "about_module_matrix": "**📊 Test Matrix:** Helps reduce the number of test cases by generating test combinations using Pairwise and Full Combinatorial methods.",
        "about_module_test_design": "**🧠 Test Design:** A calculator for quickly determining Boundary Value Analysis (BVA) and Equivalence Partitioning.",
        "about_module_json": "**📦 JSON Lab:** A validator and formatter for JSON. It can fix minor syntax errors and display data as a tree or table.",
        "about_module_diff": "**🧮 Text Diff:** Finds and highlights differences between two blocks of text, ideal for comparing logs or configurations.",
        "about_module_log_analyzer": "**📜 Log Analyzer:** Allows filtering and searching for necessary information in large log files, and shows statistics by log level.",
        "about_module_hash": "**🛡️ Hash Checker:** Calculates checksums (MD5, SHA-256) to verify file integrity.",
        "about_module_visual": "**👁️ Visual Check:** Allows managing a database of reference screenshots and comparing them against actual ones to find visual regressions.",
        "about_module_base64": "**🧬 Base64 Coder:** A tool for encoding and decoding data to/from Base64 format.",
        "about_module_links": "**🔗 Link Tracker:** Traces redirect chains and parses URLs into components, including UTM tags.",
        "about_module_notes": "**📝 Notes:** A simple notepad for temporarily storing text that persists between sessions.",
        "about_module_logs": "**🪲 Error Log:** View system logs and errors that occurred during runtime.",
        "about_module_about": "**ℹ️ About:** Information about the version, author, and technologies used.",
        "about_author_header": "👨‍💻 Contact Me",
        "about_author_desc": "", # No equivalent in the original EN version
        "about_author_email": "yur4enko.danil.18@gmail.com",
        "about_author_telegram": "[@DanilYurc](https://t.me/DanilYurc)",

        # data_generator
        "data_gen_header": "🧪 Data Generator",
        "data_gen_fields_expander": "⚙️ Select fields to generate",
        "data_gen_cat_personal": "Personal Data",
        "data_gen_cat_location": "Location/Work",
        "data_gen_cat_tech": "IT/Technical",
        "data_gen_cat_finance": "Finance/Other",
        "data_gen_field_full_name": "Full Name",
        "data_gen_field_phone": "Phone",
        "data_gen_field_email": "Email",
        "data_gen_field_birthdate": "Birthdate",
        "data_gen_field_inn": "Tax ID (RU)",
        "data_gen_field_snils": "Pension ID (RU)",
        "data_gen_field_address": "Address",
        "data_gen_field_company": "Company",
        "data_gen_field_job": "Job Title",
        "data_gen_field_country_city": "Country/City",
        "data_gen_field_coordinates": "Coordinates",
        "data_gen_field_ipv4": "IPv4 Address",
        "data_gen_field_uuid4": "UUID v4",
        "data_gen_field_user_agent": "User Agent",
        "data_gen_field_mac_address": "MAC Address",
        "data_gen_field_login": "Login",
        "data_gen_field_password": "Password",
        "data_gen_field_card_number": "Card Number",
        "data_gen_field_iban": "IBAN",
        "data_gen_field_hex_color": "HEX Color",
        "data_gen_field_sentence": "Text (sentence)",
        "data_gen_rows_label": "Number of rows:",
        "data_gen_format_label": "Format:",
        "data_gen_format_table": "Table",
        "data_gen_button_generate": "🚀 Generate Data",
        "data_gen_error_no_fields": "Select at least one field!",
        "data_gen_spinner": "Generating data...",
        "data_gen_button_download": "📥 Download result (CSV)",

        # json_lab
        "json_lab_header": "📦 JSON Lab: Validator & Formatter",
        "json_lab_tab_paste": "Paste Text",
        "json_lab_tab_upload": "Upload File",
        "json_lab_upload_label": "Select a .json or .txt file:",
        "json_lab_paste_label": "Paste raw JSON here:",
        "json_lab_button_fix": "🔧 Auto-Fix JSON",
        "json_lab_button_clear": "🧹 Clear",
        "json_lab_valid": "✅ JSON is valid!",
        "json_lab_view_mode": "View mode:",
        "json_lab_mode_tree": "Tree",
        "json_lab_mode_pretty": "Pretty Text",
        "json_lab_mode_table": "Table",
        "json_lab_sort_keys": "Sort keys",
        "json_lab_button_log": "📋 Log it",
        "json_lab_error_prefix": "❌ Error",
        "json_lab_error_tip": "💡 Tip: Use double quotes. Comments and trailing commas are not allowed in standard JSON.",

        # chat_log_lab
        "chat_log_header": "📋 Chat Log",
        "chat_log_info": "A place to save the conversation history with the assistant. Just copy and paste the dialogue here to come back to it later.",
        "chat_log_initial_title": "Chat History",
        "chat_log_editor_label": "Log content:",
        "chat_log_saved_toast": "Log saved!",

        "about_github_link": "⭐ Project on GitHub",
        "about_tech_header": "⚙️ Technologies",
        "about_tech_content": """
- **Python 3.10+**
- **Streamlit** — for creating the interactive web interface.
- **Pandas** — for data and table manipulation.
- **Playwright** — for browser automation in the "Frontend Analyzer" module.
- **Pillow (PIL)** — for image processing.
- **Requests** — for making HTTP requests.
- **EasyOCR** — for text recognition on screenshots.""",

        # link_lab
        "link_lab_header": "🔗 Link Analyzer",
        "link_lab_url_label": "Enter URL to analyze:",
        "link_lab_button_trace": "🛰️ Trace Redirects",
        "link_lab_spinner_text": "Tracing redirects...",
        "link_lab_no_redirects": "No redirects found (Direct link)",
        "link_lab_error_request": "Request error: {e}",
        "link_lab_params_header": "📊 Parameters Breakdown",
        "link_lab_base_url": "**Base URL:**",
        "link_lab_utm_info": "ℹ️ UTM tags detected in the URL",
        "link_lab_no_params": "No query string parameters found.",
        "link_lab_redirects_header": "🛰️ Redirect Chain",
        "link_lab_table_status": "Status",
        "link_lab_table_url": "URL",
        "link_lab_table_type": "Type",
        "link_lab_table_time": "Response Time",
        "link_lab_redirect_type_redirect": "Redirect",
        "link_lab_redirect_type_final": "Final Destination",
        "link_lab_params_table_param": "Parameter",
        "link_lab_params_table_value": "Value",
        "link_lab_guide_header": "💡 How to use this tool?",
        "link_lab_guide_content": """
        1. **Check URL Shorteners:** Paste a link from `bit.ly` or similar services to see the actual destination address.
        2. **Verify Tags:** Ensure that `utm_source` or `client_id` are not lost during redirects from a landing page to the main site.
        3. **Status Codes:** Check that redirects are `301` (Permanent) or `302` (Temporary) and do not result in a `404` error.
        """,

        # log_viewer
        "log_viewer_header": "🪲 Error Log",
        "log_viewer_info": "This section displays technical errors that occurred while the application was running. If something went wrong, copy this text and attach it to your bug report.",
        "log_viewer_read_error": "Failed to read log file: ",
        "log_viewer_no_errors": "🎉 No errors found. The log is empty.",
        "log_viewer_clear_button": "🗑️ Clear Log",
        "log_viewer_refresh_button": "🔄 Refresh",
        "log_viewer_download_button": "📥 Download Log",
        "log_viewer_not_created": "🎉 Log file not created yet. No errors have occurred.",

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
        "log_analyzer_clear_button": "Clear",
        "log_level_error": "ERROR",
        "log_level_warn": "WARN",
        "log_level_info": "INFO",
        "log_level_debug": "DEBUG",
        "log_analyzer_welcome_info": "Upload or paste a log to begin analysis.",
        "log_analyzer_search_regex": "Search as RegEx",
        "log_analyzer_search_case_sensitive": "Case-sensitive",
        "log_analyzer_context_lines": "Context (lines before/after)",
        "log_analyzer_context_lines_help": "Show N lines before and after a matched line. 0 to disable.",
        "log_analyzer_auto_analysis_info": "Analysis runs automatically when text is changed or a file is uploaded.",

        # visual_lab
        "visual_header": "👁️ Visual Check",
        "visual_ref_header": "1. Baseline (Reference)",
        "visual_ref_source_label": "Baseline source:",
        "visual_ref_source_upload": "Upload New",
        "visual_ref_source_db": "Select from Database",
        "visual_ref_upload_label": "Upload baseline screenshot",
        "visual_ref_db_empty": "Reference database is empty.",
        "visual_ref_gallery_header": "Reference Gallery",
        "visual_ref_load_button": "Compare",
        "visual_ref_delete_button": "Delete",
        "visual_ref_delete_success": "Reference {filename} deleted.",
        "visual_ref_delete_error": "Error deleting file: {e}",
        "visual_actual_header": "2. Actual Result",
        "visual_actual_upload_label": "Upload actual screenshot",
        "visual_save_expander": "💾 Save current baseline to Database",
        "visual_save_filename_label": "Filename (without .png):",
        "visual_save_button": "Confirm Save",
        "visual_save_spinner": "Saving...",
        "visual_save_success": "Baseline {filename} saved!",
        "visual_save_error": "Save error: {e}",
        "visual_save_warn_name": "⚠️ Please enter a filename!",
        "visual_compare_button": "🚀 START COMPARISON",
        "visual_compare_error_size": "❌ Error: Images must have the same dimensions to be compared!",
        "visual_compare_info_size": "Baseline: {w1}x{h1} | Actual: {w2}x{h2}",
        "visual_compare_similarity": "Similarity",
        "visual_compare_identical": "✅ Images are identical!",
        "visual_compare_diffmap_caption": "Difference Map (Red = mismatch)",
        "visual_info_no_images": "Upload baseline and actual images to begin.",
        "visual_caption_ref": "Baseline",
        "visual_caption_actual": "Actual",

        # base64_lab
        "base64_header": "🧬 Base64 Coder / Decoder",
        "base64_encode_header": "Encode to Base64",
        "base64_decode_header": "Decode from Base64",
        "base64_input_label": "Input data:",
        "base64_result_label": "Result:",
        "base64_file_uploader_label": "Or upload a file to encode:",
        "base64_decode_error": "Decoding error! Check the input.",
        "base64_encode_error": "Encoding error!",
        "base64_button_encode": "Encode",
        "base64_button_decode": "Decode",
        "base64_decode_binary_warning": "⚠️ Decoded data is not valid UTF-8 text. It might be a binary file.",
        "base64_download_binary_button": "📥 Download binary file",

        # frontend_lab
        "frontend_lab_header": "🎨 Frontend Analyzer",
        "frontend_lab_tab_accessibility": "Accessibility (a11y)",
        "frontend_lab_tab_links": "Broken Links",
        "frontend_url_label": "URL to analyze:",
        "frontend_button_check": "🔍 Check",
        "frontend_button_crawl": "🕷️ Start Crawling",
        "frontend_accessibility_running": "Launching browser and analyzing page...",
        "frontend_accessibility_results": "Accessibility Analysis Results",
        "frontend_accessibility_no_violations": "✅ No accessibility violations found!",
        "frontend_accessibility_violations_found": "Violations found: {count}",
        "frontend_accessibility_impact": "Impact",
        "frontend_accessibility_help": "How to fix",
        "frontend_accessibility_nodes": "Problematic elements",
        "frontend_links_running": "Crawling the site for links...",
        "frontend_links_results": "Broken Links Scan Results",
        "frontend_links_no_broken": "✅ No broken links found!",
        "frontend_links_broken_found": "Broken links found: {count}",
        "frontend_links_table_url": "Broken URL",
        "frontend_links_table_status": "Status",
        "frontend_links_table_source": "Found on page",
        "frontend_lab_error_url": "Please enter a URL.",
        "frontend_lab_error_generic": "An error occurred: {error}",
        "frontend_lab_button_clear_cache": "Clear Cache",
        "frontend_lab_crawl_depth_label": "Crawl Depth:",
        "frontend_lab_crawling_page": "Crawling: {url}",
        
        # mobile_lab
        "mobile_lab_header": "📱 Mobile Lab",
        "mobile_lab_tab_qr": "QR Code Hub",
        "mobile_lab_tab_clipboard": "Cloud Clipboard",        
        "mobile_lab_tab_test_data_qr": "Test Data QR",
        "mobile_lab_tab_permissions": "Permissions Guide", 
        "mobile_lab_tab_l10n": "Localization Analyzer",
        "mobile_lab_tab_deeplink": "Deep Link Tester",
        "mobile_lab_tab_contrast": "Contrast Analyzer (A11y)",
        "mobile_lab_guide_header": "💡 How to use?",

        "qr_hub_guide": "1. **Generator:** Enter any text or link to instantly get a QR code. Useful for quickly transferring URLs to your phone.\n2. **Scanner:** Click 'Start Scanning' to activate the camera. Hold a QR code up to the camera, and its content will be displayed below.",
        "qr_hub_clipboard_caption": "Scan to open text in browser for copying",
        "qr_hub_text_too_long": "The text is very long. The QR code may be difficult to scan.",

        "qr_hub_generator_header": "QR Code Generator",
        "qr_hub_scanner_header": "QR Code Scanner",
        "qr_hub_input_label": "Text or link to encode:",
        "qr_hub_scan_button": "📷 Start Scanning",
        "qr_hub_scan_stop": "⏹️ Stop",
        "qr_hub_scan_result": "Scan Result:",
        "qr_hub_no_camera": "Camera not found or access denied.",
        "qr_hub_generate_button": "Generate QR Code",
        "qr_hub_uploader_label": "Or upload an image:",
        "qr_hub_no_qr_found": "QR code not found in the image.",

        "clipboard_guide": "Enter any text (token, URL, code snippet) into the field below. The tool will generate a QR code containing a special HTML page with your text. Scan the code with your phone: the browser will open with the text ready to be copied.",
        "clipboard_input_label": "Text to transfer to phone:",
        "clipboard_button": "📲 Create QR Code for Copying",

        "test_data_qr_guide": "Select a predefined test data set from the list to generate a QR code. This allows you to quickly insert complex strings into input fields on a mobile device.",
        "test_data_qr_select_label": "Select data type:",
        "test_data_qr_payload_header": "Payload:",
        "test_data_qr_generate_button": "Generate QR",

        "permissions_guide_guide": "This guide provides a brief overview of key changes in the permission system for different OS versions.",
        "permissions_guide_select_os": "Select OS version to see the guide:",
        "permissions_guide_android14_header": "Key Changes in Android 14 (API 34)",
        "permissions_guide_android14_content": """
        *   **Partial Photo/Video Access:** The user can select specific media files that the app can access.
            *   **Test Case:** When requesting gallery access, choose "Select photos". Verify the app can only see the selected files.
        *   **Full-Screen Notification Limit:** Only calling and alarm apps can use `USE_FULL_SCREEN_INTENT` by default.
            *   **Test Case:** If your app is not in this category, its full-screen notifications should be displayed as standard notifications.
        *   **Foreground Service Types:** Apps must declare a foreground service type (e.g., `location`, `camera`).
            *   **Test Case:** Check that when a service is running, the notification drawer shows correct information and the app does not crash.
        """,
        "permissions_guide_android13_header": "Key Changes in Android 13 (API 33)",
        "permissions_guide_android13_content": """
        *   **Notifications (POST_NOTIFICATIONS):** Apps must now explicitly request permission from the user to send push notifications.
            *   **Test Case:** On first launch or upon an action requiring notifications, a system permission dialog should appear.
            *   **Negative Test Case:** If the user denies permission, the app must not send notifications. Check in settings that the toggle is off.
        *   **Granular Media Access:** `READ_EXTERNAL_STORAGE` is split into `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_MEDIA_AUDIO`.
            *   **Test Case:** The app should only request access to the content type it needs (e.g., only photos, not all files).
        """,
        "permissions_guide_android12_header": "Key Changes in Android 12 (API 31)",
        "permissions_guide_android12_content": """
        *   **Approximate Location:** The user can choose to grant approximate (`COARSE`) location instead of precise (`FINE`).
            *   **Test Case:** Grant the app approximate location. Check that maps and geo-dependent features work correctly (e.g., show weather for the city, not the exact address).
        *   **Camera and Microphone Indicators:** A green icon appears in the status bar when an app uses the camera or microphone.
            *   **Test Case:** Start video/audio recording in the app. Ensure the indicator appears. Swipe down the notification shade and check that your app is listed as the source.
        *   **New Bluetooth Permissions:** `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, `BLUETOOTH_ADVERTISE` replace the old ones. Location access is no longer needed for scanning.
            *   **Test Case:** Verify the app can find Bluetooth devices without requesting location permission.
        """,
        "permissions_guide_android11_header": "Key Changes in Android 11 (API 30)",
        "permissions_guide_android11_content": """
        *   **One-time Permissions:** The user can grant permission for the current session only.
            *   **Test Case:** Request access (camera, location), choose "Only this time". Minimize and restore the app—access should persist. Kill the process and restart—the app should request permission again.
        *   **Auto-reset Permissions:** The system revokes permissions from apps that haven't been used for a long time.
            *   **Test Case:** Grant permissions. Move the device date 3 months forward. Open the app—it should request permissions again (or simulate with ADB).
        *   **Scoped Storage (Enforced):** Limited access to the file system.
            *   **Test Case:** Verify the app cannot access arbitrary folders but can work with its own files and the media library.
        """,
        "permissions_guide_ios17_header": "Key Changes in iOS 17+",
        "permissions_guide_ios17_content": """
        *   **Enhanced Photo Access:** Apps can request permission to add photos to the library without gaining full access to it.
            *   **Test Case:** When attempting to save an image from the app, a system dialog with an "Add Photos Only" option should appear.
        """,
        "permissions_guide_ios16_header": "Key Changes in iOS 16+",
        "permissions_guide_ios16_content": """
        *   **Clipboard Access:** Apps must request permission before accessing the clipboard.
            *   **Test Case:** When attempting to paste text from the clipboard (e.g., a verification code), a system prompt "Allow Paste?" should appear.
        *   **Live Activities:** Starting a Live Activity requires explicit user permission.
        """,
        "permissions_guide_ios15_header": "Key Changes in iOS 15+",
        "permissions_guide_ios15_content": """
        *   **Private Relay (iCloud+):** Hides the user's IP address and DNS queries.
            *   **Test Case:** If the app's logic depends on the IP address (e.g., country detection), test its functionality with Private Relay turned on and off.
        *   **Mail Privacy Protection:** Hides whether the user has opened an email sent from the app.
            *   **Test Case:** Open Rate metrics for email campaigns from the app become unreliable.
        """,
        "permissions_guide_ios14_header": "Key Changes in iOS 14+",
        "permissions_guide_ios14_content": """
        *   **Limited Photo Library Access:** The user can grant access to selected photos instead of the entire library.
            *   **Test Case:** When prompted for photo access, choose "Select Photos...". Verify the app can only see the selected images.
        *   **Approximate Location:** The user can disable "Precise Location" in the permission prompt.
            *   **Test Case:** Disable precise location. Check that the app functions correctly with approximate coordinates (e.g., shows weather for the city).
        *   **Local Network Access:** Apps must request permission to scan for devices on the local network.
            *   **Test Case:** When activating a feature that searches for Wi-Fi devices (e.g., Chromecast), a system prompt should appear.
        """,

        "l10n_guide": "1. Upload the base localization file (e.g., English).\n2. Upload one or more translated files.\n3. The tool will automatically compare them and show issues: missing keys, placeholder mismatches (`%s`, `%d`), or HTML tag mismatches, as well as strings where the translation is excessively long and might break the layout.",
        "l10n_base_file_label": "1. Upload base localization file (e.g., en.xml)",
        "l10n_translated_files_label": "2. Upload translated files (e.g., de.xml, fr.xml)",
        "l10n_analyze_button": "🔍 Analyze Files",
        "l10n_results_header": "Analysis Results",
        "l10n_error_parsing": "Error parsing file",
        "l10n_column_key": "Key",
        "l10n_column_issue": "Issue",
        "l10n_column_base": "Base Value",
        "l10n_column_translated": "Translated Value",

        "deeplink_guide": "This tool generates a QR code from a given URI (e.g., `myapp://user/123` or `https://example.com/products`). Scan it on a mobile device to test if your application correctly handles deep links or universal/app links.",
        "deeplink_uri_label": "Enter Deep Link / Universal Link:",
        "deeplink_generate_button": "🔗 Generate QR for Link",

        "contrast_guide": "This tool checks if text and background colors meet WCAG accessibility standards. Contrast is crucial for users with visual impairments.\n- **AA (Minimum):** Ratio ≥ 4.5:1. Normal text should meet this.\n- **AAA (Enhanced):** Ratio ≥ 7:1. The ideal level for maximum readability.",
        "contrast_fg_label": "Text Color (Foreground)",
        "contrast_bg_label": "Background Color",
        "contrast_ratio_label": "Contrast Ratio",
        "contrast_result_aaa": "✅ AAA (Excellent)",
        "contrast_result_aa": "✅ AA (Good)",
        "contrast_result_fail": "❌ Fail (Poor)",
        "contrast_demo_text": "Sample text for evaluation",

        # file_lab & tree_lab
        "file_lab_tab_single": "📄 Single Files (Generator)",
        "file_lab_tab_tree": "🌳 Folder Tree",
        "file_lab_tab_replicator": "👯 Replicator",
        "file_lab_tkinter_warning": "Folder selection only works when running the app locally. In the web version, please enter the path manually.",
        "file_gen_header": "File Generator",
        "file_gen_save_path": "Save path:",
        "file_gen_browse_button": "📂 Browse...",
        "file_gen_format": "Format:",
        "file_gen_weight_in": "Weight in:",
        "file_gen_size": "Size:",
        "file_gen_count": "Count:",
        "file_gen_fill_type": "Fill type:",
        "file_gen_fill_valid": "Valid content (from template)",
        "file_gen_fill_random": "Random bytes (Binary garbage)",
        "file_gen_fill_text": "Text (Readable characters)",
        "file_gen_fill_null": "Empty (NULL bytes)",
        "file_gen_supported_formats_expander": "ℹ️ Supported formats for valid content",
        "file_gen_available_formats": "Available formats",
        "file_gen_unsupported_formats_caption": "For other formats, a file with the correct extension will be created, but with no valid content (0 bytes).",
        "file_gen_start_button": "🚀 Start Generation",
        "file_gen_success": "Done! {count} files created in {target_dir}",
        "replicator_header": "Mass Replicator",
        "replicator_select_file_button": "📂 Select file...",
        "replicator_source_file": "Source file:",
        "replicator_select_dest_button": "📂 Select destination...",
        "replicator_dest_folder": "Destination folder:",
        "replicator_copies_count": "Number of copies:",
        "replicator_start_button": "👯 Start Replication",
        "replicator_error_no_file": "Source file not selected or does not exist!",
        "replicator_success": "Replicated {copies} times to {dest_dir}",
        "tree_lab_header": "🌳 Complex Structure Generator",
        "tree_lab_path": "Tree Path:",
        "tree_lab_min_size": "Min:",
        "tree_lab_max_size": "Max:",
        "tree_lab_all_formats": "🔓 All available formats",
        "tree_lab_all_formats_help": "Select all extensions from the list",
        "tree_lab_settings_expander": "⚙️ Formats and Nesting Settings",
        "tree_lab_formats_selected": "Selected formats: {count}",
        "tree_lab_select_extensions": "Select required extensions (grid):",
        "tree_lab_folders_count": "Folders count:",
        "tree_lab_files_count": "Files count:",
        "tree_lab_start_button": "🚀 Grow Tree",
        "tree_lab_error_no_formats": "Select at least one format!",
        "tree_lab_progress_prepare": "Preparing structure...",
        "tree_lab_progress_creating": "Creating files: {current}/{total}",
        "tree_lab_success": "✅ Structure successfully created in {path}!",
        "tree_lab_error_generic": "Error",

        # integrity_lab
        "hash_header": "🛡️ File Integrity Check (Hash)",
        "hash_upload_label": "1. Upload a file to check:",
        "hash_algo_label": "2. Select hashing algorithm:",
        "hash_expected_label": "3. (Optional) Paste the expected hash for comparison:",
        "hash_expected_placeholder": "e.g., e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "hash_calculate_button": "🔢 Calculate & Compare",
        "hash_spinner": "Calculating...",
        "hash_success": "Hash calculated successfully!",
        "hash_match": "✅ MATCH! The file is integral.",
        "hash_mismatch": "❌ MISMATCH! The file is corrupt or has been modified.",
        "hash_error_read": "Error reading file",
        "hash_warn_no_file": "Please upload a file.",

        # ui_inspector_lab
        "ui_inspector_header": "🕵️ UI Inspector",
        "ui_inspector_tab_ocr": "Text Recognition (OCR)",
        "ui_inspector_tab_notch": "Notch Simulator",
        "ui_inspector_tab_font_inspector": "Font Inspector",
        "ui_inspector_tab_gif_inspector": "GIF Inspector",
        "ui_inspector_tab_ruler": "Ruler & Grid",
        "ui_inspector_ocr_guide": "Upload a screenshot, and the tool will extract all text from it. Useful for copying error messages or IDs that cannot be selected in the app.",
        "ui_inspector_ocr_upload": "Upload screenshot:",
        "ui_inspector_ocr_processing": "Recognizing text...",
        "ui_inspector_ocr_result": "Recognized Text:",
        "ui_inspector_notch_guide": "Upload a screenshot to see how it will look on devices with different screen cutouts. This helps find issues where important UI elements are obscured by a notch.",
        "ui_inspector_notch_upload": "Upload screenshot:",
        "ui_inspector_notch_select": "Select notch type:",
        "ui_inspector_notch_classic": "Classic Notch (iPhone X-style)",
        "ui_inspector_notch_dynamic_island": "Pill Cutout (Dynamic Island)",
        "ui_inspector_notch_teardrop": "Waterdrop / Teardrop Notch",
        "ui_inspector_notch_center_hole": "Center Punch-hole (Android)",
        "ui_inspector_notch_corner_hole": "Corner Punch-hole (Android)",
        "ui_inspector_font_guide": "Upload a screenshot and draw a rectangle around a text area. The tool will attempt to determine the approximate font height in pixels.",
        "ui_inspector_font_upload": "Upload screenshot for font analysis:",
        "ui_inspector_font_result": "Approximate Font Height:",
        "ui_inspector_font_tip": "Draw a rectangle around a single line of text for a more accurate result.",
        "ui_inspector_gif_guide": "Upload a GIF animation to break it down into frames. This allows for step-by-step analysis of the animation, checking for smoothness and visual artifacts.",
        "ui_inspector_gif_upload": "Upload a GIF file:",
        "ui_inspector_gif_info_header": "File Information",
        "ui_inspector_gif_frames": "Frame Count:",
        "ui_inspector_gif_duration": "Frame Duration (ms):",
        "ui_inspector_gif_download_frame": "📥 Download Frame",
        "ui_inspector_gif_select_frame": "Select frame to view:",
        "ui_inspector_ruler_guide": "Upload a screenshot for pixel-perfect analysis. You can overlay an 8x8 pixel grid and measure the distance between elements using the 'Line' tool.",
        "ui_inspector_ruler_upload": "Upload screenshot for measurement:",
        "ui_inspector_ruler_grid": "Show 8x8 px grid",
        "ui_inspector_ocr_button_run": "🔍 Recognize Text",
        "ui_inspector_ruler_clear_button": "Clear Lines",
        "ui_inspector_ruler_distance": "Last line length:",

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
        "api_client_header": "📡 API Client",
        "api_client_url_label": "Request URL:",
        "api_client_method_label": "Method:",
        "api_client_add_param_button": "Add Parameter",
        "api_client_add_header_button": "Add Header",
        "api_client_key_placeholder": "Key (e.g. 'limit')",
        "api_client_value_placeholder": "Value (e.g. '10')",
        "api_client_body_label": "Request Body (e.g. JSON):",
        "api_client_url_error": "❌ URL cannot be empty!",
        "api_client_cookies_tab": "🍪 Cookies",
        "api_client_request_error": "❌ Request failed: {e}",
        "curl_parse_success": "✅ cURL command parsed successfully!",
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
        "viewport_res_1024_768_desc": "XGA / Legacy Office",
        "viewport_res_1280_1024_desc": "SXGA / Square",
        "viewport_res_1366_768_desc": "HD / Laptops",
        "viewport_res_fullhd": "Full HD",
        "viewport_res_2k": "QHD / 2K",
        "viewport_preset_ipad_mini": "iPad Mini",
        "viewport_preset_ipad_air": "iPad Air",
        "viewport_preset_samsung_tab_s8": "Samsung Tab S8",
        "viewport_preset_iphone_se": "iPhone SE",
        "viewport_preset_iphone_14_pro": "iPhone 14 Pro",
        "viewport_preset_iphone_14_pro_max": "iPhone 14 Pro Max",
        "viewport_preset_samsung_s22": "Samsung Galaxy S22",
        "viewport_preset_pixel_7": "Google Pixel 7",
        "viewport_preset_samsung_a54": "Samsung Galaxy A54",
        "viewport_preset_xiaomi_redmi_12": "Xiaomi Redmi Note 12",
        "viewport_presets_label": "Resolution Presets:",
        "viewport_current_size": "**Current size:** {width}x{height}",
        "viewport_custom_size": "Custom size",
        "viewport_rotate_label": "Rotate (Landscape)",
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
        ,
        # visual_diff_lab
        "visual_diff_header": "Visual Regression Testing",
        "visual_diff_info": "Upload the expected and actual images to detect visual differences. Images should be of the same size for accurate analysis.",
        "visual_diff_expected_label": "Expected Image (Baseline)",
        "visual_diff_actual_label": "Actual Image",
        "visual_diff_warn_upload": "Please upload both images to start the comparison.",
        "visual_diff_button_compare": "Compare Images",
        "visual_diff_warning_size": "Warning: Image sizes differ! Expected: {size1}, Actual: {size2}. The result may be inaccurate.",
        "visual_diff_result_similarity": "Similarity Score",
        "visual_diff_result_identical": "Images are completely identical!",
        "visual_diff_result_caption": "Difference Map (red highlights differences)",
        "visual_diff_error_process": "Error processing images: {e}"
        ,
        # repeater_lab
        "repeater_header": "🕹️ Request Repeater",
        "repeater_url_label": "Endpoint URL:",
        "repeater_method_label": "Method:",
        "repeater_concurrency_label": "Concurrency level:",
        "repeater_headers_label": "Headers (JSON):",
        "repeater_body_label": "Request Body (for POST/PUT/PATCH):",
        "repeater_mode_label": "Operating Mode:",
        "repeater_mode_count": "By Request Count",
        "repeater_mode_duration": "By Duration",
        "repeater_req_count_label": "Number of requests:",
        "repeater_duration_label": "Test Duration:",
        "repeater_duration_unit_seconds": "Seconds",
        "repeater_duration_unit_minutes": "Minutes",
        "repeater_duration_unit_hours": "Hours",
        "repeater_start_button": "🚀 Start Sending",
        "repeater_clear_button": "🧹 Clear Results",
        "repeater_live_results_header": "📈 Live Results",
        "repeater_response_time_chart_header": "Response Time Chart",
        "repeater_request_number_label": "Request Number",
        "repeater_response_time_ms_label": "Response Time (ms)",
        "repeater_response_time_chart_title": "Response Time Over Requests",
        "repeater_stop_button": "⏹️ Stop",
        "repeater_json_error_headers": "Error in JSON format for headers!",
        "repeater_json_error_body": "Error in JSON format for request body!",
        "repeater_status_preparing": "Preparing...",
        "repeater_status_running_count": "Running: {done}/{total} | Threads: {threads}",
        "repeater_status_running_duration": "Running: {elapsed} / {total} s | Requests: {req_count}",
        "repeater_results_header": "📊 Results",
        "repeater_no_requests_made": "No requests were made.",
        "repeater_total_reqs": "Total Requests",
        "repeater_success_reqs": "Successful (2xx)",
        "repeater_client_errors": "Client Errors (4xx)",
        "repeater_server_errors": "Server Errors (5xx)",
        "repeater_other_errors": "Other Errors",
        "repeater_avg_time": "Avg. Time",
        "repeater_min_time": "Min Time",
        "repeater_max_time": "Max Time",
        "repeater_ms": "ms",
        "repeater_status_codes_header": "Status Code Distribution:",
        "repeater_status_code": "Status Code",
        "repeater_description": "Description",
        "repeater_count": "Count",
        "repeater_response_body": "Response Body / Error",
        "repeater_url_empty_error": "URL cannot be empty!",
        "repeater_guide_header": "💡 How to use the Request Repeater?",
        "repeater_guide_content": """
        1.  **URL and Method:** Specify the endpoint address and HTTP method.
        2.  **Headers and Body:** If necessary, add headers and request body in JSON format.
        3.  **Operating Mode:**
            *   **By Request Count:** Specify the total number of requests and the number of concurrent threads.
            *   **By Duration:** Set the time during which requests will be sent and the number of threads.
        4.  **Start Sending:** Click the button to start the test. You will see the progress and results.
        5.  **Stop:** You can stop the test at any time using the "Stop" button.
        6.  **Results:** After the test is completed, a summary will be shown: total requests, successful/failed, average/minimum/maximum response time, and status code distribution.
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
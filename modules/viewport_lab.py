import streamlit as st
import random
from streamlit.components.v1 import html

def render_viewport_lab():
    lang = st.session_state.get('lang', 'RU')
    
    st.subheader("🖥️ Эмулятор экранов" if lang == "RU" else "🖥️ Screen Emulator")
    st.info("Открывает целевой URL в отдельном окне с точными размерами монитора или смартфона." if lang == "RU" 
            else "Opens target URL in a separate window with precise dimensions.")

    # 1. Настройки адреса
    target_url = st.text_input("Введите URL страницы:" if lang == "RU" else "Enter Page URL:", 
                               placeholder="https://example.com")

    # 2. Список разрешений
    devices = {
        "--- ДЕСКТОП (Мониторы) ---": None,
        "1024x768 (XGA / Старый офис)": (1024, 768),
        "1280x1024 (SXGA / Квадрат)": (1280, 1024),
        "1366x768 (HD / Ноутбуки)": (1366, 768),
        "1440x900 (WXGA+ / Мониторы)": (1440, 900),
        "1600x900 (HD+ Monitor)": (1600, 900),
        "1920x1080 (Full HD)": (1920, 1080),
        "2560x1440 (QHD / 2K)": (2560, 1440),
        
        "--- ПЛАНШЕТЫ ---": None,
        "iPad Mini (768x1024)": (768, 1024),
        "iPad Pro 11 (834x1194)": (834, 1194),
        
        "--- МОБИЛЬНЫЕ ---": None,
        "iPhone SE (375x667)": (375, 667),
        "iPhone 14 Pro (393x852)": (393, 852),
        "Small Android (360x800)": (360, 800)
    }

    col1, col2 = st.columns([2, 1])
    
    with col1:
        options = list(devices.keys())
        device_name = st.selectbox("Предустановки разрешения:" if lang == "RU" else "Resolution Presets:", options)
        
        if devices[device_name] is None:
            width, height = (1024, 768) # Дефолт при выборе заголовка
        else:
            width, height = devices[device_name]
    
    with col2:
        st.write(f"**Текущий размер:** {width}x{height}")
        is_custom = st.checkbox("Свой размер" if lang == "RU" else "Custom size")
        if is_custom:
            width = st.number_input("W", value=width, step=10)
            height = st.number_input("H", value=height, step=10)

    st.markdown("---")

    # 3. Кнопка запуска
    if st.button("🚀 " + ("Открыть в новом окне" if lang == "RU" else "Open in New Window")):
        if target_url:
            full_url = target_url if target_url.startswith(("http://", "https://")) else "https://" + target_url
            
            # Генерируем уникальное имя окна, чтобы можно было открыть несколько разных мониторов сразу
            win_name = f"window_{random.randint(1000, 9999)}"
            
            # JS: Центрируем окно на экране пользователя
            js_code = f"""
                <script>
                var left = (screen.width - {width}) / 2;
                var top = (screen.height - {height}) / 2;
                window.open('{full_url}', '{win_name}', 
                    'width={width},height={height},top='+top+',left='+left+',menubar=no,toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes');
                </script>
            """
            html(js_code, height=0)
        else:
            st.error("Укажите ссылку!" if lang == "RU" else "URL missing!")

    # 4. Методический гайд (Кроссбраузерность и безопасность)
    with st.expander("📝 " + ("Гайд по использованию и кроссбраузерности" if lang == "RU" else "Usage & Cross-browser Guide")):
        if lang == "RU":
            st.markdown("""
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
            """)
        else:
            st.write("To test in a different browser, simply open this QA Helper app in that browser.")
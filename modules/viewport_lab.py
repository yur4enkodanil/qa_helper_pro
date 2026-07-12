import streamlit as st
import random
from streamlit.components.v1 import html
from modules.i18n import get_text


def render_viewport_lab():
    lang = st.session_state.get("lang", "RU")
    t = get_text

    st.subheader(t("viewport_header"))
    st.info(t("viewport_info"))

    # 1. Настройки адреса
    target_url = st.text_input(
        t("viewport_url_label"),
        placeholder="https://example.com",
    )

    # 2. Список разрешений
    devices = {
        t("viewport_cat_desktop"): None,
        t("viewport_res_1"): (1024, 768),
        t("viewport_res_2"): (1280, 1024),
        t("viewport_res_3"): (1366, 768),
        t("viewport_res_4"): (1440, 900),
        "1600x900 (HD+ Monitor)": (1600, 900),
        "1920x1080 (Full HD)": (1920, 1080),
        "2560x1440 (QHD / 2K)": (2560, 1440),
        t("viewport_cat_tablet"): None,
        "iPad Mini (768x1024)": (768, 1024),
        "iPad Pro 11 (834x1194)": (834, 1194),
        t("viewport_cat_mobile"): None,
        "iPhone SE (375x667)": (375, 667),
        "iPhone 14 Pro (393x852)": (393, 852),
        "Small Android (360x800)": (360, 800),
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        options = list(devices.keys())
        device_name = st.selectbox(
            t("viewport_presets_label"),
            options,
        )

        if devices[device_name] is None:
            width, height = (1024, 768)  # Дефолт при выборе заголовка
        else:
            width, height = devices[device_name]

    with col2:
        st.write(t("viewport_current_size").format(width=width, height=height))
        is_custom = st.checkbox(t("viewport_custom_size"))
        if is_custom:
            width = st.number_input("W", value=width, step=10)
            height = st.number_input("H", value=height, step=10)

    st.markdown("---")

    # 3. Кнопка запуска
    if st.button(t("viewport_button_open")):
        if target_url:
            full_url = (
                target_url
                if target_url.startswith(("http://", "https://"))
                else "https://" + target_url
            )

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
            st.error(t("viewport_error_url"))

    # 4. Методический гайд (Кроссбраузерность и безопасность)
    with st.expander(
        f"📝 {t('viewport_guide_header')}"
    ):
        st.markdown(t("viewport_guide_content"))

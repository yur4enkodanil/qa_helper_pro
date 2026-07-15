import streamlit as st
import random
from streamlit.components.v1 import html
from modules.i18n import get_text


def render_viewport_lab():
    t = get_text

    st.subheader(t("viewport_header"))
    st.info(t("viewport_info"))

    # 1. Настройки адреса
    target_url = st.text_input(
        t("viewport_url_label"),
        placeholder="https://example.com",
    )

    # 2. Список разрешений с использованием ключей локализации
    device_presets = {
        t("viewport_cat_desktop"): None,
        f"1024x768 ({t('viewport_res_1024_768_desc')})": (1024, 768),
        f"1280x1024 ({t('viewport_res_1280_1024_desc')})": (1280, 1024),
        f"1366x768 ({t('viewport_res_1366_768_desc')})": (1366, 768),
        f"1920x1080 ({t('viewport_res_fullhd')})": (1920, 1080),
        f"2560x1440 ({t('viewport_res_2k')})": (2560, 1440),
        t("viewport_cat_tablet"): None,
        f"{t('viewport_preset_ipad_mini')} (768x1024)": (768, 1024),
        f"{t('viewport_preset_ipad_air')} (820x1180)": (820, 1180),
        f"{t('viewport_preset_samsung_tab_s8')} (800x1280)": (800, 1280),
        t("viewport_cat_mobile"): None,
        f"{t('viewport_preset_iphone_se')} (375x667)": (375, 667),
        f"{t('viewport_preset_iphone_14_pro')} (393x852)": (393, 852),
        f"{t('viewport_preset_iphone_14_pro_max')} (430x932)": (430, 932),
        f"{t('viewport_preset_samsung_s22')} (360x780)": (360, 780),
        f"{t('viewport_preset_pixel_7')} (412x915)": (412, 915),
        f"{t('viewport_preset_samsung_a54')} (360x800)": (360, 800),
        f"{t('viewport_preset_xiaomi_redmi_12')} (393x873)": (393, 873),
    }

    # Инициализация состояния для синхронизации
    if 'vp_width' not in st.session_state: st.session_state.vp_width = 1366
    if 'vp_height' not in st.session_state: st.session_state.vp_height = 768
    if 'vp_last_preset' not in st.session_state: st.session_state.vp_last_preset = f"1366x768 ({t('viewport_res_1366_768_desc')})"

    # --- UI ---
    device_name = st.selectbox(
        t("viewport_presets_label"),
        options=device_presets.keys(),
        key="vp_preset_select"
    )

    is_separator_selected = device_presets[device_name] is None

    # Синхронизация состояния при выборе пресета
    if st.session_state.vp_last_preset != device_name and not is_separator_selected:
        st.session_state.vp_last_preset = device_name
        w, h = device_presets[device_name]
        st.session_state.vp_width = w
        st.session_state.vp_height = h
        st.rerun()

    col_controls1, col_controls2 = st.columns(2)
    with col_controls1:
        is_rotated = st.checkbox(t("viewport_rotate_label"), key='vp_is_rotated')
    with col_controls2:
        is_custom = st.checkbox(t("viewport_custom_size"), key='vp_is_custom')

    # Отображение и редактирование размеров
    if is_custom:
        w_col, h_col = st.columns(2)
        st.session_state.vp_width = w_col.number_input("W", value=st.session_state.vp_width, step=10)
        st.session_state.vp_height = h_col.number_input("H", value=st.session_state.vp_height, step=10)

    final_width = st.session_state.vp_height if is_rotated else st.session_state.vp_width
    final_height = st.session_state.vp_width if is_rotated else st.session_state.vp_height
    st.info(t("viewport_current_size").format(width=final_width, height=final_height))

    st.markdown("---")

    # 3. Кнопка запуска
    if st.button(t("viewport_button_open"), disabled=is_separator_selected):
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
                var left = (screen.width - {final_width}) / 2;
                var top = (screen.height - {final_height}) / 2;
                window.open('{full_url}', '{win_name}', 
                    'width={final_width},height={final_height},top='+top+',left='+left+',menubar=no,toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes');
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

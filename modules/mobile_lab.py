import streamlit as st
from modules.i18n import get_text
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
from urllib.parse import quote
import pandas as pd
import re
import xml.etree.ElementTree as ET

# --- Helper Functions ---
def get_contrast_ratio(color1, color2):
    """Calculates WCAG contrast ratio between two hex colors."""
    def srgb_to_lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def get_luminance(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return 0.2126 * srgb_to_lin(r) + 0.7151 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)

    l1 = get_luminance(color1)
    l2 = get_luminance(color2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

def parse_android_xml(file):
    """Parses Android strings.xml file."""
    tree = ET.parse(file)
    root = tree.getroot()
    data = {}
    for string_tag in root.findall('string'):
        name = string_tag.get('name')
        value = string_tag.text or ""
        data[name] = value
    return data

def parse_ios_strings(file):
    """Parses iOS .strings file."""
    content = file.read().decode('utf-8')
    # Regex to find "key" = "value";
    pattern = re.compile(r'"(.*?)"\s*=\s*"(.*?)";')
    data = dict(pattern.findall(content))
    return data

def _process_qr_image(image_bytes):
    """Helper to decode QR code from image bytes and show result."""
    t = get_text
    try:
        image = Image.open(image_bytes)
        decoded_objects = decode(image)
        if decoded_objects:
            for obj in decoded_objects:
                st.success(f"**{t('qr_hub_scan_result')}**")
                st.code(obj.data.decode('utf-8'))
            return True
    except Exception:
        pass # Ignore errors for now
    st.warning(t('qr_hub_no_qr_found'))
    return False

# --- Tab Rendering Functions ---

def render_qr_hub_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("qr_hub_guide"))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {t('qr_hub_generator_header')}")
        qr_text = st.text_area(t("qr_hub_input_label"), height=150)
        if st.button(t("qr_hub_generate_button"), width='stretch'):
            qr_img = qrcode.make(qr_text)
            st.image(qr_img.get_image(), use_column_width=True)

    with col2:
        st.markdown(f"### {t('qr_hub_scanner_header')}")
        if 'qr_scanner_on' not in st.session_state:
            st.session_state.qr_scanner_on = False

        if st.button(t('qr_hub_scan_button') if not st.session_state.qr_scanner_on else t('qr_hub_scan_stop')):
            st.session_state.qr_scanner_on = not st.session_state.qr_scanner_on
            st.rerun()

        if st.session_state.qr_scanner_on:
            camera_bytes = st.camera_input("QR Scanner", label_visibility="collapsed")
            if camera_bytes:
                if _process_qr_image(camera_bytes):
                    st.session_state.qr_scanner_on = False
                    st.rerun()
        
        uploaded_qr_file = st.file_uploader(t("qr_hub_uploader_label"), type=["png", "jpg", "jpeg"])
        if uploaded_qr_file:
            _process_qr_image(uploaded_qr_file)

def render_clipboard_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("clipboard_guide"))

    text_to_copy = st.text_area(t("clipboard_input_label"), height=150)
    if len(text_to_copy) > 1500:
        st.warning(t("qr_hub_text_too_long"))

    if st.button(t("clipboard_button"), width='stretch'):
        if text_to_copy:
            # HTML-кодируем текст и создаем data URI для HTML-страницы
            encoded_text = text_to_copy.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            data_uri = f"data:text/html,<title>Copy Text</title><meta name=viewport content=width=device-width,initial-scale=1><textarea style='width:100%;height:80vh' readonly>{encoded_text}</textarea>"
            qr_img = qrcode.make(data_uri)
            st.image(qr_img.get_image(), width=300, caption=t("qr_hub_clipboard_caption"))

def render_test_data_qr_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("test_data_qr_guide"))

    TEST_DATA_PAYLOADS = {
        "Длинная строка (2000 симв.)": "A" * 2000,
        "Строка с эмодзи 🔥🚀": "Тест с эмодзи 🔥🚀",
        "Строка со спецсимволами": "!@#$%^&*()_+-=[]{}|;':\",./<>?`~",
        "SQL-инъекция": "' OR 1=1 --",
        "XSS-атака": "<script>alert('XSS')</script>",
        "Пустая строка": "",
        "Строка с пробелами по краям": "   leading and trailing spaces   ",
    }

    selected_payload_name = st.selectbox(t("test_data_qr_select_label"), list(TEST_DATA_PAYLOADS.keys()))
    payload_content = TEST_DATA_PAYLOADS[selected_payload_name]

    st.text_area(t("test_data_qr_payload_header"), value=payload_content, height=150, disabled=True)

    if st.button(t("test_data_qr_generate_button"), width='stretch'):
        qr_img = qrcode.make(payload_content)
        st.image(qr_img.get_image(), width=300)

def render_permissions_guide_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("permissions_guide_guide"))

    os_version = st.selectbox(t("permissions_guide_select_os"), 
                              ["Android 14", "Android 13", "Android 12", "Android 11", "iOS 17+", "iOS 16+", "iOS 15+", "iOS 14+"])

    if os_version == "Android 14":
        st.markdown(f"### {t('permissions_guide_android14_header')}")
        st.markdown(t('permissions_guide_android14_content'))
    elif os_version == "Android 13":
        st.markdown(f"### {t('permissions_guide_android13_header')}")
        st.markdown(t('permissions_guide_android13_content'))
    elif os_version == "Android 12":
        st.markdown(f"### {t('permissions_guide_android12_header')}")
        st.markdown(t('permissions_guide_android12_content'))
    elif os_version == "Android 11":
        st.markdown(f"### {t('permissions_guide_android11_header')}")
        st.markdown(t('permissions_guide_android11_content'))
    elif os_version == "iOS 17+":
        st.markdown(f"### {t('permissions_guide_ios17_header')}")
        st.markdown(t('permissions_guide_ios17_content'))
    elif os_version == "iOS 16+":
        st.markdown(f"### {t('permissions_guide_ios16_header')}")
        st.markdown(t('permissions_guide_ios16_content'))
    elif os_version == "iOS 15+":
        st.markdown(f"### {t('permissions_guide_ios15_header')}")
        st.markdown(t('permissions_guide_ios15_content'))
    elif os_version == "iOS 14+":
        st.markdown(f"### {t('permissions_guide_ios14_header')}")
        st.markdown(t('permissions_guide_ios14_content'))

def render_l10n_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("l10n_guide"))

    base_file = st.file_uploader(t("l10n_base_file_label"), type=['xml', 'strings'])
    translated_files = st.file_uploader(t("l10n_translated_files_label"), type=['xml', 'strings'], accept_multiple_files=True)

    if st.button(t("l10n_analyze_button"), width='stretch'):
        if not base_file or not translated_files:
            st.warning("Пожалуйста, загрузите базовый файл и хотя бы один файл перевода.")
            return

        issues = []
        try:
            if base_file.name.endswith('.xml'):
                base_data = parse_android_xml(base_file)
                parser = parse_android_xml
            else:
                base_data = parse_ios_strings(base_file)
                parser = parse_ios_strings
        except Exception as e:
            st.error(f"{t('l10n_error_parsing')} {base_file.name}: {e}")
            return

        placeholder_regex = re.compile(r'%[sd@]|{{\s*\w+\s*}}')

        for file in translated_files:
            try:
                translated_data = parser(file)
            except Exception as e:
                issues.append({"file": file.name, "key": "N/A", "issue": f"Parse Error: {e}", "base": "", "translated": ""})
                continue

            # Check for missing/extra keys
            base_keys = set(base_data.keys())
            translated_keys = set(translated_data.keys())

            for key in base_keys - translated_keys:
                issues.append({"file": file.name, "key": key, "issue": "Missing key", "base": base_data[key], "translated": ""})
            
            for key in translated_keys - base_keys:
                issues.append({"file": file.name, "key": key, "issue": "Extra key", "base": "", "translated": translated_data[key]})

            # Check common keys
            for key in base_keys.intersection(translated_keys):
                base_str = base_data[key]
                trans_str = translated_data[key]

                # Placeholder check
                base_placeholders = sorted(placeholder_regex.findall(base_str))
                trans_placeholders = sorted(placeholder_regex.findall(trans_str))
                if base_placeholders != trans_placeholders:
                    issues.append({"file": file.name, "key": key, "issue": "Placeholder mismatch", "base": base_str, "translated": trans_str})

                # Length check (translation is more than 3x longer and > 20 chars)
                if len(trans_str) > len(base_str) * 3 and len(trans_str) > 20:
                     issues.append({"file": file.name, "key": key, "issue": f"Length warning ({len(trans_str)} vs {len(base_str)})", "base": base_str, "translated": trans_str})

        st.markdown(f"### {t('l10n_results_header')}")
        if not issues:
            st.success("✅ Проблем не найдено!")
        else:
            df = pd.DataFrame(issues)
            df.rename(columns={
                "file": "Файл",
                "key": t("l10n_column_key"),
                "issue": t("l10n_column_issue"),
                "base": t("l10n_column_base"),
                "translated": t("l10n_column_translated")
            }, inplace=True)
            st.dataframe(df, use_container_width=True, hide_index=True)

def render_deeplink_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("deeplink_guide"))

    deeplink_uri = st.text_input(t("deeplink_uri_label"), placeholder="myapp://products/123")
    if st.button(t("deeplink_generate_button"), width='stretch'):
        if deeplink_uri:
            qr_img = qrcode.make(deeplink_uri)
            st.image(qr_img.get_image(), width=300)

def render_color_contrast_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("contrast_guide"))

    col1, col2 = st.columns(2)
    with col1:
        fg_color = st.color_picker(t("contrast_fg_label"), "#FFFFFF")
    with col2:
        bg_color = st.color_picker(t("contrast_bg_label"), "#333333")

    ratio = get_contrast_ratio(fg_color, bg_color)

    st.metric(t("contrast_ratio_label"), f"{ratio:.2f}:1")

    st.markdown(f"""
        <div style="background-color:{bg_color}; color:{fg_color}; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #888;">
            <h3 style='color:{fg_color};'>{t('contrast_demo_text')} (24px)</h3>
            <p style='color:{fg_color};'>{t('contrast_demo_text')} (16px)</p>
        </div>
    """, unsafe_allow_html=True)

    if ratio >= 7:
        st.success(t("contrast_result_aaa"))
    elif ratio >= 4.5:
        st.success(t("contrast_result_aa"))
    else:
        st.error(t("contrast_result_fail"))

def render_mobile_lab():
    t = get_text
    st.header(t("mobile_lab_header"))
    
    tabs = st.tabs([
        f"🖼️ {t('mobile_lab_tab_qr')}",
        f"📋 {t('mobile_lab_tab_clipboard')}",
        f"🧪 {t('mobile_lab_tab_test_data_qr')}",
        f"🌍 {t('mobile_lab_tab_l10n')}",
        f"🔗 {t('mobile_lab_tab_deeplink')}",
        f"🎨 {t('mobile_lab_tab_contrast')}",
        f"🛡️ {t('mobile_lab_tab_permissions')}"
    ])

    with tabs[0]:
        render_qr_hub_tab()

    with tabs[1]:
        render_clipboard_tab()

    with tabs[2]:
        render_test_data_qr_tab()

    with tabs[3]:
        render_l10n_tab()

    with tabs[4]:
        render_deeplink_tab()

    with tabs[5]:
        render_color_contrast_tab()

    with tabs[6]:
        render_permissions_guide_tab()
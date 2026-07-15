import streamlit as st
from PIL import Image, ImageChops, ImageOps
import numpy as np
from modules.i18n import get_text

def render_visual_diff_lab():
    t = get_text
    logger = st.session_state.get("logger")
    st.subheader(t("visual_diff_header"))
    
    st.info(t("visual_diff_info"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        file_1 = st.file_uploader(t("visual_diff_expected_label"), type=['png', 'jpg', 'jpeg'], key="img1")
    with col2:
        file_2 = st.file_uploader(t("visual_diff_actual_label"), type=['png', 'jpg', 'jpeg'], key="img2")
        
    if file_1 and file_2:
        if st.button(t("visual_diff_button_compare"), width='stretch'):
            try:
                img_expected = Image.open(file_1).convert('RGB')
                img_actual = Image.open(file_2).convert('RGB')
                
                if logger:
                    logger(f"Visual Diff: Comparing {file_1.name} vs {file_2.name}")
                
                # --- Улучшенное отображение ---
                st.divider()
                c1, c2 = st.columns(2)
                c1.image(img_expected, caption=t("visual_diff_expected_label"))
                c2.image(img_actual, caption=t("visual_diff_actual_label"))
                st.divider()

                if img_expected.size != img_actual.size:
                    st.warning(t("visual_diff_warning_size").format(size1=img_expected.size, size2=img_actual.size))
                
                # Создаем разницу
                diff = ImageChops.difference(img_expected, img_actual)
                
                # Расчет процента схожести
                diff_data = np.array(diff)
                non_zero_pixels = np.count_nonzero(diff_data)
                total_pixels = diff_data.size
                similarity = 100 - (non_zero_pixels / total_pixels * 100)

                st.metric(t("visual_diff_result_similarity"), f"{similarity:.2f}%")

                if similarity == 100:
                    st.success(t("visual_diff_result_identical"))
                    if logger: logger("Visual Diff: No differences found")
                else:
                    # Создаем более наглядную карту различий
                    diff_mask = np.where(diff_data > 10, 255, 0).astype(np.uint8)
                    heatmap = ImageOps.colorize(Image.fromarray(diff_mask).convert('L'), black="black", white="red")
                    # Отображаем результат в центральной колонке, чтобы он был меньше
                    st.image(heatmap, caption=t("visual_diff_result_caption"))
                    if logger: logger(f"Visual Diff: Comparison completed. Similarity {similarity:.2f}%")
                
            except Exception as e:
                st.error(t("visual_diff_error_process").format(e=e))
                if logger: logger(f"Visual Diff ERROR: {str(e)}")
    else:
        st.warning(t("visual_diff_warn_upload"))
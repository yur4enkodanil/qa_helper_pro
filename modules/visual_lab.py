import streamlit as st
import os
import numpy as np
import time
import re
from PIL import Image, ImageChops, ImageOps
from modules.i18n import get_text

# --- CONFIG ---
REF_STORAGE = os.path.join(os.getcwd(), "reference_storage")
os.makedirs(REF_STORAGE, exist_ok=True)

# --- HELPERS ---
def sanitize_filename(name):
    """Removes illegal characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_image_properties(image_path):
    """Gets image dimensions and file size."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
        file_size = os.path.getsize(image_path) / 1024 # in KB
        return width, height, file_size
    except Exception:
        return None, None, None

def compare_images(img1, img2):
    """Compares two images and creates a diff map. Assumes images are the same size."""
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    
    diff = ImageChops.difference(img1, img2)
    diff_data = np.array(diff)
    
    # Use a threshold to ignore minor anti-aliasing differences
    threshold = 15 
    diff_mask = np.where(diff_data > threshold, 255, 0).astype(np.uint8)
    
    # Calculate similarity based on significant differences
    non_zero_pixels = np.count_nonzero(diff_mask)
    total_pixels = diff_data.size
    similarity = 100 - (non_zero_pixels / total_pixels * 100)

    # Create a visible heatmap of differences
    heatmap = ImageOps.colorize(Image.fromarray(diff_mask).convert('L'), black="black", white="red")
    
    return heatmap, round(similarity, 2)

# --- MAIN RENDER FUNCTION ---
def render_visual_lab():
    t = get_text
    logger = st.session_state.get('logger')
    st.subheader(t("visual_header"))

    # --- INITIALIZE SESSION STATE ---
    if 'v_ref_img' not in st.session_state: st.session_state.v_ref_img = None
    if 'v_actual_img' not in st.session_state: st.session_state.v_actual_img = None
    if 'v_ref_props' not in st.session_state: st.session_state.v_ref_props = None
    if 'v_actual_props' not in st.session_state: st.session_state.v_actual_props = None
    if 'v_ref_img_id' not in st.session_state: st.session_state.v_ref_img_id = None
    if 'v_actual_img_id' not in st.session_state: st.session_state.v_actual_img_id = None

    # --- UI LAYOUT ---
    col_left, col_right = st.columns([1, 1])

    # --- LEFT COLUMN: REFERENCE MANAGEMENT ---
    with col_left:
        st.markdown(f"### {t('visual_ref_header')}")
        
        source_mode = st.radio(
            t("visual_ref_source_label"), 
            [t("visual_ref_source_upload"), t("visual_ref_source_db")], 
            horizontal=True, key="v_source_mode"
        )

        if source_mode == t("visual_ref_source_upload"):
            uploaded_ref = st.file_uploader(t("visual_ref_upload_label"), type=['png', 'jpg', 'jpeg'], key="v_uploader_ref")
            # Process only if a new file is uploaded to prevent infinite loop
            if uploaded_ref and uploaded_ref.file_id != st.session_state.get('v_ref_img_id'):
                st.session_state.v_ref_img_id = uploaded_ref.file_id
                img = Image.open(uploaded_ref)
                st.session_state.v_ref_img = img
                st.session_state.v_ref_props = {"w": img.width, "h": img.height, "name": uploaded_ref.name}
                st.rerun() # Rerun to update display
        
        else: # Select from DB
            st.markdown(f"#### {t('visual_ref_gallery_header')}")
            # Sort the list for deterministic order
            refs = sorted([f for f in os.listdir(REF_STORAGE) if f.endswith(('.png', '.jpg', '.jpeg'))])
            
            if not refs:
                st.info(t("visual_ref_db_empty"))
            else:
                # Gallery view
                for i in range(0, len(refs), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(refs):
                            with cols[j]:
                                ref_name = refs[i+j]
                                ref_path = os.path.join(REF_STORAGE, ref_name)
                                w, h, size_kb = get_image_properties(ref_path)
                                
                                with st.container(border=True):
                                    st.image(ref_path)
                                    st.caption(f"`{w}x{h}` | `{size_kb:.1f} KB`")
                                    
                                    c1, c2 = st.columns(2)
                                    if c1.button(t("visual_ref_load_button"), key=f"load_{ref_name}", width='stretch'):
                                        img = Image.open(ref_path)
                                        st.session_state.v_ref_img = img
                                        # Use file path as a unique ID for DB images to prevent re-processing
                                        st.session_state.v_ref_img_id = ref_path
                                        st.session_state.v_ref_props = {"w": img.width, "h": img.height, "name": ref_name}
                                        st.rerun()
                                    
                                    if c2.button(t("visual_ref_delete_button"), key=f"del_{ref_name}", width='stretch', type="secondary"):
                                        try:
                                            os.remove(ref_path)
                                            st.toast(t("visual_ref_delete_success").format(filename=ref_name), icon="🗑️")
                                            if logger: logger(f"Visual Check: Deleted baseline '{ref_name}'")
                                            time.sleep(0.5) # Give toast time to show
                                            st.rerun()
                                        except Exception as e:
                                            st.error(t("visual_ref_delete_error").format(e=e))

    # --- RIGHT COLUMN: ACTUAL IMAGE & COMPARISON ---
    with col_right:
        st.markdown(f"### {t('visual_actual_header')}")
        uploaded_actual = st.file_uploader(t("visual_actual_upload_label"), type=['png', 'jpg', 'jpeg'], key="v_uploader_actual")
        # Process only if a new file is uploaded
        if uploaded_actual and uploaded_actual.file_id != st.session_state.get('v_actual_img_id'):
            st.session_state.v_actual_img_id = uploaded_actual.file_id
            img = Image.open(uploaded_actual)
            st.session_state.v_actual_img = img
            st.session_state.v_actual_props = {"w": img.width, "h": img.height, "name": uploaded_actual.name}
            st.rerun()

    st.divider()

    # --- DISPLAY & COMPARE ---
    img_ref = st.session_state.v_ref_img
    img_actual = st.session_state.v_actual_img
    props_ref = st.session_state.v_ref_props
    props_actual = st.session_state.v_actual_props

    if not img_ref or not img_actual:
        st.info(t("visual_info_no_images"))
    else:
        # Display images
        disp_c1, disp_c2 = st.columns(2)
        with disp_c1:
            st.image(img_ref, caption=f"{t('visual_caption_ref')}: {props_ref['name']}")
            st.caption(f"`{props_ref['w']}x{props_ref['h']}`")
            
            # Save to DB expander
            with st.expander(t("visual_save_expander")):
                default_name = os.path.splitext(props_ref['name'])[0]
                save_name = st.text_input(t("visual_save_filename_label"), value=default_name, key="v_save_name")
                if st.button(t("visual_save_button"), width='stretch'):
                    if not save_name:
                        st.warning(t("visual_save_warn_name"))
                    else:
                        clean_name = sanitize_filename(save_name)
                        save_path = os.path.join(REF_STORAGE, f"{clean_name}.png")
                        try:
                            with st.spinner(t("visual_save_spinner")):
                                img_ref.convert("RGB").save(save_path, "PNG")
                            st.toast(t("visual_save_success").format(filename=f"{clean_name}.png"), icon="✅")
                            if logger: logger(f"Visual Check: Saved baseline '{clean_name}.png'")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(t("visual_save_error").format(e=e))

        with disp_c2:
            st.image(img_actual, caption=f"{t('visual_caption_actual')}: {props_actual['name']}")
            st.caption(f"`{props_actual['w']}x{props_actual['h']}`")

        st.divider()

        # Comparison logic
        sizes_match = (props_ref['w'] == props_actual['w']) and (props_ref['h'] == props_actual['h'])
        if not sizes_match:
            st.error(t("visual_compare_error_size"), icon="📐")
            st.info(t("visual_compare_info_size").format(w1=props_ref['w'], h1=props_ref['h'], w2=props_actual['w'], h2=props_actual['h']))
        
        if st.button(t("visual_compare_button"), width='stretch', disabled=not sizes_match):
            with st.spinner("Comparing..."):
                heatmap, sim = compare_images(img_ref, img_actual)
            
            st.metric(t("visual_compare_similarity"), f"{sim:.2f}%")
            
            if sim >= 99.99:
                st.success(t("visual_compare_identical"))
                if logger: logger("Visual Check: No significant differences found.")
            else:
                _, center_col, _ = st.columns([1,2,1])
                with center_col:
                    st.image(heatmap, caption=t("visual_compare_diffmap_caption"))
                if logger: logger(f"Visual Check: Comparison complete. Similarity {sim:.2f}%")
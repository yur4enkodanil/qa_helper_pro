import streamlit as st
from modules.i18n import get_text
from PIL import Image, ImageDraw, ImageOps
import easyocr
import cv2
import math
import numpy as np
import base64
from io import BytesIO
# Re-adding canvas for new tools
from streamlit_drawable_canvas import st_canvas

# --- HACK by user: Monkey-patch for streamlit-drawable-canvas on new Streamlit versions ---
from streamlit.elements import image as st_image

if not hasattr(st_image, 'image_to_url'):
    def image_to_url_monkey_patch(pil_image, width=-1, clamp=False, channels="RGB", output_format="auto", image_id=""):
        # Use Streamlit's internal media file manager to generate a proper URL
        from streamlit.runtime.media_file_storage import MediaFileStorageError
        try:
            from streamlit import runtime
            ctx = runtime.get_instance()._media_file_mgr
            
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            url = ctx.add(img_bytes, "image/png", image_id)
            return url
        except Exception as e:
            # Fallback for API changes
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/png;base64,{img_str}"

    st_image.image_to_url = image_to_url_monkey_patch
# --- END HACK ---


def get_scaled_dimensions(image_size, max_width=800):
    """Calculates scaled dimensions for an image to fit within a max width."""
    img_width, img_height = image_size
    if img_width == 0: return 0, 0, 1.0
    aspect_ratio = img_height / img_width
    canvas_width = min(img_width, max_width)
    canvas_height = canvas_width * aspect_ratio
    scale_factor = img_width / canvas_width
    return int(canvas_width), int(canvas_height), scale_factor


@st.cache_resource
def get_ocr_reader():
    """Initializes the OCR reader, cached for performance."""
    return easyocr.Reader(['ru', 'en'])


def create_notch_overlay(size, notch_type):
    """Creates a transparent overlay with a specified notch."""
    t = get_text
    width, height = size
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if notch_type == t("ui_inspector_notch_classic"):
        notch_w, notch_h = 210, 35
        x0, y0 = (width - notch_w) // 2, 0
        draw.rounded_rectangle((x0, y0, x0 + notch_w, y0 + notch_h), fill=(0, 0, 0, 255), radius=15)
    elif notch_type == t("ui_inspector_notch_dynamic_island"):
        notch_w, notch_h = 125, 35
        x0, y0 = (width - notch_w) // 2, 20
        draw.rounded_rectangle((x0, y0, x0 + notch_w, y0 + notch_h), fill=(0, 0, 0, 255), radius=20)
    elif notch_type == t("ui_inspector_notch_teardrop"):
        notch_w, notch_h = 80, 30
        x0, y0 = (width - notch_w) // 2, 0
        draw.ellipse((x0, y0, x0 + notch_w, y0 + notch_h * 2), fill=(0, 0, 0, 255))
    elif notch_type == t("ui_inspector_notch_center_hole"):
        radius = 18
        x0, y0 = (width // 2) - radius, 30
        draw.ellipse((x0, y0, x0 + 2 * radius, y0 + 2 * radius), fill=(0, 0, 0, 255))
    elif notch_type == t("ui_inspector_notch_corner_hole"):
        radius = 18
        x0, y0 = 30, 30
        draw.ellipse((x0, y0, x0 + 2 * radius, y0 + 2 * radius), fill=(0, 0, 0, 255))

    return overlay


def render_ocr_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("ui_inspector_ocr_guide"))

    uploaded_file = st.file_uploader(t("ui_inspector_ocr_upload"), type=['png', 'jpg', 'jpeg'], key="ocr_uploader")
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGBA")
        st.image(image, use_column_width="auto")
        if st.button(t("ui_inspector_ocr_button_run"), width='stretch', type="primary"):
            with st.spinner(t("ui_inspector_ocr_processing")):
                reader = get_ocr_reader()
                image_bytes = uploaded_file.getvalue()
                result = reader.readtext(image_bytes, detail=0, paragraph=True)

                st.markdown(f"#### {t('ui_inspector_ocr_result')}")
                st.text_area(t('ui_inspector_ocr_result'), "\n".join(result), height=300, label_visibility="collapsed")


def render_font_inspector_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("ui_inspector_font_guide"))

    uploaded_file = st.file_uploader(t("ui_inspector_font_upload"), type=['png', 'jpg', 'jpeg'], key="font_uploader")
    if uploaded_file:
        st.session_state.font_image_bytes = uploaded_file.getvalue()
        st.session_state.font_image_filename = uploaded_file.name # Store filename for key

    if 'font_image_bytes' in st.session_state:
        image = Image.open(BytesIO(st.session_state.font_image_bytes))
        st.info(t("ui_inspector_font_tip"))
        canvas_width, canvas_height, scale_factor = get_scaled_dimensions(image.size)

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)", stroke_width=2, stroke_color="#FFA500",
            background_image=image, update_streamlit=True,
            height=canvas_height, width=canvas_width, drawing_mode="rect",
            key=f"font_canvas_{st.session_state.get('font_image_filename', '')}",
        )

        if canvas_result.json_data and canvas_result.json_data["objects"]:
            rect = canvas_result.json_data["objects"][-1]
            height = rect["height"] * rect["scaleY"] * scale_factor
            st.metric(t("ui_inspector_font_result"), f"{height:.0f} px")


def render_gif_inspector_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("ui_inspector_gif_guide"))

    uploaded_file = st.file_uploader(t("ui_inspector_gif_upload"), type=['gif'])

    if uploaded_file:
        gif = Image.open(uploaded_file)
        
        st.markdown(f"#### {t('ui_inspector_gif_info_header')}")
        c1, c2 = st.columns(2)
        c1.metric(t('ui_inspector_gif_frames'), gif.n_frames)
        c2.metric(t('ui_inspector_gif_duration'), gif.info.get('duration', 'N/A'))

        st.divider()

        if gif.n_frames > 1:
            if 'gif_frame' not in st.session_state:
                st.session_state.gif_frame = 0

            col_prev, col_slider, col_next, col_download = st.columns([1, 6, 1, 2])
            if col_prev.button("◀️", width='stretch', type="primary"): # Changed to primary
                st.session_state.gif_frame = max(0, st.session_state.gif_frame - 1)
            if col_next.button("▶️", width='stretch', type="primary"): # Changed to primary
                st.session_state.gif_frame = min(gif.n_frames - 1, st.session_state.gif_frame + 1)
            
            selected_frame = col_slider.slider(
                t('ui_inspector_gif_select_frame'), 
                0, gif.n_frames - 1, st.session_state.gif_frame, label_visibility="collapsed"
            )
            st.session_state.gif_frame = selected_frame
            gif.seek(selected_frame)

            # Download button for current frame
            buf = BytesIO()
            gif.copy().save(buf, format="PNG")
            byte_im = buf.getvalue()
            col_download.download_button(
                label=t("ui_inspector_gif_download_frame"),
                data=byte_im,
                file_name=f"frame_{selected_frame}.png",
                mime="image/png",
                width='stretch',
                type="secondary"
            )
        
        st.image(gif.copy(), use_column_width="auto")


def render_ruler_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("ui_inspector_ruler_guide"))

    uploaded_file = st.file_uploader(t("ui_inspector_ruler_upload"), type=['png', 'jpg', 'jpeg'], key="ruler_uploader")
    if uploaded_file:
        st.session_state.ruler_image_bytes = uploaded_file.getvalue()
        st.session_state.ruler_image_filename = uploaded_file.name # Store filename for key
        st.session_state.ruler_lines = [] # Reset lines for new image

    if 'ruler_image_bytes' in st.session_state:
        image_bytes = st.session_state.ruler_image_bytes
        
        col_grid, col_clear = st.columns([3,1])
        show_grid = col_grid.checkbox(t("ui_inspector_ruler_grid"))
        if col_clear.button("🗑️ " + t("ui_inspector_ruler_clear_button"), width='stretch', type="primary"): # Changed to primary
            st.session_state.ruler_lines = []
            st.rerun()

        bg_image = Image.open(BytesIO(image_bytes)).convert("RGBA")
        
        if show_grid:
            draw = ImageDraw.Draw(bg_image)
            w, h = bg_image.size
            for i in range(0, w, 8): draw.line([(i, 0), (i, h)], fill=(128, 128, 128, 100), width=1)
            for i in range(0, h, 8): draw.line([(0, i), (w, i)], fill=(128, 128, 128, 100), width=1)

        canvas_width, canvas_height, scale_factor = get_scaled_dimensions(bg_image.size)

        canvas_key = f"ruler_canvas_{st.session_state.get('ruler_image_filename', '')}_{show_grid}_{len(st.session_state.ruler_lines)}"
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)", stroke_width=2, stroke_color="#FFA500",
            background_image=bg_image, update_streamlit=True,
            height=canvas_height, width=canvas_width, drawing_mode="line",
            initial_drawing={"objects": st.session_state.ruler_lines},
            key=canvas_key,
        )

        if canvas_result.json_data and len(canvas_result.json_data["objects"]) > len(st.session_state.ruler_lines):
            new_line = canvas_result.json_data["objects"][-1]
            st.session_state.ruler_lines.append(new_line)
            st.rerun()

        if st.session_state.get('ruler_lines'):
            last_obj = st.session_state.ruler_lines[-1]
            if last_obj['type'] == 'line':
                x1, y1, x2, y2 = last_obj['x1'], last_obj['y1'], last_obj['x2'], last_obj['y2']
                dist = math.sqrt(((x2 - x1) * scale_factor) ** 2 + ((y2 - y1) * scale_factor) ** 2)
                st.info(f"**{t('ui_inspector_ruler_distance')}** {dist:.2f} px")


def render_notch_tab():
    t = get_text
    with st.expander(t("mobile_lab_guide_header")):
        st.markdown(t("ui_inspector_notch_guide"))

    uploaded_file = st.file_uploader(t("ui_inspector_notch_upload"), type=['png', 'jpg', 'jpeg'], key="notch_uploader")
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGBA")
        notch_type = st.selectbox(
            t("ui_inspector_notch_select"),
            [
                t("ui_inspector_notch_classic"), t("ui_inspector_notch_dynamic_island"),
                t("ui_inspector_notch_teardrop"), t("ui_inspector_notch_center_hole"),
                t("ui_inspector_notch_corner_hole"),
            ]
        )
        bg = Image.new('RGBA', image.size, (0, 0, 0, 255))
        bg.paste(image, (0, 0), image)
        overlay = create_notch_overlay(image.size, notch_type)
        final_image = Image.alpha_composite(bg, overlay)
        _, c, _ = st.columns([1, 2, 1])
        with c:
            st.image(final_image, use_column_width='auto')


def render_ui_inspector_lab():
    """Main function to render the UI Inspector lab with its tabs."""
    t = get_text
    st.header(t("ui_inspector_header"))

    tabs = st.tabs([
        f"🔤 {t('ui_inspector_tab_ocr')}",
        f"📱 {t('ui_inspector_tab_notch')}",
        f"🔠 {t('ui_inspector_tab_font_inspector')}",
        f"📏 {t('ui_inspector_tab_ruler')}",
        f"🎞️ {t('ui_inspector_tab_gif_inspector')}",
    ])

    with tabs[0]: render_ocr_tab()
    with tabs[1]: render_notch_tab()
    with tabs[2]: render_font_inspector_tab()
    with tabs[3]: render_ruler_tab()
    with tabs[4]: render_gif_inspector_tab()
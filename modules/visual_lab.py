import streamlit as st
import os
import numpy as np
import time
from PIL import Image, ImageChops, ImageOps
from datetime import datetime

# Путь к хранилищу эталонов
REF_STORAGE = os.path.join(os.getcwd(), "reference_storage")
os.makedirs(REF_STORAGE, exist_ok=True)

def compare_images(img1, img2):
    """Сравнение двух изображений и создание тепловой карты различий."""
    img2 = img2.resize(img1.size).convert('RGB')
    img1 = img1.convert('RGB')
    diff = ImageChops.difference(img1, img2)
    diff_data = np.array(diff)
    diff_mask = np.where(diff_data > 10, 255, 0).astype(np.uint8)
    heatmap = ImageOps.colorize(Image.fromarray(diff_mask).convert('L'), black="black", white="red")
    sim = 100 - (np.count_nonzero(diff_data) / diff_data.size * 100)
    return heatmap, round(sim, 2)

def render_visual_lab():
    logger = st.session_state.get('logger')
    st.subheader("👁️ Визуальный регресс")

    # Сетка для загрузки файлов
    col_setup_l, col_setup_r = st.columns(2)

    # --- ЛЕВАЯ КОЛОНКА: ЭТАЛОН ---
    with col_setup_l:
        st.markdown("### 1. Эталон (Reference)")
        mode_r = st.radio("Источник эталона:", ["Загрузить файл", "Выбрать из базы"], horizontal=True, key="v_mode_selector")
        
        if mode_r == "Загрузить файл":
            up_r = st.file_uploader("Загрузить эталон", type=['png', 'jpg', 'jpeg'], key="v_uploader_ref")
            if up_r:
                st.session_state['v_ref'] = Image.open(up_r)
        else:
            refs = [f for f in os.listdir(REF_STORAGE) if f.endswith('.png')]
            if refs:
                sel_r = st.selectbox("Доступные эталоны:", refs, key="v_db_select")
                
                # Кнопки управления базой
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("📥 Загрузить", use_container_width=True, key="v_btn_load_db"):
                        st.session_state['v_ref'] = Image.open(os.path.join(REF_STORAGE, sel_r))
                        st.rerun()
                
                with btn_col2:
                    # Кнопка удаления файла
                    if st.button("🗑️ Удалить", use_container_width=True, key="v_btn_del_db"):
                        try:
                            file_to_del = os.path.join(REF_STORAGE, sel_r)
                            os.remove(file_to_del)
                            st.toast(f"Файл {sel_r} удален", icon="🗑️")
                            if logger: logger(f"Визуал: Удален эталон '{sel_r}'")
                            time.sleep(0.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ошибка при удалении: {e}")
            else:
                st.warning("База эталонов пуста.")

    # --- ПРАВАЯ КОЛОНКА: ТЕКУЩИЙ ---
    with col_setup_r:
        st.markdown("### 2. Текущий результат")
        up_c = st.file_uploader("Загрузить скриншот для теста", type=['png', 'jpg', 'jpeg'], key="v_uploader_cur")
        if up_c:
            st.session_state['v_cur'] = Image.open(up_c)

    st.divider()

    # --- ОТОБРАЖЕНИЕ И СОХРАНЕНИЕ ---
    img_r = st.session_state.get('v_ref')
    img_c = st.session_state.get('v_cur')

    if img_r or img_c:
        res_l, res_r = st.columns(2)
        
        if img_r:
            with res_l:
                st.image(img_r, caption="Выбранный Эталон", use_container_width=True)
                
                with st.expander("💾 Сохранить этот эталон в базу", expanded=False):
                    s_name = st.text_input("Имя файла (без .png):", key="v_save_name_input")
                    if st.button("Подтвердить сохранение", use_container_width=True, key="v_btn_save_exec"):
                        if s_name:
                            try:
                                with st.spinner('Выполняется сохранение...'):
                                    save_path = os.path.join(REF_STORAGE, f"{s_name}.png")
                                    img_r.save(save_path)
                                    time.sleep(0.6)
                                
                                st.toast(f'Эталон {s_name}.png сохранен!', icon='✅')
                                if logger: logger(f"Визуал: Эталон '{s_name}' сохранен")
                                time.sleep(0.5)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Ошибка сохранения: {e}")
                        else:
                            st.warning("⚠️ Введите имя файла!")

        if img_c:
            with res_r:
                st.image(img_c, caption="Текущий результат", use_container_width=True)

        if img_r and img_c:
            st.write("")
            if st.button("🚀 НАЧАТЬ СРАВНЕНИЕ ПИКСЕЛЕЙ", use_container_width=True, key="v_btn_compare"):
                heatmap, sim = compare_images(img_r, img_c)
                st.divider()
                st.markdown(f"### Сходство изображений: `{sim}%`")
                if sim < 100:
                    st.image(heatmap, caption="Карта различий (Красный цвет указывает на расхождения)", use_container_width=True)
                    if logger: logger(f"Визуал: Сравнение завершено. Сходство {sim}%")
                else:
                    st.success("Изображения полностью идентичны!")
                    if logger: logger("Визуал: Различий не обнаружено")
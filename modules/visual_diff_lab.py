import streamlit as st
from PIL import Image, ImageChops
from datetime import datetime

def write_log(message):
    """Прямая запись в историю логов в session_state"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    if 'log_history' not in st.session_state:
        st.session_state.log_history = []
    st.session_state.log_history.append(f"{timestamp} - {message}")

def render_visual_diff_lab(): # Убрали обязательный аргумент log_func
    st.subheader("📸 Сравнение скриншотов (Pixel Perfect)")
    
    st.info("Загрузите два изображения одинакового размера для поиска различий.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        file_1 = st.file_uploader("Ожидаемый результат (Expected)", type=['png', 'jpg', 'jpeg'], key="img1")
    with col2:
        file_2 = st.file_uploader("Фактический результат (Actual)", type=['png', 'jpg', 'jpeg'], key="img2")
        
    if file_1 and file_2:
        # Настройки сравнения
        show_diff = st.checkbox("Показать математическую разницу (Difference)", value=True)
        
        if st.button("🚀 Запустить сравнение", use_container_width=True):
            try:
                img_expected = Image.open(file_1).convert('RGB')
                img_actual = Image.open(file_2).convert('RGB')
                
                # Логируем действие
                write_log(f"Visual Diff: Comparing {file_1.name} vs {file_2.name}")
                
                if img_expected.size != img_actual.size:
                    st.warning(f"Внимание: Размеры изображений не совпадают! ({img_expected.size} vs {img_actual.size}). Результат может быть некорректным.")
                
                # Создаем разницу
                diff = ImageChops.difference(img_expected, img_actual)
                
                # Если разницы нет, diff будет черным. Можно подсветить.
                if show_diff:
                    st.image(diff, caption="Различия подсвечены яркими цветами", use_container_width=True)
                    
                # Выводим оригиналы для визуального контроля
                c1, c2 = st.columns(2)
                c1.image(img_expected, caption="Expected", use_container_width=True)
                c2.image(img_actual, caption="Actual", use_container_width=True)
                
                write_log("Visual Diff: Comparison completed")
                
            except Exception as e:
                st.error(f"Ошибка при обработке изображений: {e}")
                write_log(f"Visual Diff ERROR: {str(e)}")
    else:
        st.warning("Для начала работы необходимо загрузить оба файла.")
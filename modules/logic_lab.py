import streamlit as st

def calculate_bva(min_val, max_val):
    points = {min_val - 1, min_val, min_val + 1, 
              max_val - 1, max_val, max_val + 1, 
              (min_val + max_val) // 2}
    return sorted(list(points))

def render_logic_lab():
    st.subheader("🧠 Граничные значения (BVA)")
    st.info("Введите границы поля, чтобы получить критические точки для тестов.")
    
    with st.container(border=True):
        col_l, col_r = st.columns(2)
        min_v = col_l.number_input("Минимум (Min):", value=0)
        max_v = col_r.number_input("Максимум (Max):", value=100)
    
    if st.button("📊 Рассчитать точки", use_container_width=True):
        pts = calculate_bva(min_v, max_v)
        
        st.write("### Результат:")
        cols = st.columns(len(pts))
        for i, v in enumerate(pts):
            is_in = min_v <= v <= max_v
            cols[i].metric(
                "In" if is_in else "Out", 
                v, 
                delta="Valid" if is_in else "Error", 
                delta_color="normal" if is_in else "inverse"
            )
        
        md = "| Проверка | Значение | Ожидаемый результат |\n| :--- | :--- | :--- |\n"
        for v in pts:
            res = "OK (Positive)" if min_v <= v <= max_v else "Fail (Negative)"
            md += f"| Граница | `{v}` | {res} |\n"
        st.code(md, language="markdown")
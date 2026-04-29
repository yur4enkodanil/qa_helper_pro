import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs

def render_link_lab():
    lang = st.session_state.get('lang', 'RU')
    st.subheader("🔗 Анализатор ссылок и редиректов" if lang == "RU" else "🔗 Link & Redirect Tracker")
    
    url_input = st.text_input(
        ("Введите URL для анализа:" if lang == "RU" else "Enter URL to analyze:"), 
        placeholder="https://example.com/promo?utm_source=tg&utm_medium=post"
    )

    if url_input:
        # Простейшая валидация протокола
        if not url_input.startswith(("http://", "https://")):
            st.error("⚠️ Ссылка должна начинаться с http:// или https://" if lang == "RU" else "⚠️ URL must start with http:// or https://")
            return

        t1, t2 = st.tabs([
            "🛰️ " + ("Цепочка редиректов" if lang == "RU" else "Redirect Chain"),
            "📊 " + ("Разбор параметров" if lang == "RU" else "URL Parameters")
        ])

        # --- ТАБ 1: РЕДИРЕКТЫ ---
        with t1:
            if st.button("🚀 " + ("Проверить путь" if lang == "RU" else "Trace Path")):
                try:
                    with st.spinner("Анализирую переходы..." if lang == "RU" else "Tracing..."):
                        # Делаем запрос. allow_redirects=True позволяет requests пройти весь путь
                        response = requests.get(url_input, allow_redirects=True, timeout=10)
                        
                        chain = []
                        # Проходим по истории редиректов
                        for resp in response.history:
                            chain.append({
                                "Статус": resp.status_code,
                                "URL": resp.url,
                                "Тип": "Редирект" if lang == "RU" else "Redirect"
                            })
                        
                        # Добавляем финальную точку назначения
                        chain.append({
                            "Статус": response.status_code,
                            "URL": response.url,
                            "Тип": "Конечный URL" if lang == "RU" else "Final Destination"
                        })
                        
                        df = pd.DataFrame(chain)
                        st.table(df)
                        
                        if len(response.history) == 0:
                            st.success("Редиректов не обнаружено (Прямая ссылка)" if lang == "RU" else "No redirects found")
                except Exception as e:
                    st.error(f"Ошибка запроса: {e}" if lang == "RU" else f"Request error: {e}")

        # --- ТАБ 2: ПАРАМЕТРЫ URL ---
        with t2:
            parsed_url = urlparse(url_input)
            params = parse_qs(parsed_url.query)
            
            st.markdown(f"**Base URL:** `{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}`")
            
            if params:
                # Преобразуем словарь параметров в красивую таблицу
                param_data = [{"Параметр": k, "Значение": v[0]} for k, v in params.items()]
                st.dataframe(pd.DataFrame(param_data), use_container_width=True)
                
                # Быстрая проверка на наличие UTM-меток
                has_utm = any(p.startswith("utm_") for p in params.keys())
                if has_utm:
                    st.info("ℹ️ В ссылке присутствуют UTM-метки для аналитики" if lang == "RU" else "ℹ️ UTM tags detected")
            else:
                st.write("Параметры (query strings) не найдены." if lang == "RU" else "No parameters found.")

    st.divider()
    # Инструкция для тестера
    with st.expander("💡 " + ("Как использовать этот инструмент?" if lang == "RU" else "How to use?")):
        st.write("""
        1. **Проверка сокращателей:** Вставьте ссылку из `bit.ly` или `vk.cc`, чтобы увидеть реальный адрес назначения.
        2. **Проверка меток:** Убедитесь, что при редиректе с лендинга на основной сайт не «отвалились» `utm_source` или `client_id`.
        3. **Статус-коды:** Следите, чтобы редиректы были `301` (постоянные) или `302` (временные), а не падали в `404`.
        """ if lang == "RU" else "Check for redirect loops, status codes, and query parameter persistence.")
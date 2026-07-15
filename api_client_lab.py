import streamlit as st
import requests
import json

def render_api_client_lab():
    lang = st.session_state.get("lang", "RU")

    # --- Тексты для i18n ---
    texts = {
        "RU": {
            "header": "📡 API Клиент",
            "info": "Отправляйте HTTP-запросы (GET, POST, PUT и др.) и анализируйте ответы.",
            "url_label": "URL эндпоинта",
            "method_label": "Метод",
            "headers_label": "Заголовки (JSON)",
            "body_label": "Тело запроса (JSON/Text)",
            "send_button": "🚀 Отправить запрос",
            "response_header": "Ответ сервера",
            "status_code": "Статус",
            "response_headers": "Заголовки ответа",
            "response_body": "Тело ответа",
            "error_json_headers": "Ошибка в формате JSON для заголовков!",
            "guide_header": "💡 Как использовать API Клиент?",
            "guide_content": """
            1.  **Быстрая проверка:** Используйте для отправки простых GET-запросов, чтобы проверить доступность эндпоинта и посмотреть ответ.
            2.  **Тестирование POST:** Введите данные в поле "Тело запроса" в формате JSON, выберите метод POST и отправьте запрос на создание сущности.
            3.  **Отладка заголовков:** Добавьте `Authorization` или другие кастомные заголовки в формате JSON, чтобы протестировать защищенные эндпоинты.
            4.  **Анализ ответа:** Ответ сервера будет разбит на статус, заголовки и тело. Если тело является валидным JSON, оно будет отформатировано для удобства чтения.
            """
        },
        "EN": {
            "header": "📡 API Client",
            "info": "Send HTTP requests (GET, POST, PUT, etc.) and analyze the responses.",
            "url_label": "Endpoint URL",
            "method_label": "Method",
            "headers_label": "Headers (JSON)",
            "body_label": "Request Body (JSON/Text)",
            "send_button": "🚀 Send Request",
            "response_header": "Server Response",
            "status_code": "Status",
            "response_headers": "Response Headers",
            "response_body": "Response Body",
            "error_json_headers": "Invalid JSON format for headers!",
            "guide_header": "💡 How to use the API Client?",
            "guide_content": """
            1.  **Quick Check:** Use it for simple GET requests to check endpoint availability and view the response.
            2.  **POST Testing:** Enter data in the "Request Body" field in JSON format, select the POST method, and send a request to create an entity.
            3.  **Header Debugging:** Add `Authorization` or other custom headers in JSON format to test protected endpoints.
            4.  **Response Analysis:** The server response will be broken down into status, headers, and body. If the body is valid JSON, it will be formatted for easy reading.
            """
        }
    }
    t = texts[lang]

    st.subheader(t["header"])
    st.info(t["info"])

    with st.container(border=True):
        url = st.text_input(t["url_label"], "https://api.restful-api.dev/objects")
        method = st.selectbox(t["method_label"], ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        
        c1, c2 = st.columns(2)
        headers_str = c1.text_area(t["headers_label"], '{"Content-Type": "application/json"}', height=200)
        body_str = c2.text_area(t["body_label"], '{\n  "name": "Apple MacBook Pro 16",\n  "data": {\n    "year": 2019,\n    "price": 1849.99,\n    "CPU model": "Intel Core i9",\n    "Hard disk size": "1 TB"\n  }\n}', height=200)

    if st.button(t["send_button"], width='stretch'):
        try:
            headers = json.loads(headers_str) if headers_str.strip() else {}
        except json.JSONDecodeError:
            st.error(t["error_json_headers"])
            return

        with st.spinner("Выполняется запрос..."):
            try:
                response = requests.request(
                    method,
                    url,
                    headers=headers,
                    data=body_str.encode('utf-8') if body_str else None,
                    timeout=15
                )

                st.divider()
                st.markdown(f"### {t['response_header']}")

                status_color = "green" if 200 <= response.status_code < 300 else "red"
                st.markdown(f'**{t["status_code"]}:** <span style="color:{status_color}; font-weight: bold;">{response.status_code}</span>', unsafe_allow_html=True)

                with st.expander(t["response_headers"]):
                    st.json(dict(response.headers))

                st.markdown(f"**{t['response_body']}:**")
                try:
                    # Попытка распарсить и красиво отобразить JSON
                    st.json(response.json())
                except json.JSONDecodeError:
                    # Если не JSON, выводим как текст
                    st.code(response.text, language="text")

            except requests.RequestException as e:
                st.error(f"Ошибка выполнения запроса: {e}")

    with st.expander(t["guide_header"]):
        st.markdown(t["guide_content"])
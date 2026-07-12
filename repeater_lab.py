import streamlit as st
import requests
import time
import threading
from queue import Queue
import pandas as pd
import json


def worker(stop_event, results_queue, method, url, headers, data):
    """Воркер, который выполняет запросы."""
    while not stop_event.is_set():
        try:
            start_time = time.time()
            response = requests.request(method, url, headers=headers, data=data, timeout=15)
            end_time = time.time()

            results_queue.put({
                "status": response.status_code,
                "body": response.text,
                "time": end_time - start_time,
            })
        except requests.RequestException as e:
            results_queue.put({
                "status": "Error",
                "body": str(e),
                "time": 0,
            })
        # Если это не режим по времени, выходим после одной итерации
        if not stop_event.is_set(): # Проверка нужна, чтобы воркер не сделал лишний запрос после остановки
            break


def render_repeater_lab():
    lang = st.session_state.get("lang", "RU")

    STATUS_CODE_MESSAGES = {
        200: "OK", 201: "Created", 204: "No Content",
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed",
        500: "Internal Server Error", 502: "Bad Gateway", 503: "Service Unavailable",
        "Error": "Connection Error"
    }

    def get_status_desc(status_code):
        """Возвращает описание статуса или сам код, если описания нет."""
        if lang == "RU":
            # Можно добавить русские описания, если нужно
            return STATUS_CODE_MESSAGES.get(status_code, str(status_code))
        return STATUS_CODE_MESSAGES.get(status_code, str(status_code))

    # --- Тексты для i18n ---
    texts = {
        "RU": {
            "header": "🕹️ Повторитель запросов (Repeater)",
            "url_label": "URL эндпоинта",
            "method_label": "Метод",
            "headers_label": "Заголовки (JSON)",
            "body_label": "Тело запроса (для POST/PUT)",
            "mode_label": "Режим работы:",
            "mode_count": "Количество",
            "mode_duration": "Длительность",
            "req_count_label": "Количество запросов",
            "duration_label": "Длительность теста",
            "concurrency_label": "Параллельных потоков",
            "start_button": "🚀 Начать отправку",
            "status_preparing": "Подготовка...",
            "status_running": "Выполняется: {done}/{total} | Потоков: {threads}",
            "results_header": "📊 Результаты",
            "status_running_time": "Выполняется: {elapsed} / {total} сек. | Запросов: {req_count}",
            "total_reqs": "Всего запросов",
            "success_reqs": "Успешно",
            "failed_reqs": "Ошибки",
            "avg_time": "Среднее время",
            "min_time": "Мин. время",
            "max_time": "Макс. время",
            "sec": "с",
            "status_codes_header": "Коды ответа:",
        },
        "EN": {
            "header": "🕹️ Request Repeater",
            "url_label": "Endpoint URL",
            "method_label": "Method",
            "headers_label": "Headers (JSON)",
            "body_label": "Request Body (for POST/PUT)",
            "mode_label": "Operating Mode:",
            "mode_count": "By Count",
            "mode_duration": "By Duration",
            "req_count_label": "Number of requests",
            "duration_label": "Test Duration",
            "concurrency_label": "Concurrency level",
            "start_button": "🚀 Start Sending",
            "status_preparing": "Preparing...",
            "status_running": "Running: {done}/{total} | Threads: {threads}",
            "results_header": "📊 Results",
            "status_running_time": "Running: {elapsed} / {total} s | Requests: {req_count}",
            "total_reqs": "Total Requests",
            "success_reqs": "Successful",
            "failed_reqs": "Failed",
            "avg_time": "Avg. Time",
            "min_time": "Min Time",
            "max_time": "Max Time",
            "sec": "s",
            "status_codes_header": "Status Codes:",
        }
    }
    t = texts[lang]

    st.subheader(t["header"])

    with st.container(border=True):
        url = st.text_input(t["url_label"], "https://api.restful-api.dev/objects")
        c1, c2 = st.columns(2)
        method = c1.selectbox(t["method_label"], ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        concurrency = c2.slider(t["concurrency_label"], 1, 50, 10)
        
        c3, c4 = st.columns(2)
        headers_str = c3.text_area(t["headers_label"], '{"Content-Type": "application/json"}', height=150)
        body_str = c4.text_area(t["body_label"], '{"name": "Test", "data": {"year": 2024}}', height=150)

        st.divider()
        mode = st.radio(t["mode_label"], [t["mode_count"], t["mode_duration"]], horizontal=True)

        if mode == t["mode_count"]:
            req_count = st.number_input(t["req_count_label"], 1, 10000, 100)
        else:
            dur_c1, dur_c2 = st.columns(2)
            duration_value = dur_c1.number_input(t["duration_label"], min_value=1, value=10)
            duration_unit = dur_c2.selectbox("", ["Секунды", "Минуты", "Часы"] if lang == "RU" else ["Seconds", "Minutes", "Hours"])

    if st.button(t["start_button"], use_container_width=True):
        # --- ОБЩАЯ ПОДГОТОВКА ---
        try:
            headers = json.loads(headers_str) if headers_str else {}
        except json.JSONDecodeError:
            st.error("Ошибка в формате JSON для заголовков!")
            return

        results_queue = Queue()
        threads = []
        payload = body_str if method in ["POST", "PUT", "PATCH"] else None

        # --- ЗАПУСК В РЕЖИМЕ "ПО КОЛИЧЕСТВУ" ---
        if mode == t["mode_count"]:
            task_queue = Queue()
            for _ in range(req_count):
                task_queue.put(None)

            def count_worker(q, res_q):
                while not q.empty():
                    try:
                        q.get()
                        worker(threading.Event(), res_q, method, url, headers, payload)
                    finally:
                        q.task_done()

            for _ in range(min(concurrency, req_count)):
                thread = threading.Thread(target=count_worker, args=(task_queue, results_queue))
                thread.start()
                threads.append(thread)

            progress_bar = st.progress(0, text=t["status_preparing"])
            results = []
            while len(results) < req_count:
                if not results_queue.empty():
                    results.append(results_queue.get())
                progress_text = t["status_running"].format(done=len(results), total=req_count, threads=len(threads))
                progress_bar.progress(len(results) / req_count, text=progress_text)
                time.sleep(0.05)

        # --- ЗАПУСК В РЕЖИМЕ "ПО ДЛИТЕЛЬНОСТИ" ---
        else:
            unit_map = {"Seconds": 1, "Minutes": 60, "Hours": 3600, "Секунды": 1, "Минуты": 60, "Часы": 3600}
            duration_sec = duration_value * unit_map[duration_unit]
            stop_event = threading.Event()

            def duration_worker(stop_ev, res_q):
                while not stop_ev.is_set():
                    worker(stop_ev, res_q, method, url, headers, payload)

            for _ in range(concurrency):
                thread = threading.Thread(target=duration_worker, args=(stop_event, results_queue))
                thread.start()
                threads.append(thread)

            progress_bar = st.progress(0, text=t["status_preparing"])
            start_run_time = time.time()
            while time.time() - start_run_time < duration_sec:
                elapsed = time.time() - start_run_time
                progress_text = t["status_running_time"].format(elapsed=f"{elapsed:.1f}", total=duration_sec, req_count=results_queue.qsize())
                progress_bar.progress(elapsed / duration_sec, text=progress_text)
                time.sleep(0.1)

            stop_event.set()
            results = list(results_queue.queue)
            req_count = len(results)

        for thread in threads:
            thread.join()

        # --- ОБЩАЯ ОБРАБОТКА РЕЗУЛЬТАТОВ ---
        st.divider()
        st.markdown(f"### {t['results_header']}")
        
        # Успешными считаем только ответы с кодом 2xx
        successful_reqs = [r for r in results if isinstance(r.get('status'), int) and 200 <= r['status'] < 300]
        failed_reqs_count = len(results) - len(successful_reqs)
        
        response_times = [r['time'] for r in successful_reqs]
        avg_time = sum(response_times) / len(response_times) if response_times else 0
        min_time = min(response_times) if response_times else 0
        max_time = max(response_times) if response_times else 0

        # Метрики
        m1, m2, m3 = st.columns(3)
        m1.metric(t["total_reqs"], f"{req_count}")
        m2.metric(t["success_reqs"], f"{len(successful_reqs)}")
        m3.metric(t["failed_reqs"], f"{failed_reqs_count}", delta_color="inverse" if failed_reqs_count > 0 else "off")

        m4, m5, m6 = st.columns(3)
        m4.metric(t["avg_time"], f"{avg_time:.3f} {t['sec']}")
        m5.metric(t["min_time"], f"{min_time:.3f} {t['sec']}")
        m6.metric(t["max_time"], f"{max_time:.3f} {t['sec']}")

        # Статус-коды
        # Группируем результаты по коду и телу ответа, чтобы показать уникальные ответы
        grouped_results = {}
        for r in results:
            key = (r['status'], r['body'])
            if key not in grouped_results:
                grouped_results[key] = 0
            grouped_results[key] += 1

        # Формируем данные для итоговой таблицы
        summary_data = []
        for (status, body), count in grouped_results.items():
            summary_data.append({
                "Код ответа": status,
                "Описание": get_status_desc(status),
                "Количество": count,
                "Тело ответа / Ошибка": body
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        st.markdown(f"**{t['status_codes_header']}**")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
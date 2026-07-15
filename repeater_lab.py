import streamlit as st
import requests
import time
import threading
from queue import Queue, Empty
import pandas as pd
import json
from modules.i18n import get_text
import plotly.express as px

def worker(stop_event, results_queue, method, url, headers, data, is_count_mode):
    """Воркер, который выполняет запросы."""
    while not stop_event.is_set():
        try:
            start_time = time.time()
            response = requests.request(method, url, headers=headers, data=data, timeout=15)
            end_time = time.time()
            results_queue.put({
                "status": response.status_code,
                "body": response.text,
                "time": end_time - start_time, # Time in seconds
            })
        except requests.RequestException as e:
            results_queue.put({
                "status": "Error",
                "body": str(e),
                "time": 0,
            })
        # In count mode, each worker does one request and exits.
        # In duration mode, workers run until stop_event is set.
        if is_count_mode:
            break # For count mode, worker exits after one request

def _display_repeater_results(results, t):
    """Helper function to display metrics and charts for repeater results."""
    if not results:
        return

    req_count = len(results)

    # Успешными считаем только ответы с кодом 2xx
    successful_reqs = [r for r in results if isinstance(r.get('status'), int) and 200 <= r['status'] < 300]
    client_errors = [r for r in results if isinstance(r.get('status'), int) and 400 <= r['status'] < 500]
    server_errors = [r for r in results if isinstance(r.get('status'), int) and 500 <= r['status'] < 600]
    other_errors = [r for r in results if not isinstance(r.get('status'), int) or (r.get('status') < 200 or r.get('status') >= 600)]

    # Convert time to ms for display
    response_times_ms = [r['time'] * 1000 for r in successful_reqs if 'time' in r and r['time'] >= 0]
    avg_time = sum(response_times_ms) / len(response_times_ms) if response_times_ms else 0
    min_time = min(response_times_ms) if response_times_ms else 0
    max_time = max(response_times_ms) if response_times_ms else 0

    # Метрики
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("repeater_total_reqs"), f"{req_count}")
    m2.metric(t("repeater_success_reqs"), f"{len(successful_reqs)}")
    m3.metric(t("repeater_client_errors"), f"{len(client_errors)}", delta_color="inverse" if len(client_errors) > 0 else "off")
    m4.metric(t("repeater_server_errors"), f"{len(server_errors)}", delta_color="inverse" if len(server_errors) > 0 else "off")
    st.metric(t("repeater_other_errors"), f"{len(other_errors)}", delta_color="inverse" if len(other_errors) > 0 else "off")

    m5, m6, m7 = st.columns(3)
    m5.metric(t("repeater_avg_time"), f"{avg_time:.0f} {t('repeater_ms')}")
    m6.metric(t("repeater_min_time"), f"{min_time:.0f} {t('repeater_ms')}")
    m7.metric(t("repeater_max_time"), f"{max_time:.0f} {t('repeater_ms')}")

    # Line chart for response times
    if response_times_ms:
        st.markdown(f"**{t('repeater_response_time_chart_header')}**")
        rt_df = pd.DataFrame({
            t('repeater_request_number_label'): range(len(response_times_ms)),
            t('repeater_response_time_ms_label'): response_times_ms
        })
        rt_fig = px.line(rt_df, x=t('repeater_request_number_label'), y=t('repeater_response_time_ms_label'), title=t('repeater_response_time_chart_title'))
        st.plotly_chart(rt_fig, use_container_width=True)

    # Статус-коды
    status_counts = pd.DataFrame(results)['status'].value_counts().reset_index()
    status_counts.columns = [t("repeater_status_code"), t("repeater_count")]
    status_counts[t("repeater_description")] = status_counts[t("repeater_status_code")].apply(
        lambda code: requests.status_codes._codes.get(code, (str(code),))[0].replace('_', ' ').title() if isinstance(code, int) else str(code)
    )
    status_counts[t("repeater_status_code")] = status_counts[t("repeater_status_code")].astype(str)
    
    st.markdown(f"**{t('repeater_status_codes_header')}**")
    st.dataframe(status_counts[[t("repeater_status_code"), t("repeater_description"), t("repeater_count")]], use_container_width=True, hide_index=True)

    # Bar chart for status codes
    fig = px.bar(status_counts, x=t("repeater_status_code"), y=t("repeater_count"), 
                 title=t("repeater_status_codes_header"), color=t("repeater_status_code"))
    st.plotly_chart(fig, use_container_width=True)


def render_repeater_lab():
    t = get_text

    # Initialize session state variables for the repeater
    if 'repeater_is_running' not in st.session_state:
        st.session_state.repeater_is_running = False
    if 'repeater_stop_flag' not in st.session_state:
        st.session_state.repeater_stop_flag = False
    # NEW: State for managing threads and run configuration across reruns
    if 'repeater_run_config' not in st.session_state:
        st.session_state.repeater_run_config = {}
    if 'repeater_threads' not in st.session_state:
        st.session_state.repeater_threads = []
    if 'repeater_stop_event' not in st.session_state:
        st.session_state.repeater_stop_event = None
    if 'repeater_results_queue' not in st.session_state:
        st.session_state.repeater_results_queue = None
    if 'repeater_results' not in st.session_state:
        st.session_state.repeater_results = []
    if 'repeater_progress_text' not in st.session_state:
        st.session_state.repeater_progress_text = ""
    if 'repeater_progress_value' not in st.session_state:
        st.session_state.repeater_progress_value = 0
    if 'repeater_mode' not in st.session_state:
        st.session_state.repeater_mode = t("repeater_mode_count")
    if 'repeater_url' not in st.session_state:
        st.session_state.repeater_url = "https://api.restful-api.dev/objects"
    if 'repeater_method' not in st.session_state:
        st.session_state.repeater_method = "GET"
    if 'repeater_headers' not in st.session_state:
        st.session_state.repeater_headers = '{"Content-Type": "application/json"}'
    if 'repeater_body' not in st.session_state:
        st.session_state.repeater_body = '{"name": "Test", "data": {"year": 2024}}'

    # Pre-fill from API Client if available
    if st.session_state.get('api_client_url_for_repeater'):
        st.session_state.repeater_url = st.session_state.api_client_url_for_repeater
        st.session_state.repeater_method = st.session_state.api_client_method_for_repeater
        
        # Convert list of dicts to JSON string for headers
        headers_dict = {item["key"]: item["value"] for item in st.session_state.api_client_headers_for_repeater if item["key"]}
        st.session_state.repeater_headers = json.dumps(headers_dict, indent=2) if headers_dict else '{}'

        st.session_state.repeater_body = st.session_state.api_client_body_for_repeater

        # Clear the API Client data from session state
        del st.session_state.api_client_url_for_repeater
        del st.session_state.api_client_method_for_repeater
        del st.session_state.api_client_headers_for_repeater
        del st.session_state.api_client_body_for_repeater
        st.rerun() # Rerun to apply pre-filled values

    st.subheader(t("repeater_header"))

    with st.container(border=True):
        url = st.text_input(t("repeater_url_label"), value=st.session_state.repeater_url)
        st.session_state.repeater_url = url

        c1, c2 = st.columns(2)
        method = c1.selectbox(t("repeater_method_label"), ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"], key="repeater_method_select")
        st.session_state.repeater_method = method
        concurrency = c2.slider(t("repeater_concurrency_label"), 1, 50, 10)
        
        c3, c4 = st.columns(2)
        headers_str = c3.text_area(t("repeater_headers_label"), value=st.session_state.repeater_headers, height=150)
        st.session_state.repeater_headers = headers_str
        body_str = c4.text_area(t("repeater_body_label"), value=st.session_state.repeater_body, height=150)
        st.session_state.repeater_body = body_str

        st.divider()
        mode = st.radio(t("repeater_mode_label"), [t("repeater_mode_count"), t("repeater_mode_duration")], horizontal=True)
        st.session_state.repeater_mode = mode

        if st.session_state.repeater_mode == t("repeater_mode_count"):
            req_count = st.number_input(t("repeater_req_count_label"), 1, 10000, 100)
        else:
            dur_c1, dur_c2 = st.columns(2)
            duration_value = dur_c1.number_input(t("repeater_duration_label"), min_value=1, value=10)
            duration_unit = dur_c2.selectbox("", [t("repeater_duration_unit_seconds"), t("repeater_duration_unit_minutes"), t("repeater_duration_unit_hours")])

    start_button_col, stop_button_col, clear_button_col = st.columns(3)

    # --- START BUTTON HANDLER ---
    if start_button_col.button(t("repeater_start_button"), width='stretch', type="primary", disabled=st.session_state.repeater_is_running):
        if not url:
            st.error(t("repeater_url_empty_error"))
        else:
            # Set state to running and clear previous results
            st.session_state.repeater_is_running = True
            st.session_state.repeater_stop_flag = False
            st.session_state.repeater_results = []
            st.session_state.repeater_threads = []
            
            # Store all parameters for the run in session_state
            st.session_state.repeater_run_config = {
                "url": url, "method": method, "headers_str": headers_str, "body_str": body_str,
                "concurrency": concurrency, "mode": mode,
                "is_count_mode": mode == t("repeater_mode_count"),
                "req_count": req_count if mode == t("repeater_mode_count") else 0,
                "duration_value": duration_value if mode != t("repeater_mode_count") else 0,
                "duration_unit": duration_unit if mode != t("repeater_mode_count") else ""
            }
            st.rerun()

    # --- STOP BUTTON HANDLER ---
    if stop_button_col.button(t("repeater_stop_button"), width='stretch', disabled=not st.session_state.repeater_is_running):
        st.session_state.repeater_stop_flag = True
        if st.session_state.repeater_stop_event:
            st.session_state.repeater_stop_event.set()
        st.info("Остановка запросов...")
        st.rerun()

    # --- CLEAR BUTTON HANDLER ---
    with clear_button_col:
        if st.button(t("repeater_clear_button"), width='stretch', disabled=st.session_state.repeater_is_running or not st.session_state.repeater_results):
            st.session_state.repeater_results = []
            st.rerun()

    # --- MAIN PROCESSING BLOCK (runs if state is 'running') ---
    if st.session_state.repeater_is_running:
        run_config = st.session_state.repeater_run_config
        
        try:
            headers = json.loads(run_config['headers_str']) if run_config['headers_str'] else {}
        except json.JSONDecodeError:
            st.error(t("repeater_json_error_headers"))
            st.session_state.repeater_is_running = False
            st.rerun()
        
        payload = None
        if run_config['method'] in ["POST", "PUT", "PATCH"]:
            if headers.get("Content-Type") == "application/json":
                try:
                    payload = json.dumps(json.loads(run_config['body_str'])) if run_config['body_str'].strip() else None
                except json.JSONDecodeError:
                    st.error(t("repeater_json_error_body"))
                    st.session_state.repeater_is_running = False
                    st.rerun()
            else:
                payload = run_config['body_str'] if run_config['body_str'].strip() else None

        current_repeater_mode = run_config['mode']
        progress_placeholder = st.empty()
        live_results_placeholder = st.empty()

        # --- THREAD INITIALIZATION (runs only once per test) ---
        if not st.session_state.repeater_threads:
            st.session_state.repeater_stop_event = threading.Event()
            st.session_state.repeater_results_queue = Queue()
            
            if run_config['is_count_mode']:
                req_count = run_config['req_count']
                task_queue = Queue()
                for _ in range(req_count): task_queue.put(None)
                
                def count_worker(stop_ev, q, res_q, method, url, headers, payload, is_count_mode):
                    while not q.empty() and not stop_ev.is_set():
                        try:
                            q.get()
                            worker(stop_ev, res_q, method, url, headers, payload, is_count_mode)
                        finally: q.task_done()
                    res_q.put({"status": "THREAD_DONE"})
                
                for _ in range(min(run_config['concurrency'], req_count)):
                    thread = threading.Thread(target=count_worker, args=(st.session_state.repeater_stop_event, task_queue, st.session_state.repeater_results_queue, run_config['method'], run_config['url'], headers, payload, run_config['is_count_mode']))
                    thread.start()
                    st.session_state.repeater_threads.append(thread)
            else: # Duration mode
                def duration_worker(stop_ev, res_q, method, url, headers, payload, is_count_mode):
                    worker(stop_ev, res_q, method, url, headers, payload, is_count_mode)
                    res_q.put({"status": "THREAD_DONE"})
                
                st.session_state.repeater_start_time = time.time()
                for _ in range(run_config['concurrency']):
                    thread = threading.Thread(target=duration_worker, args=(st.session_state.repeater_stop_event, st.session_state.repeater_results_queue, run_config['method'], run_config['url'], headers, payload, run_config['is_count_mode']))
                    thread.start()
                    st.session_state.repeater_threads.append(thread)

        # --- PROGRESS AND RESULT HANDLING (runs on each rerun) ---
        # Collect results from queue
        while not st.session_state.repeater_results_queue.empty():
            try:
                result = st.session_state.repeater_results_queue.get_nowait()
                if result.get("status") != "THREAD_DONE":
                    st.session_state.repeater_results.append(result)
            except Empty:
                break

        # Check for finish conditions
        finished = False
        if run_config['is_count_mode']:
            req_count = run_config['req_count']
            progress_value = min(1.0, len(st.session_state.repeater_results) / req_count) if req_count > 0 else 0
            progress_text = t("repeater_status_running_count").format(done=len(st.session_state.repeater_results), total=req_count, threads=len(st.session_state.repeater_threads))
            if len(st.session_state.repeater_results) >= req_count:
                finished = True
        else: # Duration mode
            duration_sec = run_config['duration_value'] * {t("repeater_duration_unit_seconds"): 1, t("repeater_duration_unit_minutes"): 60, t("repeater_duration_unit_hours"): 3600}[run_config['duration_unit']]
            elapsed = time.time() - st.session_state.repeater_start_time
            progress_value = min(1.0, elapsed / duration_sec) if duration_sec > 0 else 0
            progress_text = t("repeater_status_running_duration").format(elapsed=f"{elapsed:.1f}", total=duration_sec, req_count=len(st.session_state.repeater_results))
            if elapsed >= duration_sec:
                finished = True

        if st.session_state.repeater_stop_flag:
            finished = True

        # Update UI
        with progress_placeholder.container():
            st.progress(progress_value, text=progress_text)

        # Display live results
        with live_results_placeholder.container():
            if st.session_state.repeater_results:
                st.divider()
                st.markdown(f"### {t('repeater_live_results_header')}")
                _display_repeater_results(st.session_state.repeater_results, t)

        # Finalize if finished
        if finished:
            if st.session_state.repeater_stop_event:
                st.session_state.repeater_stop_event.set()
            for thread in st.session_state.repeater_threads:
                thread.join(timeout=1.0)
            
            live_results_placeholder.empty()
            st.session_state.repeater_is_running = False
            st.session_state.repeater_threads = [] # Clean up
            st.rerun()
        else:
            # Schedule next rerun to update progress
            time.sleep(0.2)
            st.rerun()

    # --- ОБЩАЯ ОБРАБОТКА И ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ ---
    if not st.session_state.repeater_is_running and st.session_state.repeater_results:
        st.divider()
        st.markdown(f"### {t('repeater_results_header')}")
        _display_repeater_results(st.session_state.repeater_results, t)

    with st.expander(t("repeater_guide_header")):
        st.markdown(t("repeater_guide_content"))
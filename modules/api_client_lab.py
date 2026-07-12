import streamlit as st
import requests
import json
import shlex
import pandas as pd
from urllib.parse import urlparse, parse_qs
from modules.i18n import get_text

# A more robust cURL parser using shlex
def parse_curl_command(curl_command):
    # Remove "curl " from the beginning and backslashes for multiline commands
    curl_command = curl_command.strip().replace("curl ", "", 1).replace('\\\n', ' ')
    
    args = shlex.split(curl_command)
    
    result = {
        'url': '',
        'method': 'GET',
        'headers': {},
        'data': '',
        'params': {}
    }
    
    # The first argument is often the URL, if it doesn't start with '-'
    if args and not args[0].startswith('-'):
        raw_url = args.pop(0)
        # Parse URL to separate base from query params
        parsed_url = urlparse(raw_url)
        result['url'] = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        # The value from parse_qs is a list, we take the first element.
        result['params'] = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        if not result['url'].startswith('http'):
            result['url'] = 'https://' + result['url']

    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ['-X', '--request']:
            if i + 1 < len(args):
                result['method'] = args[i+1].upper()
                i += 1
        elif arg in ['-H', '--header']:
            if i + 1 < len(args):
                key, value = args[i+1].split(':', 1)
                result['headers'][key.strip()] = value.strip()
                i += 1
        elif arg in ['-d', '--data', '--data-raw', '--data-binary']:
            if i + 1 < len(args):
                result['data'] = args[i+1]
                i += 1
        elif arg == '--url':
             if i + 1 < len(args):
                result['url'] = args[i+1]
                i += 1
        # If a URL is found as the last argument
        elif i == len(args) - 1 and arg.startswith('http'):
            result['url'] = arg

        i += 1
        
    # If method is not specified but data is present, it's likely a POST
    if result['data'] and result['method'] == 'GET':
        result['method'] = 'POST'

    # Return headers as a dict
    
    return result

def render_api_client_lab():
    t = get_text

    st.subheader(t("about_module_api_client"))

    # --- STATE INITIALIZATION ---
    if 'api_history' not in st.session_state:
        st.session_state.api_history = []
    if 'api_response' not in st.session_state:
        st.session_state.api_response = None
    
    # --- NEW: State for data editors ---
    if 'api_params_df' not in st.session_state:
        st.session_state.api_params_df = pd.DataFrame([{"key": "", "value": ""}])
    if 'api_headers_df' not in st.session_state:
        st.session_state.api_headers_df = pd.DataFrame([
            {"key": "Content-Type", "value": "application/json"}
        ])

    # State for other input fields
    if 'api_url' not in st.session_state: st.session_state.api_url = ""
    if 'api_method' not in st.session_state: st.session_state.api_method = "GET"
    if 'api_body' not in st.session_state: st.session_state.api_body = ""
    


    # --- LAYOUT ---
    main_col, history_col = st.columns([2, 1])

    # --- HISTORY COLUMN (RIGHT) ---
    with history_col:
        st.markdown(f"#### {t('history_header')}")
        
        if st.button(t('history_clear'), use_container_width=True):
            st.session_state.api_history = []
            st.session_state.api_response = None
            st.rerun()

        st.divider()

        if not st.session_state.api_history:
            st.info(t('history_empty'))
        else:
            # Display history in reverse order (newest first)
            for i, req in reversed(list(enumerate(st.session_state.api_history))):
                with st.container(border=True):
                    st.markdown(f"**{req['method']}** `{req['url']}`")
                    
                    hc1, hc2 = st.columns(2)
                    if hc1.button(t('history_replay'), key=f"replay_{i}", use_container_width=True):
                        st.session_state.api_url = req['url']
                        st.session_state.api_method = req['method']
                        st.session_state.api_body = req['body']

                        # Handle params and headers (with backward compatibility)
                        if 'params_df' in req: # New format
                            st.session_state.api_params_df = pd.DataFrame(req['params_df']) if req['params_df'] else pd.DataFrame([{"key": "", "value": ""}])
                            st.session_state.api_headers_df = pd.DataFrame(req['headers_df']) if req['headers_df'] else pd.DataFrame([{"key": "", "value": ""}])
                        else: # Old format
                            params_list = []
                            if req.get('params'):
                                for line in req['params'].strip().split('\n'):
                                    if '=' in line:
                                        key, val = line.split('=', 1)
                                        params_list.append({"key": key.strip(), "value": val.strip()})
                            st.session_state.api_params_df = pd.DataFrame(params_list) if params_list else pd.DataFrame([{"key": "", "value": ""}])
                            try:
                                headers_dict = json.loads(req.get('headers', '{}'))
                                st.session_state.api_headers_df = pd.DataFrame(list(headers_dict.items()), columns=["key", "value"])
                            except (json.JSONDecodeError, TypeError):
                                st.session_state.api_headers_df = pd.DataFrame([{"key": "", "value": ""}])

                        st.session_state.api_response = None
                        st.rerun()

                    if hc2.button(t('history_delete'), key=f"delete_{i}", use_container_width=True):
                        st.session_state.api_history.pop(i)
                        st.rerun()

    # --- MAIN COLUMN (LEFT) ---
    with main_col:
        # --- cURL IMPORTER ---
        with st.expander(t('curl_expander')):
            curl_input = st.text_area(t('curl_label'), height=100)
            if st.button(t('curl_button')):
                if curl_input:
                    try:
                        parsed = parse_curl_command(curl_input)
                        st.session_state.api_url = parsed['url']
                        st.session_state.api_method = parsed['method']
                        st.session_state.api_body = parsed['data']
                        # Populate data editors
                        params_df = pd.DataFrame(list(parsed['params'].items()), columns=["key", "value"])
                        headers_df = pd.DataFrame(list(parsed['headers'].items()), columns=["key", "value"])
                        st.session_state.api_params_df = params_df if not params_df.empty else pd.DataFrame([{"key": "", "value": ""}])
                        st.session_state.api_headers_df = headers_df if not headers_df.empty else pd.DataFrame([{"key": "", "value": ""}])

                        st.rerun()
                    except Exception as e:
                        st.error(f"{t('curl_error')}: {e}")

        # --- REQUEST BUILDER ---
        with st.container(border=True):
            url = st.text_input("URL", value=st.session_state.api_url)
            st.session_state.api_url = url # Sync back manual changes

            method_options = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
            method_index = method_options.index(st.session_state.api_method) if st.session_state.api_method in method_options else 0
            method = st.selectbox("Method", options=method_options, index=method_index)
            st.session_state.api_method = method

            tab_params, tab_headers, tab_body = st.tabs([t("params_tab"), t("headers_tab"), t("body_tab")])

            with tab_params:
                params_df = st.data_editor(
                    st.session_state.api_params_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="params_editor"
                )
                st.session_state.api_params_df = params_df

            with tab_headers:
                headers_df = st.data_editor(
                    st.session_state.api_headers_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    key="headers_editor"
                )
                st.session_state.api_headers_df = headers_df

            with tab_body:
                body = st.text_area("Request Body", height=150, value=st.session_state.api_body)
                st.session_state.api_body = body

        if st.button(t("send_button"), use_container_width=True, type="primary"):
            if not url:
                st.error("URL не может быть пустым!")
            else:
                with st.spinner("Выполняется запрос..."):
                    try:
                        # Prepare params and headers from data editors
                        req_params = {row["key"]: row["value"] for _, row in params_df.iterrows() if row["key"]}
                        req_headers = {row["key"]: row["value"] for _, row in headers_df.iterrows() if row["key"]}

                        # Make request
                        response = requests.request(
                            method=method,
                            url=url,
                            headers=req_headers,
                            params=req_params,
                            data=body.encode('utf-8') if body.strip() else None,
                            timeout=15
                        )
                        st.session_state.api_response = response

                        # Add to history
                        st.session_state.api_history.append({
                            "url": url,
                            "method": method,
                            "params_df": params_df.to_dict('records'),
                            "headers_df": headers_df.to_dict('records'),
                            "body": body,
                        })
                        # Limit history size
                        if len(st.session_state.api_history) > 20:
                            st.session_state.api_history.pop(0)

                    except requests.RequestException as e:
                        st.session_state.api_response = e
                st.rerun()

        # --- RESPONSE VIEWER ---
        if st.session_state.api_response is not None:
            st.divider()
            st.markdown(f"### {t('response_header')}")
            response = st.session_state.api_response

            if isinstance(response, requests.Response):
                # --- NEW: Response Metrics ---
                response_time_ms = response.elapsed.total_seconds() * 1000
                response_size_kb = len(response.content) / 1024 if response.content else 0
                status_code = response.status_code
                color = "green" if 200 <= status_code < 300 else "orange" if 400 <= status_code < 500 else "red"

                st.markdown(
                    f"""
                    **{t('response_status')}:** <span style='color:{color}; font-weight:bold;'>{status_code} {response.reason}</span> &nbsp;&nbsp;&nbsp;
                    **{t('response_time')}:** <span style='font-weight:bold;'>{response_time_ms:.0f} ms</span> &nbsp;&nbsp;&nbsp;
                    **{t('response_size')}:** <span style='font-weight:bold;'>{response_size_kb:.2f} KB</span>
                    """, unsafe_allow_html=True)
                
                resp_tab1, resp_tab2 = st.tabs([t('response_body_tab'), t('response_headers_tab')])
                with resp_tab1:
                    try:
                        # Try to pretty-print JSON
                        st.json(response.json())
                    except (json.JSONDecodeError, AttributeError):
                        # Fallback to plain text
                        st.code(response.text, language='text')                
                with resp_tab2:
                    st.json(dict(response.headers))

            elif isinstance(response, requests.RequestException):
                st.error(f"Ошибка подключения: {response}")
    
    with st.expander(t("guide_header")):
        st.markdown(t("api_client_guide_content"))
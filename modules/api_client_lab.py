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

def render_kv_editor(items_list, add_button_label, key_placeholder, value_placeholder, list_key):
    """Renders a dynamic key-value editor using text inputs."""
    for i, item in enumerate(items_list):
        col1, col2, col3 = st.columns([5, 5, 1])
        new_key = col1.text_input(f"Key {i}", value=item["key"], placeholder=key_placeholder, key=f"{list_key}_k_{i}", label_visibility="collapsed") # Label is for accessibility
        new_value = col2.text_input(f"Value {i}", value=item["value"], placeholder=value_placeholder, key=f"{list_key}_v_{i}", label_visibility="collapsed") # Label is for accessibility
        
        items_list[i]["key"] = new_key
        items_list[i]["value"] = new_value

        if col3.button("🗑️", key=f"{list_key}_del_{i}"):
            items_list.pop(i)
            st.rerun()

    if st.button(add_button_label, width='stretch'):
        items_list.append({"key": "", "value": ""})
        st.rerun()

    return items_list

def render_api_client_lab():
    t = get_text

    st.subheader(t("api_client_header"))

    # --- STATE INITIALIZATION ---
    if 'api_history' not in st.session_state:
        st.session_state.api_history = []
    if 'api_response' not in st.session_state:
        st.session_state.api_response = None
    
    # --- NEW: State for dynamic editors ---
    if 'api_params' not in st.session_state:
        st.session_state.api_params = [{"key": "", "value": ""}]
    if 'api_headers' not in st.session_state:
        st.session_state.api_headers = [
            {"key": "Content-Type", "value": "application/json"}
        ]

    # State for other input fields
    if 'api_url' not in st.session_state: st.session_state.api_url = ""
    if 'api_method' not in st.session_state: st.session_state.api_method = "GET"
    if 'api_body' not in st.session_state: st.session_state.api_body = ""
    


    # --- LAYOUT ---
    main_col, history_col = st.columns([2, 1])

    # --- HISTORY COLUMN (RIGHT) ---
    with history_col:
        st.markdown(f"#### {t('history_header')}")
        
        if st.button(t('history_clear'), width='stretch'):
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
                    if hc1.button(t('history_replay'), key=f"replay_{i}", width='stretch'):
                        st.session_state.api_url = req['url']
                        st.session_state.api_method = req['method']
                        st.session_state.api_body = req['body']

                        # Populate dynamic editors
                        st.session_state.api_params = req.get('params', [{"key": "", "value": ""}])
                        st.session_state.api_headers = req.get('headers', [{"key": "", "value": ""}])
                        # Ensure lists are not empty
                        if not st.session_state.api_params: st.session_state.api_params = [{"key": "", "value": ""}]
                        if not st.session_state.api_headers: st.session_state.api_headers = [{"key": "", "value": ""}]

                        st.session_state.api_response = None
                        st.rerun()

                    if hc2.button(t('history_delete'), key=f"delete_{i}", width='stretch'):
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
                        st.session_state.api_params = [{"key": k, "value": v} for k, v in parsed['params'].items()]
                        st.session_state.api_headers = [{"key": k, "value": v} for k, v in parsed['headers'].items()]
                        if not st.session_state.api_params: st.session_state.api_params = [{"key": "", "value": ""}]
                        if not st.session_state.api_headers: st.session_state.api_headers = [{"key": "", "value": ""}]

                        st.toast(t("curl_parse_success"))
                        st.rerun()
                    except Exception as e:
                        st.error(f"{t('curl_error')}: {e}")

        # --- REQUEST BUILDER ---
        with st.container(border=True):
            url = st.text_input(t("api_client_url_label"), value=st.session_state.api_url, placeholder="https://api.example.com/v1/users")
            st.session_state.api_url = url # Sync back manual changes

            method_options = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
            method_index = method_options.index(st.session_state.api_method) if st.session_state.api_method in method_options else 0
            method = st.selectbox(t("api_client_method_label"), options=method_options, index=method_index, label_visibility="collapsed")
            st.session_state.api_method = method

            tab_params, tab_headers, tab_body = st.tabs([t("params_tab"), t("headers_tab"), t("body_tab")])

            with tab_params:
                st.session_state.api_params = render_kv_editor(st.session_state.api_params, f"➕ {t('api_client_add_param_button')}", t("api_client_key_placeholder"), t("api_client_value_placeholder"), "params")

            with tab_headers:
                st.session_state.api_headers = render_kv_editor(st.session_state.api_headers, f"➕ {t('api_client_add_header_button')}", t("api_client_key_placeholder"), t("api_client_value_placeholder"), "headers")

            with tab_body:
                body = st.text_area(t("api_client_body_label"), height=150, value=st.session_state.api_body, placeholder='{ "key": "value" }')
                st.session_state.api_body = body

        if st.button(t("send_button"), width='stretch', type="primary"):
            # Store current request for Repeater integration
            st.session_state.api_client_url_for_repeater = url
            st.session_state.api_client_method_for_repeater = method
            st.session_state.api_client_headers_for_repeater = st.session_state.api_headers
            st.session_state.api_client_body_for_repeater = body

            if not url:
                st.error(t("api_client_url_error"))
            else:
                with st.spinner(t("link_lab_spinner_text")): # Reusing spinner text
                    try:
                        # Prepare params and headers from data editors
                        req_params = {item["key"]: item["value"] for item in st.session_state.api_params if item["key"]}
                        req_headers = {item["key"]: item["value"] for item in st.session_state.api_headers if item["key"]}

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
                            "params": st.session_state.api_params,
                            "headers": st.session_state.api_headers,
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
                
                if 200 <= status_code < 300:
                    status_icon, color = "✅", "green"
                elif 400 <= status_code < 500:
                    status_icon, color = "⚠️", "orange"
                else:
                    status_icon, color = "❌", "red"

                st.markdown(
                    f"""
                    {status_icon} **{t('response_status')}:** <span style='color:{color}; font-weight:bold;'>{status_code} {response.reason}</span> &nbsp;&nbsp;&nbsp;
                    **{t('response_time')}:** <span style='font-weight:bold;'>{response_time_ms:.0f} ms</span> &nbsp;&nbsp;&nbsp;
                    **{t('response_size')}:** <span style='font-weight:bold;'>{response_size_kb:.2f} KB</span>
                    """, unsafe_allow_html=True)
                
                resp_tab1, resp_tab2, resp_tab3 = st.tabs([t('response_body_tab'), t('response_headers_tab'), t('api_client_cookies_tab')])
                with resp_tab1:
                    try:
                        st.json(response.json())
                    except (json.JSONDecodeError, AttributeError):
                        st.code(response.text, language='text')                
                with resp_tab2:
                    st.json(dict(response.headers))
                with resp_tab3:
                    st.json(dict(response.cookies))

            elif isinstance(response, requests.RequestException):
                st.error(t("api_client_request_error").format(e=response))
    
    with st.expander(t("guide_header")):
        st.markdown(t("api_client_guide_content"))
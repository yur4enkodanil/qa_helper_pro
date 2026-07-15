import streamlit as st
from modules.i18n import get_text
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import pandas as pd
from playwright.sync_api import sync_playwright, Error as PlaywrightError
from axe_core_python.sync_playwright import Axe


@st.cache_data(show_spinner=False)
def check_accessibility(url):
    """Запускает Playwright, открывает URL и выполняет проверку с помощью axe-core."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=30000)
            results = Axe().run(page)
            browser.close()
            return results['violations'], None
    except PlaywrightError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)


@st.cache_data(show_spinner=False)
def crawl_links(start_url, depth_limit=2):
    """Обходит сайт в поисках битых ссылок с ограничением глубины."""
    try:
        domain = urlparse(start_url).netloc
        queue = deque([(start_url, 0)])
        visited = {start_url}
        broken_links = []
        session = requests.Session()
        session.headers.update({'User-Agent': 'QA-Helper-Pro-Link-Checker/1.0'})

        while queue:
            current_url, current_depth = queue.popleft()

            try:
                # Используем HEAD для скорости, если не сработает - GET
                response = session.head(current_url, timeout=5, allow_redirects=True)
                if not response.ok:
                    # Проверяем GET, т.к. HEAD может быть заблокирован
                    response = session.get(current_url, timeout=5)

                if not response.ok:
                    broken_links.append({"url": current_url, "status": response.status_code, "source": "N/A"}) # Source is hard to track here
                    continue

                # Ищем ссылки только на страницах нашего домена и в пределах глубины
                if current_depth < depth_limit and 'text/html' in response.headers.get('Content-Type', ''):
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        absolute_url = urljoin(current_url, href)

                        # Убираем якоря и параметры для чистоты
                        absolute_url = urlparse(absolute_url)._replace(query="", fragment="").geturl().rstrip('/')

                        if absolute_url not in visited and urlparse(absolute_url).netloc == domain:
                            visited.add(absolute_url)
                            queue.append((absolute_url, current_depth + 1))

            except requests.RequestException as e:
                broken_links.append({"url": current_url, "status": "Error", "source": "N/A"})

        return broken_links, None
    except Exception as e:
        return None, str(e)


def render_frontend_lab():
    t = get_text
    st.subheader(t("frontend_lab_header"))

    tab_accessibility, tab_links = st.tabs([
        t("frontend_lab_tab_accessibility"),
        t("frontend_lab_tab_links")
    ])

    # --- ВКЛАДКА АНАЛИЗА ДОСТУПНОСТИ ---
    with tab_accessibility:
        url_a11y = st.text_input(t("frontend_url_label"), key="a11y_url", placeholder="https://example.com")
        
        col1, col2 = st.columns(2)
        if col1.button(t("frontend_button_check"), key="a11y_check", width='stretch'):
            if not url_a11y:
                st.warning(t("frontend_lab_error_url"))
            else:
                with st.spinner(t("frontend_accessibility_running")):
                    violations, error = check_accessibility(url_a11y)

                st.markdown(f"#### {t('frontend_accessibility_results')}")
                if error:
                    st.error(t("frontend_lab_error_generic").format(error=error))
                elif not violations:
                    st.success(t("frontend_accessibility_no_violations"))
                else:
                    st.warning(t("frontend_accessibility_violations_found").format(count=len(violations)))
                    for i, v in enumerate(violations):
                        impact_color = {"minor": "grey", "moderate": "orange", "serious": "orange", "critical": "red"}.get(v['impact'], "grey")
                        with st.expander(f"**{v['id']}** ({t('frontend_accessibility_impact')}: :{impact_color}[{v['impact']}] )"):
                            st.markdown(f"**{v['description']}**")
                            st.markdown(f"[{v['help']}]({v['helpUrl']})")
                            st.markdown(f"**{t('frontend_accessibility_nodes')}:**")
                            for node in v['nodes']:
                                st.code(node['html'], language='html')

        if col2.button(t("frontend_lab_button_clear_cache"), key="a11y_clear", width='stretch', type="secondary"):
            check_accessibility.clear()
            st.toast("Cache for Accessibility check cleared!")

    # --- ВКЛАДКА ПОИСКА БИТЫХ ССЫЛОК ---
    with tab_links:
        url_links = st.text_input(t("frontend_url_label"), key="links_url", placeholder="https://example.com")
        depth_limit = st.number_input(
            t("frontend_lab_crawl_depth_label"), 
            min_value=0, max_value=10, value=2, 
            help="0 - только стартовая страница, 1 - стартовая + ссылки с нее, и т.д."
        )

        col3, col4 = st.columns(2)
        if col3.button(t("frontend_button_crawl"), key="links_crawl", width='stretch'):
            if not url_links:
                st.warning(t("frontend_lab_error_url"))
            else:
                with st.spinner(t("frontend_links_running")):
                    # Вызываем кешированную функцию
                    broken_links, error = crawl_links(url_links, depth_limit)

                st.markdown(f"#### {t('frontend_links_results')}")
                if error:
                    st.error(t("frontend_lab_error_generic").format(error=error))
                elif not broken_links:
                    st.success(t("frontend_links_no_broken"))
                else:
                    st.warning(t("frontend_links_broken_found").format(count=len(broken_links)))
                    df = pd.DataFrame(broken_links)
                    df.rename(columns={
                        "url": t("frontend_links_table_url"),
                        "status": t("frontend_links_table_status"),
                        "source": t("frontend_links_table_source")
                    }, inplace=True)
                    st.dataframe(df, use_container_width=True, hide_index=True)

        if col4.button(t("frontend_lab_button_clear_cache"), key="links_clear", width='stretch', type="secondary"):
            crawl_links.clear()
            st.toast("Cache for Broken Links check cleared!")
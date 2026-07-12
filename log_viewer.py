import streamlit as st
import os

def render_log_viewer():
    """
    Отображает содержимое файла логов и позволяет его очистить.
    """
    lang = st.session_state.get("lang", "RU")
    
    # --- Тексты для i18n ---
    texts = {
        "RU": {
            "header": "🪲 Журнал ошибок (Logs)",
            "info": "Здесь отображаются технические ошибки, которые произошли во время работы приложения. Если что-то пошло не так, скопируйте этот текст и приложите к сообщению об ошибке.",
            "read_error": "Не удалось прочитать файл логов: ",
            "no_errors": "🎉 Ошибок не найдено. Журнал пуст.",
            "clear_button": "🗑️ Очистить журнал логов",
            "not_created": "🎉 Файл логов еще не создан. Ошибок не было."
        },
        "EN": {
            "header": "🪲 Error Log",
            "info": "This section displays technical errors that occurred while the application was running. If something went wrong, copy this text and attach it to your bug report.",
            "read_error": "Failed to read log file: ",
            "no_errors": "🎉 No errors found. The log is empty.",
            "clear_button": "🗑️ Clear Log File",
            "not_created": "🎉 Log file not created yet. No errors have occurred."
        }
    }
    t = texts[lang]

    st.subheader(t["header"])
    st.info(t["info"])

    # Путь к лог-файлу в корневой папке проекта
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    log_file_path = os.path.join(project_root, "qa_helper_pro.log")

    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r", encoding="utf-8") as f:
                log_content = f.read()
            
            st.code(log_content, language="log") if log_content else st.success(t["no_errors"])

            if st.button(t["clear_button"]):
                with open(log_file_path, "w", encoding="utf-8") as f: f.write("")
                st.rerun()
        except Exception as e:
            st.error(f"{t['read_error']}{e}")
    else:
        st.success(t["not_created"])
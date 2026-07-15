import streamlit as st
import os
import json
from datetime import datetime

NOTES_DIR = "qa_notes_storage"
TEMPLATES_FILE = os.path.join(NOTES_DIR, "templates.json")

# Инициализация папок и дефолтных шаблонов
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR, exist_ok=True)

if not os.path.exists(TEMPLATES_FILE):
    default_templates = {
        "🐞 Баг-репорт": "--- BUG REPORT ---\nSummary: \nSteps:\n1. \nActual:\nExpected:",
        "📋 Чек-лист": "- [ ] Проверка 1\n- [ ] Проверка 2",
        "🔑 Аккаунты": "Admin: admin / admin123\nUser: user / user123",
    }
    with open(TEMPLATES_FILE, "w", encoding="utf-8") as f:
        json.dump(default_templates, f, ensure_ascii=False, indent=4)


def load_templates():
    with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_templates(templates):
    with open(TEMPLATES_FILE, "w", encoding="utf-8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=4)


def render_notes_lab():
    logger = st.session_state.get("logger")
    lang = st.session_state.get("lang", "RU")
    st.subheader("📝 Лаборатория заметок" if lang == "RU" else "📝 Notes Lab")

    # Загрузка шаблонов и файлов
    templates = load_templates()
    existing_files = sorted([f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")])
    if not existing_files:
        with open(os.path.join(NOTES_DIR, "General.txt"), "w", encoding="utf-8") as f:
            f.write("")
        existing_files = ["General.txt"]

    # --- СЕКЦИЯ РЕДАКТИРОВАНИЯ ШАБЛОНОВ ---
    with st.expander(
        "⚙️ Управление шаблонами" if lang == "RU" else "⚙️ Manage Templates"
    ):
        st.write(
            "Здесь можно изменить текст кнопок или добавить новые."
            if lang == "RU"
            else "Edit button texts or add new ones here."
        )

        # Редактирование существующих
        updated_templates = {}
        for label, text in templates.items():
            c_name, c_text, c_del = st.columns([1, 2, 0.5])
            new_label = c_name.text_input(
                "Название кнопки" if lang == "RU" else "Button Name",
                value=label,
                key=f"lab_{label}",
            )
            new_text = c_text.text_area(
                "Текст шаблона" if lang == "RU" else "Template Text",
                value=text,
                key=f"txt_{label}",
                height=68,
            )
            if not c_del.button("🗑️", key=f"del_{label}"):
                updated_templates[new_label] = new_text

        st.divider()
        # Добавление нового
        st.write(
            "**Добавить новый шаблон:**" if lang == "RU" else "**Add new template:**"
        )
        add_col1, add_col2, add_col3 = st.columns([1, 2, 0.5])
        add_label = add_col1.text_input(
            "Название" if lang == "RU" else "Name",
            key="add_label",
            placeholder="Напр: API" if lang == "RU" else "e.g.: API",
        )
        add_text = add_col2.text_area(
            "Текст" if lang == "RU" else "Text",
            key="add_text",
            placeholder="Endpoint: ...",
        )

        if add_col3.button("➕", key="add_btn"):
            if add_label:
                updated_templates[add_label] = add_text
                save_templates(updated_templates)
                st.rerun()

        btn_save = (
            "💾 Сохранить все изменения шаблонов"
            if lang == "RU"
            else "💾 Save all template changes"
        )
        if st.button(btn_save, width='stretch'):
            save_templates(updated_templates)
            if logger:
                logger(
                    "Заметки: Конфигурация шаблонов обновлена"
                    if lang == "RU"
                    else "Notes: Template config updated"
                )
            st.rerun()

    st.divider()

    # --- ОСНОВНОЙ ИНТЕРФЕЙС ЗАМЕТОК ---
    col_list, col_edit = st.columns([1, 3])

    with col_list:
        st.write("### 📂 Списки" if lang == "RU" else "### 📂 Lists")
        current_file = st.radio(
            "Файл:" if lang == "RU" else "File:",
            existing_files,
            label_visibility="collapsed",
        )
        new_name = st.text_input(
            "Новый список:" if lang == "RU" else "New list:", key="new_file_input"
        )
        if st.button(
            "➕ Создать файл" if lang == "RU" else "➕ Create file",
            width='stretch',
        ):
            if new_name:
                with open(
                    os.path.join(NOTES_DIR, f"{new_name.strip()}.txt"),
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write("")
                st.rerun()

    with col_edit:
        file_path = os.path.join(NOTES_DIR, current_file)
        state_key = f"content_{current_file}"

        if state_key not in st.session_state:
            with open(file_path, "r", encoding="utf-8") as f:
                st.session_state[state_key] = f.read()

        # Динамические кнопки шаблонов
        st.write("### 🛠️ Быстрая вставка" if lang == "RU" else "### 🛠️ Quick Insert")
        # Располагаем кнопки в ряд по 3-4 штуки
        cols = st.columns(min(len(templates), 4) if templates else 1)
        for idx, (label, text) in enumerate(templates.items()):
            if cols[idx % len(cols)].button(label, width='stretch'):
                st.session_state[state_key] += f"\n\n{text}"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(st.session_state[state_key])
                st.rerun()

        # Редактор
        st.text_area(
            f"Правка: {current_file}" if lang == "RU" else f"Edit: {current_file}",
            height=400,
            key=state_key,
        )

        # Сохранение фона
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(st.session_state[state_key])

        if st.button(
            (
                f"🗑️ Удалить {current_file}"
                if lang == "RU"
                else f"🗑️ Delete {current_file}"
            ),
            type="secondary",
        ):
            if current_file != "General.txt":
                os.remove(file_path)
                if state_key in st.session_state:
                    del st.session_state[state_key]
                st.rerun()

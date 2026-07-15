import streamlit as st
import pandas as pd
import itertools
from datetime import datetime


def write_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if "log_history" not in st.session_state:
        st.session_state.log_history = []
    st.session_state.log_history.append(f"{timestamp} - {message}")


def get_pairwise_results(parameters):
    """Генерация попарных комбинаций (Pairwise)"""
    if not parameters:
        return []

    # Копируем список, чтобы не мутировать оригинал при сортировке
    params = sorted(parameters, key=len, reverse=True)

    # Инициализация с декартова произведения первых двух параметров
    pairs = list(itertools.product(params[0], params[1]))

    for i in range(2, len(params)):
        new_pairs = []
        current_param = params[i]
        for j, existing_row in enumerate(pairs):
            # Циклическое добавление значений нового параметра
            val = current_param[j % len(current_param)]
            new_pairs.append(existing_row + (val,))
        pairs = new_pairs

    return pairs


def render_matrix_lab():
    lang = st.session_state.get("lang", "RU")
    st.subheader(
        "📊 Конструктор тестовой матрицы"
        if lang == "RU"
        else "📊 Test Matrix Constructor"
    )

    col_param = "Параметр" if lang == "RU" else "Parameter"
    col_val = "Значения" if lang == "RU" else "Values"

    # 1. Инициализация данных в session_state, чтобы они не пропадали
    if (
        "matrix_df" not in st.session_state
        or col_param not in st.session_state.matrix_df.columns
    ):
        st.session_state.matrix_df = pd.DataFrame(
            [
                {
                    col_param: "Браузер" if lang == "RU" else "Browser",
                    col_val: "Chrome, Firefox, Safari",
                },
                {
                    col_param: "ОС" if lang == "RU" else "OS",
                    col_val: "Windows, MacOS, Linux",
                },
                {
                    col_param: "Роль" if lang == "RU" else "Role",
                    col_val: "Admin, User, Guest",
                },
            ]
            + [{col_param: "", col_val: ""} for _ in range(7)]
        )

    # 2. Перенос выбора метода в более удобное место (в колонки сверху)
    col_header, col_method = st.columns([2, 1])
    with col_header:
        st.write(
            "Введите параметры и значения через запятую:"
            if lang == "RU"
            else "Enter parameters and values separated by commas:"
        )
    with col_method:
        method = st.selectbox(
            "Метод генерации:" if lang == "RU" else "Generation method:",
            (
                ["Full Combinatorial (Все)", "Pairwise (Попарно)"]
                if lang == "RU"
                else ["Full Combinatorial (All)", "Pairwise"]
            ),
            label_visibility="collapsed",  # Скрываем текст, оставляем только выбор
        )

    # 3. Редактор данных с фиксом пропадания значений
    # Мы сохраняем результат в session_state напрямую через параметр key
    edited_df = st.data_editor(
        st.session_state.matrix_df,
        num_rows="dynamic",
        use_container_width=True,
        key="matrix_editor_widget",
    )

    # Обновляем наше состояние данных
    st.session_state.matrix_df = edited_df

    if st.button(
        "🚀 Сгенерировать сценарии" if lang == "RU" else "🚀 Generate Scenarios",
        width='stretch',
    ):
        write_log(f"Matrix: Generation started ({method})")

        # Очистка пустых строк
        clean_df = edited_df.dropna(subset=[col_param, col_val])
        clean_df = clean_df[clean_df[col_param].astype(str).str.strip() != ""]

        if clean_df.empty:
            st.error(
                "Добавьте параметры и значения!"
                if lang == "RU"
                else "Please add parameters and values!"
            )
            return

        all_labels = clean_df[col_param].tolist()
        all_values = [
            [v.strip() for v in str(row[col_val]).split(",") if v.strip()]
            for _, row in clean_df.iterrows()
        ]

        # Проверка на наличие значений
        if any(not v for v in all_values):
            st.error(
                "У каждого параметра должно быть хотя бы одно значение!"
                if lang == "RU"
                else "Each parameter must have at least one value!"
            )
            return

        # Логика генерации
        try:
            if "Full" in method:
                combinations = list(itertools.product(*all_values))
            else:
                combinations = get_pairwise_results(all_values)

            result_df = pd.DataFrame(combinations, columns=all_labels)
            result_df.insert(0, "✅", False)

            st.divider()
            st.success(
                f"Матрица построена: {len(result_df)} сценариев"
                if lang == "RU"
                else f"Matrix generated: {len(result_df)} scenarios"
            )

            # Отображение результата
            st.data_editor(
                result_df,
                use_container_width=True,
                key=f"result_table_{len(result_df)}",  # Уникальный ключ для таблицы результатов
            )

            write_log(f"Matrix: Success, {len(result_df)} cases generated")

        except Exception as e:
            st.error(
                f"Ошибка генерации: {e}" if lang == "RU" else f"Generation error: {e}"
            )
            write_log(f"Matrix ERROR: {str(e)}")

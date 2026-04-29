import streamlit as st
import pandas as pd
import random
from faker import Faker

# Инициализируем Faker с русской локализацией
fake = Faker(['ru_RU'])

# Полный список доступных полей, разбитый по категориям для логики генерации
DATA_MAPPING = {
    "ФИО": fake.name,
    "Телефон": fake.phone_number,
    "Email": fake.email,
    "Дата рождения": lambda: fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d'),
    "Адрес": fake.address,
    "Компания": fake.company,
    "Профессия": fake.job,
    "Страна/Город": lambda: f"{fake.country()}, {fake.city()}",
    "IPv4 адрес": fake.ipv4,
    "UUID v4": fake.uuid4,
    "User Agent": fake.user_agent,
    "MAC адрес": fake.mac_address,
    "Номер карты": fake.credit_card_number,
    "IBAN": fake.iban,
    "HEX Цвет": fake.hex_color,
    "Текст (Sentence)": fake.sentence,
    # Новые поля для расширения
    "ИНН": lambda: "".join([str(random.randint(0, 9)) for _ in range(12)]),
    "СНИЛС": lambda: "".join([str(random.randint(0, 9)) for _ in range(11)]),
    "Пароль": fake.password,
    "Логин": fake.user_name,
    "Координаты": lambda: f"{fake.latitude()}, {fake.longitude()}"
}

def render_data_generator():
    st.subheader("🧪 Генератор тестовых данных")

    # Организуем выбор полей в колонки, как на твоем скриншоте
    with st.expander("⚙️ Выбор полей для генерации", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        selected_fields = []
        
        with col1:
            st.markdown("**Личные данные**")
            for f in ["ФИО", "Телефон", "Email", "Дата рождения", "ИНН", "СНИЛС"]:
                if st.checkbox(f, key=f"gen_{f}"): selected_fields.append(f)
        
        with col2:
            st.markdown("**Локация/Работа**")
            for f in ["Адрес", "Компания", "Профессия", "Страна/Город", "Координаты"]:
                if st.checkbox(f, key=f"gen_{f}"): selected_fields.append(f)
                
        with col3:
            st.markdown("**IT/Технические**")
            for f in ["IPv4 адрес", "UUID v4", "User Agent", "MAC адрес", "Логин", "Пароль"]:
                if st.checkbox(f, key=f"gen_{f}"): selected_fields.append(f)
                
        with col4:
            st.markdown("**Финансы/Прочее**")
            for f in ["Номер карты", "IBAN", "HEX Цвет", "Текст (Sentence)"]:
                if st.checkbox(f, key=f"gen_{f}"): selected_fields.append(f)

    # Настройки количества и формата
    with st.container(border=True):
        c_count, c_form = st.columns(2)
        num_rows = c_count.number_input("Количество строк:", min_value=1, max_value=5000, value=10)
        out_format = c_form.selectbox("Формат:", ["Таблица", "JSON", "CSV"])

    if st.button("🚀 Сгенерировать данные", use_container_width=True):
        if not selected_fields:
            st.error("Выберите хотя бы одно поле!")
            return

        data = []
        for _ in range(num_rows):
            row = {field: DATA_MAPPING[field]() if callable(DATA_MAPPING[field]) else DATA_MAPPING[field] for field in selected_fields}
            data.append(row)
        
        df = pd.DataFrame(data)

        if out_format == "Таблица":
            st.dataframe(df, use_container_width=True)
        elif out_format == "JSON":
            st.code(df.to_json(orient="records", force_ascii=False, indent=4), language="json")
        else:
            st.code(df.to_csv(index=False), language="text")
        
        # Кнопка скачивания CSV всегда полезна
        st.download_button(
            "📥 Скачать результат (CSV)",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name="test_data.csv",
            mime="text/csv"
        )
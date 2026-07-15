import streamlit as st
import pandas as pd
import random
from faker import Faker
from modules.i18n import get_text

# Инициализируем Faker с русской локализацией
fake = Faker(['ru_RU'])

def generate_inn():
    """Генерирует валидный 12-значный ИНН для физлица."""
    digits = [random.randint(0, 9) for _ in range(10)]
    
    # Расчет 11-й цифры (первая контрольная сумма)
    coeffs1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum1 = sum(d * c for d, c in zip(digits, coeffs1)) % 11 % 10
    digits.append(checksum1)
    
    # Расчет 12-й цифры (вторая контрольная сумма)
    coeffs2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    checksum2 = sum(d * c for d, c in zip(digits, coeffs2)) % 11 % 10
    digits.append(checksum2)
    
    return "".join(map(str, digits))

def generate_snils():
    """Генерирует валидный СНИЛС с правильной контрольной суммой."""
    base_digits = [random.randint(0, 9) for _ in range(9)]
    if sum(base_digits) == 0: base_digits[0] = 1 # СНИЛС не может быть из одних нулей

    coeffs = list(range(9, 0, -1))
    checksum_val = sum(d * c for d, c in zip(base_digits, coeffs))

    if checksum_val < 100:
        control = checksum_val
    elif checksum_val in [100, 101]:
        control = 0
    else: # > 101
        control = checksum_val % 101
        if control == 100: control = 0
    
    return f"{''.join(map(str, base_digits))}{control:02d}"

# Полный список доступных полей, разбитый по категориям для логики генерации
# Ключи теперь language-agnostic для поддержки i18n
DATA_MAPPING = {
    "full_name": {"func": fake.name, "category": "personal"},
    "phone": {"func": fake.phone_number, "category": "personal"},
    "email": {"func": fake.email, "category": "personal"},
    "birthdate": {"func": lambda: fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d'), "category": "personal"},
    "inn": {"func": generate_inn, "category": "personal"},
    "snils": {"func": generate_snils, "category": "personal"},
    "address": {"func": fake.address, "category": "location"},
    "company": {"func": fake.company, "category": "location"},
    "job": {"func": fake.job, "category": "location"},
    "country_city": {"func": lambda: f"{fake.country()}, {fake.city()}", "category": "location"},
    "coordinates": {"func": lambda: f"{fake.latitude()}, {fake.longitude()}", "category": "location"},
    "ipv4": {"func": fake.ipv4, "category": "tech"},
    "uuid4": {"func": fake.uuid4, "category": "tech"},
    "user_agent": {"func": fake.user_agent, "category": "tech"},
    "mac_address": {"func": fake.mac_address, "category": "tech"},
    "login": {"func": fake.user_name, "category": "tech"},
    "password": {"func": fake.password, "category": "tech"},
    "card_number": {"func": fake.credit_card_number, "category": "finance"},
    "iban": {"func": fake.iban, "category": "finance"},
    "hex_color": {"func": fake.hex_color, "category": "finance"},
    "sentence": {"func": fake.sentence, "category": "finance"},
}

def render_data_generator():
    t = get_text
    st.subheader(t("data_gen_header"))

    # Организуем выбор полей в колонки, как на твоем скриншоте
    with st.expander(t("data_gen_fields_expander"), expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        cols_map = {"personal": col1, "location": col2, "tech": col3, "finance": col4}
        cats_rendered = set()

        selected_fields = []

        for key, details in DATA_MAPPING.items():
            category = details["category"]
            column = cols_map[category]
            if category not in cats_rendered:
                with column:
                    st.markdown(f"**{t(f'data_gen_cat_{category}')}**")
                cats_rendered.add(category)
            
            with column:
                if st.checkbox(t(f"data_gen_field_{key}"), key=f"gen_{key}"):
                    selected_fields.append(key)

    # Настройки количества и формата
    with st.container(border=True):
        c_count, c_form = st.columns(2)
        num_rows = c_count.number_input(t("data_gen_rows_label"), min_value=1, max_value=5000, value=10)
        out_format = c_form.selectbox(t("data_gen_format_label"), [t("data_gen_format_table"), "JSON", "CSV"])

    if st.button(t("data_gen_button_generate"), width='stretch'):
        if not selected_fields:
            st.error(t("data_gen_error_no_fields"))
            return

        with st.spinner(t("data_gen_spinner")):
            data = []
            for _ in range(num_rows):
                row = {}
                for field_key in selected_fields:
                    # Получаем отображаемое имя для колонки
                    display_name = t(f"data_gen_field_{field_key}")
                    # Вызываем функцию генерации
                    row[display_name] = DATA_MAPPING[field_key]["func"]()
                data.append(row)
            
            df = pd.DataFrame(data)

        if out_format == t("data_gen_format_table"):
            st.dataframe(df, use_container_width=True)
        elif out_format == "JSON":
            st.code(df.to_json(orient="records", force_ascii=False, indent=4), language="json")
        else:
            st.code(df.to_csv(index=False), language="text")
        
        # Кнопка скачивания CSV всегда полезна
        st.download_button(
            t("data_gen_button_download"),
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name="test_data.csv",
            mime="text/csv"
        )
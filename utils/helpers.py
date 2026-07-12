import secrets

def fill_raw_bytes(f, num_bytes_to_add):
    """
    Заполняет файл указанным количеством случайных байтов чанками по 1МБ.
    Эта функция дописывает данные в конец файла.
    """
    chunk = 1024 * 1024
    if num_bytes_to_add <= 0:
        return

    remaining = num_bytes_to_add
    while remaining > 0:
        bytes_to_write = min(chunk, remaining)
        f.write(secrets.token_bytes(bytes_to_write))
        remaining -= bytes_to_write

def get_multiplier(unit):
    """Возвращает множитель для перевода в байты"""
    return {"KB": 1024, "MB": 1024**2, "GB": 1024**3}.get(unit, 1024**2)
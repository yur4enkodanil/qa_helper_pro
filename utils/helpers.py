import secrets

def fill_raw_bytes(f, target_bytes):
    """Заполняет файл случайными байтами чанками по 1МБ"""
    current_pos = f.tell()
    remaining = target_bytes - current_pos
    chunk = 1024 * 1024
    if remaining > 0:
        for _ in range(remaining // chunk):
            f.write(secrets.token_bytes(chunk))
        f.write(secrets.token_bytes(remaining % chunk))

def get_multiplier(unit):
    """Возвращает множитель для перевода в байты"""
    return {"KB": 1024, "MB": 1024**2, "GB": 1024**3}.get(unit, 1024**2)
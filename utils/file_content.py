# -*- coding: utf-8 -*-
import os
import base64
import logging

"""
Централизованное хранилище валидного контента для генерации файлов.
Скрипт автоматически создает и использует файлы-шаблоны из папки file_templates.
"""

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Словарь с base64-строками для первоначального создания файлов-шаблонов.
# Эти данные используются только один раз, если файлы в папке file_templates отсутствуют.
VALID_FILE_TEMPLATES_B64 = {
    # --- Изображения ---
    'png': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=', # 1x1 red png
    'jpg': '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', # 1x1 black jpg
    'gif': 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7', # 1x1 transparent gif
    'bmp': 'Qk1CAAAAAAAAAD4AAAAoAAAAAQAAAAEAAAABAAEAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAA==', # 1x1 24-bit bmp
    'webp': 'UklGRhoAAABXRUJQVlA4TA0AAAAvAAAAEAcQERGIiP4HAA==', # 1x1 transparent lossy webp
    'svg': 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxIiBoZWlnaHQ9IjEiPjwvc3ZnPg==', # 1x1 empty svg
    'avif': 'AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxAAAAAG1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAG1kaXJhcHByAAAAAAAAAAAAAAAAAAAAADxwaXRtAAAAAAABAAAAImlsb2MAAAAAREAAAQABAAAAAAEOAAEAAAAAAAAANgAAACNpaW5mAAAAAAABAAAAFWluZmUCAAAAAAABAGF2MDFJbWFnZQAAAB5pcHJwAAAAU2lwY28AAAAUaXNwZQAAAAAAAAABAAAAAQAAABBwaXhpAAAAAAMICAgAAAAAGGlwbWEAAAAAAAAAQABYGCA4QAAABsbWRhdAAAAAAAAAAGgAARAEIAgQkeyJ/3w==', # 1x1 black avif

    # --- Аудио ---
    'mp3': 'SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==', # Empty ID3v2 tag
    'wav': 'UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABgAAABkYXRhAgAA', # Short silent wav,
    'ogg': 'T2dnUwACAAAAAAAAAAABAAAAAMLZ9wEAAAAA/w8AAAAAb3B1c0hlYWQAAAAACAEAAAAAAACoAAAAAABPZ2dTAAAAAAAAAAAAAAEAAAAAwtb3AQAAAAEBCgACAAAAAG9wdXNUYWdzAQAAABMAAAAVZW5jb2Rlcj1vcmdjLXBjbi0xLjMAAAAA', # Short silent ogg
    # --- Видео ---
    'mp4': 'AAAAFGZ0eXBNU05WAAACAVNvbmEgTlYgAAAAAA5tZGF0', # Minimal mp4
    'mov': 'AAAAGGZ0eXpxdCAgAAAAAG1kYXQ=', # Minimal mov
    'mkv': 'GkXfH4xtAABpbnZgQEuYhEEAnQAAEU2hAQ==', # Minimal mkv

    # --- Документы и текст ---
    'pdf': 'JVBERi0xLjAKMSAwIG9iago8PAo+PgplbmRvYmoKdHJhaWxlcgo8PAovUm9vdCAxIDAgUgo+PgolJUVPRg==', # Empty PDF
    'html': 'PCFET0NUWVBFIGh0bWw+PGh0bWw+PGhlYWQ+PC9oZWFkPjxib2R5PjwvYm9keT48L2h0bWw+', # Empty HTML5
    'java': 'Y2xhc3MgSGVsbG9Xb3JsZCB7IHB1YmxpYyBzdGF0aWMgdm9pZCBtYWluKFN0cmluZ1tdIGFyZ3MpIHsgU3lzdGVtLm91dC5wcmludGxuKCJIZWxsbyBmcm9tIFFBIEhlbHBlciBQcm8iKTsgfSB9',
    'xml': 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPG5vdGU+CiAgPGZyb20+UUEgSGVscGVyPC9mcm9tPgo8L25vdGU+Cg==',
    'drawio': 'PG14ZmlsZT48ZGlhZ3JhbT5Wc25WbWpEWlJ2VnFhV3hmY2pveU1pMHhLdz09PC9kaWFncmFtPjwvbXhmaWxlPg==', # Empty drawio
    'gltf': 'ewogICAgImFzc2V0IjogewogICAgICAgICJ2ZXJzaW9uIjogIjIuMCIKICAgIH0KfQ==', # Minimal gltf

    # --- Архивы и Office ---
    'zip': 'UEsDBAoAAAAAAAC1jVdTAAAAAAAAAAAAAAAAAwAAAGVtcC9QSwECPwAKAAAAAAAAtY1XUwAAAAAAAAAAAAAAAAUAAAAAAAAAAAAgAAAAAAAAAGVtcC9QSwUGAAAAAAEAAQA1AAAAbAAAAAAA', # Empty zip with empty folder
    'doc': '0M8R4KGxGuEAAAAAAAAAAAAAAAAAAAAAPgADAP7/CQAGAAAAAAAAAAAAAAABAAAAAgAAAAAAAAAAEAAA', # Minimal OLE

    # --- 3D и CAD ---
    'glb': 'Z2xURgIAAAAuAAAAZ2xURgIAAAAAAAAAAAAAAEpTT057ImFzc2V0Ijp7InZlcnNpb24iOiIyLjAifX0gQklOAAE=', # Minimal glb
    'ifc': 'SVNPLTEwMzAzLTIxO0hFQURFUiY7RU5ESEUgREVTO0RBVEEmO0VORA1EU0VDO0VORA1JU08tMTAzMDMtMjE7', # Minimal ifc
}

# Глобальный словарь для хранения содержимого файлов
VALID_FILE_CONTENT = {}

def bootstrap_templates():
    """
    Создает директорию file_templates и наполняет ее файлами-шаблонами,
    декодируя их из VALID_FILE_TEMPLATES_B64.
    Файлы создаются только если они отсутствуют.
    """
    base_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(base_dir, 'file_templates')

    if not os.path.isdir(templates_dir):
        try:
            os.makedirs(templates_dir)
            logger.info(f"Создана директория для шаблонов: {templates_dir}")
        except OSError as e:
            logger.error(f"Не удалось создать директорию {templates_dir}: {e}")
            return

    for ext, content_b64 in VALID_FILE_TEMPLATES_B64.items():
        template_path = os.path.join(templates_dir, f"template.{ext}")
        if not os.path.exists(template_path):
            try:
                content_bytes = base64.b64decode(content_b64)
                with open(template_path, 'wb') as f:
                    f.write(content_bytes)
                logger.info(f"Создан файл-шаблон: {template_path}")
            except Exception as e:
                logger.error(f"Не удалось создать файл-шаблон для '{ext}': {e}")

def load_templates_from_disk():
    """
    Загружает все файлы-шаблоны из директории file_templates.
    Имя файла должно быть в формате 'template.{ext}'.
    """
    global VALID_FILE_CONTENT
    templates_dir = os.path.join(os.path.dirname(__file__), 'file_templates')

    if not os.path.isdir(templates_dir):
        logger.warning(f"Директория с шаблонами не найдена: {templates_dir}. Генерация бинарных файлов будет недоступна.")
        return

    for filename in os.listdir(templates_dir):
        filepath = os.path.join(templates_dir, filename)
        if os.path.isfile(filepath):
            parts = filename.split('.')
            if len(parts) == 2 and parts[0] == 'template':
                ext = parts[1].lower()
                try:
                    with open(filepath, 'rb') as f:
                        VALID_FILE_CONTENT[ext] = f.read()
                    logger.info(f"Загружен шаблон для '{ext}'")
                except Exception as e:
                    logger.error(f"Ошибка при чтении шаблона {filepath}: {e}")

# Добавляем простые текстовые форматы, которые не требуют отдельных файлов
VALID_FILE_CONTENT['txt'] = b'This is a test file from QA Helper Pro.'
VALID_FILE_CONTENT['csv'] = b'id,name,value\n1,test,100'
VALID_FILE_CONTENT['bas'] = b'10 PRINT "HELLO FROM QA HELPER PRO"\n20 GOTO 10'
VALID_FILE_CONTENT['js'] = b'console.log("Hello from QA Helper Pro");'
VALID_FILE_CONTENT['json'] = b'{ "hello": "world" }'

def setup_aliases():
    """
    Настраивает псевдонимы для форматов, использующих общие шаблоны.
    """
    aliases = {
        'apng': 'png',
        'oga': 'ogg',
        'opus': 'ogg',
        'ogv': 'ogg',
        'm4v': 'mp4',
        'webm': 'mkv',
        'jpeg': 'jpg',
    }
    for alias, source in aliases.items():
        if source in VALID_FILE_CONTENT and alias not in VALID_FILE_CONTENT:
            VALID_FILE_CONTENT[alias] = VALID_FILE_CONTENT[source]

    # Форматы на базе ZIP
    if 'zip' in VALID_FILE_CONTENT:
        for ext in ['docx', 'xlsx', 'pptx', 'vsdx', 'ods']:
            if ext not in VALID_FILE_CONTENT:
                VALID_FILE_CONTENT[ext] = VALID_FILE_CONTENT['zip']
    
    # Форматы на базе OLE
    if 'doc' in VALID_FILE_CONTENT:
        for ext in ['xls', 'ppt', 'vsd']:
            if ext not in VALID_FILE_CONTENT:
                VALID_FILE_CONTENT[ext] = VALID_FILE_CONTENT['doc']

# --- ОСНОВНАЯ ЛОГИКА ПРИ ИМПОРТЕ ---

# 1. Создаем файлы-шаблоны из base64, если их нет
bootstrap_templates()

# 2. Загружаем созданные (или уже существующие) шаблоны из файлов
load_templates_from_disk()

# 3. Настраиваем псевдонимы для расширений
setup_aliases()

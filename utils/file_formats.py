# -*- coding: utf-8 -*-

"""
Централизованное хранилище информации о файловых форматах.
"""

# Полная база сигнатур (магических байт) для различных форматов файлов.
MAGIC_BYTES = {
    # Office (Modern - ZIP based)
    'docx': b'\x50\x4B\x03\x04', 'xlsx': b'\x50\x4B\x03\x04', 'pptx': b'\x50\x4B\x03\x04',
    'vsdx': b'\x50\x4B\x03\x04', 'ods': b'\x50\x4B\x03\x04',

    # Office (Legacy - OLE)
    'doc': b'\xD0\xCF\x11\xE0', 'xls': b'\xD0\xCF\x11\xE0', 'ppt': b'\xD0\xCF\x11\xE0',
    'vsd': b'\xD0\xCF\x11\xE0',

    # Documents & Text
    'pdf': b'%PDF-1.4\n', 'txt': b'', 'csv': b'', 'js': b'', 'java': b'', 'bas': b'',
    'gltf': b'{', 'drawio': b'<mxfile>', 'ifc': b'ISO-10303-21;',

    # Images
    'png': b'\x89PNG\r\n\x1a\n', 'apng': b'\x89PNG\r\n\x1a\n',
    'jpg': b'\xff\xd8\xff\xe0', 'jpeg': b'\xff\xd8\xff\xe0',
    'gif': b'GIF89a', 'bmp': b'BM',
    'tif': b'II*\x00', 'tiff': b'II*\x00', 'geo-tiff': b'II*\x00',
    'webp': b'RIFF\x00\x00\x00\x00WEBP', 'avif': b'\x00\x00\x00 ftypavif',
    'svg': b'<?xml',

    # Audio
    'mp3': b'ID3', 'wav': b'RIFF\x00\x00\x00\x00WAVE', 'flac': b'fLaC',
    'aac': b'\xFF\xF1', 'm4a': b'\x00\x00\x00\x18ftypM4A ',
    'ogg': b'OggS', 'oga': b'OggS', 'opus': b'OggS',

    # Video
    'mp4': b'\x00\x00\x00\x18ftypmp42', 'm4v': b'\x00\x00\x00\x18ftypmp42',
    'mov': b'\x00\x00\x00\x08ftypqt  ',
    'webm': b'\x1aE\xdf\xa3', 'mkv': b'\x1aE\xdf\xa3',
    'ogv': b'OggS',

    # Archives
    'zip': b'\x50\x4B\x03\x04', '7z': b'7z\xbc\xaf\x27\x1c', 'rar': b'Rar!\x1a\x07',

    # 3D & CAD
    'glb': b'glTF\x02\x00\x00\x00',

    # GIS & Scientific
    'grd': b'DSAA', 'shp': b'\x00\x00\x27\x0a', 'las': b'LASF',
    'dlis': b'\x00\x00\x00\x50', 'seg-y': b'\x00\x00\x00\x00', 'lis': b'\x00\x00',
}

# Полный список всех расширений для UI
ALL_EXTENSIONS = sorted(list(MAGIC_BYTES.keys()) + ["bin", "dat", "exe", "tmp", "log", "cst", "roff", "unrst", "egrid"])
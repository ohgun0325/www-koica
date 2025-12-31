# -*- coding: utf-8 -*-
"""
유틸리티 함수 모듈
"""

import json
import os


def read_json(filename):
    """JSON 파일 읽기"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(data, filename):
    """JSON 파일 쓰기"""
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_txt(filename):
    """텍스트 파일 읽기"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def write_txt(data, filename):
    """텍스트 파일 쓰기"""
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)


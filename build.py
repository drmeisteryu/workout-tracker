#!/usr/bin/env python3
"""운동기록 앱 빌드: _template.html + seed JSON + Supabase 설정 → index.html
사용법: python3 build.py
Supabase 키가 있으면 supabase.config.json 에 {"url":"...","anon":"..."} 형태로 두면 자동 주입됨.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def p(name): return os.path.join(HERE, name)

prog = json.load(open(p('program_seed.json'), encoding='utf-8'))
hist = json.load(open(p('history_seed.json'), encoding='utf-8'))
mus  = json.load(open(p('muscle_seed.json'),  encoding='utf-8'))
tpl  = open(p('_template.html'), encoding='utf-8').read()

# Supabase config (optional)
url, anon = '', ''
cfg_path = p('supabase.config.json')
if os.path.exists(cfg_path):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    url, anon = cfg.get('url', ''), cfg.get('anon', '')

def mini(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':'))

out = (tpl
    .replace('__PROGRAM__', mini(prog))
    .replace('__HISTORY__', mini(hist))
    .replace('__MUSCLE__',  mini(mus))
    .replace('__SUPABASE_URL__', url)
    .replace('__SUPABASE_ANON__', anon))

left = sum(out.count(t) for t in ('__PROGRAM__','__HISTORY__','__MUSCLE__'))
open(p('index.html'), 'w', encoding='utf-8').write(out)
print(f'built index.html: {len(out)} bytes; cloud={"ON" if url else "OFF (local mode)"}; placeholders left={left}')

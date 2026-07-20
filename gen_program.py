# -*- coding: utf-8 -*-
"""3분할(A/B/C) 롤링 12주 × 주4회 프로그램 생성 → program_seed.json"""
import json

def s(reps, rpe, load):
    return {"reps": str(reps), "rpe": rpe, "load": load}

# ── 종목 정의: (이름, 세트수키, 반복, 기본중량, 주간증가) ────────────────
# base = W1 중량, step = 2주마다 증가폭 (머신은 앱이 실기록으로 자동조정)
A_MAIN = ("Flat Dumbbell Press", 10, 14, 2)      # 프리(덤벨) 한손
A_EX = [
    ("Flat Machine Press", 12, 30, 2.5),
    ("Machine Shoulder Press", 12, 20, 2.5),
    ("Dumbbell Side Lateral Raise", 15, 5, 1),
    ("Cable Push Down", 15, 15, 2.5),
]
A_EXTRA = ("Chest Fly", 15, 20, 2.5)             # W5부터 추가

B_MAIN = ("Bent Over Barbell Row", 10, 30, 2.5)  # 프리(바벨)
B_EX = [
    ("Lat Pull-Down", 12, 40, 2.5),
    ("Seated Cable Row", 12, 35, 2.5),
    ("Rear Delt Fly", 15, 15, 2.5),
    ("Machine Curl", 15, 15, 2.5),
]
B_EXTRA = ("Chest Supported Row", 12, 30, 2.5)

C_MAIN = ("Goblet Squat", 12, 16, 2)             # 프리(덤벨)
C_EX = [
    ("Leg Press", 12, 60, 5),
    ("Leg Extension", 15, 25, 2.5),
    ("Lying Leg Curl", 15, 25, 2.5),
    ("Back Extension", 15, "BW", 0),             # 힙쓰러스트 대체
]
C_EXTRA = ("Machine Abs", 15, 20, 2.5)

WARM = {
 "A": [("동적 스트레칭 / 폼롤러", "5분"), ("Band Pull-Apart", "15"), ("Push-Up", "10")],
 "B": [("동적 스트레칭 / 폼롤러", "5분"), ("Cat-Camel", "10"), ("Band Pull-Apart", "15")],
 "C": [("동적 스트레칭 / 폼롤러", "5분"), ("Glute Bridge", "15"), ("BW Squat", "10")],
}
TITLE = {"A": "A · 가슴·어깨·삼두 Push", "B": "B · 등·이두 Pull", "C": "C · 하체·코어"}

def phase(w):
    if w <= 4:  return dict(name="적응기", main_sets=3, ex_sets=2, extra=False, rpe_m="@6~7", rpe_e="@7", mult=1.00)
    if w <= 8:  return dict(name="볼륨 축적", main_sets=3, ex_sets=3, extra=True,  rpe_m="@7",   rpe_e="@7", mult=1.00)
    if w <= 11: return dict(name="강도 진행", main_sets=3, ex_sets=3, extra=True,  rpe_m="@7~8", rpe_e="@7~8", mult=1.00)
    return dict(name="마무리 · 재측정", main_sets=2, ex_sets=2, extra=False, rpe_m="@6", rpe_e="@6", mult=0.85)

def load_at(base, step, w, mult):
    if base == "BW": return "BW"
    v = base + step * ((w - 1) // 2)      # 2주마다 1스텝
    v = v * mult
    return round(v * 2) / 2               # 0.5 단위 정리

def build_day(letter, w, dlabel):
    p = phase(w)
    exs = []
    for nm, reps in WARM[letter]:
        exs.append({"name": nm, "type": "warmup", "sets": [s(reps, None, "BW" if reps != "5분" else "-")]})
    main, ex_list, extra = {"A": (A_MAIN, A_EX, A_EXTRA), "B": (B_MAIN, B_EX, B_EXTRA),
                            "C": (C_MAIN, C_EX, C_EXTRA)}[letter]
    nm, reps, base, step = main
    exs.append({"name": nm, "type": "work",
                "sets": [s(reps, p["rpe_m"], load_at(base, step, w, p["mult"])) for _ in range(p["main_sets"])]})
    items = list(ex_list) + ([extra] if p["extra"] else [])
    for nm, reps, base, step in items:
        exs.append({"name": nm, "type": "work",
                    "sets": [s(reps, p["rpe_e"], load_at(base, step, w, p["mult"])) for _ in range(p["ex_sets"])]})
    exs.append({"name": "정적 스트레칭", "type": "cooldown", "sets": [s("5분", None, "-")]})
    return {"label": dlabel, "exercises": exs}

weeks, k = [], 0
cnt = {"A": 0, "B": 0, "C": 0}
for w in range(1, 13):
    p = phase(w)
    days = []
    for d in range(1, 5):
        letter = "ABC"[k % 3]; k += 1
        cnt[letter] += 1
        sid = f"{letter}{cnt[letter]}"          # 고유 세션 id: A1, B1, C1, A2...
        days.append(build_day(letter, w, f"{sid} ({TITLE[letter]})"))
    weeks.append({"id": f"W{w}", "title": f"{w}주 · {p['name']}", "days": days})

json.dump({"weeks": weeks}, open("program_seed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = sum(len(x["days"]) for x in weeks)
print(f"생성 완료: {len(weeks)}주 / {tot}세션")
d0 = weeks[0]["days"][0]
print("W1D1:", d0["label"])
for e in d0["exercises"]:
    if e["type"] == "work":
        print(f"  - {e['name']:30s} {len(e['sets'])}세트 x {e['sets'][0]['reps']} {e['sets'][0]['rpe']} @ {e['sets'][0]['load']}")

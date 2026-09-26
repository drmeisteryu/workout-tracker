# -*- coding: utf-8 -*-
"""벌크업 상/하체 2분할 16주 × 주4회 프로그램 생성 → program_seed.json

구성: 상체A(가슴·등) / 하체A(스쿼트) / 상체B(어깨·팔) / 하체B(힙힌지)
      → 부위마다 주 2회 자극. 권장 요일: 월·화·목·금
시간: 스트레칭·유산소 제외 웨이트만 세션당 60분 이내(est 필드로 검증)
"""
import json

def s(reps, rpe, load):
    return {"reps": str(reps), "rpe": rpe, "load": load}

# ── 종목: (이름, 종류, W1 중량, 주당 증가, 반올림 단위) ─────────────────────
# 종류: main(메인 복합) / comp(보조 복합) / iso(고립)
# 계획 중량은 출발점일 뿐, 앱이 실제 기록(반복·RPE)으로 다음 중량을 자동 추천한다.
DAYS = {
    "UA": ("상체 A · 가슴·등", "upper", [
        ("Flat Bench Press",            "main", 30, 1.25, 2.5),
        ("Bent Over Barbell Row",       "comp", 30, 1.25, 2.5),
        ("Lat Pull-Down",               "comp", 35, 1.25, 2.5),
        ("Machine Shoulder Press",      "comp", 20, 1.25, 2.5),
        ("Dumbbell Side Lateral Raise", "iso",   5, 0.5,  1),
        ("Cable Push Down",             "iso",  15, 1.25, 2.5),
    ]),
    "LA": ("하체 A · 스쿼트", "lower", [
        ("Barbell Back Squat",   "main", 35, 2.5,  2.5),
        ("Leg Press",            "comp", 60, 5,    5),
        ("Lying Leg Curl",       "iso",  25, 1.25, 2.5),
        ("Leg Extension",        "iso",  25, 1.25, 2.5),
        ("Standing Calf Raise",  "iso",  30, 2.5,  2.5),
        ("Cable Crunch",         "iso",  20, 1.25, 2.5),
    ]),
    "UB": ("상체 B · 어깨·팔", "upper", [
        ("Incline Dumbbell Press",     "main", 12, 0.5,  1),
        ("Seated Cable Row",           "comp", 35, 1.25, 2.5),
        ("Dumbbell Shoulder Press",    "comp", 10, 0.5,  1),
        ("Dumbbell Curl",              "iso",   8, 0.5,  1),
        ("Overhead Triceps Extension", "iso",  15, 1.25, 2.5),
        ("Rear Delt Fly",              "iso",  15, 1.25, 2.5),
    ]),
    "LB": ("하체 B · 힙힌지", "lower", [
        ("Romanian Deadlift",     "main", 40, 2.5,  2.5),
        ("Bulgarian Split Squat", "comp",  6, 0.5,  1),
        ("Hip Thruster",          "comp", 40, 2.5,  2.5),
        ("Seated Leg Curl",       "iso",  25, 1.25, 2.5),
        ("Standing Calf Raise",   "iso",  30, 2.5,  2.5),
        ("Machine Abs",           "iso",  20, 1.25, 2.5),
    ]),
}
ORDER = ["UA", "LA", "UB", "LB"]
REST = {"main": "휴식 2~3분", "comp": "휴식 90초~2분", "iso": "휴식 60~90초"}
# 세트당 소요(수행+휴식, 분). 편측 운동은 양쪽이라 더 길다.
MIN_PER_SET = {"main": 3.5, "comp": 2.75, "iso": 2.0}
UNILATERAL = {"Bulgarian Split Squat": 3.5}
RAMP_MIN = 4  # 메인 종목 준비세트(빈 바 → 50% → 75%)

WARM = {
    "upper": [("동적 스트레칭 / 폼롤러", "5분"), ("Band Pull-Apart", "15"), ("Push-Up", "10")],
    "lower": [("동적 스트레칭 / 폼롤러", "5분"), ("Glute Bridge", "15"), ("BW Squat", "10")],
}
CARDIO = ("유산소 (선택) · 인클라인 걷기 / 실내자전거", "20분",
          "대화 가능한 강도(존2). 체중이 주 0.5kg 넘게 늘 때만 주 2회 추가")

def phase(w):
    """주차별 단계. n_ex: 종목 수, sets: 종류별 세트, reps/rpe: 종류별 목표, mult: 중량 배수"""
    if w <= 2:
        return dict(name="재적응", n_ex=5, sets=dict(main=2, comp=2, iso=2),
                    reps=dict(main=8, comp=10, iso=12), rpe=dict(main="@6", comp="@6", iso="@6"), mult=1.0)
    if w <= 4:
        return dict(name="적응", n_ex=6, sets=dict(main=3, comp=2, iso=2),
                    reps=dict(main=8, comp=10, iso=12), rpe=dict(main="@7", comp="@7", iso="@7"), mult=1.0)
    if w <= 8:
        return dict(name="벌크 볼륨 1", n_ex=6, sets=dict(main=3, comp=3, iso=3),
                    reps=dict(main=8, comp=10, iso=12), rpe=dict(main="@7~8", comp="@8", iso="@8"), mult=1.0)
    if w == 9:
        return dict(name="디로드", n_ex=6, sets=dict(main=2, comp=2, iso=2),
                    reps=dict(main=8, comp=10, iso=12), rpe=dict(main="@6", comp="@6", iso="@6"), mult=0.9)
    if w <= 13:
        return dict(name="벌크 볼륨 2", n_ex=6, sets=dict(main=4, comp=3, iso=3),
                    reps=dict(main=8, comp=10, iso=12), rpe=dict(main="@8", comp="@8", iso="@8"), mult=1.0)
    if w <= 15:
        return dict(name="강도 진행", n_ex=6, sets=dict(main=4, comp=3, iso=3),
                    reps=dict(main=6, comp=8, iso=12), rpe=dict(main="@8~9", comp="@8", iso="@8~9"), mult=1.05)
    return dict(name="디로드 · 재측정", n_ex=6, sets=dict(main=3, comp=2, iso=2),
                reps=dict(main=5, comp=10, iso=12), rpe=dict(main="@7", comp="@6", iso="@6"), mult=1.0)

def prog_weeks(w):
    """진행 주 수: 디로드 주는 증량하지 않는다 (W9 = W8 중량 유지)."""
    return w - 1 if w <= 8 else (7 if w == 9 else w - 2)

def load_at(base, step, grid, w, mult):
    v = (base + step * prog_weeks(w)) * mult
    return round(round(v / grid) * grid, 2)

def build_day(key, w, n):
    title, kind, exs_def = DAYS[key]
    p = phase(w)
    exs = [{"name": nm, "type": "warmup", "sets": [s(r, None, "BW" if r != "5분" else "-")]}
           for nm, r in WARM[kind]]
    exs.append({"name": "메인 준비세트", "type": "warmup",
                "sets": [s("빈 바×10 → 50%×5 → 75%×3", None, "-")]})
    est = RAMP_MIN
    for nm, k, base, step, grid in exs_def[:p["n_ex"]]:
        lw, mult = w, p["mult"]
        if w == 16:  # 재측정 주: 메인은 W15 중량으로 5회 확인, 나머지는 W15의 90%로 가볍게
            lw, mult = 15, (phase(15)["mult"] if k == "main" else 0.9)
        n_sets = p["sets"][k]
        est += n_sets * UNILATERAL.get(nm, MIN_PER_SET[k])
        exs.append({"name": nm, "type": "work", "note": REST[k] + (" · 한쪽씩" if nm in UNILATERAL else ""),
                    "sets": [s(p["reps"][k], p["rpe"][k], load_at(base, step, grid, lw, mult))
                             for _ in range(n_sets)]})
    exs.append({"name": CARDIO[0], "type": "cardio", "note": CARDIO[2], "sets": [s(CARDIO[1], None, "-")]})
    exs.append({"name": "정적 스트레칭", "type": "cooldown", "sets": [s("5분", None, "-")]})
    sid = f"{key}{n}"                     # 고유 세션 id: UA1, LA1, UB1, LB1, UA2 ...
    return {"label": f"{sid} ({title})", "est": round(est), "exercises": exs}

weeks = []
for w in range(1, 17):
    p = phase(w)
    weeks.append({"id": f"W{w}", "title": f"{w}주 · {p['name']}",
                  "days": [build_day(key, w, w) for key in ORDER]})

if __name__ == "__main__":
    json.dump({"weeks": weeks}, open("program_seed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot = sum(len(x["days"]) for x in weeks)
    print(f"생성 완료: {len(weeks)}주 / {tot}세션")
    worst = max((d["est"], d["label"], wk["id"]) for wk in weeks for d in wk["days"])
    print(f"최장 세션(웨이트만): {worst[0]}분 — {worst[2]} {worst[1]}")
    assert worst[0] <= 60, "세션이 60분을 넘습니다"
    for wk in (weeks[0], weeks[9], weeks[14]):
        d0 = wk["days"][0]
        print(f"{wk['title']} · {d0['label']} · 약 {d0['est']}분")
        for e in d0["exercises"]:
            if e["type"] == "work":
                st = e["sets"][0]
                print(f"  - {e['name']:28s} {len(e['sets'])}세트 x {st['reps']} {st['rpe']} @ {st['load']}")

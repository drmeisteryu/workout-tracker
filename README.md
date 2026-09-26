# 유병관 운동기록 (벌크업 상/하체 2분할 16주 프로그램)

모바일 최적화 개인 운동 계획·기록 웹앱. GitHub Pages로 배포, Supabase로 로그인·클라우드 저장.

## 프로그램 (`gen_program.py` → `program_seed.json`)
- 상체A(가슴·등) · 하체A(스쿼트) · 상체B(어깨·팔) · 하체B(힙힌지), 주 4회(권장 월·화·목·금), 부위별 주 2회
- 16주 단계: 재적응(1~2주) → 적응(3~4) → 벌크 볼륨1(5~8) → 디로드(9) → 벌크 볼륨2(10~13) → 강도 진행(14~15) → 디로드·재측정(16)
- 웨이트만 세션당 최대 55분 (스트레칭·유산소 제외, 생성 시 60분 초과면 오류)
- 유산소는 세션마다 선택 항목. 체중 추세가 주 +0.5kg를 넘으면 추가를 권장

## 기능
- 영양 탭: 운동일/휴식일별 식사·크레아틴·단백질 보충제 시간표와 체크, 체중 기준 단백질·열량 목표, 체중 추세 조언
- 세트별 중량/반복/RPE 기록, **지난 기록 기반 중량·반복 자동 추천**
- 일일 체중·컨디션(수면/영양/동기/자신감/스트레스/피로도) 기록
- 운동 바꾸기 + 같은 부위 대체운동 추천
- 통계: 월별 운동 달력, 체중 추이, 3대 운동 추정 1RM 그래프
- 엑셀(.xlsx) 운동기록 다운로드 / 엑셀 운동프로그램 불러오기
- 이메일·비밀번호 로그인 + 클라우드 자동 저장(기기 바꿔도 유지)
- 중량 조정 단위: 바벨 5kg · 덤벨 1kg

## 빌드
```
python3 build.py
```
`_template.html` + `program_seed.json` / `history_seed.json` / `muscle_seed.json` + (선택)`supabase.config.json` → `index.html` 생성.

## Supabase 설정
1. supabase.com 프로젝트 생성
2. `supabase_setup.sql` 내용을 SQL Editor에서 실행
3. Authentication → Email → "Confirm email" 끄기(즉시 로그인용)
4. Project Settings → API 에서 Project URL, anon public key 복사
5. `supabase.config.json` 작성: `{"url":"https://xxx.supabase.co","anon":"eyJ..."}`
6. `python3 build.py` 재실행 → 배포

## 배포 (GitHub Pages)
이 폴더를 저장소 루트로 push 후, Settings → Pages → Branch: main / root 선택.
앱 주소: `https://<github-id>.github.io/<repo>/`

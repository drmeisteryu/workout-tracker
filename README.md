# 유병관 운동기록 (Push/Pull 근비대 프로그램)

모바일 최적화 개인 운동 계획·기록 웹앱. GitHub Pages로 배포, Supabase로 로그인·클라우드 저장.

## 기능
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

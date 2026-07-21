-- 리프트로그 · 비밀번호 없는(이메일만) 로그인용 설정
-- Supabase 대시보드 → SQL Editor → New query → 아래 전체 붙여넣고 RUN

-- 1) 이메일 키 기반 데이터 테이블
--    user_key = 이메일의 sha256 해시 (이메일 원문은 저장하지 않음)
create table if not exists public.app_data (
  user_key   text primary key,
  data       jsonb,
  updated_at timestamptz default now()
);

-- 2) 로그인(Auth) 없이 앱이 직접 읽고 쓰므로 익명 접근 허용
alter table public.app_data enable row level security;
drop policy if exists "app_open" on public.app_data;
create policy "app_open" on public.app_data
  for all to anon, authenticated
  using (true) with check (true);

-- 3) 기존 기록(mr.bkyu@gmail.com) 이전
--    아래 해시는 'mr.bkyu@gmail.com'의 sha256 값입니다.
insert into public.app_data (user_key, data, updated_at)
select '851347e35e3949d082d087b2550b1725dc6f08ec33a27f844e8086b6719d2de7',
       d.data, now()
from public.user_data d
join auth.users u on u.id = d.user_id
where lower(u.email) = 'mr.bkyu@gmail.com'
on conflict (user_key) do update
  set data = excluded.data, updated_at = now();

-- 4) 확인: 아래가 1행 나오면 이전 성공
select user_key, updated_at, (data->'logs') is not null as has_logs
from public.app_data;

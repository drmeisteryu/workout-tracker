-- 리프트로그 · 이메일만 입력하는 로그인용 클라우드 저장소
-- Supabase 대시보드 → SQL Editor → New query → 아래 전체 붙여넣고 RUN (여러 번 실행해도 안전)
--
-- 보안: 앱은 테이블을 직접 읽고 쓰지 않고, 아래 두 함수만 쓴다.
--   get_app_data(키) / put_app_data(키, 데이터)  — 키 = 이메일의 sha256 해시
--   → 웹페이지에 들어 있는 공개 키(anon)로는 다른 사람의 기록을 목록으로 볼 수 없고,
--     이메일을 아는 경우에만 그 사람의 기록에 접근할 수 있다.

-- 1) 데이터 테이블 (이메일 원문은 저장하지 않음)
create table if not exists public.app_data (
  user_key   text primary key,
  data       jsonb,
  updated_at timestamptz default now()
);

-- 2) 테이블 직접 접근 차단: RLS 켜고 정책 없음 + 권한 회수
alter table public.app_data enable row level security;
drop policy if exists "app_open" on public.app_data;
revoke all on public.app_data from anon, authenticated;

-- 3) 앱이 쓰는 함수 두 개 (키 형식이 맞을 때만 동작)
create or replace function public.get_app_data(p_key text)
returns jsonb language sql stable security definer set search_path = public as $$
  select data from public.app_data where user_key = p_key and p_key ~ '^[0-9a-f]{64}$';
$$;

create or replace function public.put_app_data(p_key text, p_data jsonb)
returns void language plpgsql security definer set search_path = public as $$
begin
  if p_key !~ '^[0-9a-f]{64}$' then raise exception 'invalid key'; end if;
  insert into public.app_data (user_key, data, updated_at) values (p_key, p_data, now())
  on conflict (user_key) do update set data = excluded.data, updated_at = now();
end $$;

revoke all on function public.get_app_data(text) from public;
revoke all on function public.put_app_data(text, jsonb) from public;
grant execute on function public.get_app_data(text) to anon, authenticated;
grant execute on function public.put_app_data(text, jsonb) to anon, authenticated;

-- 4) 예전 이메일·비밀번호 로그인 시절(~2026-07) 기록을 처음 한 번만 옮김
--    아래 해시는 'mr.bkyu@gmail.com'의 sha256 값입니다.
--    이미 앱이 올린 데이터가 있으면 덮어쓰지 않습니다(on conflict do nothing).
--    앱이 처음 연결될 때 이 기록과 폰에 저장된 기록을 합쳐서 다시 올립니다.
insert into public.app_data (user_key, data, updated_at)
select '851347e35e3949d082d087b2550b1725dc6f08ec33a27f844e8086b6719d2de7', d.data, now()
from public.user_data d
join auth.users u on u.id = d.user_id
where lower(u.email) = 'mr.bkyu@gmail.com'
on conflict (user_key) do nothing;

-- 5) 확인: 1행이 나오면 준비 완료
select user_key, updated_at, (data->'logs') is not null as has_logs
from public.app_data;

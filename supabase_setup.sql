-- 운동기록 앱 Supabase 설정
-- Supabase 대시보드 → 좌측 메뉴 "SQL Editor" → New query → 아래 전체 붙여넣고 RUN

-- 1) 사용자별 데이터 테이블 (앱 상태 전체를 JSON 한 줄로 저장)
create table if not exists public.user_data (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  data       jsonb,
  updated_at timestamptz default now()
);

-- 2) RLS(행 수준 보안) 켜기 — 각자 자기 데이터만 접근
alter table public.user_data enable row level security;

-- 3) 본인 행만 읽기/쓰기 허용
drop policy if exists "own_select" on public.user_data;
drop policy if exists "own_insert" on public.user_data;
drop policy if exists "own_update" on public.user_data;
create policy "own_select" on public.user_data for select using (auth.uid() = user_id);
create policy "own_insert" on public.user_data for insert with check (auth.uid() = user_id);
create policy "own_update" on public.user_data for update using (auth.uid() = user_id);

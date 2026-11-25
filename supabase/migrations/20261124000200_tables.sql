-- =====================================================================
-- HANSLIERY ACADEMY · 0002 · Tablas, claves, restricciones e índices
-- Importes: numeric(14,2). Correos: citext normalizado. PK: uuid.
-- =====================================================================

-- ---------- Identidad ----------
create table public.profiles (
  id                uuid primary key default gen_random_uuid(),
  user_id           uuid unique references auth.users(id) on delete set null,
  email             extensions.citext not null,
  first_name        text not null default '' check (char_length(first_name) <= 80),
  last_name         text not null default '' check (char_length(last_name) <= 80),
  phone             text check (phone is null or phone ~ '^\+?[0-9 ()-]{7,20}$'),
  country           text check (char_length(country) <= 60),
  city              text check (char_length(city) <= 80),
  occupation        text check (char_length(occupation) <= 120),
  organization      text check (char_length(organization) <= 120),
  interest_area     text check (char_length(interest_area) <= 120),
  avatar_path       text check (char_length(avatar_path) <= 300),
  status            public.account_status not null default 'active',
  last_activity_at  timestamptz not null default now(),
  terms_version     text,
  terms_accepted_at timestamptz,
  privacy_consent_at timestamptz,
  public_recognition_consent boolean not null default false,
  anonymized_at     timestamptz,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now(),
  constraint profiles_email_normalized check (email::text = lower(btrim(email::text))),
  constraint profiles_email_format check (email::text ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$')
);
create unique index profiles_email_key on public.profiles (email);
create index profiles_status_activity_idx on public.profiles (status, last_activity_at);

create table public.student_accounts (
  profile_id        uuid primary key references public.profiles(id) on delete cascade,
  student_code      text not null unique,
  onboarding_completed boolean not null default false,
  tutorial_seen     boolean not null default false,
  inactivity_warning_level smallint not null default 0,
  suspended_at      timestamptz,
  created_at        timestamptz not null default now()
);

create table public.user_roles (
  id          uuid primary key default gen_random_uuid(),
  profile_id  uuid not null references public.profiles(id) on delete cascade,
  role        public.app_role not null,
  course_id   uuid,  -- ámbito: solo para instructores (FK añadida tras crear courses)
  granted_by  uuid references public.profiles(id) on delete set null,
  granted_at  timestamptz not null default now(),
  constraint user_roles_unique unique nulls not distinct (profile_id, role, course_id),
  constraint user_roles_scope check ((role = 'instructor' and course_id is not null) or (role <> 'instructor' and course_id is null))
);
create index user_roles_profile_idx on public.user_roles (profile_id);

-- ---------- Académico ----------
create table public.courses (
  id               uuid primary key default gen_random_uuid(),
  slug             text not null unique check (slug ~ '^[a-z0-9-]{3,120}$'),
  title            text not null check (char_length(title) between 3 and 200),
  summary          text,
  level            text,
  tag              text,
  duration_minutes integer check (duration_minutes is null or duration_minutes > 0),
  academic_hours   numeric(5,1) check (academic_hours is null or academic_hours > 0),
  public_url       text,
  status           public.course_status not null default 'draft',
  is_free          boolean not null default true,
  price_dop        numeric(14,2) not null default 0 check (price_dop >= 0),
  price_usd        numeric(14,2) not null default 0 check (price_usd >= 0),
  capacity         integer check (capacity is null or capacity > 0),
  pass_percentage  numeric(5,2) not null default 80 check (pass_percentage between 0 and 100),
  requires_exam    boolean not null default true,
  published_at     timestamptz,
  created_by       uuid references public.profiles(id) on delete set null,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  constraint courses_price_coherent check (is_free or price_dop > 0 or price_usd > 0)
);
alter table public.user_roles
  add constraint user_roles_course_fk foreign key (course_id) references public.courses(id) on delete cascade;
create index user_roles_course_idx on public.user_roles (course_id) where course_id is not null;

create table public.course_modules (
  id        uuid primary key default gen_random_uuid(),
  course_id uuid not null references public.courses(id) on delete cascade,
  position  smallint not null check (position > 0),
  title     text not null,
  anchor    text not null,  -- id de la sección en la página pública (p. ej. modulo-3)
  unique (course_id, position),
  unique (course_id, anchor)
);

create table public.lessons (
  id               uuid primary key default gen_random_uuid(),
  module_id        uuid not null references public.course_modules(id) on delete cascade,
  position         smallint not null check (position > 0),
  title            text not null,
  kind             public.lesson_kind not null default 'page',
  content_url      text,
  storage_path     text,
  duration_minutes integer check (duration_minutes is null or duration_minutes > 0),
  created_at       timestamptz not null default now(),
  unique (module_id, position)
);

create table public.enrollments (
  id            uuid primary key default gen_random_uuid(),
  profile_id    uuid not null references public.profiles(id) on delete restrict,
  course_id     uuid not null references public.courses(id) on delete restrict,
  status        public.enrollment_status not null default 'active',
  progress_pct  numeric(5,2) not null default 0 check (progress_pct between 0 and 100),
  enrolled_at   timestamptz not null default now(),
  completed_at  timestamptz,
  payment_id    uuid,
  scholarship_id uuid,
  unique (profile_id, course_id)
);
create index enrollments_course_idx on public.enrollments (course_id, status);

create table public.lesson_progress (
  id            uuid primary key default gen_random_uuid(),
  enrollment_id uuid not null references public.enrollments(id) on delete cascade,
  module_id     uuid references public.course_modules(id) on delete cascade,
  lesson_id     uuid references public.lessons(id) on delete cascade,
  completed_at  timestamptz not null default now(),
  constraint lesson_progress_target check (num_nonnulls(module_id, lesson_id) = 1),
  unique (enrollment_id, module_id),
  unique (enrollment_id, lesson_id)
);

-- ---------- Evaluación ----------
create table public.exams (
  id                    uuid primary key default gen_random_uuid(),
  course_id             uuid references public.courses(id) on delete restrict,
  title                 text not null,
  description           text,
  is_certification      boolean not null default true,
  status                public.course_status not null default 'draft',
  time_limit_minutes    integer check (time_limit_minutes is null or time_limit_minutes between 1 and 600),
  max_attempts          smallint not null default 3 check (max_attempts between 1 and 20),
  pass_percentage       numeric(5,2) not null default 80 check (pass_percentage between 0 and 100),
  questions_per_attempt smallint check (questions_per_attempt is null or questions_per_attempt > 0),
  shuffle_questions     boolean not null default true,
  available_from        timestamptz,
  available_until       timestamptz,
  is_free               boolean not null default true,
  price_dop             numeric(14,2) not null default 0 check (price_dop >= 0),
  price_usd             numeric(14,2) not null default 0 check (price_usd >= 0),
  created_by            uuid references public.profiles(id) on delete set null,
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now(),
  check (available_until is null or available_from is null or available_until > available_from)
);
create index exams_course_idx on public.exams (course_id);

create table public.questions (
  id          uuid primary key default gen_random_uuid(),
  exam_id     uuid not null references public.exams(id) on delete cascade,
  type        public.question_type not null,
  prompt      text not null,
  points      numeric(6,2) not null default 1 check (points > 0),
  explanation text,
  position    smallint not null default 1,
  is_active   boolean not null default true,
  created_at  timestamptz not null default now()
);
create index questions_exam_idx on public.questions (exam_id) where is_active;

-- Opciones de respuesta (incluye la clave: nunca legible por estudiantes)
create table public.answers (
  id          uuid primary key default gen_random_uuid(),
  question_id uuid not null references public.questions(id) on delete cascade,
  label       text not null,
  is_correct  boolean not null default false,
  position    smallint not null default 1,
  unique (question_id, position)
);

create table public.exam_attempts (
  id             uuid primary key default gen_random_uuid(),
  exam_id        uuid not null references public.exams(id) on delete restrict,
  profile_id     uuid not null references public.profiles(id) on delete restrict,
  attempt_number smallint not null check (attempt_number > 0),
  status         public.attempt_status not null default 'in_progress',
  question_ids   uuid[] not null default '{}',
  responses      jsonb not null default '{}'::jsonb,
  started_at     timestamptz not null default now(),
  expires_at     timestamptz,
  submitted_at   timestamptz,
  auto_score     numeric(7,2),
  manual_score   numeric(7,2),
  max_score      numeric(7,2),
  score_pct      numeric(5,2) check (score_pct is null or score_pct between 0 and 100),
  passed         boolean,
  feedback       text,
  graded_by      uuid references public.profiles(id) on delete set null,
  graded_at      timestamptz,
  unique (exam_id, profile_id, attempt_number)
);
create index exam_attempts_profile_idx on public.exam_attempts (profile_id, exam_id);

create table public.assignments (
  id              uuid primary key default gen_random_uuid(),
  course_id       uuid not null references public.courses(id) on delete restrict,
  title           text not null,
  instructions    text,
  due_at          timestamptz,
  max_score       numeric(6,2) not null default 100 check (max_score > 0),
  attachment_path text,
  is_published    boolean not null default false,
  created_by      uuid references public.profiles(id) on delete set null,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
create index assignments_course_idx on public.assignments (course_id);

create table public.assignment_submissions (
  id            uuid primary key default gen_random_uuid(),
  assignment_id uuid not null references public.assignments(id) on delete restrict,
  profile_id    uuid not null references public.profiles(id) on delete restrict,
  file_path     text,
  comment       text check (char_length(comment) <= 4000),
  status        public.submission_status not null default 'submitted',
  submitted_at  timestamptz not null default now(),
  score         numeric(6,2) check (score is null or score >= 0),
  feedback      text,
  graded_by     uuid references public.profiles(id) on delete set null,
  graded_at     timestamptz,
  unique (assignment_id, profile_id)
);

-- ---------- Certificación ----------
create table public.certificates (
  id                 uuid primary key default gen_random_uuid(),
  verification_code  text not null unique check (verification_code ~ '^HS-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$'),
  profile_id         uuid not null references public.profiles(id) on delete restrict,
  course_id          uuid not null references public.courses(id) on delete restrict,
  enrollment_id      uuid references public.enrollments(id) on delete set null,
  exam_attempt_id    uuid references public.exam_attempts(id) on delete set null,
  student_name       text not null,  -- copia al emitir: el certificado es un registro conservado
  course_title       text not null,
  academic_hours     numeric(5,1),
  completed_on       date not null,
  grade_pct          numeric(5,2),
  status             public.certificate_status not null default 'valid',
  revoked_reason     text,
  pdf_path           text,
  issued_by          uuid references public.profiles(id) on delete set null,
  issued_at          timestamptz not null default now()
);
create unique index certificates_one_valid on public.certificates (profile_id, course_id) where status = 'valid';

-- ---------- Finanzas ----------
create table public.revenue_categories (
  id         uuid primary key default gen_random_uuid(),
  code       text not null unique check (code ~ '^[a-z0-9_]{2,40}$'),
  name       text not null,
  grp        public.revenue_group not null,
  parent_id  uuid references public.revenue_categories(id) on delete restrict,
  is_active  boolean not null default true,
  created_at timestamptz not null default now()
);

create table public.payments (
  id               uuid primary key default gen_random_uuid(),
  category_id      uuid not null references public.revenue_categories(id) on delete restrict,
  profile_id       uuid references public.profiles(id) on delete restrict,
  client_name      text,
  concept          text not null check (char_length(concept) between 3 and 200),
  product_type     public.product_type not null,
  course_id        uuid references public.courses(id) on delete restrict,
  exam_id          uuid references public.exams(id) on delete restrict,
  product_name     text,
  occurred_on      date not null default current_date,
  amount           numeric(14,2) not null check (amount > 0),
  currency         public.currency_code not null,
  fee_amount       numeric(14,2) not null default 0 check (fee_amount >= 0),
  refunded_amount  numeric(14,2) not null default 0 check (refunded_amount >= 0),
  net_amount       numeric(14,2) generated always as (amount - fee_amount - refunded_amount) stored,
  discount_amount  numeric(14,2) not null default 0 check (discount_amount >= 0),
  scholarship_id   uuid,
  method           public.payment_method not null,
  status           public.payment_status not null default 'pending',
  reference        text,
  evidence_path    text,
  confirmed_by     uuid references public.profiles(id) on delete set null,
  confirmed_at     timestamptz,
  notes            text,
  created_by       uuid references public.profiles(id) on delete set null,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  constraint payments_party check (profile_id is not null or client_name is not null),
  constraint payments_refund_le_amount check (refunded_amount + fee_amount <= amount),
  constraint payments_confirmed_has_actor check (status not in ('confirmed','refunded','partially_refunded') or confirmed_at is not null)
);
create unique index payments_reference_key on public.payments (method, reference) where reference is not null;
create index payments_period_idx on public.payments (occurred_on, status, currency);
create index payments_category_idx on public.payments (category_id);
create index payments_profile_idx on public.payments (profile_id);

alter table public.enrollments
  add constraint enrollments_payment_fk foreign key (payment_id) references public.payments(id) on delete set null;

-- ---------- Reconocimientos ----------
create table public.awards (
  id               uuid primary key default gen_random_uuid(),
  profile_id       uuid not null references public.profiles(id) on delete restrict,
  period_label     text not null check (char_length(period_label) between 4 and 40),
  level            public.award_level not null,
  score            numeric(6,2) not null check (score between 0 and 100),
  score_breakdown  jsonb not null default '{}'::jsonb,
  status           public.award_status not null default 'candidate',
  constancia_code  text unique,
  reviewed_by      uuid references public.profiles(id) on delete set null,
  reviewed_at      timestamptz,
  created_at       timestamptz not null default now(),
  unique (profile_id, period_label)
);

create table public.scholarships (
  id              uuid primary key default gen_random_uuid(),
  profile_id      uuid not null references public.profiles(id) on delete restrict,
  award_id        uuid references public.awards(id) on delete set null,
  percentage      numeric(5,2) not null default 50 check (percentage > 0 and percentage <= 100),
  period_label    text not null,
  conditions      text,
  status          public.scholarship_status not null default 'proposed',
  expires_on      date,
  proposed_by     uuid references public.profiles(id) on delete set null,
  approved_by     uuid references public.profiles(id) on delete set null,
  approved_at     timestamptz,
  used_enrollment_id uuid references public.enrollments(id) on delete set null,
  used_at         timestamptz,
  created_at      timestamptz not null default now(),
  constraint scholarships_approved_actor check (status not in ('approved','used') or (approved_by is not null and approved_at is not null))
);
create index scholarships_profile_idx on public.scholarships (profile_id, status);
alter table public.enrollments
  add constraint enrollments_scholarship_fk foreign key (scholarship_id) references public.scholarships(id) on delete set null;
alter table public.payments
  add constraint payments_scholarship_fk foreign key (scholarship_id) references public.scholarships(id) on delete set null;

-- ---------- Comunicación ----------
create table public.message_threads (
  id          uuid primary key default gen_random_uuid(),
  profile_id  uuid not null references public.profiles(id) on delete restrict,
  course_id   uuid references public.courses(id) on delete set null,
  subject     text not null check (char_length(subject) between 3 and 200),
  status      public.thread_status not null default 'open',
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index message_threads_profile_idx on public.message_threads (profile_id, status);

create table public.messages (
  id                uuid primary key default gen_random_uuid(),
  thread_id         uuid not null references public.message_threads(id) on delete cascade,
  sender_profile_id uuid references public.profiles(id) on delete set null,
  body              text not null check (char_length(body) between 1 and 8000),
  attachment_path   text,
  read_at           timestamptz,
  created_at        timestamptz not null default now()
);
create index messages_thread_idx on public.messages (thread_id, created_at);

create table public.notifications (
  id            uuid primary key default gen_random_uuid(),
  profile_id    uuid not null references public.profiles(id) on delete cascade,
  kind          text not null check (kind ~ '^[a-z_]{3,40}$'),
  title         text not null check (char_length(title) <= 200),
  body          text check (char_length(body) <= 4000),
  link          text,
  read_at       timestamptz,
  email_sent_at timestamptz,
  created_by    uuid references public.profiles(id) on delete set null,
  created_at    timestamptz not null default now()
);
create index notifications_profile_idx on public.notifications (profile_id, read_at, created_at desc);

-- ---------- Bitácora y bajas ----------
create table public.activity_logs (
  id               bigint generated always as identity primary key,
  actor_user_id    uuid,
  actor_profile_id uuid,
  action           text not null,
  entity           text,
  entity_id        text,
  metadata         jsonb not null default '{}'::jsonb,
  created_at       timestamptz not null default now()
);
create index activity_logs_actor_idx on public.activity_logs (actor_profile_id, created_at desc);
create index activity_logs_entity_idx on public.activity_logs (entity, entity_id);

create table public.account_deletion_requests (
  id               uuid primary key default gen_random_uuid(),
  profile_id       uuid not null references public.profiles(id) on delete restrict,
  reason           public.deletion_reason not null,
  status           public.deletion_status not null default 'open',
  blocking_reasons text[] not null default '{}',
  requested_at     timestamptz not null default now(),
  scheduled_for    timestamptz,
  completed_at     timestamptz,
  processed_by     uuid references public.profiles(id) on delete set null
);
create unique index deletion_one_open on public.account_deletion_requests (profile_id) where status in ('open','blocked','scheduled');

-- ---------- Configuración ----------
create table public.academy_settings (
  key        text primary key,
  value      jsonb not null,
  updated_by uuid references public.profiles(id) on delete set null,
  updated_at timestamptz not null default now()
);

-- updated_at
do $$
declare t text;
begin
  foreach t in array array['profiles','courses','exams','assignments','payments','message_threads'] loop
    execute format('create trigger %I_updated_at before update on public.%I for each row execute function private.set_updated_at()', t, t);
  end loop;
end $$;

-- =====================================================================
-- HANSLIERY ACADEMY · 0001 · Base: extensiones, esquema privado y tipos
-- =====================================================================
create extension if not exists citext with schema extensions;
create extension if not exists pgcrypto with schema extensions;

-- Esquema para funciones internas (no expuesto por la API)
create schema if not exists private;
revoke all on schema private from public, anon, authenticated;
grant usage on schema private to authenticated, anon;  -- solo para ejecutar helpers usados en RLS

create type public.app_role as enum ('superadmin', 'academic_admin', 'instructor', 'student');
create type public.account_status as enum ('active', 'suspended', 'pending_deletion', 'anonymized');
create type public.course_status as enum ('draft', 'published', 'archived');
create type public.enrollment_status as enum ('active', 'completed', 'cancelled');
create type public.lesson_kind as enum ('page', 'video', 'pdf', 'link', 'text');
create type public.question_type as enum ('single', 'multiple', 'true_false', 'open', 'case');
create type public.attempt_status as enum ('in_progress', 'submitted', 'graded', 'expired');
create type public.submission_status as enum ('submitted', 'in_review', 'graded', 'returned');
create type public.payment_status as enum ('pending', 'confirmed', 'rejected', 'refunded', 'partially_refunded');
create type public.currency_code as enum ('DOP', 'USD');
create type public.payment_method as enum ('transfer', 'deposit', 'card', 'cash', 'paypal', 'gateway', 'other');
create type public.product_type as enum ('course', 'workshop', 'corporate_training', 'exam', 'software', 'service', 'other');
create type public.revenue_group as enum ('training', 'software', 'evaluation', 'other');
create type public.certificate_status as enum ('valid', 'revoked');
create type public.award_level as enum ('excelencia_academica', 'alto_rendimiento', 'merito_compromiso');
create type public.award_status as enum ('candidate', 'approved', 'rejected');
create type public.scholarship_status as enum ('proposed', 'approved', 'rejected', 'used', 'expired', 'revoked');
create type public.thread_status as enum ('open', 'pending', 'answered', 'archived');
create type public.deletion_reason as enum ('inactivity', 'user_request', 'admin');
create type public.deletion_status as enum ('open', 'blocked', 'scheduled', 'completed', 'cancelled');

-- updated_at genérico
create or replace function private.set_updated_at()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.updated_at := now();
  return new;
end $$;

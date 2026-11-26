// =================================================================
// academy-jobs · tareas de mantenimiento de la Academy
//  - cleanup: borra archivos en cola (cuentas anonimizadas) y elimina
//             de Auth los usuarios ya anonimizados.
//  - email:   envía por correo las notificaciones pendientes. Solo actúa
//             si existen los secretos RESEND_API_KEY y MAIL_FROM (requieren
//             dominio propio verificado); si faltan, no hace nada.
// Autorización: encabezado x-job-secret (pg_cron, validado contra Vault)
// o sesión de superadministración con 2FA (botón del centro de control).
// =================================================================
import { createClient } from "npm:@supabase/supabase-js@2";

const URL_ = Deno.env.get("SUPABASE_URL")!;
const SERVICE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const RESEND = Deno.env.get("RESEND_API_KEY") ?? "";
const MAIL_FROM = Deno.env.get("MAIL_FROM") ?? "";
const SITE = "https://hansliery89.github.io/hansliery-web/academy/";
const ORIGINS = ["https://hansliery89.github.io"];

function cors(req: Request) {
  const o = req.headers.get("origin") ?? "";
  return {
    "Access-Control-Allow-Origin": ORIGINS.includes(o) ? o : ORIGINS[0],
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}
const json = (req: Request, body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors(req), "Content-Type": "application/json" } });

const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

async function authorized(req: Request, admin: ReturnType<typeof createClient>): Promise<boolean> {
  const secret = req.headers.get("x-job-secret");
  if (secret) {
    const { data } = await admin.rpc("job_secret_ok", { p_secret: secret });
    return data === true;
  }
  const auth = req.headers.get("authorization") ?? "";
  if (!auth.startsWith("Bearer ")) return false;
  const user = createClient(URL_, ANON, { global: { headers: { Authorization: auth } }, auth: { persistSession: false } });
  const { data } = await user.rpc("job_caller_is_admin");
  return data === true; // la función exige superadministración en sesión aal2
}

async function cleanup(admin: ReturnType<typeof createClient>) {
  const { data, error } = await admin.rpc("job_cleanup_batch");
  if (error) throw error;
  const done: number[] = [];
  let files = 0;
  for (const item of (data?.storage ?? []) as { id: number; bucket: string; prefix: string }[]) {
    const { data: list, error: le } = await admin.storage.from(item.bucket).list(item.prefix.replace(/\/$/, ""), { limit: 1000 });
    if (le) continue;
    const paths = (list ?? []).filter((f) => f.id).map((f) => item.prefix.replace(/\/?$/, "/") + f.name);
    if (paths.length) {
      const { error: re } = await admin.storage.from(item.bucket).remove(paths);
      if (re) continue;
      files += paths.length;
    }
    done.push(item.id);
  }
  const users: string[] = [];
  for (const id of (data?.users ?? []) as string[]) {
    const { error: de } = await admin.auth.admin.deleteUser(id);
    if (!de) users.push(id);
  }
  await admin.rpc("job_cleanup_done", { p_queue: done, p_users: users });
  return { queue_processed: done.length, files_removed: files, auth_users_deleted: users.length };
}

async function email(admin: ReturnType<typeof createClient>) {
  if (!RESEND || !MAIL_FROM) return { status: "disabled" };
  const { data, error } = await admin.rpc("job_pending_emails", { p_limit: 50 });
  if (error) throw error;
  const sent: string[] = [], failed: string[] = [];
  for (const n of (data ?? []) as { id: string; email: string; first_name: string; title: string; body: string | null; link: string | null }[]) {
    const link = n.link ? SITE + n.link.replace(/^\/+/, "") : SITE + "panel.html";
    const html = `<div style="font-family:Arial,sans-serif;max-width:560px;color:#0b1b2b">
      <p>Hola ${esc(n.first_name || "")},</p><h2 style="font-size:18px">${esc(n.title)}</h2>
      ${n.body ? `<p>${esc(n.body)}</p>` : ""}
      <p><a href="${esc(link)}" style="background:#0b6e6e;color:#fff;padding:10px 16px;border-radius:6px;text-decoration:none">Abrir el aula virtual</a></p>
      <p style="font-size:12px;color:#5b6b7b">Hansliery Sánchez · Compliance &amp; Risk Advisory — Academy. Recibes este correo porque tienes una cuenta en el aula virtual.</p></div>`;
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${RESEND}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: MAIL_FROM, to: [n.email], subject: n.title, html }),
    });
    (r.ok ? sent : failed).push(n.id);
  }
  await admin.rpc("job_mark_emails", { p_sent: sent, p_failed: failed });
  return { status: "enabled", sent: sent.length, failed: failed.length };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(req) });
  if (req.method !== "POST") return json(req, { error: "method_not_allowed" }, 405);
  const admin = createClient(URL_, SERVICE, { auth: { persistSession: false } });
  if (!(await authorized(req, admin))) return json(req, { error: "not_allowed" }, 401);
  let tasks = ["cleanup", "email"];
  try { const b = await req.json(); if (Array.isArray(b?.tasks)) tasks = b.tasks.filter((t: unknown) => t === "cleanup" || t === "email"); } catch { /* cuerpo opcional */ }
  const out: Record<string, unknown> = {};
  try {
    if (tasks.includes("cleanup")) out.cleanup = await cleanup(admin);
    if (tasks.includes("email")) out.email = await email(admin);
  } catch (e) {
    console.error(e);
    return json(req, { error: "job_failed" }, 500);
  }
  return json(req, out);
});

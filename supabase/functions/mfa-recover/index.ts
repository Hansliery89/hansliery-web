// HANSLIERY ACADEMY · mfa-recover
// Permite recuperar el acceso cuando el estudiante perdió su aplicación de
// autenticación: valida un código de recuperación de un solo uso y elimina
// sus factores TOTP con la API de administración. El usuario debe tener una
// sesión válida (contraseña correcta, nivel aal1). Máx. 5 fallos / 15 min.
import { createClient } from "npm:@supabase/supabase-js@2";

const ALLOWED_ORIGINS = ["https://hansliery89.github.io"];

function cors(origin: string | null) {
  const allow = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

function json(body: unknown, status: number, origin: string | null) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors(origin), "Content-Type": "application/json; charset=utf-8" },
  });
}

Deno.serve(async (req) => {
  const origin = req.headers.get("Origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);

  const token = (req.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
  if (!token) return json({ error: "not_authenticated" }, 401, origin);

  let code = "";
  try {
    const body = await req.json();
    code = String(body?.code ?? "").trim();
  } catch (_) {
    return json({ error: "invalid_body" }, 400, origin);
  }
  if (!/^[A-Za-z0-9-]{8,12}$/.test(code)) return json({ error: "invalid_code" }, 400, origin);

  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  const { data: userData, error: userErr } = await admin.auth.getUser(token);
  if (userErr || !userData?.user) return json({ error: "not_authenticated" }, 401, origin);
  const userId = userData.user.id;

  const { data: ok, error: rpcErr } = await admin.rpc("consume_recovery_code", { p_user: userId, p_code: code });
  if (rpcErr) {
    const tooMany = /too_many_attempts/.test(rpcErr.message);
    return json({ error: tooMany ? "too_many_attempts" : "server_error" }, tooMany ? 429 : 500, origin);
  }
  if (!ok) return json({ error: "invalid_code" }, 400, origin);

  const { data: factors, error: listErr } = await admin.auth.admin.mfa.listFactors({ userId });
  if (listErr) return json({ error: "server_error" }, 500, origin);
  for (const f of factors?.factors ?? []) {
    const { error } = await admin.auth.admin.mfa.deleteFactor({ id: f.id, userId });
    if (error) return json({ error: "server_error" }, 500, origin);
  }
  return json({ ok: true, removed: (factors?.factors ?? []).length }, 200, origin);
});

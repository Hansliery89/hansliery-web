# Academy · Backend (Supabase)

Backend de **HANSLIERY SÁNCHEZ | COMPLIANCE & RISK ADVISORY · Academy**. Este directorio no contiene secretos: solo migraciones, pruebas y documentación. La seguridad depende de las políticas RLS y de las funciones del servidor, no del código del navegador.

| Dato | Valor |
|---|---|
| Proyecto | `hansliery-academy` (ref. `vbodazonicfzfovlighm`) |
| Región / plan | us-east-1 · Free (desarrollo) |
| URL de la API | `https://vbodazonicfzfovlighm.supabase.co` |
| Clave pública (frontend) | `sb_publishable_C5Gi-NlDKhEpb3AnaH0QGg_gtae0P4W` — es pública por diseño; nunca use aquí la clave secreta ni la `service_role`. |

> **Antes de recibir estudiantes reales:** pasar la organización a plan Pro (el plan Free se pausa tras una semana sin actividad, no tiene copias de seguridad y no incluye la protección contra contraseñas filtradas).

## Migraciones (aplicadas en este orden)

| Archivo | Contenido |
|---|---|
| `0100_base` | Extensiones, esquema `private`, tipos enumerados. |
| `0200_tables` | 25 tablas: las 23 del requerimiento + `message_threads` y `academy_settings`. Claves, restricciones, índices, `numeric(14,2)` para importes, correo `citext` normalizado y único. |
| `0300_functions` | Ayudantes de autorización, alta automática de cuentas, bitácora, auditoría y funciones RPC seguras. |
| `0400_rls` | Privilegios mínimos por columna y políticas RLS en todas las tablas. |
| `0450_rls_public_catalog` | Catálogo público para visitantes sin sesión. |
| `0500_storage` | 6 buckets privados con límites de tamaño y tipo, y sus políticas. |
| `0600_inactivity` | Política de 100 días y tarea diaria `pg_cron` (06:15 UTC). |
| `0650_storage_cleanup_queue` | Cola de limpieza de archivos (Supabase no permite borrar Storage desde SQL). |
| `0700_seed` | Configuración, 15 categorías de ingresos, 13 cursos (en **borrador**) y sus 93 módulos. |

## Modelo de seguridad

- **Roles:** `superadmin`, `academic_admin`, `instructor` (con ámbito por curso) y `student`. Solo el superadministrador asigna roles; no se puede retirar el último.
- **Doble factor obligatorio para el personal.** Toda política de personal exige sesión `aal2` (TOTP verificado). Un administrador que entra solo con contraseña tiene acceso de estudiante.
- **Doble factor del estudiante.** Si el estudiante activó TOTP, no accede ni a su propio perfil hasta verificarlo en la sesión.
- **Aislamiento.** Un estudiante solo ve sus datos; un instructor solo ve a los estudiantes de sus cursos; el administrador académico no ve finanzas ni puede registrar pagos; las finanzas son exclusivas del superadministrador con `aal2`.
- **Claves de examen.** `questions` y `answers` son ilegibles para estudiantes. Los intentos y los certificados solo los escribe el servidor (Fase 5).
- **Columnas protegidas.** El estudiante no puede cambiar su correo, estado, consentimientos ni calificaciones; esas operaciones pasan por funciones del servidor.
- **Registro sin duplicados en tres capas:** validación en formulario (Fase 3), disparador `handle_new_user` y el índice `UNIQUE` sobre el correo normalizado, que también resuelve registros simultáneos.
- **Mensaje ante correo ya registrado.** Para no revelar qué correos tienen cuenta (enumeración), la interfaz mostrará: «Si el correo no estaba registrado, recibirás un enlace de verificación. Si ya tienes cuenta, inicia sesión o recupera tu contraseña».
- **Bitácora.** Altas, cambios de roles, pagos, cursos, exámenes, becas, premios, certificados, configuración y eventos de inactividad quedan en `activity_logs` (se registran las columnas cambiadas, no los valores personales).

### Funciones RPC expuestas

| Función | Quién | Para qué |
|---|---|---|
| `my_account()` | autenticado | Estado de la cuenta, roles, si falta 2FA o consentimiento. |
| `touch_activity()` | autenticado | Registra actividad; reactiva una cuenta suspendida por inactividad. |
| `accept_terms(version, privacy)` | autenticado | Consentimiento con fecha del servidor (p. ej., tras registrarse con Google). |
| `enroll_in_course(course)` | autenticado | Matrícula en curso gratuito publicado, con cupo atómico. |
| `mark_module_read(slug, anchor)` | autenticado | Avance por módulo desde las páginas públicas de los cursos. |
| `my_access_history()` | autenticado | Historial de sesiones registrado por Auth. |
| `request_account_deletion()` | autenticado | Solicitud de baja. |
| `verify_certificate(code)` | público | Verificación con datos mínimos. |
| `public_recognitions()` | público | Premios aprobados de estudiantes que autorizaron publicar su nombre. |

El asesor de seguridad de Supabase advierte que estas funciones `SECURITY DEFINER` son ejecutables desde la API. **Es intencional**: cada una valida la identidad, el estado de la cuenta y los permisos en el servidor, y las pruebas lo verifican.

### Política de inactividad

Avisos a los 70, 85 y 95 días → suspensión a los 100 → solicitud de baja con 30 días de gracia → anonimización **solo si no hay** pagos pendientes, entregas o exámenes por calificar, becas vigentes ni conversaciones abiertas. Certificados, pagos y registros académicos se conservan vinculados al perfil anonimizado. Si el estudiante vuelve a iniciar sesión antes de la anonimización, la cuenta se reactiva. Todos los plazos están en `academy_settings` y deben validarse con criterio legal.

## Pruebas

`tests/001_rls_and_auth.sql` crea usuarios de cada rol, ejecuta 27 comprobaciones y **revierte todo** al terminar (el resultado llega como mensaje `TEST_RESULT`). Ejecútelo completo en el editor SQL tras cada cambio de esquema.

Resultado del 24-11-2026: **27 de 27 correctas** (registro, duplicados, aislamiento entre estudiantes, columnas protegidas, escalada de privilegios, 2FA del personal y del estudiante, instructor por curso, separación financiera, catálogo público, verificación de certificados, inactividad completa, protección del último superadministrador y bitácora).

## Configuración pendiente en el panel de Supabase

Estas opciones no se pueden fijar con migraciones. Hágalas en **Authentication** del proyecto:

1. **Sign In / Providers → Email:** activado, con *Confirm email* activado.
2. **Contraseñas:** longitud mínima **12** y requisito de letras y dígitos. *Leaked password protection* (contraseñas comprometidas) requiere plan Pro: actívela al migrar.
3. **Multi-Factor → TOTP:** activado (viene activado por defecto).
4. **URL Configuration:** *Site URL* `https://hansliery89.github.io/hansliery-web/academy/` y, en *Redirect URLs*, la misma dirección con `**` al final. Con dominio propio, reemplácelas.
5. **Google:** en Google Cloud Console cree un *OAuth client ID* (tipo «Aplicación web»), con origen autorizado `https://hansliery89.github.io` y URI de redirección `https://vbodazonicfzfovlighm.supabase.co/auth/v1/callback`. Copie el *Client ID* y el *Client Secret* en **Providers → Google**. El secreto se escribe solo en el panel; no lo pegue en el chat ni en el repositorio.
6. **SMTP propio (Emails → SMTP Settings):** el correo integrado de Supabase es solo para pruebas y no entrega a direcciones externas al equipo del proyecto. Configure un proveedor (por ejemplo Resend, Brevo o Amazon SES) antes de abrir el registro.

## Crear el primer superadministrador

1. Regístrese en la Academy con su correo (Fase 3) y verifique el enlace.
2. En el editor SQL ejecute:

```sql
insert into public.user_roles (profile_id, role)
select id, 'superadmin' from public.profiles where email = 'su-correo@ejemplo.com';
```

3. Inicie sesión y active el doble factor en su perfil: sin `aal2`, el panel administrativo no mostrará datos.

## Siguientes fases que dependen de este backend

- **Edge Functions:** motor de exámenes y certificados (Fase 5), notificaciones por correo (Fase 8), procesamiento de `private.storage_cleanup_queue` y eliminación de la cuenta de Auth tras la anonimización (Fase 9).
- Los 13 cursos están en **borrador**: el administrador fija horas académicas, precio y los publica.

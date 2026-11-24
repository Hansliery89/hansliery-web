"""Bloques de lectura por capas para los cursos.

ess(texto)  -> «Lo esencial»: abre cada módulo en lenguaje sencillo (público general).
deep(html)  -> «Para profundizar»: bloque desplegable con detalle técnico (profesionales).
El texto intermedio del módulo es el «Desarrollo» (estudiantes y personal de primera línea).
"""


def ess(texto):
    return f'<div class="essential"><b>Lo esencial</b><p>{texto}</p></div>'


def deep(html, nivel="Nivel profesional"):
    return (f'<details class="deep"><summary><span>Para profundizar</span><small>{nivel}</small></summary>'
            f'<div class="deep-body">{html}</div></details>')

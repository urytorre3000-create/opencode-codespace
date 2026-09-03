#!/usr/bin/env python3
"""
🧗 Entrenador personal de calistenia — generador del plan diario.

Genera el plan de entrenamiento de HOY según:
  - El nivel del atleta (principiante / intermedio / avanzado).
  - Una rotación semanal (Empuje / Tracción / Piernas+Core / Descanso activo).
  - El historial guardado en `calistenia_log.json` (para progresar y no repetir).

Uso:
  python3 entrenador_calistenia.py             # muestra el plan de hoy
  python3 entrenador_calistenia.py --completado  # marca hoy como entrenado
  python3 entrenador_calistenia.py --fecha 2026-09-02  # plan de otra fecha
  python3 entrenador_calistenia.py --reset-log        # limpia el historial
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

# --------------------------------------------------------------------------- #
# Cargar preferencias del atleta
# --------------------------------------------------------------------------- #

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calistenia_config.json")
DEFAULT_CONFIG = {
    "nombre": "Atleta",
    "nivel": "principiante",          # principiante | intermedio | avanzado
    "dias_por_semana": 3,             # 2-6 sesiones de entrenamiento
    "duracion_min": 30,               # minutos por sesión
    "objetivo": "primera dominada",   # habilidad a practicar
    "enfoque_semanal": ["empuje", "traccion", "piernas_core"],
}

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calistenia_log.json")


def cargar_config():
    """Carga la configuración del atleta (con valores por defecto)."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as f:
            cfg = json.load(f)
        # Fusionar con los valores por defecto
        merged = dict(DEFAULT_CONFIG)
        merged.update(cfg)
        return merged
    return dict(DEFAULT_CONFIG)


def cargar_log():
    """Carga el historial de entrenamientos."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_log(log):
    """Guarda el historial de entrenamientos."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
# Rutinas por nivel
# --------------------------------------------------------------------------- #

# Cada entrada: (ejercicio, series x repeticiones, descanso entre series)
RUTINAS = {
    "principiante": {
        "empuje": [
            ("Flexiones en pared", "3 × 8-12", "60 s"),
            ("Flexiones de rodillas", "3 × 6-10", "60 s"),
            ("Fondos en banco", "3 × 8-12", "60 s"),
            ("Plancha (rodillas)", "3 × 20-30 s", "45 s"),
        ],
        "traccion": [
            ("Dominada australiana (agarre ancho)", "3 × 8-12", "75 s"),
            ("Dominada australiana (agarre supino)", "3 × 8-12", "75 s"),
            ("Remo con toalla / anillas", "3 × 8-12", "60 s"),
            ("Encogimientos en barra", "3 × 10-15", "45 s"),
        ],
        "piernas_core": [
            ("Sentadilla con peso corporal", "3 × 12-20", "60 s"),
            ("Zancadas alternas", "3 × 8-10 por pierna", "60 s"),
            ("Puente de glúteo", "3 × 12-15", "45 s"),
            ("Plancha frontal", "3 × 20-40 s", "45 s"),
            ("Elevaciones de pierna tumbado", "3 × 10-15", "45 s"),
        ],
    },
    "intermedio": {
        "empuje": [
            ("Flexiones completas", "4 × 10-15", "75 s"),
            ("Flexiones diamante", "3 × 6-10", "75 s"),
            ("Fondos en paralelas", "3 × 8-12", "90 s"),
            ("Flexiones con pies elevados", "3 × 8-12", "75 s"),
            ("Plancha frontal", "3 × 45-60 s", "45 s"),
        ],
        "traccion": [
            ("Dominadas con banda / negativas", "4 × 5-8", "90 s"),
            ("Dominada australiana a una mano (regresión)", "3 × 6-10", "75 s"),
            ("Remo en barra (agarre neutro)", "3 × 10-12", "75 s"),
            ("Encogimientos en barra", "3 × 15-20", "45 s"),
        ],
        "piernas_core": [
            ("Sentadilla búlgara asistida", "3 × 8-10 por pierna", "75 s"),
            ("Pistol squat asistido", "3 × 5-8 por pierna", "90 s"),
            ("Puente de glúteo a una pierna", "3 × 8-12", "60 s"),
            ("Hollow body hold", "3 × 20-40 s", "45 s"),
            ("L-sit (pies en suelo / rodillas)", "3 × 15-30 s", "45 s"),
        ],
    },
    "avanzado": {
        "empuje": [
            ("Flexiones archer", "4 × 6-10", "90 s"),
            ("Flexiones en anillas / pseudo-planche", "4 × 6-10", "90 s"),
            ("Fondos lastrados", "4 × 8-12", "90 s"),
            ("Handstand push-up (o negativas)", "3 × 3-6", "2 min"),
        ],
        "traccion": [
            ("Dominadas lastradas / archer", "4 × 5-8", "2 min"),
            ("Muscle-up (o transiciones)", "3 × 3-5", "2 min"),
            ("Dominadas con agarre tipo L", "3 × 5-8", "2 min"),
            ("Front lever (tuck → avanzado)", "3 × 10-20 s", "90 s"),
        ],
        "piernas_core": [
            ("Pistol squat", "3 × 5-8 por pierna", "2 min"),
            ("Shrimp squat", "3 × 5-8 por pierna", "2 min"),
            ("Nordic curl (regresión)", "3 × 5-8", "90 s"),
            ("Dragon flag (o negativas)", "3 × 5-8", "90 s"),
            ("L-sit completo", "3 × 15-30 s", "60 s"),
        ],
    },
}

HABILIDADES = {
    "primera dominada": [
        "Dominada australiana baja, 5 × máx con 90 s de descanso.",
        "Negativas lentas (bajar 5 s), 5 × 3-5.",
        "Dominadas con banda de asistencia, 4 × 5-8.",
    ],
    "handstand": [
        "Pino en pared: 5 × 30-60 s manteniendo el cuerpo alineado.",
        "Equilibrio a una pierna en pared: 4 × 20-30 s por lado.",
        "Patinadas (wall walks) hacia el pino: 3 × 5 repeticiones.",
    ],
    "muscle-up": [
        "Transiciones (de dominada a fondos) con banda: 5 × 3-5.",
        "Dominadas explosivas hasta el pecho: 4 × 5.",
        "Fondos en paralelas profundos: 4 × 8-10.",
    ],
    "planche": [
        "Planche tuck: 5 × 10-20 s.",
        "Planche tuck con una pierna extendida: 4 × 8-15 s.",
        "Pseudo-planche push-ups: 4 × 6-10.",
    ],
    "front lever": [
        "Front lever tuck: 5 × 15-25 s.",
        "Front lever tuck con una pierna extendida: 4 × 8-15 s.",
        "Dominadas en posición hueca: 4 × 6-8.",
    ],
}

# --------------------------------------------------------------------------- #
# Lógica del plan
# --------------------------------------------------------------------------- #

NIVELES_VALIDOS = ("principiante", "intermedio", "avanzado")
DIA_NOMBRE = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def dia_de_entrenamiento(fecha, dias_por_semana):
    """Devuelve True si la fecha corresponde a un día de entrenamiento.

    Distribuye los días de entrenamiento uniformemente a lo largo de la semana,
    evitando dos sesiones seguidas de la misma semana cuando es posible.
    """
    if dias_por_semana >= 7:
        return True
    weekday = fecha.weekday()  # 0=lunes ... 6=domingo
    # Mapa de qué weekday entrena, según el número de días por semana.
    # Se reparte para dejar descanso entre sesiones.
    planes = {
        6: [0, 2, 4, 6],
        5: [0, 2, 4, 6],
        4: [0, 1, 3, 5],
        3: [0, 2, 4],
        2: [0, 3],
        1: [0],
    }
    return weekday in planes[min(max(dias_por_semana, 1), 6)]


def num_sesion_semana(fecha, dias_por_semana):
    """Devuelve el número de sesión (1-based) que le toca a la fecha dentro de
    su semana, recorriendo los días de entrenamiento en orden."""
    if dias_por_semana >= 7:
        return fecha.weekday() + 1
    planes = {
        6: [0, 2, 4, 6],
        5: [0, 2, 4, 6],
        4: [0, 1, 3, 5],
        3: [0, 2, 4],
        2: [0, 3],
        1: [0],
    }
    dias = planes[min(max(dias_por_semana, 1), 6)]
    # Buscar dentro de la semana (lunes..domingo) la posición del día actual.
    lunes = fecha - timedelta(days=fecha.weekday())
    for idx, wd in enumerate(dias):
        if lunes + timedelta(days=wd) == fecha:
            return idx + 1
    return None


def focus_del_dia(fecha, enfoque_semanal, dias_por_semana):
    """Elige el enfoque del día rotando por cada sesión de la semana."""
    sesion = num_sesion_semana(fecha, dias_por_semana)
    if sesion is None:
        return None
    return enfoque_semanal[(sesion - 1) % len(enfoque_semanal)]


def construir_plan(cfg, fecha):
    """Construye el plan completo para la fecha dada."""
    nivel = cfg.get("nivel", "principiante").lower()
    if nivel not in NIVELES_VALIDOS:
        nivel = "principiante"
    nombre = cfg.get("nombre", "Atleta")
    correo = cfg.get("correo", "")
    objetivo = cfg.get("objetivo", "primera dominada").lower()
    duracion = cfg.get("duracion_min", 30)
    dias = cfg.get("dias_por_semana", 3)
    enfoque = cfg.get("enfoque_semanal", ["empuje", "traccion", "piernas_core"])

    hoy = fecha
    es_entrenamiento = dia_de_entrenamiento(hoy, dias)

    if not es_entrenamiento:
        return {
            "fecha": hoy.isoformat(),
            "dia": DIA_NOMBRE[hoy.weekday()],
            "tipo": "descanso",
            "nombre": nombre,
            "correo": correo,
            "mensaje": (
                "Hoy es día de DESCANSO. 👉 Recuperación activa: camina 20-30 min, "
                "estira 10 min y movilidad de hombros y caderas. "
                "La recuperación es parte del progreso. 💤"
            ),
            "calentamiento": [],
            "rutina": [],
            "foco": [],
            "enfriamiento": [],
        }

    foco = focus_del_dia(hoy, enfoque, dias)
    rutina = RUTINAS[nivel].get(foco, RUTINAS[nivel]["empuje"])
    habilidades = HABILIDADES.get(objetivo, HABILIDADES["primera dominada"])

    calentamiento = [
        "Rotaciones de cuello y hombros (círculos) — 1 min",
        "Movilidad de muñecas (flex/ext + círculos) — 1 min",
        "Balanceos de pierna y sentadillas de movilidad — 2 min",
        "Activación: 10 flexiones suaves + 10 dominadas australianas fáciles",
        "Elevar pulsaciones: saltos de tijera / mountain climbers — 2 min",
    ]

    enfriamiento = [
        "Estiramiento de pecho y hombros (puerta / pared) — 2 min por lado",
        "Estiramiento de dorsal y espalda (agarre en barra) — 1 min",
        "Estiramiento de cuádriceps e isquios — 1 min por lado",
        "Respiración profunda / relajación — 2 min",
    ]

    etiquetas = {
        "empuje": "💪 EMPUJE",
        "traccion": "🏋️ TRACCIÓN",
        "piernas_core": "🦵 PIERNAS + CORE",
    }

    return {
        "fecha": hoy.isoformat(),
        "dia": DIA_NOMBRE[hoy.weekday()],
        "tipo": "entrenamiento",
        "etiqueta": etiquetas.get(foco, "ENTRENAMIENTO"),
        "foco": foco,
        "nombre": nombre,
        "correo": correo,
        "nivel": nivel,
        "duracion": duracion,
        "objetivo": objetivo,
        "calentamiento": calentamiento,
        "rutina": rutina,
        "foco_ejercicios": habilidades,
        "enfriamiento": enfriamiento,
    }


def imprimir_plan(plan):
    """Muestra el plan por consola de forma legible."""
    print("=" * 58)
    print(f"🧗 ENTRENADOR DE CALISTENIA — {plan['fecha']} ({plan['dia']})")
    print(f"   Atleta: {plan['nombre']}")
    print("=" * 58)

    if plan["tipo"] == "descanso":
        print()
        print("  ✅ " + plan["mensaje"])
        print()
        return

    print(f"  Etiqueta: {plan['etiqueta']}")
    print(f"  Duración aprox.: {plan['duracion']} min  |  Nivel: {plan['nivel'].title()}")
    print()
    print("🔥 CALENTAMIENTO (5-8 min)")
    for i, ej in enumerate(plan["calentamiento"], 1):
        print(f"  {i}. {ej}")
    print()
    print("💪 ENTRENAMIENTO PRINCIPAL")
    for i, (ej, reps, desc) in enumerate(plan["rutina"], 1):
        print(f"  {i}. {ej:<45} {reps:<16} descanso {desc}")
    print()
    print("🎯 FOCO / HABILIDAD (10 min) — objetivo: " + plan["objetivo"])
    for i, ej in enumerate(plan["foco_ejercicios"], 1):
        print(f"  {i}. {ej}")
    print()
    print("🧘 ENFRIAMIENTO (5 min)")
    for i, ej in enumerate(plan["enfriamiento"], 1):
        print(f"  {i}. {ej}")
    print()
    print("💡 Consejo: forma perfecta > más reps. Descansa 48 h antes de repetir grupo.")
    print("=" * 58)


def texto_plan(plan):
    """Devuelve el plan como texto (para correo o mensajes)."""
    lineas = []
    lineas.append(f"🧗 PLAN DE CALISTENIA — {plan['fecha']} ({plan['dia']})")
    lineas.append(f"   Atleta: {plan['nombre']}")
    lineas.append("")

    if plan["tipo"] == "descanso":
        lineas.append("✅ " + plan["mensaje"])
        return "\n".join(lineas)

    lineas.append(f"🏷️  {plan['etiqueta']}  ·  Nivel: {plan['nivel'].title()}  ·  ~{plan['duracion']} min")
    lineas.append("")
    lineas.append("🔥 CALENTAMIENTO (5-8 min)")
    for i, ej in enumerate(plan["calentamiento"], 1):
        lineas.append(f"  {i}. {ej}")
    lineas.append("")
    lineas.append("💪 ENTRENAMIENTO PRINCIPAL")
    for i, (ej, reps, desc) in enumerate(plan["rutina"], 1):
        lineas.append(f"  {i}. {ej} — {reps}  (descanso {desc})")
    lineas.append("")
    lineas.append("🎯 FOCO / HABILIDAD (10 min)")
    lineas.append(f"   Objetivo actual: {plan['objetivo']}")
    for i, ej in enumerate(plan["foco_ejercicios"], 1):
        lineas.append(f"  {i}. {ej}")
    lineas.append("")
    lineas.append("🧘 ENFRIAMIENTO (5 min)")
    for i, ej in enumerate(plan["enfriamiento"], 1):
        lineas.append(f"  {i}. {ej}")
    lineas.append("")
    lineas.append("💡 Consejo: forma perfecta > más reps. ¡Disfruta la sesión! 💪")
    return "\n".join(lineas)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="Entrenador de calistenia: plan diario.")
    parser.add_argument("--fecha", help="Fecha (YYYY-MM-DD). Por defecto: hoy.")
    parser.add_argument("--completado", action="store_true",
                        help="Marca hoy como entrenado en el log.")
    parser.add_argument("--reset-log", action="store_true",
                        help="Borra el historial de entrenamientos.")
    args = parser.parse_args()

    cfg = cargar_config()

    if args.reset_log:
        guardar_log({})
        print("🗑️  Historial de entrenamientos borrado.")
        return

    hoy = datetime.now().date()
    fecha = date.fromisoformat(args.fecha) if args.fecha else hoy
    plan = construir_plan(cfg, fecha)
    imprimir_plan(plan)

    if args.completado:
        log = cargar_log()
        log[plan["fecha"]] = {
            "tipo": plan["tipo"],
            "foco": plan.get("foco", "descanso"),
            "nivel": cfg.get("nivel"),
        }
        guardar_log(log)
        print("\n✅ Entrenamiento registrado. ¡Buen trabajo! 🎉")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera una guía turística de Venezuela en PDF usando reportlab."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image, NextPageTemplate
)

# ---------------------------------------------------------------- paleta
AMARILLO = colors.HexColor("#FFCC00")
AZUL = colors.HexColor("#002FA7")
ROJO = colors.HexColor("#CE1126")
NEGRO = colors.HexColor("#1A1A1A")
GRIS = colors.HexColor("#5A5A5A")
CREMA = colors.HexColor("#FDF6E3")
VERDE = colors.HexColor("#1E7A46")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Guia_Turistica_Venezuela.pdf")

# ---------------------------------------------------------------- estilos
ss = getSampleStyleSheet()

est_titulo = ParagraphStyle(
    "Titulo", parent=ss["Title"], fontName="Helvetica-Bold",
    fontSize=30, leading=36, textColor=colors.white, alignment=TA_CENTER)

est_subtitulo = ParagraphStyle(
    "Subtitulo", parent=ss["Title"], fontName="Helvetica",
    fontSize=15, leading=20, textColor=colors.white, alignment=TA_CENTER)

est_h1 = ParagraphStyle(
    "H1", parent=ss["Heading1"], fontName="Helvetica-Bold",
    fontSize=20, leading=24, textColor=colors.white, alignment=TA_LEFT,
    spaceBefore=6, spaceAfter=10)

est_h2 = ParagraphStyle(
    "H2", parent=ss["Heading2"], fontName="Helvetica-Bold",
    fontSize=14, leading=18, textColor=AZUL, spaceBefore=14, spaceAfter=6)

est_body = ParagraphStyle(
    "Body", parent=ss["BodyText"], fontName="Helvetica",
    fontSize=10.5, leading=15, textColor=NEGRO, alignment=TA_JUSTIFY,
    spaceAfter=8)

est_bullet = ParagraphStyle(
    "Bullet", parent=est_body, leftIndent=14, bulletIndent=4, spaceAfter=4)

est_caption = ParagraphStyle(
    "Caption", parent=est_body, fontSize=9, leading=12,
    textColor=GRIS, alignment=TA_CENTER, spaceAfter=10)

est_quick = ParagraphStyle(
    "Quick", parent=est_body, fontSize=10, leading=14, alignment=TA_LEFT,
    textColor=NEGRO, spaceAfter=0)

# ---------------------------------------------------------------- páginas
def dibujar_fondo_portada(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(AMARILLO)
    canvas.rect(0, h - h / 2, w, h / 2, stroke=0, fill=1)
    canvas.setFillColor(AZUL)
    canvas.rect(0, h / 3, w, h / 6, stroke=0, fill=1)
    canvas.setFillColor(ROJO)
    canvas.rect(0, 0, w, h / 3, stroke=0, fill=1)
    # estrellas decorativas
    canvas.setFillColor(colors.white)
    for cx, cy in [(2.2 * cm, h - 2.2 * cm), (w - 2.2 * cm, h - 2.2 * cm),
                   (w / 2, 2.2 * cm), (2.2 * cm, 2.2 * cm), (w - 2.2 * cm, 2.2 * cm)]:
        canvas.circle(cx, cy, 0.28 * cm, stroke=0, fill=1)
    canvas.restoreState()

def dibujar_pie(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(GRIS)
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, 1.5 * cm, w - 2 * cm, 1.5 * cm)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.1 * cm, "Venezuela — Guía Turística")
    canvas.drawRightString(w - 2 * cm, 1.1 * cm, "Página %d" % doc.page)
    canvas.restoreState()

def dibujar_membrete(canvas, doc):
    """Banda tricolor fina arriba de las páginas interiores."""
    canvas.saveState()
    w, h = A4
    strip = h / 2 / 60
    canvas.setFillColor(AMARILLO); canvas.rect(0, h - strip, w, strip, stroke=0, fill=1)
    canvas.setFillColor(AZUL);     canvas.rect(0, h - 2 * strip, w, strip, stroke=0, fill=1)
    canvas.setFillColor(ROJO);     canvas.rect(0, h - 3 * strip, w, strip, stroke=0, fill=1)
    canvas.restoreState()

# ---------------------------------------------------------------- doc
doc = BaseDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2.2 * cm, bottomMargin=2 * cm,
    title="Venezuela - Guia Turistica",
    author="Generado con reportlab")

frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id="principal")

doc.addPageTemplates([
    PageTemplate(id="portada", frames=[frame], onPage=dibujar_fondo_portada),
    PageTemplate(id="interior", frames=[frame],
                 onPage=lambda c, d: (dibujar_membrete(c, d), dibujar_pie(c, d))),
])

story = []

# ================================================================ PORTADA
story.append(Spacer(1, 8.2 * cm))
story.append(Paragraph("VENEZUELA", est_titulo))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Guía Turística", est_subtitulo))
story.append(Spacer(1, 0.35 * cm))
story.append(Paragraph(
    "Salto Ángel · Canaima · Los Roques · Margarita · Roraima · Mérida",
    ParagraphStyle("sub2", parent=est_subtitulo, fontSize=11, leading=15)))
story.append(NextPageTemplate("interior"))
story.append(PageBreak())

# ================================================================ INTRO
story.append(Paragraph("Bienvenido a Venezuela", est_h1))
story.append(Paragraph(
    "Venezuela, oficialmente República Bolivariana de Venezuela, es un país del norte de "
    "Sudamérica bañado por el mar Caribe y el océano Atlántico. Su increíble diversidad "
    "geográfica —playas caribeñas, montañas andinas, selvas amazónicas y los tepuyes más "
    "antiguos del planeta— la convierte en un destino único para los viajeros que buscan "
    "naturaleza, aventura y cultura.", est_body))

story.append(Paragraph("Datos rápidos", est_h2))
tabla_datos = Table([
    ["<b>Capital</b>", "Caracas"],
    ["<b>Idioma oficial</b>", "Español"],
    ["<b>Moneda</b>", "Bolívar (VES); se acepta ampliamente el dólar estadounidense"],
    ["<b>Huso horario</b>", "UTC−4"],
    ["<b>Clima</b>", "Tropical; seco (dic–abr) y lluvioso (may–nov)"],
    ["<b>Electricidad</b>", "120 V / 60 Hz (enchufes tipo A y B)"],
    ["<b>Mejor época para viajar</b>", "Diciembre a abril (temporada seca)"],
    ["<b>Preparativos</b>", "Vacunas (fiebre amarilla), repelente, efectivo en dólares"],
], colWidths=[4.2 * cm, 12.3 * cm])
tabla_datos.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ("BACKGROUND", (0, 0), (0, -1), CREMA),
    ("BACKGROUND", (1, 0), (1, -1), colors.white),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(tabla_datos)
story.append(Spacer(1, 0.5 * cm))

story.append(Paragraph(
    "Aviso importante: la situación política y económica del país ha dificultado el turismo "
    "internacional en años recientes. Antes de viajar, verifica los avisos de tu ministerio de "
    "exteriores, contrata un seguro de viaje con cobertura médica y organiza tu itinerario con "
    "operadores locales de confianza.", est_body))
story.append(PageBreak())

# ================================================================ DESTINOS
story.append(Paragraph("Destinos imperdibles", est_h1))
story.append(Paragraph(
    "Estos son los lugares más emblemáticos que no puedes dejar de ver en Venezuela.",
    est_body))

def seccion_destino(nombre, region, descripcion, imperdibles):
    """Crea el bloque visual de un destino con encabezado de color."""
    header = Table([[Paragraph(
        "<b>%s</b>  <font color='#FFFFFF' size='9'>— %s</font>" % (nombre, region),
        ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=14, leading=18,
                       textColor=colors.white))]],
        colWidths=[doc.width])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    items = [Paragraph("Imperdibles:", est_h2)]
    for imp in imperdibles:
        items.append(Paragraph(imp, est_bullet, bulletText="•"))
    bloque = [header, Spacer(1, 0.3 * cm), Paragraph(descripcion, est_body)] + items
    return KeepTogether(bloque)

destinos = [
    ("Salto Ángel y el Parque Nacional Canaima",
     "Estado Bolívar",
     "El Salto Ángel es la cascada más alta del mundo, con 979 metros de caída libre desde el "
     "tepuy Auyantepui. El Parque Nacional Canaima, Patrimonio de la Humanidad por la UNESCO, "
     "abarca selvas, ríos de aguas rojizas y las imponentes mesetas tabulares (tepuyes) que "
     "inspiraron la novela El mundo perdido de Arthur Conan Doyle. Se visita en excursiones de "
     "varios días partiendo de Ciudad Bolívar o del propio campamento de Canaima.",
     ["Vuelo o caminata hasta la base del Salto Ángel y paseo en curiara",
      "Laguna de Canaima con sus siete saltos y playas de arena rosada",
      "Sapo Falls: caminata tras la cortina de agua",
      "Trekking al mirador del Auyantepui (2–3 días)"],
    ),
    ("Los Roques",
     "Dependencias Federales",
     "Un archipiélago de más de 300 islas y cayos de arena blanca rodeados de aguas turquesa, "
     "declarado parque nacional en 1972. Es el paraíso caribeño de Venezuela: aquí el tiempo "
     "parece detenerse entre chiringuitos de pescadores, arrecifes de coral y atardeceres "
     "increíbles. Se llega en avioneta desde Caracas en unos 30 minutos.",
     ["Gran Roque: el único pueblo del archipiélago",
      "Cayo de Agua y Cayo Francés: los bancos de arena más fotografiados",
      "Buceo y esnórquel entre corales, tortugas y rayas",
      "Pesca deportiva y kitesurf"],
    ),
    ("Isla de Margarita",
     "Estado Nueva Esparta",
     "La mayor isla de Venezuela combina playas caribeñas, historia colonial y buenas compras "
     "en su zona franca. Playa El Agua, Playa Parguito y la península de Macanao ofrecen "
     "paisajes para todos los gustos, mientras que La Asunción y Pampatar conservan fortalezas "
     "y casas de la época colonial.",
     ["Playa El Agua y Playa Parguito",
      "Fortín de La Galera y Castillo San Carlos Borromeo",
      "Parque Nacional Laguna de La Restinga (paseos en peñero)",
      "Compras en la zona franca de Porlamar"],
    ),
    ("Monte Roraima",
     "Estado Bolívar",
     "El tepuy más famoso del mundo, con 2.810 m de altura y frontera natural con Brasil y "
     "Guyana. Sus cumbres de arenisca albergan plantas carnívoras, anfibios endémicos y "
     "paisajes lunares. El ascenso es una expedición de 6 a 8 días guiada por indígenas "
     "pemones, que consideran la montaña sagrada.",
     ["Ascenso de 6–8 días con guías pemones",
      "El 'Valle de los Cristales' y las ventanas de la cumbre",
      "Plantas carnívoras y flora endémica",
      "Amanecer desde el punto más alto del tepuy"],
    ),
    ("Mérida y la Sierra Nevada",
     "Estado Mérida",
     "Ciudad universitaria y andina a 1.600 m, rodeada de los picos más altos de Venezuela: "
     "el Bolívar (4.978 m), Humboldt y Bonpland. Su teleférico, el más alto y largo del mundo "
     "en su tipo, llega hasta el Pico Espejo (4.765 m) y es una de las experiencias "
     "imprescindibles del país.",
     ["Teleférico Mukumbarí hasta el Pico Espejo",
      "Trekking al Pico Bolívar (con guía y aclimatación)",
      "Mucuchíes y el páramo andino",
      "Gastronomía local: arepas andinas y dulce de leche"],
    ),
    ("Los Llanos",
     "Estados Apure y Barinas",
     "Las vastas llanuras del centro-sur son la sabana africana de Sudamérica: un paraíso para "
     "el avistamiento de fauna silvestre. En los hatos (ranchos) turísticos se hacen safaris a "
     "caballo, en jeep o en bongo, donde es fácil ver chigüires (capibaras), caimanes, "
     "garzas, anacondas y, con suerte, jaguares.",
     ["Safari de fauna en los hatos llaneros",
      "Cabalgatas al atardecer",
      "Pesca deportiva del pavón",
      "Música llanera: arpa, cuatro y maracas"],
    ),
    ("Choroní y el Parque Nacional Henri Pittier",
     "Estado Aragua",
     "Pueblo colonial de calles empedradas al pie de la selva nublada, a solo dos horas de "
     "Caracas. El parque Henri Pittier, el más antiguo de Venezuela, protege más de 500 "
     "especies de aves y desciende desde la montaña hasta playas vírgenes como Playa Grande, "
     "Playa Catica y La Choroní.",
     ["Playa Grande y Playa Catica",
      "Senderismo por la selva nublada y cascadas",
      "Observación de aves (tucanes, guacamayas)",
      "Cacao y chocolate artesanal de la costa"],
    ),
    ("Parque Nacional Morrocoy",
     "Estado Falcón",
     "Un conjunto de cayos y manglares en la costa caribeña, famoso por sus aguas someras y "
     "transparentes. Es el destino favorito de los caraqueños para escapar el fin de semana: "
     "se recorre en lancha saltando de playa en playa.",
     ["Cayo Sombrero y Cayo Sal",
      "Paseos en lancha entre los cayos",
      "Esnórquel en aguas cristalinas",
      "Pueblo pesquero de Tucacas y gastronomía marina"],
    ),
]

for nombre, region, desc, imperdibles in destinos:
    story.append(seccion_destino(nombre, region, desc, imperdibles))
    story.append(Spacer(1, 0.55 * cm))

story.append(PageBreak())

# ================================================================ GASTRONOMIA
story.append(Paragraph("Sabores de Venezuela", est_h1))
story.append(Paragraph(
    "La cocina venezolana es un mestizaje de tradiciones indígenas, africanas y europeas. "
    "Estos son los platos y productos que debes probar:", est_body))

platos = [
    ("La arepa", "el pan de cada día: disco de maíz relleno de queso, carne mechada, "
     "pernil, aguacate o caraotas. Prueba la 'reina pepiada' (pollo con aguacate)."),
    ("El pabellón criollo", "plato nacional: arroz, caraotas negras, carne mechada, "
     "plátano frito y huevo frito."),
    ("La cachapa", "tortilla dulce de maíz tierno con queso de mano."),
    ("Las hallacas", "tamal navideño de harina de maíz relleno de guiso de carne, "
     "envuelto en hojas de plátano."),
    ("El asado negro", "carne de res en salsa oscura dulce, acompañada de arroz y tajadas."),
    ("La arepa de huevo", "especialidad de la costa oriental, rellena de huevo frito."),
    ("El dulce de lechosa", "papaya verde en almíbar con papelón, típico de Semana Santa."),
    ("El ron y el cocuy", "los destilados nacionales; el ron venezolano es premiado "
     "internacionalmente."),
]
for nombre, desc in platos:
    story.append(Paragraph("<b>%s:</b> %s" % (nombre, desc), est_bullet, bulletText="•"))

story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Consejos prácticos", est_h2))
consejos = [
    "Lleva efectivo en dólares y bolívares en billetes pequeños; el cambio de moneda es "
    "complicado y muchas operaciones son en efectivo.",
    "Usa repelente de mosquitos y protector solar en todas las zonas costeras y selváticas.",
    "El transporte interno se realiza en avión (para Los Roques, Canaima o Margarita), "
    "autobuses largos o vehículos con chofer privado.",
    "La electricidad puede sufrir cortes; lleva baterías externas y una linterna.",
    "Vacúnate contra la fiebre amarilla al menos 10 días antes de viajar a zonas selváticas.",
    "Contrata un seguro de viaje internacional con cobertura de evacuación médica.",
]
for c in consejos:
    story.append(Paragraph(c, est_bullet, bulletText="•"))

story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph(
    "<i>Documento informativo generado con fines turísticos. Verifica siempre las "
    "recomendaciones oficiales de viaje vigentes antes de planificar tu visita.</i>",
    est_caption))

# ================================================================ construir
doc.build(story)
print("PDF generado:", OUT)
print("Tamaño:", os.path.getsize(OUT), "bytes")

// ===== Menú móvil =====
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');

menuToggle.addEventListener('click', () => {
  menuToggle.classList.toggle('open');
  mobileMenu.classList.toggle('open');
});

mobileMenu.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuToggle.classList.remove('open');
    mobileMenu.classList.remove('open');
  });
});

// ===== Formulario CTA =====
const ctaForm = document.getElementById('ctaForm');
const ctaNote = document.getElementById('ctaNote');

ctaForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = ctaForm.querySelector('input[type="email"]').value;
  ctaNote.textContent = `🔥 ¡Listo, ${email}! Mañana recibirás tu plan del día. Nos vemos en la barra.`;
  ctaForm.reset();
});

// ===== Pestañas de rutinas por día =====
const semanaTabs = document.querySelectorAll('.semana__tab');
const rutinas = document.querySelectorAll('.rutina');

semanaTabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    semanaTabs.forEach((t) => t.setAttribute('aria-selected', 'false'));
    tab.setAttribute('aria-selected', 'true');
    const id = `dia-${tab.dataset.dia}`;
    rutinas.forEach((r) => {
      r.classList.toggle('is-active', r.id === id);
    });
  });
});

// ===== Animación de aparición al hacer scroll =====
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll('.card, .faq__item, .ladder__row').forEach((el) => {
  el.classList.add('reveal');
  observer.observe(el);
});

// ===== Resaltar enlace del navbar activo =====
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.navbar__links a');

window.addEventListener('scroll', () => {
  const scrollPos = window.scrollY + 100;
  let current = '';

  sections.forEach((section) => {
    if (scrollPos >= section.offsetTop) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach((link) => {
    link.style.color = link.getAttribute('href') === `#${current}` ? 'var(--primary)' : '';
  });
});

// ===== Generador del plan del día =====
const RUTINAS_JS = {
  principiante: {
    empuje: [
      ['Flexiones en pared', '3 × 8-12', '60 s'],
      ['Flexiones de rodillas', '3 × 6-10', '60 s'],
      ['Fondos en banco', '3 × 8-12', '60 s'],
      ['Plancha (rodillas)', '3 × 20-30 s', '45 s'],
    ],
    traccion: [
      ['Dominada australiana (agarre ancho)', '3 × 8-12', '75 s'],
      ['Dominada australiana (agarre supino)', '3 × 8-12', '75 s'],
      ['Remo con toalla / anillas', '3 × 8-12', '60 s'],
      ['Encogimientos en barra', '3 × 10-15', '45 s'],
    ],
    piernas_core: [
      ['Sentadilla con peso corporal', '3 × 12-20', '60 s'],
      ['Zancadas alternas', '3 × 8-10 por pierna', '60 s'],
      ['Puente de glúteo', '3 × 12-15', '45 s'],
      ['Plancha frontal', '3 × 20-40 s', '45 s'],
      ['Elevaciones de pierna tumbado', '3 × 10-15', '45 s'],
    ],
  },
  intermedio: {
    empuje: [
      ['Flexiones completas', '4 × 10-15', '75 s'],
      ['Flexiones diamante', '3 × 6-10', '75 s'],
      ['Fondos en paralelas', '3 × 8-12', '90 s'],
      ['Flexiones con pies elevados', '3 × 8-12', '75 s'],
      ['Plancha frontal', '3 × 45-60 s', '45 s'],
    ],
    traccion: [
      ['Dominadas con banda / negativas', '4 × 5-8', '90 s'],
      ['Dominada australiana a una mano (regresión)', '3 × 6-10', '75 s'],
      ['Remo en barra (agarre neutro)', '3 × 10-12', '75 s'],
      ['Encogimientos en barra', '3 × 15-20', '45 s'],
    ],
    piernas_core: [
      ['Sentadilla búlgara asistida', '3 × 8-10 por pierna', '75 s'],
      ['Pistol squat asistido', '3 × 5-8 por pierna', '90 s'],
      ['Puente de glúteo a una pierna', '3 × 8-12', '60 s'],
      ['Hollow body hold', '3 × 20-40 s', '45 s'],
      ['L-sit (pies en suelo / rodillas)', '3 × 15-30 s', '45 s'],
    ],
  },
  avanzado: {
    empuje: [
      ['Flexiones archer', '4 × 6-10', '90 s'],
      ['Flexiones en anillas / pseudo-planche', '4 × 6-10', '90 s'],
      ['Fondos lastrados', '4 × 8-12', '90 s'],
      ['Handstand push-up (o negativas)', '3 × 3-6', '2 min'],
    ],
    traccion: [
      ['Dominadas lastradas / archer', '4 × 5-8', '2 min'],
      ['Muscle-up (o transiciones)', '3 × 3-5', '2 min'],
      ['Dominadas con agarre tipo L', '3 × 5-8', '2 min'],
      ['Front lever (tuck → avanzado)', '3 × 10-20 s', '90 s'],
    ],
    piernas_core: [
      ['Pistol squat', '3 × 5-8 por pierna', '2 min'],
      ['Shrimp squat', '3 × 5-8 por pierna', '2 min'],
      ['Nordic curl (regresión)', '3 × 5-8', '90 s'],
      ['Dragon flag (o negativas)', '3 × 5-8', '90 s'],
      ['L-sit completo', '3 × 15-30 s', '60 s'],
    ],
  },
};

const HABILIDADES_JS = {
  'primera dominada': [
    'Dominada australiana baja: 5 × máx con 90 s de descanso.',
    'Negativas lentas (bajar 5 s): 5 × 3-5.',
    'Dominadas con banda de asistencia: 4 × 5-8.',
  ],
  handstand: [
    'Pino en pared: 5 × 30-60 s manteniendo el cuerpo alineado.',
    'Equilibrio a una pierna en pared: 4 × 20-30 s por lado.',
    'Patinadas (wall walks) hacia el pino: 3 × 5 repeticiones.',
  ],
  'muscle-up': [
    'Transiciones (de dominada a fondos) con banda: 5 × 3-5.',
    'Dominadas explosivas hasta el pecho: 4 × 5.',
    'Fondos en paralelas profundos: 4 × 8-10.',
  ],
  planche: [
    'Planche tuck: 5 × 10-20 s.',
    'Planche tuck con una pierna extendida: 4 × 8-15 s.',
    'Pseudo-planche push-ups: 4 × 6-10.',
  ],
  'front lever': [
    'Front lever tuck: 5 × 15-25 s.',
    'Front lever tuck con una pierna extendida: 4 × 8-15 s.',
    'Dominadas en posición hueca: 4 × 6-8.',
  ],
};

const CALENTAMIENTO_JS = [
  'Rotaciones de cuello y hombros (círculos) — 1 min',
  'Movilidad de muñecas (flex/ext + círculos) — 1 min',
  'Balanceos de pierna y sentadillas de movilidad — 2 min',
  'Activación: 10 flexiones suaves + 10 dominadas australianas fáciles',
  'Elevar pulsaciones: saltos de tijera / mountain climbers — 2 min',
];

const ENFRIAMIENTO_JS = [
  'Estiramiento de pecho y hombros (puerta / pared) — 2 min por lado',
  'Estiramiento de dorsal y espalda (agarre en barra) — 1 min',
  'Estiramiento de cuádriceps e isquios — 1 min por lado',
  'Respiración profunda / relajación — 2 min',
];

const ETIQUETAS_JS = {
  empuje: '💪 EMPUJE',
  traccion: '🏋️ TRACCIÓN',
  piernas_core: '🦵 PIERNAS + CORE',
};

const NIVEL_LABEL = {
  principiante: 'Principiante',
  intermedio: 'Intermedio',
  avanzado: 'Avanzado',
};

const dayPlanForm = document.getElementById('dayPlanForm');
const dayplanOut = document.getElementById('dayplanOut');

function escaparHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

dayPlanForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const nivel = document.getElementById('dpNivel').value;
  const objetivo = document.getElementById('dpObjetivo').value;
  const bloque = document.getElementById('dpBloque').value;

  const rutina = RUTINAS_JS[nivel][bloque];
  const habilidades = HABILIDADES_JS[objetivo];
  const diaActual = new Date().toLocaleDateString('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });

  const planCard = document.createElement('div');
  planCard.className = 'plan-card';

  planCard.innerHTML = `
    <div class="plan-card__head">
      <h3>Plan del día — ${escaparHTML(diaActual)}</h3>
      <span class="plan-card__badge">${ETIQUETAS_JS[bloque]}</span>
    </div>

    <div class="plan-block">
      <h4>🔥 Calentamiento <span>(5-8 min)</span></h4>
      <ol>
        ${CALENTAMIENTO_JS.map((i) => `<li>${escaparHTML(i)}</li>`).join('')}
      </ol>
    </div>

    <div class="plan-block">
      <h4>💪 Entrenamiento principal <span>· Nivel ${NIVEL_LABEL[nivel]} · ~30 min</span></h4>
      ${rutina
        .map(
          ([ej, reps, desc]) => `
            <div class="plan-ej">
              <strong>${escaparHTML(ej)}</strong>
              <span class="plan-ej__reps">${escaparHTML(reps)}</span>
              <span class="plan-ej__rest">descanso ${escaparHTML(desc)}</span>
            </div>`
        )
        .join('')}
    </div>

    <div class="plan-block">
      <h4>🎯 Foco del día <span>· objetivo: ${escaparHTML(objetivo)}</span></h4>
      <ol>
        ${habilidades.map((i) => `<li>${escaparHTML(i)}</li>`).join('')}
      </ol>
    </div>

    <div class="plan-block">
      <h4>🧘 Enfriamiento <span>(5 min)</span></h4>
      <ol>
        ${ENFRIAMIENTO_JS.map((i) => `<li>${escaparHTML(i)}</li>`).join('')}
      </ol>
    </div>

    <div class="plan-tip">💡 Forma perfecta &gt; más repeticiones. Si dominas el ejercicio sin llegar al fallo, la próxima vez sube 1-2 reps.</div>
  `;

  dayplanOut.innerHTML = '';
  dayplanOut.appendChild(planCard);
  dayplanOut.hidden = false;
  dayplanOut.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

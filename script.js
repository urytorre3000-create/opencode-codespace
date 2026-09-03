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

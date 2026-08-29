// ===== Menú móvil =====
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');

menuToggle.addEventListener('click', () => {
  menuToggle.classList.toggle('open');
  mobileMenu.classList.toggle('open');
});

// Cerrar el menú móvil al hacer clic en un enlace
mobileMenu.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuToggle.classList.remove('open');
    mobileMenu.classList.remove('open');
  });
});

// ===== Cambio de precios mensual / anual =====
const billingToggle = document.getElementById('billingToggle');

billingToggle.addEventListener('change', () => {
  const isYearly = billingToggle.checked;
  document.querySelectorAll('.amount').forEach((amount) => {
    const value = isYearly
      ? amount.dataset.yearly
      : amount.dataset.monthly;
    amount.textContent = value;
  });
});

// ===== Formulario CTA =====
const ctaForm = document.getElementById('ctaForm');
const ctaNote = document.getElementById('ctaNote');

ctaForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = ctaForm.querySelector('input[type="email"]').value;
  ctaNote.textContent = `🎉 ¡Gracias ${email}! Te hemos enviado un email para activar tu cuenta.`;
  ctaForm.reset();
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
  { threshold: 0.15 }
);

document.querySelectorAll('.card, .faq__item').forEach((el) => {
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

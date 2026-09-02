document.documentElement.classList.add('js');

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reduceMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }),
    { threshold: 0.12 }
  );

  document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
} else {
  document.querySelectorAll('.reveal').forEach((element) => element.classList.add('is-visible'));
}

document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    const status = button.parentElement.querySelector('.copy-status');
    if (!target || !navigator.clipboard) {
      status.textContent = 'Selecione e copie o comando manualmente.';
      return;
    }

    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      button.textContent = 'Copiado';
      status.textContent = 'Comando copiado para a área de transferência.';
      window.setTimeout(() => { button.textContent = 'Copiar'; }, 1800);
    } catch {
      status.textContent = 'Selecione e copie o comando manualmente.';
    }
  });
});

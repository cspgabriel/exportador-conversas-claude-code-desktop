document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const source = document.getElementById(button.dataset.copyTarget);
    const status = button.parentElement.querySelector('.copy-status');
    if (!source || !navigator.clipboard) { status.textContent = 'Selecione e copie o comando manualmente.'; return; }
    try {
      await navigator.clipboard.writeText(source.textContent.trim());
      button.textContent = 'COPIADO';
      status.textContent = 'Comando copiado para a área de transferência.';
      window.setTimeout(() => { button.textContent = 'COPIAR COMANDO'; }, 1800);
    } catch { status.textContent = 'Selecione e copie o comando manualmente.'; }
  });
});

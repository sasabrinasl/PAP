function goToPage(pageId) {
    // Esconde todas as páginas
    document.querySelectorAll('body > div:not(.header)').forEach(page => {
        page.style.display = 'none';
    });

    // Mostra a página selecionada
    document.getElementById(pageId).style.display = 'block';
}

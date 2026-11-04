/* Progressive enhancement: all chapters, links, and resource cards work without JS. */
(() => {
  const menu = document.querySelector('.chapter-menu');
  if (menu && window.matchMedia('(max-width: 900px)').matches) menu.open = false;

  document.querySelectorAll('[data-print]').forEach(button => {
    button.addEventListener('click', () => window.print());
  });

  const filters = document.querySelector('[data-library-filters]');
  if (filters) {
    const cards = [...document.querySelectorAll('[data-resource]')];
    const count = document.querySelector('[data-resource-count]');
    const empty = document.querySelector('[data-empty-state]');
    const field = name => filters.elements.namedItem(name);
    const apply = () => {
      const words = field('q').value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      const topic = field('topic').value;
      const format = field('format').value;
      const access = field('access').value;
      let visible = 0;
      for (const card of cards) {
        const matches = words.every(word => card.dataset.search.includes(word)) &&
          (!topic || card.dataset.topics.split('|').includes(topic)) &&
          (!format || card.dataset.format === format) &&
          (!access || card.dataset.access === access);
        card.hidden = !matches;
        if (matches) visible++;
      }
      count.textContent = `${visible} of ${cards.length} resources`;
      empty.hidden = visible !== 0;
    };
    filters.hidden = false;
    filters.addEventListener('submit', event => event.preventDefault());
    filters.addEventListener('input', apply);
    filters.addEventListener('change', apply);
    filters.addEventListener('reset', () => setTimeout(apply, 0));
    apply();
    document.querySelectorAll('[data-starter-link]').forEach(link => {
      link.addEventListener('click', event => {
        const target = document.getElementById(link.hash.slice(1));
        if (!target) return;
        event.preventDefault();
        filters.reset();
        apply();
        target.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
        target.focus({preventScroll:true});
        history.replaceState(null,'',link.hash);
      });
    });
  }

  const links = [...document.querySelectorAll('.page-toc .toc-list a')];
  if (links.length && 'IntersectionObserver' in window) {
    const byId = new Map(links.map(link => [decodeURIComponent(link.hash.slice(1)), link]));
    const observer = new IntersectionObserver(entries => {
      const current = entries.filter(entry => entry.isIntersecting)
        .sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (!current) return;
      for (const link of links) link.classList.remove('is-current');
      byId.get(current.target.id)?.classList.add('is-current');
    }, {rootMargin:'-5% 0px -68% 0px',threshold:0});
    for (const id of byId.keys()) {
      const heading = document.getElementById(id);
      if (heading) observer.observe(heading);
    }
  }
})();

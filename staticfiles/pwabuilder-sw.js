// Nome do cache para os arquivos offline
const CACHE = "pwabuilder-offline-page";

// Carregar o Workbox para estratégias de cache
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// Página de fallback quando estiver offline
const offlineFallbackPage = "offline.html"; // Substitua com o nome correto da sua página de fallback

// Evento de mensagem para forçar a ativação imediata
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();  // Faz o Service Worker assumir o controle imediatamente
  }
});

// Evento de instalação: abre o cache e adiciona a página de fallback
self.addEventListener('install', async (event) => {
  console.log('Service Worker instalado');
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.add(offlineFallbackPage)) // Adiciona a página de fallback ao cache
  );
  self.skipWaiting(); // Força a ativação imediata
});

// Evento de ativação: garante que o novo Service Worker assuma imediatamente
self.addEventListener('activate', (event) => {
  console.log('Service Worker ativado');
  event.waitUntil(self.clients.claim()); // Faz o Service Worker controlar as páginas abertas
});

// Habilita a navegação pré-carregada se for suportada
if (workbox.navigationPreload.isSupported()) {
  workbox.navigationPreload.enable();
}

// Estratégia de cache: "Stale While Revalidate" para todos os arquivos estáticos como JS, CSS, imagens, etc.
workbox.routing.registerRoute(
  new RegExp('.*\.(?:js|css|html|png|jpg|jpeg|svg|woff2?)'), // Pode ajustar conforme necessário
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE // Nome do cache para arquivos estáticos
  })
);

// Estratégia de cache para navegação: retorna a página de fallback caso esteja offline
self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        // Tentativa de usar a resposta pré-carregada
        const preloadResp = await event.preloadResponse;

        if (preloadResp) {
          return preloadResp; // Se a resposta pré-carregada estiver disponível, usa-a
        }

        // Tentativa de buscar a resposta da rede
        const networkResp = await fetch(event.request);
        return networkResp;
      } catch (error) {
        // Se não for possível acessar a rede, retorna a página offline do cache
        const cache = await caches.open(CACHE);
        const cachedResp = await cache.match(offlineFallbackPage);
        return cachedResp;
      }
    })());
  }
});

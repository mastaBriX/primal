// Service Worker 版本号
const CACHE_NAME = 'primal-checker-v1';
const RUNTIME_CACHE = 'primal-runtime-v1';

// 需要缓存的资源
const STATIC_CACHE_URLS = [
  '/',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// 安装 Service Worker
self.addEventListener('install', (event) => {
  console.log('[Service Worker] 安装中...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] 缓存静态资源');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => self.skipWaiting())
  );
});

// 激活 Service Worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] 激活中...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => {
            return cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE;
          })
          .map((cacheName) => {
            console.log('[Service Worker] 删除旧缓存:', cacheName);
            return caches.delete(cacheName);
          })
      );
    })
    .then(() => self.clients.claim())
  );
});

// 拦截网络请求
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // 跳过非 GET 请求
  if (request.method !== 'GET') {
    return;
  }

  // 跳过 API 请求（实时数据，不缓存）
  if (url.pathname === '/check') {
    return;
  }

  // 对于页面和静态资源，使用缓存优先策略
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }

        // 如果缓存中没有，从网络获取
        return fetch(request)
          .then((response) => {
            // 只缓存成功的响应
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // 克隆响应（因为响应流只能使用一次）
            const responseToCache = response.clone();

            // 将响应添加到缓存
            caches.open(RUNTIME_CACHE)
              .then((cache) => {
                cache.put(request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // 如果网络失败，尝试返回离线页面
            if (request.mode === 'navigate') {
              return caches.match('/');
            }
          });
      })
  );
});


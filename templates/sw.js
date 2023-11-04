const cacheName = 'ALE_Hotel'; function precache() {
    return caches.open('my-cache').then(function (cache) {
        return cache.addAll([
            '{% url "unlock_door" %}', 
            '{% url "check_in_out" %}', 
            '{% url "check_in_completed" %}', 
            '{% url "check_in" %}', 
            '{% url "check_out" %}', 
            '{% url "listing" %}', 
            '{% url "stellar_login" %}', 
            '{% url "stellar_login_face" %}', 
            '{% url "home" %}', 
        ]);
    });
}
{% load static %}
const staticAssets = [
    '{% static "css/aos.css" %}',
    '{% static "css/style.css" %}',
    '{% static "css/bootstrap.min.css" %}',
    '{% static "css/bootstrap.min.css" %}',
    '{% static "css/animate.css" %}',
    '{% static "css/owl.carousel.min.css" %}',
    '{% static "css/aos.css" %}',
    '{% static "css/bootstrap-datepicker.css" %}',
    '{% static "css/jquery.timepicker.css" %}',
    '{% static "css/fancybox.min.css" %}',
    '{% static "images/img_1_1.jpg" %}',
    '{% static "images/img_2_2.png" %}',
    '{% static "images/img_3_3.jpg" %}',
    '{% static "images/food-1.jpg" %}',
    '{% static "images/img_1.jpg" %}',
    '{% static "images/slider-1.jpg" %}',
    '{% static "images/slider-2.jpg" %}',
    '{% static "images/slider-3.jpg" %}',
    '{% static "images/slider-4.jpg" %}',
    '{% static "images/slider-5.jpg" %}',
    '{% static "images/slider-6.jpg" %}',
    '{% static "images/slider-7.jpg" %}',
    '{% static "images/hero_4.jpg" %}',


    // YOU CAN ADD ALL YOUR STATIC FILES HERE
];
            
    
self.addEventListener('install', async e => { 
    const cache = await caches.open(cacheName); 
    await cache.addAll(staticAssets); 
    return self.skipWaiting(); 
}); 

self.addEventListener('activate', e => { 
    self.clients.claim(); 
}); 

self.addEventListener('fetch', async e => { 
    const req = e.request; 
    const url = new URL(req.url); 
    if (url.origin === location.origin) { 
        e.respondWith(cacheFirst(req)); 
    } else { 
        e.respondWith(networkAndCache(req)); 
    }
}); 
    
async function cacheFirst(req) { 
    const cache = await caches.open(cacheName); 
    const cached = await cache.match(req); 
    return cached || fetch(req); 
} 

async function networkAndCache(req) { 
    const cache = await caches.open(cacheName);
    try { 
        const fresh = await fetch(req); 
        await cache.put(req, fresh.clone()); 
        return fresh; 
    } catch (e) { 
        const cached = await cache.match(req); 
        return cached; 
    } 
}
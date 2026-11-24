// ===== HERO SLIDER =====
let heroSlides = document.querySelectorAll('.hero-slider .slide');
let heroCurrent = 0;

function showHeroSlide(index) {
    heroSlides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
    });
}

function nextHeroSlide() {
    heroCurrent = (heroCurrent + 1) % heroSlides.length;
    showHeroSlide(heroCurrent);
}

function prevHeroSlide() {
    heroCurrent = (heroCurrent - 1 + heroSlides.length) % heroSlides.length;
    showHeroSlide(heroCurrent);
}

// Auto-slide hero
if (heroSlides.length > 0) {
    setInterval(nextHeroSlide, 5000);
}

document.querySelectorAll('.hero-slider .next').forEach(btn => {
    btn.addEventListener('click', nextHeroSlide);
});

document.querySelectorAll('.hero-slider .prev').forEach(btn => {
    btn.addEventListener('click', prevHeroSlide);
});

// ===== GALLERY SLIDER =====
let gallerySlides = document.querySelectorAll('.gallery-slide');
let galleryCurrent = 0;

function showGallerySlide(index) {
    gallerySlides.forEach((slide, i) => {
        slide.style.display = i === index ? 'block' : 'none';
    });
}

function nextGallerySlide() {
    galleryCurrent = (galleryCurrent + 1) % gallerySlides.length;
    showGallerySlide(galleryCurrent);
}

function prevGallerySlide() {
    galleryCurrent = (galleryCurrent - 1 + gallerySlides.length) % gallerySlides.length;
    showGallerySlide(galleryCurrent);
}

if (gallerySlides.length > 0) {
    showGallerySlide(0);
    setInterval(nextGallerySlide, 4000);
}

document.querySelectorAll('.gallery-arrow.next').forEach(btn => {
    btn.addEventListener('click', nextGallerySlide);
});

document.querySelectorAll('.gallery-arrow.prev').forEach(btn => {
    btn.addEventListener('click', prevGallerySlide);
});

// ===== BOOKING FORM =====
document.getElementById('bookingForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const msgDiv = document.getElementById('bookingMsg');
    
    fetch('/book-table/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        msgDiv.innerHTML = data.success 
            ? `<div class="alert alert-success">${data.message}</div>`
            : `<div class="alert alert-danger">${data.message}</div>`;
        if (data.success) {
            this.reset();
        }
    })
    .catch(error => {
        msgDiv.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
});

// ===== CONTACT FORM =====
document.getElementById('contactForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const msgDiv = document.getElementById('contactMsg');
    
    fetch('/contact/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        msgDiv.innerHTML = data.success 
            ? `<div class="alert alert-success">${data.message}</div>`
            : `<div class="alert alert-danger">${data.message}</div>`;
        if (data.success) {
            this.reset();
        }
    })
    .catch(error => {
        msgDiv.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
});

// ===== LOGIN FORM =====
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const msgDiv = document.getElementById('loginMsg');
    
    fetch('/login/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        msgDiv.innerHTML = data.success 
            ? `<div class="alert alert-success">${data.message}</div>`
            : `<div class="alert alert-danger">${data.message}</div>`;
        if (data.success) {
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        }
    })
    .catch(error => {
        msgDiv.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
});

// ===== SIGNUP FORM =====
document.getElementById('signupForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const msgDiv = document.getElementById('signupMsg');
    
    fetch('/signup/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        msgDiv.innerHTML = data.success 
            ? `<div class="alert alert-success">${data.message}</div>`
            : `<div class="alert alert-danger">${data.message}</div>`;
        if (data.success) {
            setTimeout(() => {
                window.location.href = '/login/';
            }, 1500);
        }
    })
    .catch(error => {
        msgDiv.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
});

// ===== PROFILE FORM =====
document.getElementById('profileForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const msgDiv = document.getElementById('profileMsg');
    
    fetch('/profile/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        msgDiv.innerHTML = data.success 
            ? `<div class="alert alert-success">${data.message}</div>`
            : `<div class="alert alert-danger">${data.message}</div>`;
        if (data.success) {
            // Update display name
            document.getElementById('profileDisplayName').textContent = document.getElementById('profileName').value;
            document.getElementById('profileDisplayEmail').textContent = document.getElementById('profileEmail').value;
        }
    })
    .catch(error => {
        msgDiv.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
});

// ===== CHANGE PASSWORD =====
document.getElementById('savePasswordBtn')?.addEventListener('click', function() {
    const form = document.getElementById('changePasswordForm');
    const formData = new FormData(form);
    const msgDiv = document.getElementById('passwordChangeMsg');
    
    fetch('/change-password/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        msgDiv.innerHTML = data.success 
            ? `<div class="alert alert-success">${data.message}</div>`
            : `<div class="alert alert-danger">${data.message}</div>`;
        if (data.success) {
            form.reset();
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
            }, 1500);
        }
    })
    .catch(error => {
        msgDiv.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again.</div>`;
    });
});

// ===== PASSWORD TOGGLE =====
document.getElementById('togglePassword')?.addEventListener('click', function() {
    const passwordInput = document.getElementById('loginPassword');
    const icon = this.querySelector('i');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});

document.getElementById('toggleSignupPassword')?.addEventListener('click', function() {
    const passwordInput = document.getElementById('signupPassword');
    const icon = this.querySelector('i');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});
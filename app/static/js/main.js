/* ═══════════════════════════════════════════
   GRAY TO GREEN — main.js
   Frontend JS: nav, forms, gallery, API calls
═══════════════════════════════════════════ */

/* ─── NAV: mobile menu & scroll highlight ─── */
document.addEventListener('DOMContentLoaded', () => {

  // Mobile hamburger
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
    });
  }

  // Active nav link
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  // Sticky nav shadow on scroll
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.boxShadow = window.scrollY > 30
        ? '0 4px 30px rgba(0,0,0,0.5)'
        : 'none';
    });
  }

  // ─── QUOTE FORM ───
  const quoteForm = document.getElementById('quoteForm');
  if (quoteForm) {
    initQuoteForm(quoteForm);
  }

  // ─── GALLERY LOAD ───
  const galleryGrid = document.getElementById('galleryGrid');
  if (galleryGrid) {
    loadGallery(galleryGrid);
  }

  // ─── GALLERY FILTER ───
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterGallery(btn.dataset.filter);
    });
  });

  // ─── FILE UPLOAD AREA ───
  const fileArea = document.querySelector('.file-upload-area');
  const fileInput = document.getElementById('projectImages');
  if (fileArea && fileInput) {
    fileArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileChange);
    fileArea.addEventListener('dragover', e => {
      e.preventDefault();
      fileArea.style.borderColor = 'var(--green-light)';
      fileArea.style.background = 'rgba(45,122,45,0.08)';
    });
    fileArea.addEventListener('dragleave', () => {
      fileArea.style.borderColor = '';
      fileArea.style.background = '';
    });
    fileArea.addEventListener('drop', e => {
      e.preventDefault();
      fileArea.style.borderColor = '';
      fileArea.style.background = '';
      fileInput.files = e.dataTransfer.files;
      handleFileChange({ target: fileInput });
    });
  }

  // ─── LOAD SERVICES (homepage preview) ───
  const servicesPreview = document.getElementById('servicesPreview');
  if (servicesPreview) {
    loadServicesPreview(servicesPreview);
  }
});


/* ═══════════════════════════════════════════
   SERVICES
═══════════════════════════════════════════ */

const SERVICES_DATA = [
  {
    id: 'mulch-installation',
    name: 'Mulch Installation',
    icon: '🍂',
    description: 'Fresh mulch installation to protect your plants, suppress weeds, and give your beds a clean, polished look.',
    tag: 'Most Popular'
  },
  {
    id: 'lawn-care',
    name: 'Lawn Care & Maintenance',
    icon: '🌿',
    description: 'Regular mowing, edging, trimming, and seasonal maintenance to keep your lawn looking its best all year.',
    tag: 'Year-Round'
  },
  {
    id: 'landscape-design',
    name: 'Landscape Design',
    icon: '🏡',
    description: 'Custom landscape planning that transforms your outdoor space into something beautiful and functional.',
    tag: 'Custom'
  },
  {
    id: 'hardscaping',
    name: 'Hardscaping',
    icon: '🪨',
    description: 'Patios, walkways, retaining walls, and stone features that add structure and value to your property.',
    tag: 'Premium'
  },
  {
    id: 'tree-shrub-trimming',
    name: 'Tree & Shrub Trimming',
    icon: '✂️',
    description: 'Expert pruning and shaping to keep your trees and shrubs healthy, safe, and looking great.',
    tag: 'Seasonal'
  },
  {
    id: 'clean-ups',
    name: 'Fall & Spring Clean-Ups',
    icon: '🍁',
    description: 'Seasonal cleanup services to prep your yard for winter or wake it up for spring — no job too small.',
    tag: 'Seasonal'
  },
  {
    id: 'rock-stone',
    name: 'Rock & Stone Installation',
    icon: '⛰️',
    description: 'Decorative rock, river stone, and boulder placement for edging, drainage, and curb appeal.',
    tag: 'Design'
  },
  {
    id: 'sod-installation',
    name: 'Sod Installation',
    icon: '🌱',
    description: 'Instant lush lawn with professional sod installation — prep, lay, and aftercare included.',
    tag: 'Transform'
  }
];

async function loadServicesPreview(container) {
  try {
    const res = await fetch('/api/services');
    const data = await res.json();
    if (data.success && data.services) {
      renderServicesPreview(container, data.services.slice(0, 6));
      return;
    }
  } catch (_) {
    // Fall through to dummy data
  }
  renderServicesPreview(container, SERVICES_DATA.slice(0, 6));
}

function renderServicesPreview(container, services) {
  container.innerHTML = services.map(s => `
    <div class="service-card fade-up">
      <span class="service-icon">${s.icon}</span>
      <h3>${s.name}</h3>
      <p>${s.description}</p>
    </div>
  `).join('');
}


/* ═══════════════════════════════════════════
   GALLERY
═══════════════════════════════════════════ */

// Placeholder gallery items for demo (before backend images load)
const GALLERY_PLACEHOLDER = [
  { id: 1, category: 'mulch', title: 'Mulch & Rock Border', label: 'Mulch Installation', beforeAfter: true },
  { id: 2, category: 'design', title: 'Front Bed Redesign', label: 'Landscape Design', beforeAfter: true },
  { id: 3, category: 'hardscape', title: 'Paver Patio Install', label: 'Hardscaping', beforeAfter: true },
  { id: 4, category: 'mulch', title: 'Tree Line Mulch Bed', label: 'Mulch Installation', beforeAfter: true },
  { id: 5, category: 'cleanup', title: 'Spring Cleanup', label: 'Clean-Up', beforeAfter: false },
  { id: 6, category: 'design', title: 'Flower Bed Refresh', label: 'Landscape Design', beforeAfter: true },
  { id: 7, category: 'trimming', title: 'Shrub Edging', label: 'Trimming', beforeAfter: false },
  { id: 8, category: 'hardscape', title: 'Walkway Stones', label: 'Rock Installation', beforeAfter: false },
  { id: 9, category: 'mulch', title: 'Side Yard Beds', label: 'Mulch Installation', beforeAfter: true },
];

const galleryImages = [];

async function loadGallery(container) {
  try {
    const res = await fetch('/api/gallery');
    const data = await res.json();
    if (data.success && data.images && data.images.length > 0) {
      renderGallery(container, data.images);
      return;
    }
  } catch (_) {}
  renderGallery(container, GALLERY_PLACEHOLDER);
}

function renderGallery(container, items) {
  galleryImages.length = 0;
  items.forEach(item => galleryImages.push(item));

  container.innerHTML = items.map(item => `
    <div class="gallery-masonry-item" data-category="${item.category}" data-id="${item.id}">
      ${item.beforeAfter ? '<span class="before-after-badge">Before & After</span>' : ''}
      ${item.imageUrl
        ? `<img src="${item.imageUrl}" alt="${item.title}" loading="lazy">`
        : `<div class="gallery-placeholder" style="height:${200 + (item.id % 3) * 80}px">
            <div class="gallery-placeholder-icon">📷</div>
            <div class="gallery-placeholder-label">${item.label}</div>
          </div>`
      }
      <div class="gallery-label">
        <div class="gallery-label-tag">${item.label}</div>
        <div class="gallery-label-title">${item.title}</div>
      </div>
    </div>
  `).join('');
}

function filterGallery(category) {
  document.querySelectorAll('.gallery-masonry-item').forEach(item => {
    if (category === 'all' || item.dataset.category === category) {
      item.style.display = 'block';
    } else {
      item.style.display = 'none';
    }
  });
}


/* ═══════════════════════════════════════════
   QUOTE FORM
═══════════════════════════════════════════ */

function initQuoteForm(form) {
  // Populate service dropdown
  const serviceSelect = form.querySelector('#serviceId');
  if (serviceSelect) {
    SERVICES_DATA.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.id;
      opt.textContent = s.name;
      serviceSelect.appendChild(opt);
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById('formMessage');
    const submitBtn = form.querySelector('button[type="submit"]');

    // Collect form data
    const formData = {
      fullName: form.fullName.value.trim(),
      phone: form.phone.value.trim(),
      email: form.email.value.trim(),
      address: form.address.value.trim(),
      serviceId: form.serviceId.value,
      lawnSize: form.lawnSize.value,
      description: form.description.value.trim(),
      preferredDate: form.preferredDate.value,
    };

    // Basic validation
    if (!formData.fullName || !formData.phone || !formData.email || !formData.serviceId) {
      showMessage(msgEl, 'error', '⚠️ Please fill in all required fields.');
      return;
    }

    console.log('Quote form data:', formData);

    // Disable button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    try {
      const res = await fetch('/api/quotes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (data.success) {
        showMessage(msgEl, 'success', '✅ ' + (data.message || 'Your quote request was submitted! We\'ll be in touch soon.'));
        form.reset();
        document.querySelector('.file-upload-text span') && (document.querySelector('.file-names') && (document.querySelector('.file-names').textContent = ''));
      } else {
        showMessage(msgEl, 'error', '❌ ' + (data.message || 'Something went wrong. Please try again.'));
      }
    } catch (err) {
      // Dev mode: simulate success if backend isn't running
      console.warn('Backend not reachable, simulating success for dev:', err);
      showMessage(msgEl, 'success', '✅ Quote request received! (Dev mode — backend offline)');
      form.reset();
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Quote Request';
    }
  });
}

function showMessage(el, type, text) {
  if (!el) return;
  el.className = 'form-message ' + type;
  el.textContent = text;
  el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}


/* ═══════════════════════════════════════════
   FILE UPLOAD DISPLAY
═══════════════════════════════════════════ */

function handleFileChange(e) {
  const files = e.target.files;
  const area = document.querySelector('.file-upload-area');
  if (!files.length || !area) return;

  const names = Array.from(files).map(f => f.name).join(', ');
  const textEl = area.querySelector('.file-upload-text');
  if (textEl) {
    textEl.innerHTML = `<span>${files.length} file${files.length > 1 ? 's' : ''} selected</span>: ${names}`;
  }
}


/* ═══════════════════════════════════════════
   APPOINTMENT FORM (contact page)
═══════════════════════════════════════════ */

const apptForm = document.getElementById('appointmentForm');
if (apptForm) {
  apptForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msgEl = document.getElementById('apptMessage');
    const submitBtn = apptForm.querySelector('button[type="submit"]');

    const formData = {
      fullName: apptForm.fullName.value.trim(),
      phone: apptForm.phone.value.trim(),
      email: apptForm.email.value.trim(),
      address: apptForm.address.value.trim(),
      serviceId: apptForm.serviceId.value,
      appointmentDate: apptForm.appointmentDate.value,
      appointmentTime: apptForm.appointmentTime.value,
      notes: apptForm.notes ? apptForm.notes.value.trim() : '',
    };

    console.log('Appointment form data:', formData);

    submitBtn.disabled = true;
    submitBtn.textContent = 'Scheduling...';

    try {
      const res = await fetch('/api/appointments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await res.json();

      if (data.success) {
        showMessage(msgEl, 'success', '✅ ' + (data.message || 'Appointment requested! We\'ll confirm shortly.'));
        apptForm.reset();
      } else {
        showMessage(msgEl, 'error', '❌ ' + (data.message || 'Could not schedule. Please call us directly.'));
      }
    } catch (err) {
      console.warn('Backend offline, simulating success:', err);
      showMessage(msgEl, 'success', '✅ Appointment request received! (Dev mode)');
      apptForm.reset();
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Request Appointment';
    }
  });
}

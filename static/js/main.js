/**
 * TalentHeart Limited — Main JavaScript
 * Progressive enhancement; all core functionality works without JS.
 */

(function () {
  'use strict';

  /* -----------------------------------------------------------------------
     Auto-dismiss flash messages after 5 seconds
  ----------------------------------------------------------------------- */
  document.querySelectorAll('.alert[data-bs-dismiss="alert"]').forEach(function (el) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert && bsAlert.close();
    }, 5000);
  });

  /* -----------------------------------------------------------------------
     Mark active nav link based on current path
  ----------------------------------------------------------------------- */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  /* -----------------------------------------------------------------------
     Confirm dangerous actions (cancel order, etc.)
     Add data-confirm="Your message" to any form or button to trigger.
  ----------------------------------------------------------------------- */
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!window.confirm(el.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  /* -----------------------------------------------------------------------
     Image preview for profile upload
  ----------------------------------------------------------------------- */
  const imageInput = document.getElementById('id_profile_image');
  if (imageInput) {
    imageInput.addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function (e) {
        const preview = document.querySelector('.profile-image-preview');
        if (preview) preview.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  /* -----------------------------------------------------------------------
     Smooth scroll for anchor links
  ----------------------------------------------------------------------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

})();

/* 星空只在页面可见且动态开启时运行，不依赖第三方库。 */
(() => {
  'use strict';

  const canvas = document.getElementById('starfield');
  const context = canvas.getContext('2d');
  const toggle = document.getElementById('motion-toggle');
  const label = toggle.querySelector('[data-motion-label]');
  const languageToggle = document.getElementById('language-toggle');
  const description = document.querySelector('meta[name="description"]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const palette = ['117, 202, 255', '128, 255, 255', '209, 166, 255'];
  const frameInterval = 1000 / 30;

  let width = 0;
  let height = 0;
  let stars = [];
  let frame = 0;
  let previousFrame = 0;
  let elapsed = 0;
  let nextMeteor = 5.5;
  let meteor = null;
  let motionEnabled = !reducedMotion.matches;
  let currentView = 'research';
  let navigationFrame = 0;
  const sectionLinks = [...document.querySelectorAll('.section-nav a[href^="#"]')];
  const pointer = { x: 0, y: 0, targetX: 0, targetY: 0 };

  function updateMotionLabel() {
    const isEnglish = document.documentElement.lang === 'en';
    label.textContent = isEnglish
      ? (motionEnabled ? 'Motion on' : 'Motion off')
      : (motionEnabled ? '动态开启' : '动态暂停');
  }

  function updatePageIdentity() {
    const isEnglish = document.documentElement.lang === 'en';
    const isResearch = currentView === 'research';
    document.title = isEnglish
      ? `Xiang Li | CharlyX · ${isResearch ? 'Research' : 'Campus'}`
      : `李响 | CharlyX · ${isResearch ? '科研经历' : '校园经历'}`;
    if (description) {
      description.content = isEnglish
        ? (isResearch
          ? 'Xiang Li (CharlyX): publications, education, research and industry experience, academic services, and skills in robotics and 3D vision.'
          : 'Xiang Li (CharlyX): education at Dalian University of Technology, student leadership, honors, scholarships, and competitions.')
        : (isResearch
          ? '李响（CharlyX）：论文成果、教育经历、科研经历、实习经历、学术任职与专业技能。'
          : '李响（CharlyX）：大连理工大学教育经历、学生工作任职、荣誉称号、奖学金及竞赛经历。');
    }
    const cvPreview = document.getElementById('cv-preview');
    if (cvPreview) {
      const viewKey = isResearch ? 'Research' : 'Campus';
      cvPreview.href = cvPreview.dataset[`preview${viewKey}${isEnglish ? 'En' : 'Zh'}`]
        || `cv.html?lang=${document.documentElement.lang}&view=${currentView}`;
    }
    const viewStatus = document.getElementById('view-status');
    if (viewStatus) {
      viewStatus.textContent = isEnglish
        ? `${isResearch ? 'Research' : 'Campus'} view selected`
        : `已切换至${isResearch ? '科研经历' : '校园经历'}视图`;
    }
  }

  function updateLocation(method, resetHash = false) {
    const url = new URL(window.location.href);
    url.searchParams.set('view', currentView);
    url.searchParams.set('lang', document.documentElement.lang);
    if (resetHash) url.hash = '';
    const section = document.getElementById(url.hash.slice(1));
    const audience = section?.closest('[data-audience]')?.dataset.audience;
    if ((audience && audience !== currentView) || (section && getComputedStyle(section).display === 'none')) url.hash = '';
    window.history[method]({}, '', url);
  }

  function setView(view, updateHistory = true) {
    // Published Experience links now open the renamed Campus view.
    currentView = view === 'campus' || view === 'experience' ? 'campus' : 'research';
    // Save the previous view's position before its sections change height.
    if (updateHistory) updateLocation('pushState', true);
    document.body.dataset.view = currentView;
    document.querySelectorAll('[data-view-select]').forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.viewSelect === currentView));
    });
    updatePageIdentity();
    if (updateHistory) window.scrollTo({ top: 0, behavior: 'instant' });
    scheduleNavigationUpdate();
  }

  function setLanguage(language, updateHistory = true) {
    const isEnglish = language === 'en';
    document.documentElement.lang = language;
    updatePageIdentity();
    document.querySelectorAll('[data-label-en][data-label-zh]').forEach((element) => {
      const text = isEnglish ? element.dataset.labelEn : element.dataset.labelZh;
      element.setAttribute('aria-label', text);
      element.setAttribute('title', text);
    });
    languageToggle.textContent = isEnglish ? '中文' : 'EN';
    languageToggle.setAttribute('aria-label', isEnglish ? 'Switch to Chinese' : '切换为英文');
    languageToggle.setAttribute('title', isEnglish ? 'Switch to Chinese' : '切换为英文');
    document.querySelectorAll('.email-status').forEach((status) => {
      status.textContent = '';
    });
    updateMotionLabel();
    if (updateHistory) updateLocation('replaceState');
    scheduleNavigationUpdate();
  }

  function restoreLocation() {
    const params = new URLSearchParams(window.location.search);
    setView(params.get('view'), false);
    setLanguage(params.get('lang') === 'zh-CN' ? 'zh-CN' : 'en', false);
    updateLocation('replaceState');
  }

  function updateSectionNavigation() {
    navigationFrame = 0;
    const visibleLinks = sectionLinks.filter(link => link.getClientRects().length);
    const headerBottom = document.querySelector('.site-header').getBoundingClientRect().bottom;
    const scrollPadding = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop);
    const activationTop = Math.max(headerBottom + 32, scrollPadding + 8);
    let active = visibleLinks[0];
    for (const link of visibleLinks) {
      const section = document.getElementById(link.hash.slice(1));
      if (section.getBoundingClientRect().top <= activationTop) active = link;
    }
    sectionLinks.forEach(link => {
      if (link === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  function scheduleNavigationUpdate() {
    if (!navigationFrame) navigationFrame = window.requestAnimationFrame(updateSectionNavigation);
  }

  async function copyEmail(address) {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(address);
        return true;
      }
    } catch {
      // Local-file previews may not have clipboard API access.
    }
    const field = document.createElement('textarea');
    field.value = address;
    field.readOnly = true;
    field.style.cssText = 'position:fixed;left:-9999px;top:0;opacity:0';
    document.body.append(field);
    const previousFocus = document.activeElement;
    field.select();
    let copied = false;
    try {
      copied = document.execCommand('copy');
    } finally {
      field.remove();
      previousFocus?.focus({ preventScroll: true });
    }
    return copied;
  }

  // 固定种子使窗口缩放后的星空分布自然、稳定。
  function makeStars(count) {
    let seed = 112;
    const random = () => {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      return seed / 4294967296;
    };
    return Array.from({ length: count }, () => ({
      x: random(),
      y: random(),
      radius: 0.45 + random() * 1.05,
      opacity: 0.2 + random() * 0.57,
      phase: random() * Math.PI * 2,
      depth: 0.3 + random() * 0.7,
      color: palette[Math.floor(random() * palette.length)],
    }));
  }

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    stars = makeStars(width < 760 ? 65 : 125);
    draw();
  }

  function draw() {
    context.clearRect(0, 0, width, height);

    stars.forEach((star, index) => {
      const x = star.x * width + pointer.x * star.depth;
      const drift = elapsed * (0.7 + star.depth * 0.9);
      const y = ((star.y * height - drift + pointer.y * star.depth) % height + height) % height;
      const twinkle = 0.78 + Math.sin(elapsed * 0.7 + star.phase) * 0.22;
      const alpha = star.opacity * twinkle;
      context.fillStyle = `rgba(${star.color}, ${alpha})`;
      context.beginPath();
      context.arc(x, y, star.radius, 0, Math.PI * 2);
      context.fill();

      // 少量十字星芒，避免每个粒子都产生昂贵的模糊阴影。
      if (index % 17 === 0) {
        context.strokeStyle = `rgba(${star.color}, ${alpha * 0.45})`;
        context.lineWidth = 0.6;
        context.beginPath();
        context.moveTo(x - 3.8, y);
        context.lineTo(x + 3.8, y);
        context.moveTo(x, y - 3.8);
        context.lineTo(x, y + 3.8);
        context.stroke();
      }
    });

    if (meteor) {
      const progress = meteor.age / meteor.duration;
      const x = meteor.x + meteor.age * 610;
      const y = meteor.y + meteor.age * 185;
      const tail = Math.min(155, meteor.age * 480);
      const opacity = Math.sin(progress * Math.PI) * 0.65;
      const gradient = context.createLinearGradient(x - tail, y - tail * 0.303, x, y);
      gradient.addColorStop(0, 'rgba(0, 255, 255, 0)');
      gradient.addColorStop(1, `rgba(190, 237, 255, ${opacity})`);
      context.strokeStyle = gradient;
      context.lineWidth = 1.25;
      context.beginPath();
      context.moveTo(x - tail, y - tail * 0.303);
      context.lineTo(x, y);
      context.stroke();
    }
  }

  function animate(timestamp) {
    frame = 0;
    if (!motionEnabled || document.hidden) return;
    if (!previousFrame) previousFrame = timestamp - frameInterval;
    const difference = timestamp - previousFrame;
    if (difference >= frameInterval) {
      const delta = Math.min(difference / 1000, 0.1);
      previousFrame = timestamp - (difference % frameInterval);
      elapsed += delta;
      pointer.x += (pointer.targetX - pointer.x) * 0.06;
      pointer.y += (pointer.targetY - pointer.y) * 0.06;

      if (elapsed >= nextMeteor && !meteor) {
        meteor = {
          x: width * (0.15 + Math.random() * 0.45),
          y: height * (0.08 + Math.random() * 0.28),
          age: 0,
          duration: 0.85,
        };
        nextMeteor = elapsed + 8 + Math.random() * 7;
      }
      if (meteor) {
        meteor.age += delta;
        if (meteor.age >= meteor.duration) meteor = null;
      }
      draw();
    }
    frame = window.requestAnimationFrame(animate);
  }

  function syncAnimation() {
    window.cancelAnimationFrame(frame);
    frame = 0;
    previousFrame = 0;
    if (motionEnabled && !document.hidden) {
      frame = window.requestAnimationFrame(animate);
    }
  }

  function setMotion(enabled) {
    motionEnabled = enabled;
    document.body.classList.toggle('motion-paused', !enabled);
    document.body.dataset.motion = enabled ? 'on' : 'off';
    toggle.setAttribute('aria-pressed', String(enabled));
    updateMotionLabel();
    syncAnimation();
  }

  languageToggle.addEventListener('click', () => {
    setLanguage(document.documentElement.lang === 'en' ? 'zh-CN' : 'en');
  });
  document.querySelectorAll('[data-view-select]').forEach((button) => {
    button.addEventListener('click', () => {
      if (button.dataset.viewSelect !== currentView) setView(button.dataset.viewSelect);
    });
  });
  window.addEventListener('popstate', restoreLocation);
  window.addEventListener('scroll', scheduleNavigationUpdate, { passive: true });
  window.addEventListener('resize', scheduleNavigationUpdate, { passive: true });
  window.addEventListener('hashchange', scheduleNavigationUpdate);
  toggle.addEventListener('click', () => setMotion(!motionEnabled));
  document.querySelectorAll('.copy-email').forEach((button) => {
    button.addEventListener('click', async () => {
      const copied = await copyEmail(button.dataset.email);
      const status = button.closest('.email-widget').querySelector('.email-status');
      const isEnglish = document.documentElement.lang === 'en';
      status.textContent = copied
        ? (isEnglish ? 'Email address copied' : '邮箱地址已复制')
        : (isEnglish ? 'Copy unavailable. Please use the email icon.' : '暂时无法复制，请点击邮件图标联系。');
    });
  });
  reducedMotion.addEventListener('change', (event) => setMotion(!event.matches));
  document.addEventListener('visibilitychange', syncAnimation);
  window.addEventListener('resize', resize, { passive: true });
  window.addEventListener('pointermove', (event) => {
    pointer.targetX = (event.clientX / width - 0.5) * 12;
    pointer.targetY = (event.clientY / height - 0.5) * 10;
  }, { passive: true });
  document.addEventListener('pointerleave', () => {
    pointer.targetX = 0;
    pointer.targetY = 0;
  });

  restoreLocation();
  resize();
  setMotion(motionEnabled);
})();

'use strict';
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); }
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); });
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenu(); menu.focus(); } });
const stages = [
 ['Attract', 'Reach the right audience.', 'Connect high-intent searches, useful content and distribution so the right people discover your business.'],
 ['Convert', 'Turn interest into qualified opportunities.', 'Bring positioning, proof and clear inquiry paths together to help visitors evaluate your business and take the next step.'],
 ['Grow', 'Build on what works.', 'Connect qualified inquiries to business priorities. Refine search, content and conversion over time through a growth retainer or broader partnership.']
];
const tabs = [...document.querySelectorAll('[data-stage]')];
function activate(button) {
 tabs.forEach(tab => { tab.setAttribute('aria-selected', String(tab === button)); tab.tabIndex = tab === button ? 0 : -1; });
 const [label, title, text] = stages[Number(button.dataset.stage)];
 const panel = document.querySelector('#system-detail'); panel.setAttribute('aria-labelledby', button.id);
 panel.querySelector('.eyebrow').textContent = label; panel.querySelector('h3').textContent = title; panel.querySelector('p').textContent = text;
}
tabs.forEach(tab => {
 tab.addEventListener('click', () => activate(tab));
 tab.addEventListener('keydown', e => { let i = tabs.indexOf(tab); if (['ArrowRight', 'ArrowDown'].includes(e.key)) i = (i + 1) % tabs.length; else if (['ArrowLeft', 'ArrowUp'].includes(e.key)) i = (i - 1 + tabs.length) % tabs.length; else if (e.key === 'Home') i = 0; else if (e.key === 'End') i = tabs.length - 1; else return; e.preventDefault(); activate(tabs[i]); tabs[i].focus(); });
});
function domain(value) {
 try { const u = new URL(/^https?:\/\//i.test(value) ? value : 'https://' + value); if (!/^https?:$/.test(u.protocol) || u.username || u.password || !/^([a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$/i.test(u.hostname)) return null; return u.hostname; } catch { return null; }
}
function emailDraft(id, subject, text) { document.querySelector(id).href = 'mailto:hello@vistadigital.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(text); }
function copy(button, field, status) { document.querySelector(button).addEventListener('click', async () => { const input = document.querySelector(field); try { await navigator.clipboard.writeText(input.value); document.querySelector(status).textContent = 'Copied. Send the request to hello@vistadigital.com to reach Vista.'; } catch { input.focus(); input.select(); document.querySelector(status).textContent = 'Select and copy the request, then email it to hello@vistadigital.com.'; } }); }
const request = document.querySelector('#growth-request');
if (request) {
 const select = document.querySelector('#request-priority');
 const suppliedWebsite = new URLSearchParams(location.search).get('website'); if (suppliedWebsite && domain(suppliedWebsite)) document.querySelector('#request-website').value = domain(suppliedWebsite);
 const priorities = ['generate-qualified-leads', 'improve-search-visibility', 'improve-conversion', 'modernize-your-website', 'connect-your-digital-team'];
 const queryPriority = new URLSearchParams(location.search).get('priority'); const index = priorities.indexOf(queryPriority); if (index >= 0) select.selectedIndex = index;
 request.addEventListener('submit', e => {
  e.preventDefault(); const value = id => document.querySelector(id).value.trim();
  const website = domain(value('#request-website')); const error = document.querySelector('#request-error');
  if (!website) { error.textContent = 'Enter a valid website, such as yourbusiness.com.'; document.querySelector('#request-website').setAttribute('aria-invalid', 'true'); document.querySelector('#request-website').focus(); return; }
  error.textContent = ''; document.querySelector('#request-website').removeAttribute('aria-invalid');
  const text = ['Hello Vista,', '', 'I would like to discuss a Digital Growth Assessment and practical Growth Plan.', '', 'Name: ' + value('#request-name'), 'Company: ' + value('#request-company'), 'Work email: ' + value('#request-email'), 'Website: ' + website, 'Business priority: ' + select.value, 'Business context: ' + (value('#request-context') || 'To discuss'), '', 'Review areas: website performance, search visibility, conversion readiness, content presence and local visibility.', 'Next step: agree the review scope and discuss the findings and suitable engagement.'].join('\n');
  document.querySelector('#request-draft').value = text; emailDraft('#send-request', 'Growth Assessment request — ' + value('#request-company'), text);
  document.querySelector('#request-result').hidden = false; document.querySelector('#request-draft').focus();
 });
 copy('#copy-request', '#request-draft', '#request-status');
}
const contact = document.querySelector('#contact-form');
if (contact) {
 contact.addEventListener('submit', e => { e.preventDefault(); const value = id => document.querySelector(id).value.trim(); const text = ['Hello Vista,', '', 'Name: ' + value('#contact-name'), 'Company: ' + value('#contact-company'), 'Email: ' + value('#contact-email'), 'Website: ' + (value('#contact-website') || 'Not provided'), 'Priority: ' + value('#contact-priority'), '', 'Context:', value('#contact-message')].join('\n'); document.querySelector('#contact-draft').value = text; document.querySelector('#contact-result').hidden = false; emailDraft('#open-email', 'Digital growth enquiry — ' + value('#contact-company'), text); document.querySelector('#contact-status').textContent = 'Review and send the draft in your email app. Nothing has been sent yet.'; document.querySelector('#contact-draft').focus(); });
 copy('#copy-enquiry', '#contact-draft', '#contact-status');
}

const start = document.querySelector('#assessment-start');
if (start) start.addEventListener('submit', e => { const input = document.querySelector('#hero-website'); const host = domain(input.value.trim()); if (!host) { e.preventDefault(); document.querySelector('#hero-website-error').textContent = 'Enter a valid website, such as yourbusiness.com.'; input.setAttribute('aria-invalid', 'true'); input.focus(); } else { input.removeAttribute('aria-invalid'); input.value = host; } });

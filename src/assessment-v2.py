from pathlib import Path
import re
ROOT=Path(__file__).parent.parent
labels=['Website Performance','Search Visibility','Conversion Readiness','Content Presence','Local Visibility']
def apply():
    panel='''<div class="assessment assessment-product" id="assessment"><div class="assessment-cover"><div class="assessment-heading"><p class="eyebrow">Digital Growth Assessment</p><span class="preview-tag">DEMO</span></div><h2>Five signals.<br>Your next opportunity.</h2><p class="cover-caption">A connected perspective on digital growth.</p></div><div class="assessment-body"><form id="assessment-start" novalidate><label for="hero-website">Your website</label><div class="input-group"><input id="hero-website" name="website" placeholder="yourbusiness.com" inputmode="url" autocomplete="url" required maxlength="300" aria-describedby="assessment-disclaimer hero-website-error"><button class="button dark" type="submit">Analyze</button></div><p class="input-error" id="hero-website-error" role="alert"></p></form><p class="fine" id="assessment-disclaimer">Interactive demo · Simulated scores, not a live website analysis.</p><div class="analysis-signal" aria-hidden="true"><i></i><span>VISTA / SIGNAL</span><b>01 — 05</b></div><p id="scan-message" role="status" aria-live="polite">Enter your website to explore the preliminary report.</p><div class="analysis-progress" role="progressbar" aria-label="Demo assessment progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span></span></div><ol class="signal-results">'''+''.join(f'<li data-signal="{i}"><span><small>{i+1:02}</small>{label}</span><strong aria-label="{label}: awaiting analysis">—</strong><div class="signal-meter" aria-hidden="true"><i></i></div></li>' for i,label in enumerate(labels))+'''</ol><div id="assessment-summary" hidden tabindex="-1"><div class="report-total"><div><p class="eyebrow">Digital Growth Score</p><strong id="digital-score">—</strong><span> / 100</span></div><div><strong id="opportunity-count">—</strong><p>illustrative growth<br>opportunities identified</p></div></div><p class="fine">Preliminary demo report for <b id="report-domain"></b>. These values illustrate the experience; they are not findings about this business.</p><button id="full-assessment" class="button orange" type="button">Get My Full Assessment →</button><p class="fine">Next: share your details for Vista follow-up.</p></div></div></div>'''
    for name in ['index.html','assessment/index.html']:
        f=ROOT/'docs'/name;s=f.read_text()
        begin=s.index('<div class="assessment assessment-invitation"');end=s.index('</section>',begin)
        s=s[:begin]+panel+s[end:]
        if name=='assessment/index.html':
            s=s.replace('id="assessment-request" class=', 'id="assessment-request" hidden class=')
            s=s.replace('<h2>Find the gap.<br>Get a practical Growth Plan.</h2>','<h2>Your next step.<br>A full assessment.</h2>')
            s=s.replace('Share your website and business priority to start a review','You have explored the preliminary demo. Share your details to request a real review')
            s=s.replace('<label for="request-website">','<label for="request-phone">Phone <span>(optional)</span></label><input id="request-phone" type="tel" autocomplete="tel" maxlength="50"><label for="request-website">')
        s=s.replace('</body>','<script src="/assessment.js" defer></script></body>');f.write_text(s)
    # All assessment entry links begin at the tool rather than the hidden contact step.
    for f in (ROOT/'docs').rglob('*.html'):
        s=f.read_text()
        s=s.replace('/assessment/#assessment-request','/assessment/#assessment').replace('?priority=generate-qualified-leads#assessment-request','?priority=generate-qualified-leads#assessment')
        s=re.sub(r'(\?priority=[a-z-]+)#assessment-request',r'\1#assessment',s)
        f.write_text(s)
    (ROOT/'docs/assessment.js').write_text((ROOT/'src/assessment.js').read_text())

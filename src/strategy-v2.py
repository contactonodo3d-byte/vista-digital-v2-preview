"""Apply the approved strategy to generated pages. No inferred client results."""
from pathlib import Path
import re, json
from html import escape

ROOT=Path(__file__).parent.parent
D=ROOT/'docs'
CHEV='<svg class="chevron" viewBox="0 0 20 20" aria-hidden="true"><path d="m7 4 6 6-6 6"/></svg>'
def a(url,text,cls='text-link'):
    return f'<a class="{cls}" href="{url}">{text}{CHEV}</a>'
def section(id,label,title,cards,dark=False):
    return f'<section id="{id}" class="strategy-section section-pad {"strategy-dark" if dark else "paper"}"><div class="wrap"><p class="eyebrow">{label}</p><h2>{title}</h2><div class="strategy-cards">'+''.join(f'<article><span class="eyebrow">{i:02}</span><h3>{t}</h3><p>{b}</p></article>' for i,(t,b) in enumerate(cards,1))+'</div></div></section>'

STAGES=[('Attract','Search, content & distribution','Reach the right audience.','Connect high-intent searches, useful content and distribution so the right people discover your business.'),('Convert','Web, trust & customer experience','Turn interest into qualified opportunities.','Bring positioning, proof and clear inquiry paths together to help visitors evaluate your business and take the next step.'),('Grow','Measurement, optimization & continuity','Build on what works.','Connect qualified inquiries to business priorities. Refine search, content and conversion over time through a growth retainer or broader partnership.')]
SYSTEM='<section id="system" class="strategy-dark section-pad system" aria-labelledby="system-title"><div class="wrap"><p class="eyebrow">The Vista Growth System</p><div class="section-heading"><h2 id="system-title">Attract. Convert. Grow.</h2><p>One connected system, built around your business. Start with an assessment and a clear plan; keep improving with evidence.</p></div><div class="system-grid" role="tablist" aria-label="Growth System stages">'+''.join(f'<button role="tab" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" id="stage-{i}" aria-controls="system-detail" data-stage="{i}"><small>{i+1:02}</small><h3>{t}</h3><span>{scope}</span><i class="node" aria-hidden="true"></i><p>{body}</p></button>' for i,(t,scope,title,body) in enumerate(STAGES))+'</div><div class="system-detail" role="tabpanel" id="system-detail" tabindex="0" aria-labelledby="stage-0"><span class="eyebrow">Attract</span><div><h3>'+STAGES[0][2]+'</h3><p>'+STAGES[0][3]+'</p></div></div></div></section>'
ENGAGEMENT=[('Focused project','Resolve a defined gap: a website, positioning or conversion project. Set the scope around the opportunity identified in your Growth Plan.'),('Growth retainer','Build momentum through ongoing search, content, conversion improvement and reporting. Review useful evidence and agree the next priorities.'),('Growth partnership','Connect the broader digital roadmap with business priorities. Coordinate work across channels as a long-term extension of your team.')]
OUTCOMES=[('Get found by the right audience','Connect visibility with the services, customers and markets that matter to your business.'),('Build trust before the conversation','Make your expertise, offer and evidence clear enough for prospective customers to evaluate.'),('Create more qualified opportunities','Give visitors a clear path to an inquiry, consultation or appointment—and measure the quality of those opportunities.')]
WHY=[('Business priorities first','Start with the gap between your business and its digital presence, then decide what deserves investment.'),('Senior-led strategy. Direct collaboration.','Keep the people shaping the strategy close to the work, with clear ownership and a connected view across disciplines.'),('One plan across channels','Bring your website, search, content and marketing together instead of managing disconnected activity.')]
REQUEST='''<section id="assessment-request" class="wrap contact-grid"><div><p class="eyebrow">Digital Growth Assessment</p><h2>Find the gap.<br>Get a practical Growth Plan.</h2><p>Share your website and business priority to start a review of performance, search visibility, conversion readiness, content and local visibility.</p><ol class="request-steps"><li>Send your assessment request.</li><li>Discuss your goals and the scope of the review with Vista.</li><li>Use the findings to prioritize a project, growth retainer or growth partnership.</li></ol><p class="fine">This preview prepares an email request. Review and send it in your email app; it is not submitted automatically.</p></div><form id="growth-request"><div class="contact-field-pair"><div><label for="request-name">Name</label><input id="request-name" required autocomplete="name" maxlength="120"></div><div><label for="request-company">Company</label><input id="request-company" required autocomplete="organization" maxlength="160"></div></div><label for="request-email">Work email</label><input id="request-email" required type="email" autocomplete="email" maxlength="254"><label for="request-website">Your website</label><input id="request-website" required inputmode="url" autocomplete="url" placeholder="yourbusiness.com" maxlength="300"><p id="request-error" class="input-error" role="alert"></p><label for="request-priority">Your business priority</label><select id="request-priority"><option>Generate more qualified inquiries</option><option>Improve search visibility</option><option>Improve conversion</option><option>Modernize our website</option><option>Connect our digital team</option></select><label for="request-context">Business context <span>(optional)</span></label><textarea id="request-context" rows="3" maxlength="1200" placeholder="What has changed, and what needs to improve?"></textarea><p class="fine">Please share business context only. See <a href="/privacy/">how this preview handles your information</a>.</p><button class="button orange" type="submit">Prepare assessment request</button><div id="request-result" hidden><p class="eyebrow">Your next step</p><h3>Review your request, then send it.</h3><textarea id="request-draft" readonly rows="9" aria-label="Assessment request draft"></textarea><div class="contact-result-actions"><a id="send-request" class="button orange" href="mailto:hello@vistadigital.com">Open email to Vista</a><button id="copy-request" class="text-button" type="button">Copy request</button></div><p id="request-status" class="fine" role="status">Your email app opens a draft. Send it there to reach Vista.</p></div></form></section>'''
PANEL='''<div class="assessment assessment-invitation" id="assessment"><div class="assessment-cover"><p class="eyebrow">Digital Growth Assessment</p><h2>Five signals.<br>A clearer starting point.</h2><p class="cover-caption">Business context before digital activity.</p></div><div class="assessment-body"><p class="eyebrow">What the review covers</p><ol class="assessment-scope"><li><span>01</span>Website performance</li><li><span>02</span>Search visibility</li><li><span>03</span>Conversion readiness</li><li><span>04</span>Content presence</li><li><span>05</span>Local visibility</li></ol><form id="assessment-start" action="/assessment/#assessment-request" method="get"><label for="hero-website">Your website</label><div class="input-group"><input id="hero-website" name="website" placeholder="yourbusiness.com" inputmode="url" autocomplete="url" required maxlength="300"><button class="button dark" type="submit">Start assessment</button></div><p class="input-error" id="hero-website-error" role="alert"></p></form><p class="fine">Start with your website and business priority. Build a practical plan for what to improve next.</p><details class="sample-preview"><summary>Preview the assessment format<span aria-hidden="true">+</span></summary><p class="fine">Illustrative example—not a review of your website.</p><p class="eyebrow">Signal → opportunity → next step</p><h3>Search visibility</h3><p>A service page may explain the offer but miss the questions customers search for.</p><p><strong>Possible next step:</strong> connect search intent with clearer service content and an inquiry path.</p></details></div></div>'''

def apply():
    for f in D.rglob('*.html'):
        s=f.read_text()
        s=s.replace('Medical &amp; IV clinics','Medical &amp; wellness').replace('Medical & IV clinics','Medical & wellness')
        s=re.sub(r'<button class="([^"<>]*)" data-contact>(.*?)</button>',lambda m:a('/contact/',m[2],m[1]),s,flags=re.S)
        s=s.replace('href="#assessment"','href="/assessment/#assessment-request"')
        s=s.replace('</nav>','<a class="mobile-action" href="/contact/">Talk to Vista</a><a class="mobile-action mobile-primary" href="/assessment/#assessment-request">Get Your Growth Assessment</a></nav>')
        s=s.replace('href="/assessment/"','href="/assessment/#assessment-request"')
        s=re.sub(r'<section id="system".*?</section>',SYSTEM,s,flags=re.S)
        s=s.replace('Beyond the score','From review to Growth Plan')
        s=s.replace('Four connected stages.','Three connected stages.').replace('Understand your opportunity. Attract the right audience. Convert attention into intent. Improve the system using evidence.','Attract the right audience. Convert interest into qualified opportunities. Grow through measurement, optimization and ongoing collaboration.')
        s=s.replace('Understand, attract, convert and improve','Attract, convert and grow')
        s=re.sub(r'<dialog id="assessment-dialog".*?</dialog>','',s,flags=re.S)
        s=s.replace('src="/script.js"','src="/pages.js"')
        s=s.replace('Assessment results are illustrative · Enquiries are not submitted automatically','US-focused digital growth consultancy')
        s=s.replace('<span>Vista Digital / V2 website prototype</span>','<span>Vista Digital</span>')
        s=s.replace('<a href="/contact/">Contact</a>','<a href="/contact/">Contact</a><a href="/privacy/">Privacy</a>')
        if f==D/'index.html':
            hero=re.search(r'<section class="hero wrap".*?</section>',s,re.S).group()
            hero=hero[:hero.index('<div class="assessment"')]+PANEL+'</section>'
            hero=hero.replace('Digital growth for established businesses','Digital growth for established US businesses').replace('Your business<br>is growing.<br>Your digital presence<br>should be too.','<span class="hero-first">Your business is growing.</span><span class="hero-second">Your digital presence should be too.</span>')
            s=re.sub(r'<section class="hero wrap".*?</section>',lambda m:hero,s,flags=re.S)
            s=re.sub(r'<div class="proof">.*?</div></div><p class="fine">.*?</p></div>','',s,count=1,flags=re.S)
            # Remove the whole proof column using its section boundary, preserving logos.
            s=re.sub(r'<div class="proof">.*?</div></div></section>','</div></section>',s,count=1,flags=re.S)
            s=s.replace('aria-label="Client proof placeholders"','aria-label="Selected portfolio brands"')
            s=s.replace(SYSTEM,SYSTEM+section('outcomes','Business outcomes','Digital work with a business purpose.',OUTCOMES))
            s=re.sub(r'<section id="about".*?</section>',section('about','Why Vista','A boutique consultancy.<br>A connected perspective.',WHY),s,flags=re.S)
            s=s.replace('<section id="industries"',section('engagements','Ways to work together','A focused start.<br>A path to sustained growth.',ENGAGEMENT)+'<section id="industries"')
            articles=[('outgrown-your-website','7 signs your business has outgrown its website'),('traffic-vs-qualified-leads','Website traffic vs. qualified leads'),('where-to-invest-in-digital-growth','Where to invest in digital growth')]
            insights='<section id="insights" class="wrap section-pad"><p class="eyebrow">Growth perspectives</p><h2>Questions worth asking first.</h2><div class="homepage-articles">'+''.join(a('/insights/'+slug+'/',title) for slug,title in articles)+'</div></section>'
            s=re.sub(r'<section id="insights".*?</section>',lambda m:insights,s,flags=re.S)
            assessment_section=section('assessment-next','Your starting point','Clarity before the next investment.',[('Review the five signals','Connect website performance, search, conversion, content and local visibility.'),('Prioritize the opportunity','Use business context to decide what matters first and what can follow.'),('Build your Vista Growth Plan','Connect priorities with a practical scope and a suitable engagement.')],True)
            assessment_section=assessment_section.replace('</div></section>',a('/assessment/#assessment-request','Get Your Growth Assessment','button orange')+'</div></section>')
            s=s.replace('<section class="closing"',assessment_section+'<section class="closing"')
            s=s.replace('Qualified lead / customer','Qualified inquiry').replace('Connect digital to business','Connect attention to opportunity')
            s=s.replace('<h3>Qualified inquiry</h3><p>Connect attention to opportunity</p></div></div></section>','<h3>Qualified inquiry</h3><p>Connect attention to opportunity</p></div><div><span class="signal-node"><i></i><small>04</small></span><h3>Customer &amp; growth</h3><p>Build the relationship over time</p></div></div></section>').replace('A closer look at the brands and businesses in Vista’s published portfolio.','Published work across web, content and brand design. Explore what was delivered and how those capabilities fit a connected growth system.')
            s=s.replace('The work behind<br>the growth.','The work.<br>The business context.')
        if f==D/'assessment/index.html':
            start='<section class="wrap dedicated-assessment"><div><p class="eyebrow">Vista Digital Growth Assessment</p><h1>Find your next<br>growth opportunity.</h1><p class="page-lede">A connected review for established businesses whose digital presence has not kept pace. Turn website, visibility and conversion gaps into a practical Growth Plan.</p></div>'+PANEL+'</section>'+REQUEST
            s=re.sub(r'<section class="wrap dedicated-assessment">.*?</section>',lambda m:start,s,flags=re.S)
            s=re.sub(r'<form id="assessment-start".*?</form>',a('#assessment-request','Start your request','button orange'),s,flags=re.S)
            s=s.replace('Explore Vista’s simulated digital growth assessment and prepare a conversation brief.','Request a connected review of your website, visibility and conversion priorities.')
        if f==D/'about/index.html':
            s=s.replace('<section class="closing"',section('team-model','How collaboration works','A focused team.<br>Clear ownership.',WHY)+'<section class="closing"')
        if '/work/' in str(f) and f.parent.name!='work':
            category=re.search(r'<p class="eyebrow">Published category</p><h3>(.*?)</h3>',s)
            if category:
                scope={'Web':('Website','A clear digital destination helps prospective customers understand a business and take the next step.'),'Content':('Content','Useful, consistent content supports how customers discover and evaluate a business.'),'Design':('Brand & packaging design','A coherent identity helps a business present its offer consistently across customer touchpoints.')}
                delivered,rationale=scope[category[1]]
                proof=section('project-context','Published project record','The work in context.',[('Documented work',delivered+' is the category documented in Vista’s published portfolio.'),('Role in a growth system',rationale+' This explains the capability’s role, rather than claiming a measured result for this project.'),('Evidence available','The published portfolio visual and project category are the available evidence. No performance outcome is claimed.')])
                s=re.sub(r'<section class="paper section-pad">.*?</section>',lambda m:proof,s,count=1,flags=re.S)
        if f==D/'about/index.html':
            s=s.replace('<section class="closing"','<aside class="wrap evidence-pin"><strong>📌 TEAM DETAILS · PLACEHOLDER</strong>Add approved names, roles, biographies and real team photography here. Names and credentials are awaiting approval.</aside><section class="closing"')
        if '/work/' in str(f) and f.parent.name!='work':
            s=s.replace('<section class="closing"','<aside class="wrap evidence-pin"><strong>📌 CASE STUDY EVIDENCE · PLACEHOLDER</strong>Add the approved business challenge, project scope, client quote and documented results here. No sample performance metrics are presented as actual results.</aside><section class="closing"')
        # Responsive derivatives preserve original assets as references.
        s=re.sub(r'<img([^>]*?)src="/assets/existing/([^"]+\.webp)"([^>]*)>',lambda m:f'<img{m[1]}src="/assets/existing/{m[2]}" srcset="/assets/existing/{m[2][:-5]}-640.webp 640w, /assets/existing/{m[2][:-5]}-1280.webp 1280w" sizes="(max-width: 760px) calc(100vw - 40px), 50vw"{m[3]}>' if (D/'assets/existing'/f'{m[2][:-5]}-640.webp').exists() else m[0],s)
        f.write_text(s)
    # Give outcomes their own destination, retaining the visitor's business goal.
    hub=D/'solutions/index.html';s=hub.read_text()
    items=[('generate-qualified-leads','Generate more qualified leads','Connect the right audience with a clear reason to inquire.','Reach high-intent visitors','Build confidence with relevant proof','Measure qualified inquiries'),('improve-search-visibility','Improve search visibility','Be discovered for the services and expertise your business offers.','Understand customer search demand','Connect service content with intent','Review useful visibility and inquiries'),('improve-conversion','Improve conversion','Help the right visitors evaluate your offer and take the next step.','Clarify the value proposition','Connect proof with decisions','Reduce friction in inquiry paths'),('modernize-your-website','Modernize your website','Bring your website up to the level of the business you have built.','Review positioning and structure','Create a credible mobile experience','Connect launch with measurement'),('connect-your-digital-team','Connect your digital team','Give strategy, web, search and content one shared direction.','Agree commercial priorities','Sequence work across disciplines','Review and refine the roadmap')]
    for slug,title,desc,*steps in items:
        pattern=r'<a class="text-link" href="[^"]+">Explore '+re.escape(title)
        s=re.sub(pattern,'<a class="text-link" href="/solutions/'+slug+'/">Explore '+title,s)
        template=(D/'solutions/growth-system/index.html').read_text()
        body='<section class="wrap page-hero"><p class="eyebrow">Business outcome</p><h1>'+title+'</h1><p class="page-lede">'+desc+'</p>'+a('/assessment/?priority='+slug+'#assessment-request','Get Your Growth Assessment','button orange')+'</section>'+section('approach','A connected approach','Start with the goal.<br>Build the right system.',[(t,STAGES[i][3]) for i,t in enumerate(steps)])+section('fit','Ways to work together','Match the engagement to the opportunity.',ENGAGEMENT)
        template=re.sub(r'<main id="main">.*?</main>',lambda m:'<main id="main">'+body+'</main>',template,flags=re.S)
        template=re.sub(r'<title>.*?</title>','<title>'+title+' — Vista Digital</title>',template)
        template=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+desc+'">',template)
        p=D/'solutions'/slug/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(template)
    hub.write_text(s)
    privacy=(D/'contact/index.html').read_text()
    body='<section class="wrap article-page"><h1>Privacy in this preview</h1><div class="privacy-copy"><h2>Information you enter</h2><p>Assessment and contact details stay in the page while you prepare your request. This preview does not send those fields to a server or save them in browser storage.</p><h2>Sending your request</h2><p>Opening an email draft passes the prepared details to your email application. Review the draft and send it to hello@vistadigital.com to contact Vista. Your email provider handles that message under its own policies.</p><h2>Hosting</h2><p>GitHub Pages serves this preview and may process request information under <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub’s privacy statement</a>. This preview includes no analytics or advertising trackers.</p><h2>Questions</h2><p>Contact <a href="mailto:hello@vistadigital.com">hello@vistadigital.com</a> about the information you choose to send.</p></div></section>'
    privacy=re.sub(r'<main id="main">.*?</main>',lambda m:'<main id="main">'+body+'</main>',privacy,flags=re.S)
    privacy=re.sub(r'<title>.*?</title>','<title>Preview privacy — Vista Digital</title>',privacy)
    p=D/'privacy/index.html';p.parent.mkdir(exist_ok=True);p.write_text(privacy)
    routes=['/'+str(p.parent.relative_to(D)).strip('.')+'/' for p in D.rglob('index.html')];routes=[r.replace('//','/') for r in routes]
    (ROOT/'page-map.json').write_text(json.dumps(sorted(routes),indent=2))
    origin='https://contactonodo3d-byte.github.io/vista-digital-v2-preview'
    for f in D.rglob('*.html'):
        route='/'+str(f.parent.relative_to(D)).strip('.')+'/';url=origin+route.replace('//','/')
        s=f.read_text();title=re.search(r'<title>(.*?)</title>',s)[1];desc=re.search(r'<meta name="description" content="([^"]*)">',s)[1]
        metadata=f'<meta name="robots" content="noindex, follow"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">'
        s=s.replace('</head>',metadata+'</head>').replace('open-sans-variable.ttf','open-sans-variable.woff').replace('type="font/ttf"','type="font/woff"');f.write_text(s)
    (D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+origin+r+'</loc></url>' for r in sorted(routes))+'</urlset>')
    # A preview remains excluded from search; replace this policy on production launch.
    (D/'robots.txt').write_text('User-agent: *\nDisallow: /\n')

if __name__=='__main__':
    apply()
    import runpy
    runpy.run_path(str(ROOT/'src/assessment-v2.py'))['apply']()
    (D/'pages.js').write_text((ROOT/'src/strategy-pages.js').read_text())
    css=(D/'style.css').read_text().split('/* Approved Vista V2 strategy refinements */')[0]
    (D/'style.css').write_text((css+'\n'+(ROOT/'src/strategy.css').read_text()).replace('open-sans-variable.ttf','open-sans-variable.woff').replace("format('truetype')","format('woff')"))

if __name__=='__main__':
    for f in D.rglob('*.html'):
        s=f.read_text().replace('href="/','href="/vista-digital-v2-preview/').replace('src="/','src="/vista-digital-v2-preview/').replace('action="/','action="/vista-digital-v2-preview/').replace('srcset="/assets/','srcset="/vista-digital-v2-preview/assets/').replace(', /assets/',', /vista-digital-v2-preview/assets/')
        f.write_text(s)

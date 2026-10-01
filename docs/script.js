'use strict';
const menu=document.querySelector('.menu-toggle');
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.querySelector('#nav').classList.toggle('open',open);});
document.querySelectorAll('#nav a').forEach(a=>a.addEventListener('click',()=>{menu.setAttribute('aria-expanded','false');document.querySelector('#nav').classList.remove('open');}));
const dialog=document.querySelector('#assessment-dialog');
const website=document.querySelector('#website');
const error=document.querySelector('#website-error');
const form=document.querySelector('#assessment-form');
let chosenDomain='';
let sampleReportMode=false;
function parseDomain(value){try{const url=new URL(/^https?:\/\//i.test(value.trim())?value.trim():'https://'+value.trim());if(!/^https?:$/.test(url.protocol)||url.username||url.password||!url.hostname.includes('.')||/\s/.test(value)||!/[a-z]/i.test(url.hostname)||url.hostname.startsWith('.')||url.hostname.endsWith('.')||!/^([a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$/i.test(url.hostname))return null;return url.hostname.toLowerCase();}catch{return null;}}
const sampleScores=[82,58,64,71,76];
const sampleFindings=[
 ['Strong foundation, with a few speed opportunities.',['Mobile layouts are clear and usable in this sample.','Large page assets leave room for a faster first impression.'],'Prioritize image delivery and page speed on your key landing pages.'],
 ['Visibility is the biggest gap.',['Core service pages could align more closely with high-intent searches.','Local discovery could connect more clearly to the services you offer.'],'Build focused service pages around the questions qualified customers ask.'],
 ['Interest is not yet a clear next step.',['The main inquiry path could be more prominent.','Trust signals could sit closer to the point of contact.'],'Simplify the inquiry path and connect proof with your primary CTA.'],
 ['Expertise could work harder.',['The sample has a solid service overview.','Decision-stage questions need more useful, specific answers.'],'Create content that helps customers evaluate their options and act.'],
 ['A good base for local growth.',['The sample presents consistent business information.','Location pages could provide more relevant service detail.'],'Connect location information, service relevance and appointment paths.']
];
function showAssessment(domain,contact=false,sample=false){
 chosenDomain=domain||'';sampleReportMode=sample;
 document.querySelector('#assessed-domain').textContent=domain?(sample?'Sample report for: ':'Website: ')+domain:'';
 document.querySelector('#dialog-title').textContent=sample?'Your digital growth snapshot.':contact?'Let’s find your starting point.':'A clearer starting point.';
 document.querySelector('#dialog-demo-label').textContent=sample?'Sample report · Simulated analysis':'Demo · No live analysis';
 document.querySelector('#dialog-intro').textContent=sample?'A preview of how Vista could connect visibility, performance and conversion into a practical growth roadmap. All scores and findings below are illustrative.':'Explore what a growth assessment would cover. This preview does not scan your website or generate findings.';
 document.querySelector('#sample-report-intro').hidden=!sample;
 document.querySelector('.brief-form').hidden=false;document.querySelector('.brief-result').hidden=true;document.querySelector('#copy-status').textContent='';
 updateReview(document.querySelector('[data-review][aria-selected="true"]'));
 dialog.showModal();
}
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
function animateScore(el,target){
 if(matchMedia('(prefers-reduced-motion: reduce)').matches){el.textContent=target;return;}
 const start=performance.now();function frame(now){const progress=Math.min((now-start)/500,1);el.textContent=Math.round(target*(1-Math.pow(1-progress,3)));if(progress<1)requestAnimationFrame(frame);}requestAnimationFrame(frame);
}
let scanRunning=false;
async function runSampleScan(domain){
 if(scanRunning)return;scanRunning=true;
 const assessment=document.querySelector('.assessment'),button=document.querySelector('#analyze-button'),rows=[...document.querySelectorAll('[data-area]')],progress=document.querySelector('.scan-progress>span'),message=document.querySelector('#scan-message');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 assessment.classList.remove('scan-complete');assessment.classList.add('scanning');document.querySelector('#overall-score').textContent='—';document.querySelector('.snapshot-ring').style.strokeDashoffset='289';document.querySelector('#snapshot-title').textContent='Connecting the signals.';document.querySelector('#snapshot-description').textContent='Building your sample growth snapshot…';assessment.setAttribute('aria-busy','true');button.disabled=true;website.disabled=true;button.textContent='Analyzing demo…';
 document.querySelector('.sample-summary').hidden=true;document.querySelector('#view-sample-report').hidden=true;progress.style.width='0%';
 rows.forEach(row=>{row.classList.remove('is-scanning','is-complete');row.querySelector('.score-bar i').style.width='0%';row.querySelector('.score-value').textContent='—';});
 for(let i=0;i<rows.length;i++){
  const row=rows[i];row.classList.add('is-scanning');message.textContent='Simulating '+row.firstElementChild.textContent.toLowerCase()+'…';
  await pause(reduced?70:620);row.classList.remove('is-scanning');row.classList.add('is-complete');row.querySelector('.score-bar i').style.width=sampleScores[i]+'%';animateScore(row.querySelector('.score-value'),sampleScores[i]);progress.style.width=((i+1)*20)+'%';document.querySelector('.snapshot-ring').style.strokeDashoffset=String(289*(1-(i+1)*.14));
 }
 await pause(reduced?0:300);assessment.classList.remove('scanning');assessment.setAttribute('aria-busy','false');assessment.classList.add('scan-complete');message.textContent='Sample report ready';document.querySelector('#snapshot-title').textContent='A stronger path to growth.';document.querySelector('#snapshot-description').textContent='3 priorities identified across 5 growth signals.';document.querySelector('.sample-summary').hidden=false;document.querySelector('#view-sample-report').hidden=false;animateScore(document.querySelector('#overall-score'),70);button.disabled=false;website.disabled=false;button.innerHTML='Run Demo Again <svg class="chevron" viewBox="0 0 20 20" aria-hidden="true"><path d="m7 4 6 6-6 6"/></svg>';scanRunning=false;
 chosenDomain=domain;document.querySelector('#view-sample-report').dataset.domain=domain;
}
form.addEventListener('submit',event=>{event.preventDefault();const domain=parseDomain(website.value);if(!domain){error.textContent='Enter a valid website, such as yourbusiness.com.';website.setAttribute('aria-invalid','true');website.focus();return;}website.removeAttribute('aria-invalid');error.textContent='';runSampleScan(domain);});
document.querySelector('#view-sample-report').addEventListener('click',event=>showAssessment(event.currentTarget.dataset.domain,false,true));
website.addEventListener('input',()=>{website.removeAttribute('aria-invalid');error.textContent='';});
document.querySelectorAll('[data-contact]').forEach(button=>button.addEventListener('click',()=>showAssessment(parseDomain(website.value),true)));
document.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();}});
document.querySelectorAll('a[href="#assessment"]').forEach(a=>a.addEventListener('click',()=>{window.setTimeout(()=>website.focus({preventScroll:true}),400);}));
const stages=[['Start with clarity','Know what needs to change before you invest.','Connect your business goals with a review of your website, visibility and conversion path. Prioritize the work with the strongest business rationale.'],['Be found','Reach people already looking for what you do.','Connect search demand, useful content and distribution. Build a clearer path from the questions your audience asks to the expertise your business offers.'],['Turn attention into intent','Make the next step clear and credible.','Bring your positioning to life through your website. Help visitors evaluate your business, trust its expertise and take the next step toward a qualified inquiry.'],['Keep improving','Let the evidence guide the next investment.','Connect digital activity to meaningful business outcomes. Review what creates qualified opportunities, identify friction and refine the system over time.']];
const reviewAreas=[['Website performance',['Speed and usability across desktop and mobile','Clear structure, accessibility and technical foundations','Whether the experience reflects your business today']],['Search visibility',['The customer searches relevant to your business','Technical foundations that support discoverability','How service pages connect to search intent']],['Conversion readiness',['Clarity of your value proposition and next steps','Trust signals and customer decision support','Friction in inquiry, booking and contact paths']],['Content presence',['Useful answers to the questions your customers ask','Consistency between expertise, messaging and distribution','How content supports customer decisions']],['Local visibility',['Accuracy and consistency of business information','Location pages and relevant service areas','Local discovery and paths to contact or book']]];
function activateTab(button,buttons,change){buttons.forEach(b=>{const active=b===button;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;});change(button);}
function tabKeyboard(event,buttons,change){let index=buttons.indexOf(event.currentTarget);if(['ArrowRight','ArrowDown'].includes(event.key))index=(index+1)%buttons.length;else if(['ArrowLeft','ArrowUp'].includes(event.key))index=(index-1+buttons.length)%buttons.length;else if(event.key==='Home')index=0;else if(event.key==='End')index=buttons.length-1;else return;event.preventDefault();activateTab(buttons[index],buttons,change);buttons[index].focus();}
const stageButtons=[...document.querySelectorAll('[data-stage]')];
function updateStage(button){const d=stages[Number(button.dataset.stage)];const panel=document.querySelector('#system-detail');panel.setAttribute('aria-labelledby',button.id);panel.querySelector('.eyebrow').textContent=d[0];panel.querySelector('h3').textContent=d[1];panel.querySelector('p').textContent=d[2];}
stageButtons.forEach(button=>{button.addEventListener('click',()=>activateTab(button,stageButtons,updateStage));button.addEventListener('keydown',event=>tabKeyboard(event,stageButtons,updateStage));});
const reviewButtons=[...document.querySelectorAll('[data-review]')];
function updateReview(button){
 const index=Number(button.dataset.review);const [title,items]=reviewAreas[index];const panel=document.querySelector('#review-panel');
 panel.setAttribute('aria-labelledby',button.id);panel.querySelector('.eyebrow').textContent=sampleReportMode?'Sample finding':'What we would review';panel.querySelector('h3').textContent=sampleReportMode?sampleFindings[index][0]:title;
 panel.querySelector('ul').replaceChildren(...(sampleReportMode?sampleFindings[index][1]:items).map(item=>{const li=document.createElement('li');li.textContent=item;return li;}));
 panel.querySelectorAll('.finding-score,.finding-next-step').forEach(el=>el.remove());
 if(sampleReportMode){const score=document.createElement('p');score.className='finding-score';score.textContent=title+' · Sample score: '+sampleScores[index]+'/100';panel.insertBefore(score,panel.querySelector('ul'));const next=document.createElement('p');next.className='finding-next-step';next.textContent='Next step: '+sampleFindings[index][2];panel.append(next);}
}
reviewButtons.forEach(button=>{button.addEventListener('click',()=>activateTab(button,reviewButtons,updateReview));button.addEventListener('keydown',event=>tabKeyboard(event,reviewButtons,updateReview));});
document.querySelector('#prepare-brief').addEventListener('click',()=>{const notes=document.querySelector('#business-notes').value.trim();const content=['VISTA DIGITAL — CONVERSATION BRIEF','',chosenDomain?'Website: '+chosenDomain:'Website: To discuss','Priority: '+document.querySelector('#priority').value,notes?'Context: '+notes:'','Assessment scope: Website performance, search visibility, conversion readiness, content presence and local visibility.','','Prepared from a design demo. No website analysis has been performed.'].filter(line=>line!==null).join('\n');document.querySelector('#prepared-brief').value=content;document.querySelector('.brief-form').hidden=true;document.querySelector('.brief-result').hidden=false;document.querySelector('#prepared-brief').focus();});
document.querySelector('#edit-brief').addEventListener('click',()=>{document.querySelector('.brief-form').hidden=false;document.querySelector('.brief-result').hidden=true;document.querySelector('#priority').focus();});
document.querySelector('#copy-brief').addEventListener('click',async()=>{const field=document.querySelector('#prepared-brief');try{await navigator.clipboard.writeText(field.value);document.querySelector('#copy-status').textContent='Brief copied. Nothing has been submitted to Vista.';}catch{field.focus();field.select();document.querySelector('#copy-status').textContent='Select and copy the brief with your keyboard. Nothing has been submitted.';}});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!dialog.open){menu.setAttribute('aria-expanded','false');document.querySelector('#nav').classList.remove('open');}});

'use strict';
// Provider contract: {source, domain, signals: [{label, score}], score, opportunities}.
// Replace this provider with a backend adapter; never expose service secrets in the browser.
const VistaAssessmentProvider = {
 async analyze(host) {
  const labels = ['Website Performance', 'Search Visibility', 'Conversion Readiness', 'Content Presence', 'Local Visibility'];
  const hash = [...host].reduce((n, c) => (n * 31 + c.charCodeAt(0)) >>> 0, 0);
  const scores = [82, 61, 68, 54, 72].map((n, i) => n + ((hash >>> (i * 4)) % 9) - 4);
  return {source: 'demo', domain: host, signals: labels.map((label,i)=>({label,score:scores[i]})), score: Math.round(scores.reduce((a,b)=>a+b,0)/5), opportunities: scores.reduce((n,s)=>n+Math.max(1,Math.ceil((85-s)/10)),0)};
 }
};
const assessmentForm = document.querySelector('#assessment-start');
if (assessmentForm) {
 const panel=document.querySelector('#assessment'), input=document.querySelector('#hero-website'), submit=assessmentForm.querySelector('button'), summary=document.querySelector('#assessment-summary'), progress=document.querySelector('.analysis-progress'), message=document.querySelector('#scan-message'), rows=[...document.querySelectorAll('[data-signal]')];
 const supplied=new URLSearchParams(location.search).get('website'); if(supplied && domain(supplied)) input.value=domain(supplied);
 let result;
 const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
 assessmentForm.addEventListener('submit',async e=>{
  e.preventDefault(); if(submit.disabled) return;
  const host=domain(input.value.trim()), error=document.querySelector('#hero-website-error');
  if(!host){error.textContent='Enter a valid website, such as yourbusiness.com.';input.setAttribute('aria-invalid','true');input.focus();return;}
  error.textContent='';input.removeAttribute('aria-invalid');input.value=host;
  const capture=document.querySelector('#assessment-request');if(capture) capture.hidden=true;
  summary.hidden=true;result=undefined;submit.disabled=true;input.readOnly=true;panel.classList.add('is-scanning');panel.setAttribute('aria-busy','true');
  rows.forEach(row=>{row.classList.remove('revealed','checking');row.querySelector('strong').textContent='—';row.querySelector('strong').setAttribute('aria-label','Awaiting demo score');row.querySelector('i').style.width='0%';});
  progress.setAttribute('aria-valuenow','0');progress.querySelector('span').style.width='0%';
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  try {
   message.textContent='Preparing simulated report for '+host+'…';
   result=await VistaAssessmentProvider.analyze(host);
   for(let i=0;i<result.signals.length;i++){
    const signal=result.signals[i],row=rows[i];row.classList.add('checking');message.textContent='Demo check '+(i+1)+' of 5 · '+signal.label;
    await pause(reduced?60:650);
    row.classList.remove('checking');row.classList.add('revealed');row.querySelector('strong').textContent=signal.score;row.querySelector('strong').setAttribute('aria-label',signal.label+': '+signal.score+' out of 100, simulated');row.querySelector('i').style.width=signal.score+'%';
    progress.setAttribute('aria-valuenow',String((i+1)*20));progress.querySelector('span').style.width=(i+1)*20+'%';
   }
   document.querySelector('#digital-score').textContent=result.score;document.querySelector('#opportunity-count').textContent=result.opportunities;document.querySelector('#report-domain').textContent=host;
   summary.hidden=false;message.textContent='Demo complete. Digital Growth Score '+result.score+' out of 100. '+result.opportunities+' illustrative growth opportunities.';
   summary.focus({preventScroll:true});
  }catch{message.textContent='The assessment could not complete. Please try again.';result=undefined;}
  finally{submit.disabled=false;submit.textContent='Analyze again';input.readOnly=false;panel.classList.remove('is-scanning');panel.setAttribute('aria-busy','false');}
 });
 document.querySelector('#full-assessment').addEventListener('click',()=>{
  if(!result)return;
  const capture=document.querySelector('#assessment-request');
  if(capture){capture.hidden=false;document.querySelector('#request-website').value=result.domain;document.querySelector('#request-name').focus();capture.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});}
  else location.href=new URL('assessment/?website='+encodeURIComponent(result.domain)+'&report=demo'+location.search.replace('?','&')+'#assessment',document.querySelector('.brand').href).href;
 });
 // Reconstruct the same deterministic report on the assessment page, then open capture.
 if(new URLSearchParams(location.search).get('report')==='demo' && supplied && document.querySelector('#assessment-request')) {
  assessmentForm.requestSubmit();
  const openWhenReady=setInterval(()=>{if(!submit.disabled){clearInterval(openWhenReady);if(result)document.querySelector('#full-assessment').click();}},100);
 }
}

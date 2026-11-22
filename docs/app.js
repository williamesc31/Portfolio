'use strict';
const grid=document.querySelector('#project-grid');
projects.forEach((project,index)=>{
  const card=document.createElement('article');card.className='project-card'+(project.category==='planned'?' planned-card':'');card.dataset.category=project.category;
  const meta=document.createElement('div');meta.className='card-meta';const label=document.createElement('span');label.textContent=project.label;const number=document.createElement('span');number.className='index';number.textContent=String(index+1).padStart(2,'0');meta.append(label,number);
  const title=document.createElement('h3');title.textContent=project.name;const desc=document.createElement('p');desc.textContent=project.description;card.append(meta,title,desc);
  if(project.category==='planned'){const status=document.createElement('span');status.className='planned-label';status.textContent='Project details to follow';card.append(status)}
  else{const button=document.createElement('button');button.className='text-link';button.dataset.project=project.id;button.textContent='Explore project ↗';button.setAttribute('aria-label','Explore '+project.name);card.append(button)}
  grid.append(card);
});
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  let count=0;document.querySelectorAll('.project-card').forEach(card=>{card.hidden=button.dataset.filter!=='all'&&card.dataset.category!==button.dataset.filter;if(!card.hidden)count++});
  document.querySelector('#project-count').textContent='Showing '+count+' project'+(count===1?'':'s');
}));
const dialog=document.querySelector('#project-dialog');let lastTrigger=null;
function paragraph(text){const p=document.createElement('p');p.textContent=text;return p}
function section(title,text){const h=document.createElement('h3');h.textContent=title;return [h,paragraph(text)]}
document.addEventListener('click',event=>{
  const trigger=event.target.closest('[data-project]');if(!trigger)return;
  const project=projects.find(p=>p.id===trigger.dataset.project);if(!project)return;lastTrigger=trigger;
  const content=document.querySelector('#dialog-content');content.replaceChildren();const type=paragraph(project.label);type.className='eyebrow';const title=document.createElement('h2');title.id='dialog-title';title.textContent=project.name;
  content.append(type,title,...section('The question',project.question),...section('Approach',project.approach),...section('Verified results',project.result),...section('What the project demonstrates',project.lesson),...section('Tools and methods',project.tools));
  if(project.readme){const a=document.createElement('a');a.href=project.readme;a.download='';a.className='button dark';a.textContent='Download README ↓';content.append(a)}
  const repository=document.createElement('a');repository.href=project.repository;repository.target='_blank';repository.rel='noopener noreferrer';repository.className='button dark';repository.textContent='View project source ↗';content.append(repository);
  if(project.image){const img=document.createElement('img');img.src=project.image;img.alt=project.name+' generated result chart';img.className='project-chart';img.loading='lazy';content.append(img);}
  const status=paragraph('The default analysis command passed end-to-end verification against the bundled snapshot. See VERIFICATION.json in the repository for execution details.');status.className='status';content.append(status);
  dialog.showModal();document.body.classList.add('dialog-open');
});
function closeDialog(){dialog.close()}
document.querySelector('.close-dialog').addEventListener('click',closeDialog);
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)closeDialog()}});
dialog.addEventListener('close',()=>{document.body.classList.remove('dialog-open');lastTrigger?.focus()});

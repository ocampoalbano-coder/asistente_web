const $ = (q,ctx=document)=>ctx.querySelector(q);
const $$ = (q,ctx=document)=>[...ctx.querySelectorAll(q)];

const drop = $('.drop');
if (drop){
  ['dragover','dragenter'].forEach(ev=>{
    drop.addEventListener(ev,e=>{e.preventDefault(); drop.classList.add('drag');});
  });
  ['dragleave','drop'].forEach(ev=>{
    drop.addEventListener(ev,e=>{e.preventDefault(); drop.classList.remove('drag');});
  });
  drop.addEventListener('drop', e=>{
    const input = $('#file');
    if (e.dataTransfer?.files?.length){
      input.files = e.dataTransfer.files;
      $('#file-label').textContent = input.files[0].name;
    }
  });
}
const input = $('#file');
if (input){
  input.addEventListener('change', ()=>{
    $('#file-label').textContent = input.files?.[0]?.name || 'Seleccionar archivo';
  });
}
const demoBtn = $('#demo-btn');
if (demoBtn){
  demoBtn.addEventListener('click', ()=>{
    $('#demo-hidden').value = "1";
    $('#form').submit();
  });
}

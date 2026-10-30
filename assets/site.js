/* Ferreira Bandeira Advocacia: script comum a todas as páginas */
(function(){
  var WA='5541988107330', MAIL='mbandeira.adv@gmail.com';
  var waMsg='Olá, Dr. Maurício. Vim pelo site e gostaria de agendar um atendimento.';
  document.querySelectorAll('.wa-link').forEach(function(a){a.href='https://wa.me/'+WA+'?text='+encodeURIComponent(waMsg)});

  /* cena noturna do hero: céu, horizonte iluminado e silhuetas de edifícios */
  var cv=document.getElementById('cena'), cx=cv&&cv.getContext('2d');
  function rng(s){return function(){s=(s*16807)%2147483647;return (s-1)/2147483646}}
  function desenha(){
    if(!cv)return;
    var r=cv.getBoundingClientRect(), d=Math.min(window.devicePixelRatio||1,2), W=r.width, H=r.height;
    if(!W||!H)return;
    cv.width=Math.round(W*d); cv.height=Math.round(H*d); cx.setTransform(d,0,0,d,0,0);
    var R=rng(7), hz=H*0.78;
    var g=cx.createLinearGradient(0,0,0,hz); g.addColorStop(0,'#070F21'); g.addColorStop(.55,'#14284B'); g.addColorStop(1,'#3A3550');
    cx.fillStyle=g; cx.fillRect(0,0,W,H);
    var gl=cx.createRadialGradient(W*.74,hz,0,W*.74,hz,Math.max(W,H)*.6); gl.addColorStop(0,'rgba(236,161,81,.55)'); gl.addColorStop(.35,'rgba(229,138,46,.18)'); gl.addColorStop(1,'rgba(229,138,46,0)');
    cx.fillStyle=gl; cx.fillRect(0,0,W,H);
    for(var i=0;i<Math.round(W*H/5200);i++){var x=R()*W,y=R()*hz*.75,a=R()*.6+.15;cx.fillStyle='rgba(255,255,255,'+a+')';cx.fillRect(x,y,R()<.9?1:1.6,R()<.9?1:1.6)}
    function camada(base,minH,maxH,minW,maxW,cor,janelas,acesas){
      var x=-20; while(x<W+20){var w=minW+R()*(maxW-minW), h=minH+R()*(maxH-minH);
        if(R()<.12){h*=1.5}
        cx.fillStyle=cor; cx.fillRect(x,base-h,w,h+H);
        if(R()<.25){cx.fillRect(x+w*.4,base-h-h*.12,w*.18,h*.12)}
        if(janelas){for(var yy=base-h+10;yy<base-6;yy+=11){for(var xx=x+6;xx<x+w-8;xx+=9){var p=R(); if(p<acesas){cx.fillStyle=p<acesas*.35?'rgba(255,214,150,.85)':'rgba(236,161,81,.55)';cx.fillRect(xx,yy,3.5,5)}}}cx.fillStyle=cor}
        x+=w+(R()<.3?R()*14:1)}
    }
    camada(hz+4,H*.10,H*.30,28,70,'#1C2E52',false,0);
    camada(hz+18,H*.06,H*.24,36,90,'#0E1A35',true,.07);
    cx.fillStyle='#070F21'; cx.fillRect(0,hz+18,W,H);
    var rf=cx.createLinearGradient(0,hz+18,0,H); rf.addColorStop(0,'rgba(236,161,81,.14)'); rf.addColorStop(1,'rgba(236,161,81,0)');
    cx.fillStyle=rf; cx.fillRect(W*.45,hz+18,W*.55,H);
  }
  desenha(); var t;
  /* estante de livros jurídicos no cartão do advogado */
  var es=document.getElementById('estante');
  function estante(){
    if(!es)return; var r=es.getBoundingClientRect(), d=Math.min(window.devicePixelRatio||1,2), W=r.width, H=r.height; if(!W||!H)return;
    es.width=Math.round(W*d); es.height=Math.round(H*d); var c=es.getContext('2d'); c.setTransform(d,0,0,d,0,0);
    var R=rng(11);
    var bg=c.createLinearGradient(0,0,0,H); bg.addColorStop(0,'#1A2440'); bg.addColorStop(1,'#0B1326'); c.fillStyle=bg; c.fillRect(0,0,W,H);
    var cores=['#14284B','#1E3866','#2A4A7C','#3A2326','#5B2A2A','#2E2A3E','#6B4423','#22304F','#4A1F24','#1B3B4F'];
    var prat=4, mh=H/prat;
    for(var s=0;s<prat;s++){
      var y0=s*mh+8, base=(s+1)*mh-14, x=10;
      while(x<W-10){
        var w=9+R()*15, h=(base-y0)*(.62+R()*.33), col=R()<.05?'#B8701F':cores[Math.floor(R()*cores.length)];
        if(x+w>W-10)break;
        var lean=R()<.05&&x>40;
        c.save(); if(lean){c.translate(x,base);c.rotate(-.12);c.translate(-x,-base)}
        var gb=c.createLinearGradient(x,0,x+w,0); gb.addColorStop(0,'rgba(0,0,0,.35)'); gb.addColorStop(.35,'rgba(255,255,255,.07)'); gb.addColorStop(1,'rgba(0,0,0,.4)');
        c.fillStyle=col; c.fillRect(x,base-h,w,h); c.fillStyle=gb; c.fillRect(x,base-h,w,h);
        c.fillStyle='rgba(236,161,81,.55)'; c.fillRect(x+1,base-h+7,w-2,1.2); c.fillRect(x+1,base-h+11,w-2,.8); c.fillRect(x+1,base-12,w-2,1.2);
        if(w>13){c.fillStyle='rgba(20,16,10,.55)'; c.fillRect(x+2.5,base-h+h*.28,w-5,h*.14); c.fillStyle='rgba(236,161,81,.45)'; c.fillRect(x+4,base-h+h*.33,w-8,1)}
        c.restore(); x+=w+(R()<.08?6+R()*10:.8);
      }
      var pg=c.createLinearGradient(0,base,0,base+14); pg.addColorStop(0,'#3A2A1E'); pg.addColorStop(.2,'#24180F'); pg.addColorStop(1,'#120C08');
      c.fillStyle=pg; c.fillRect(0,base,W,14); c.fillStyle='rgba(0,0,0,.45)'; c.fillRect(0,base+14,W,6);
    }
    var lz=c.createRadialGradient(W*.82,H*.08,0,W*.82,H*.08,Math.max(W,H)*.9); lz.addColorStop(0,'rgba(255,200,130,.42)'); lz.addColorStop(.3,'rgba(236,161,81,.16)'); lz.addColorStop(1,'rgba(0,0,0,0)');
    c.globalCompositeOperation='screen'; c.fillStyle=lz; c.fillRect(0,0,W,H); c.globalCompositeOperation='source-over';
    var vg=c.createRadialGradient(W*.6,H*.4,Math.min(W,H)*.2,W*.5,H*.5,Math.max(W,H)*.85); vg.addColorStop(0,'rgba(0,0,0,0)'); vg.addColorStop(1,'rgba(4,8,18,.6)'); c.fillStyle=vg; c.fillRect(0,0,W,H);
  }
  estante(); addEventListener('resize',function(){clearTimeout(t);t=setTimeout(function(){desenha();estante()},150)});



  /* cabeçalho: transparente sobre o topo da página inicial, sólido nas internas */
  var topo=document.getElementById('topo');
  function hdr(){ if(!topo.classList.contains('fixo')) topo.classList.toggle('solid',scrollY>40)} hdr(); addEventListener('scroll',hdr,{passive:true});
  var b=document.getElementById('burger'), m=document.getElementById('menu');
  if(b&&m){
    b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);topo.classList.add('solid')});
    m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){m.classList.remove('open');b.setAttribute('aria-expanded','false')})});
  }

  /* botões que levam ao formulário já com o assunto escolhido */
  document.querySelectorAll('[data-assunto]').forEach(function(a){a.addEventListener('click',function(){var s=document.getElementById('f-area'); if(!s)return; for(var i=0;i<s.options.length;i++){if(s.options[i].text===a.dataset.assunto){s.selectedIndex=i}}})});

  function copiar(txt,btn){var t=btn.textContent;var ok=function(){btn.textContent='copiado';setTimeout(function(){btn.textContent=t},1500)};try{navigator.clipboard.writeText(txt).then(ok,function(){})}catch(e){}}
  document.querySelectorAll('[data-copy]').forEach(function(bt){bt.addEventListener('click',function(){copiar(bt.dataset.copy,bt)})});

  var f=document.getElementById('form'), via='wa';
  if(f){
  f.querySelectorAll('[data-via]').forEach(function(x){x.addEventListener('click',function(){via=x.dataset.via})});
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var g=function(id){return document.getElementById(id).value.trim()};
    var err=document.getElementById('erro');
    if(!g('f-nome')||!g('f-tel')||!g('f-msg')){err.textContent='Preencha nome, WhatsApp e o relato do caso para continuar.';err.hidden=false;return}
    if(!document.getElementById('f-lgpd').checked){err.textContent='Marque a autorização de uso dos dados para enviar.';err.hidden=false;return}
    err.hidden=true;
    var txt='Olá, Dr. Maurício. Vim pelo site e gostaria de agendar um atendimento.\n\nNome: '+g('f-nome')+'\nWhatsApp: '+g('f-tel')+(g('f-mail')?'\nE-mail: '+g('f-mail'):'')+(g('f-cid')?'\nCidade: '+g('f-cid'):'')+'\nAssunto: '+g('f-area')+'\nPreferência: '+g('f-pref')+'\n\nRelato: '+g('f-msg');
    document.getElementById('ok-mail').hidden=true;
    if(via==='mail'){
      var bt=document.getElementById('btn-mail'), rot=bt.textContent;
      bt.disabled=true; bt.textContent='Enviando...';
      var dados={'Nome':g('f-nome'),'WhatsApp':g('f-tel'),'E-mail':g('f-mail')||'(não informado)','Cidade':g('f-cid')||'(não informada)','Assunto':g('f-area'),'Preferência':g('f-pref'),'Relato':g('f-msg'),_honey:document.getElementById('f-honey').value};
      fetch('https://script.google.com/macros/s/AKfycbwqJKdfWnX9znlkZDObRgVfbw16tc-SF4BXs5APsai1uEOl_itbXqOeqYHVo4OhxunAWg/exec',{method:'POST',body:JSON.stringify(dados)})
        .then(function(r){return r.json().then(function(j){if(!j||j.ok!==true)throw new Error((j&&j.erro)||'falha');})})
        .then(function(){f.reset();document.getElementById('saida').hidden=true;document.getElementById('ok-mail').hidden=false;document.getElementById('ok-mail').scrollIntoView({block:'nearest'})})
        .catch(function(){err.textContent='Não foi possível enviar agora. Tente novamente em instantes ou fale pelo WhatsApp (41) 98810-7330.';err.hidden=false})
        .then(function(){bt.disabled=false;bt.textContent=rot});
      return;
    }
    var url='https://wa.me/'+WA+'?text='+encodeURIComponent(txt);
    document.getElementById('saida-link').href=url;
    document.getElementById('saida-txt').textContent='Sua mensagem foi preparada e o WhatsApp deve abrir em seguida. Se não abrir, use o botão abaixo ou copie o texto.';
    document.getElementById('saida-msg').textContent=txt;
    document.getElementById('saida').hidden=false;
    window.open(url,'_blank');
  });
  var sc=document.getElementById('saida-copy'); if(sc) sc.addEventListener('click',function(){copiar(document.getElementById('saida-msg').textContent,this)});
  }
})();

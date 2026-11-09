/* Built from site/home-live.html by site/build.py. Do not edit by hand. */
(function(){
var root=document.getElementById('nh-root');if(!root)return;
var st=document.createElement('style');st.textContent=".nh-wrap{font-family:'Poppins',sans-serif;color:#1e1e1e;max-width:1080px;margin:0 auto;text-align:left}\n.nh-wrap *{box-sizing:border-box}\n.nh-head{text-align:center;margin-bottom:26px}\n.nh-live{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid #f1e3cf;border-radius:50px;padding:7px 14px;font-size:13px;font-weight:500;color:#1e1e1e}\n.nh-dot{width:9px;height:9px;border-radius:50%;background:#1faa59;box-shadow:0 0 0 0 rgba(31,170,89,.6);animation:nhpulse 1.8s infinite}\n@keyframes nhpulse{0%{box-shadow:0 0 0 0 rgba(31,170,89,.55)}70%{box-shadow:0 0 0 9px rgba(31,170,89,0)}100%{box-shadow:0 0 0 0 rgba(31,170,89,0)}}\n.nh-head h2{font-family:'Playfair Display',serif;font-weight:400;margin:16px 0 10px}\n.nh-head p{margin:0 auto;max-width:640px;color:#5b5b5b}\n.nh-card{background:#fff;border:1px solid #ededed;border-radius:24px;padding:28px;box-shadow:0 18px 50px rgba(120,80,30,.08)}\n.nh-tabs{display:flex;gap:6px;background:#fff4e6;border-radius:50px;padding:5px;width:max-content;max-width:100%;margin:0 auto 24px}\n.nh-tab{border:0;background:transparent;font:500 15px 'Poppins',sans-serif;color:#1e1e1e;padding:10px 20px;border-radius:50px;cursor:pointer;white-space:nowrap}\n.nh-tab[aria-selected=\"true\"]{background:#1e1e1e;color:#fff}\n.nh-tab span{opacity:.6;font-weight:400;margin-left:4px}\n.nh-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:20px}\n.nh-row label{font-weight:500;font-size:15px}\n.nh-amt{display:flex;align-items:center;border:1.5px solid #1e1e1e;border-radius:50px;padding:0 14px;height:42px;background:#fff}\n.nh-amt b{font-weight:500;margin-right:2px}\n.nh-amt input{border:0;outline:0;width:96px;font:500 16px 'Poppins',sans-serif;color:#1e1e1e;background:transparent;padding:0}\n.nh-chip{border:1px solid #e3e3e3;background:#fff;border-radius:50px;padding:8px 14px;font:400 14px 'Poppins',sans-serif;color:#1e1e1e;cursor:pointer}\n.nh-chip[aria-pressed=\"true\"]{background:#ff8e0f;border-color:#ff8e0f;font-weight:500}\n.nh-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}\n.nh-tile{display:flex;flex-direction:column;border:1px solid #ededed;border-radius:18px;padding:18px;text-decoration:none!important;color:#1e1e1e!important;background:#fffbf7;transition:transform .15s,box-shadow .15s,border-color .15s}\n.nh-tile:hover{transform:translateY(-3px);box-shadow:0 10px 26px rgba(120,80,30,.12);border-color:#ff8e0f}\n.nh-kind{font-size:12px;letter-spacing:1.6px;text-transform:uppercase;color:#767676;font-weight:500}\n.nh-rate{font-family:'Playfair Display',serif;font-size:46px;line-height:1.05;margin:10px 0 0}\n.nh-rate small{font-size:22px}\n.nh-sub{font-size:12px;color:#767676;margin-bottom:12px}\n.nh-bank{display:flex;align-items:center;gap:10px;min-height:38px;margin-bottom:10px}\n.nh-bank img{width:38px;height:38px;object-fit:contain;border-radius:8px;background:#fff;border:1px solid #ededed;padding:3px}\n.nh-bank div{font-size:14px;font-weight:500;line-height:1.25}\n.nh-bank div em{display:block;font-style:normal;font-weight:400;font-size:12px;color:#767676}\n.nh-profit{margin-top:auto;background:#fff4e6;border-radius:12px;padding:9px 12px;font-size:13px;line-height:1.35}\n.nh-profit b{font-weight:600}\n.nh-meta{font-size:12px;color:#767676;margin-top:8px}\n.nh-foot{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:22px}\n.nh-foot p{margin:0;font-size:13px;color:#767676;max-width:560px}\n.nh-btn{display:inline-block;background:#ff8e0f;color:#1e1e1e!important;font:500 16px 'Poppins',sans-serif;border-radius:50px;padding:13px 26px;text-decoration:none!important;white-space:nowrap}\n.nh-btn:hover{background:#f08200}\n.nh-list{display:flex;flex-direction:column;gap:8px}\n.nh-fund{display:grid;grid-template-columns:28px 1fr 120px 84px;align-items:center;gap:14px;border:1px solid #ededed;border-radius:14px;padding:12px 16px;background:#fffbf7;text-decoration:none!important;color:#1e1e1e!important;transition:border-color .15s}\n.nh-fund:hover{border-color:#ff8e0f}\n.nh-rank{font-family:'Playfair Display',serif;font-size:20px;color:#ff8e0f}\n.nh-fname{font-size:14.5px;font-weight:500;line-height:1.3}\n.nh-ftags{font-size:12px;color:#767676;margin-top:2px}\n.nh-ret{text-align:right;font-weight:600;font-size:17px}\n.nh-up{color:#168a47}.nh-down{color:#c0392b}\n.nh-spark{width:120px;height:34px;display:block}\n.nh-hide{display:none!important}\n.nh-skel{height:150px;border-radius:18px;background:linear-gradient(90deg,#f6efe6,#fbf6ee,#f6efe6);background-size:200% 100%;animation:nhsk 1.2s infinite}\n@keyframes nhsk{to{background-position:-200% 0}}\n@media(max-width:900px){.nh-grid{grid-template-columns:repeat(2,1fr)}}\n@media(max-width:560px){\n .nh-card{padding:16px;border-radius:20px}\n .nh-tab{padding:9px 13px;font-size:14px}\n .nh-grid{gap:10px}.nh-tile{padding:14px}.nh-rate{font-size:36px}.nh-rate small{font-size:18px}\n .nh-bank img{width:30px;height:30px}.nh-bank div{font-size:13px}\n .nh-fund{grid-template-columns:22px 1fr 70px;gap:10px;padding:11px 12px}.nh-spark{display:none}\n .nh-foot{flex-direction:column;align-items:stretch;text-align:center}.nh-btn{text-align:center}\n .nh-amt input{width:80px}\n}";document.head.appendChild(st);
root.innerHTML="<div class=\"nh-wrap\" id=\"nh-live\">\n  <div class=\"nh-head\">\n    <div class=\"nh-live\"><i class=\"nh-dot\"></i><span id=\"nh-checked\">Checked with the banks every morning</span></div>\n    <h2>Today's Islamic savings rates and halal funds</h2>\n    <p>Every UK Islamic savings account and halal fund we track, side by side and free to use. Type in what you're saving to see what it could earn.</p>\n  </div>\n  <div class=\"nh-card\">\n    <div class=\"nh-tabs\" role=\"tablist\">\n      <button class=\"nh-tab\" role=\"tab\" aria-selected=\"true\" data-tab=\"sav\">Savings accounts<span id=\"nh-nsav\"></span></button>\n      <button class=\"nh-tab\" role=\"tab\" aria-selected=\"false\" data-tab=\"fund\">Halal funds<span id=\"nh-nfund\"></span></button>\n    </div>\n    <div id=\"nh-sav\">\n      <div class=\"nh-row\">\n        <label for=\"nh-amount\">I'm saving</label>\n        <div class=\"nh-amt\"><b>\u00a3</b><input id=\"nh-amount\" inputmode=\"numeric\" value=\"10,000\" aria-label=\"Amount you are saving in pounds\"></div>\n        <button class=\"nh-chip\" data-amt=\"1000\">\u00a31k</button>\n        <button class=\"nh-chip\" data-amt=\"5000\">\u00a35k</button>\n        <button class=\"nh-chip\" data-amt=\"10000\" aria-pressed=\"true\">\u00a310k</button>\n        <button class=\"nh-chip\" data-amt=\"25000\">\u00a325k</button>\n        <button class=\"nh-chip\" data-amt=\"50000\">\u00a350k</button>\n      </div>\n      <div class=\"nh-grid\" id=\"nh-tiles\"><div class=\"nh-skel\"></div><div class=\"nh-skel\"></div><div class=\"nh-skel\"></div><div class=\"nh-skel\"></div></div>\n      <div class=\"nh-foot\">\n        <p>Top expected profit rate in each category that you can open with this amount. Expected profit is not guaranteed. Education only, not personalised financial advice.</p>\n        <a class=\"nh-btn\" href=\"/savings-accounts\" id=\"nh-savbtn\">Compare all accounts</a>\n      </div>\n    </div>\n    <div id=\"nh-fund\" class=\"nh-hide\">\n      <div class=\"nh-row\" id=\"nh-periods\">\n        <label>Return over</label>\n        <button class=\"nh-chip\" data-p=\"1m\">1 month</button>\n        <button class=\"nh-chip\" data-p=\"6m\">6 months</button>\n        <button class=\"nh-chip\" data-p=\"1y\" aria-pressed=\"true\">1 year</button>\n      </div>\n      <div class=\"nh-row\" id=\"nh-classes\">\n        <label>Show</label>\n        <button class=\"nh-chip\" data-c=\"all\" aria-pressed=\"true\">All</button>\n        <button class=\"nh-chip\" data-c=\"Equity\">Shares</button>\n        <button class=\"nh-chip\" data-c=\"Sukuk\">Sukuk</button>\n        <button class=\"nh-chip\" data-c=\"Commodity\">Gold and commodities</button>\n        <button class=\"nh-chip\" data-c=\"REIT\">Property</button>\n      </div>\n      <div class=\"nh-list\" id=\"nh-funds\"><div class=\"nh-skel\" style=\"height:60px\"></div><div class=\"nh-skel\" style=\"height:60px\"></div><div class=\"nh-skel\" style=\"height:60px\"></div></div>\n      <div class=\"nh-foot\">\n        <p id=\"nh-fundnote\">Highest returns in pounds over the period, from the funds we track. Past performance is not a guide to future returns. Education only, not personalised financial advice.</p>\n        <a class=\"nh-btn\" href=\"/funds\" id=\"nh-fundbtn\">See all funds</a>\n      </div>\n    </div>\n  </div>\n</div>";
})();
(function(){
  var RAW='https://raw.githubusercontent.com/nisbacode/nisba-rates/main/docs/';
  var CDN='https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@main/docs/';
  var $=function(id){return document.getElementById(id)};
  var rates=null,funds=null,amount=10000,period='1y',cls='all';
  function load(file){
    return fetch(RAW+file,{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()})
      .catch(function(){return fetch(CDN+file).then(function(r){return r.json()})});
  }
  function gbp(n){return '£'+Math.round(n).toLocaleString('en-GB')}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function pick(list){
    if(!list.length)return null;
    var ok=list.filter(function(a){return amount>=(a.min||0)&&(!a.max||amount<=a.max)});
    var pool=ok.length?ok:list;
    var best=pool.slice().sort(function(a,b){return b.rate-a.rate||(a.min||0)-(b.min||0)})[0];
    return {a:best,open:ok.length>0};
  }
  function tile(kind,res){
    if(!res)return '';
    var a=res.a,bank=(rates.banks||{})[a.bank]||{name:a.bank},logo=bank.logo||'';
    if(logo&&logo.indexOf('http')!==0)logo=CDN+logo;
    var parts=a.rate.toFixed(2).split('.');
    var via=a.platform&&a.platform!=='Direct'?'via '+a.platform:'direct with the bank';
    var profit=res.open
      ?'About <b>'+gbp(amount*a.rate/100)+'</b> expected profit a year on '+gbp(amount)
      :'Needs at least <b>'+gbp(a.min)+'</b> to open';
    return '<a class="nh-tile" href="/savings-accounts">'
      +'<span class="nh-kind">'+kind+'</span>'
      +'<div class="nh-rate"><span data-count="'+a.rate+'">'+parts[0]+'.'+parts[1]+'</span><small>%</small></div>'
      +'<div class="nh-sub">expected profit rate</div>'
      +'<div class="nh-bank">'+(logo?'<img src="'+esc(logo)+'" alt="" loading="lazy" onerror="this.remove()">':'')
      +'<div>'+esc(bank.name)+'<em>'+esc(a.name)+'</em></div></div>'
      +'<div class="nh-profit">'+profit+'</div>'
      +'<div class="nh-meta">Min '+gbp(a.min||0)+', '+via+'</div></a>';
  }
  function countUp(root){
    var els=root.querySelectorAll('[data-count]');
    if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    var t0=null;
    function step(t){
      if(!t0)t0=t;var k=Math.min(1,(t-t0)/600),e=1-Math.pow(1-k,3);
      for(var i=0;i<els.length;i++){els[i].textContent=(parseFloat(els[i].getAttribute('data-count'))*e).toFixed(2)}
      if(k<1)requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function drawSav(){
    if(!rates)return;
    var acc=rates.accounts.filter(function(a){return !a.stale&&typeof a.rate==='number'});
    var f=function(fn){return acc.filter(fn)};
    var html=tile('Easy access',pick(f(function(a){return a.type==='easy'&&!a.isa})))
      +tile('Notice',pick(f(function(a){return a.type==='notice'&&!a.isa})))
      +tile('1 year fixed',pick(f(function(a){return a.type==='fixed'&&!a.isa&&a.term_months===12})))
      +tile('Cash ISA',pick(f(function(a){return a.isa})));
    $('nh-tiles').innerHTML=html;countUp($('nh-tiles'));
  }
  function spark(h,up){
    if(!h||h.length<2)return '<span></span>';
    var v=h.map(function(p){return p[1]}),mn=Math.min.apply(null,v),mx=Math.max.apply(null,v),r=(mx-mn)||1;
    var pts=v.map(function(y,i){return (i/(v.length-1)*118+1).toFixed(1)+','+(31-(y-mn)/r*28).toFixed(1)}).join(' ');
    return '<svg class="nh-spark" viewBox="0 0 120 34" aria-hidden="true"><polyline fill="none" stroke="'+(up?'#168a47':'#c0392b')+'" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" points="'+pts+'"/></svg>';
  }
  var CLS={Equity:'Shares',Sukuk:'Sukuk',Commodity:'Commodity',REIT:'Property',Mix:'Mixed',Crypto:'Crypto'};
  function drawFunds(){
    if(!funds)return;
    var seen={},rows=funds.funds.filter(function(f){
      var p=f.perf_gbp&&f.perf_gbp[period];
      return typeof p==='number'&&!f.stale&&(cls==='all'||f.asset_class===cls);
    }).sort(function(a,b){return b.perf_gbp[period]-a.perf_gbp[period]}).filter(function(f){
      if(seen[f.name])return false;seen[f.name]=1;return true;
    }).slice(0,5);
    var n=period==='1m'?5:period==='6m'?27:999;
    $('nh-funds').innerHTML=rows.length?rows.map(function(f,i){
      var p=f.perf_gbp[period],up=p>=0,h=(f.hist_gbp||[]).slice(-n);
      return '<a class="nh-fund" href="/funds"><span class="nh-rank">'+(i+1)+'</span>'
        +'<div><div class="nh-fname">'+esc(f.name)+'</div><div class="nh-ftags">'+(CLS[f.asset_class]||esc(f.asset_class))+', '+esc(f.category)
        +(typeof f.fee==='number'?', '+f.fee.toFixed(2)+'% yearly fee':'')+'</div></div>'
        +spark(h,up)
        +'<div class="nh-ret '+(up?'nh-up':'nh-down')+'">'+(up?'+':'')+p.toFixed(1)+'%</div></a>';
    }).join(''):'<p style="margin:0;color:#767676">No funds with data for this view yet.</p>';
  }
  function press(group,btn){
    var b=group.querySelectorAll('.nh-chip');
    for(var i=0;i<b.length;i++)b[i].setAttribute('aria-pressed',b[i]===btn?'true':'false');
  }
  var root=$('nh-live');
  root.addEventListener('click',function(e){
    var t=e.target.closest('button');if(!t)return;
    if(t.dataset.tab){
      var tabs=root.querySelectorAll('.nh-tab');
      for(var i=0;i<tabs.length;i++)tabs[i].setAttribute('aria-selected',tabs[i]===t?'true':'false');
      $('nh-sav').classList.toggle('nh-hide',t.dataset.tab!=='sav');
      $('nh-fund').classList.toggle('nh-hide',t.dataset.tab!=='fund');
    }else if(t.dataset.amt){
      amount=+t.dataset.amt;$('nh-amount').value=amount.toLocaleString('en-GB');press(t.parentNode,t);drawSav();
    }else if(t.dataset.p){period=t.dataset.p;press(t.parentNode,t);drawFunds();
    }else if(t.dataset.c){cls=t.dataset.c;press(t.parentNode,t);drawFunds();}
  });
  $('nh-amount').addEventListener('input',function(){
    var n=parseInt(this.value.replace(/[^0-9]/g,''),10)||0;
    amount=Math.min(n,10000000);this.value=n?amount.toLocaleString('en-GB'):'';
    var b=root.querySelectorAll('[data-amt]');
    for(var i=0;i<b.length;i++)b[i].setAttribute('aria-pressed',(+b[i].dataset.amt===amount)?'true':'false');
    drawSav();
  });
  load('rates.json').then(function(d){
    rates=d;drawSav();
    $('nh-nsav').textContent=d.accounts.length;
    $('nh-savbtn').textContent='Compare all '+d.accounts.length+' accounts';
    var c=new Date(d.checked_at),now=new Date();
    var time=c.toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',timeZone:'Europe/London'});
    var day=function(x){return x.toLocaleDateString('en-GB',{timeZone:'Europe/London'})};
    var when=day(c)===day(now)?'today':'on '+c.toLocaleDateString('en-GB',{day:'numeric',month:'short',timeZone:'Europe/London'});
    $('nh-checked').textContent='Rates checked with the banks '+when+' at '+time;
  }).catch(function(){
    $('nh-tiles').innerHTML='<p style="grid-column:1/-1;margin:0">Rates are loading slowly. <a href="/savings-accounts">Open the full comparison</a>.</p>';
  });
  load('funds.json').then(function(d){
    funds=d;drawFunds();
    $('nh-nfund').textContent=d.funds.length;
    $('nh-fundbtn').textContent='See all '+d.funds.length+' funds';
  }).catch(function(){
    $('nh-funds').innerHTML='<p style="margin:0">Funds are loading slowly. <a href="/funds">Open the full list</a>.</p>';
  });
})();

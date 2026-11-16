/* Built from site/platforms-directory.html by site/build.py. Do not edit by hand. */
(function(){
var root=document.getElementById('np-root');if(!root)return;
var st=document.createElement('style');st.textContent="/* Tool: same tokens and components as site/savings-tool.html */\n.np{--o:#ff8e0f;--od:#e67800;--cream:#fffbf7;--cream2:#fff5de;--ink:#1e1e1e;--mut:#6b6259;--line:#efe4d6;font-family:Poppins,system-ui,sans-serif;color:var(--ink);max-width:1120px;margin:0 auto 64px;padding:32px;background:var(--cream);border-radius:28px;box-sizing:border-box;text-align:left}\n.np *{box-sizing:border-box}\n.np button,.np input{font-family:inherit}\n.np-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:18px}\n.np-eyebrow{margin:0 0 4px;color:var(--o);font-weight:600;font-size:13px;letter-spacing:.08em;text-transform:uppercase}\n.np-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0;font-weight:700}\n.np-checked{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px;color:var(--mut)}\n.np-dot{width:8px;height:8px;border-radius:50%;background:#22a35a;box-shadow:0 0 0 4px rgba(34,163,90,.15);flex:none}\n.np-panel{background:var(--cream2);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:18px}\n.np-row{display:flex;flex-direction:column;gap:8px}\n.np-label{font-size:14px;font-weight:600}\n.np-search{background:#fff;border:2px solid var(--line);border-radius:16px;padding:12px 16px;font-size:16px;max-width:420px;outline:0;color:var(--ink)}\n.np-search:focus{border-color:var(--o)}\n.np-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 24px}\n.np-seg{display:flex;flex-wrap:wrap;gap:8px}\n.np-seg button{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:500;cursor:pointer;transition:all .15s}\n.np-seg button:hover{border-color:var(--o)}\n.np-seg button.on{background:var(--ink);border-color:var(--ink);color:#fff}\n.np-summary{margin:22px 4px 12px;font-size:15px;color:var(--mut)}\n.np-summary strong{color:var(--ink)}\n.np-list{display:flex;flex-direction:column;gap:12px}\n.np-card{display:grid;grid-template-columns:110px minmax(0,1.6fr) minmax(0,1fr) 170px;align-items:center;gap:20px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 22px;transition:box-shadow .15s,transform .15s}\n.np-card:hover{box-shadow:0 10px 30px rgba(30,30,30,.07);transform:translateY(-1px)}\n.np-type{font-size:13px;color:var(--mut);margin:0 0 2px}\n.np-name{font-weight:600;font-size:17px;margin:0 0 4px}\n.np-what{font-size:13px;color:var(--mut);margin:0 0 8px;line-height:1.5}\n.np-tags{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px}\n.np-aff{font-size:12.5px;font-weight:600;color:var(--od);margin:-4px 0 8px}\n.np-logo{width:110px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:12px}\n.np-logo.dark{background:#1e1e1e;padding:8px 10px}\n.np-logo img{max-width:100%;max-height:40px;object-fit:contain}\n.np-firm{font-size:12.5px;color:var(--mut)}\n.np-tag{font-size:11.5px;font-weight:500;background:var(--cream);border:1px solid var(--line);border-radius:999px;padding:3px 9px;white-space:nowrap}\n.np-tag.auth{background:#e9d4ff;border-color:#e9d4ff}\n.np-fact span{display:block;font-size:12px;color:var(--mut);margin-bottom:2px}\n.np-fact b{display:block;font-size:14px;font-weight:500;line-height:1.45}\n.np-frn{font-size:15px!important;font-weight:600!important;letter-spacing:.02em}\n.np-ctas{display:flex;flex-direction:column;gap:6px;align-items:stretch}\n.np-cta{display:inline-flex;align-items:center;justify-content:center;background:var(--o);color:#fff!important;text-decoration:none!important;font-weight:600;font-size:14px;border-radius:999px;padding:12px 20px;white-space:nowrap;transition:background .15s}\n.np-cta:hover{background:var(--od)}\n.np-reg{text-align:center;font-size:12.5px;color:var(--ink)!important}\n.np-alt{grid-column:1/-1;border-top:1px dashed var(--line);padding-top:12px;margin-top:-4px;font-size:13px;color:var(--mut)}\n.np-alt summary{cursor:pointer;font-weight:600;color:var(--ink);list-style:none;display:inline-flex;align-items:center;gap:6px}\n.np-alt summary::-webkit-details-marker{display:none}\n.np-alt summary::after{content:'+';color:var(--o);font-size:18px;line-height:1}\n.np-alt[open] summary::after{content:'\\2212'}\n.np-alt p{margin:8px 0 0;line-height:1.6}\n.np-empty{background:#fff;border-radius:20px;padding:28px;text-align:center;color:var(--mut)}\n.np-small{font-size:12px;color:var(--mut);margin:20px 4px 0;line-height:1.6}\n@media(max-width:860px){.np-card{grid-template-columns:minmax(0,1fr);gap:14px 16px;padding:16px}.np-card>div:nth-child(2),.np-ctas{grid-column:1/-1}.np-logo{justify-content:flex-start;width:auto;max-width:140px}}\n@media(max-width:640px){.np{padding:20px 14px;border-radius:20px}.np-panel{padding:18px;border-radius:20px}.np-grid{grid-template-columns:1fr}.np-search{max-width:none}.np-head{align-items:flex-start}}";document.head.appendChild(st);
root.innerHTML="<div class=\"np\" id=\"np-app\">\n<div class=\"np-head\">\n<div><p class=\"np-eyebrow\">Platform directory</p><h2 class=\"np-title\">Who runs each platform</h2></div>\n<div class=\"np-checked\"><span class=\"np-dot\"></span><span>Details checked 15 Nov 2026</span></div>\n</div>\n<div class=\"np-panel\">\n<div class=\"np-row\"><label class=\"np-label\" for=\"np-q\">Search</label><input id=\"np-q\" class=\"np-search\" type=\"search\" placeholder=\"Name or product, e.g. ISA\"></div>\n<div class=\"np-grid\">\n<div class=\"np-row\"><span class=\"np-label\">Type</span><div class=\"np-seg\" id=\"np-c\"></div></div>\n<div class=\"np-row\"><span class=\"np-label\">Regulation</span><div class=\"np-seg\" id=\"np-s\"></div></div>\n</div>\n</div>\n<div class=\"np-summary\" id=\"np-sum\"></div>\n<div class=\"np-list\" id=\"np-list\"></div>\n<p class=\"np-small\">Details are taken from each firm's own website and can change, so always check the firm reference number on the FCA Register before you sign up. A regulated firm can still offer products that are not covered by the Financial Services Compensation Scheme, and regulation does not protect you from investments falling in value or tell you whether a product is Shariah compliant. Where Nisba has a commercial relationship with a platform, its entry says so. This list is for education only. It is not a recommendation or personalised financial advice. Spotted something out of date? Email hello@nisba.co.uk.</p>\n</div>";
})();
{
const S={auth:'FCA authorised',ar:'Representative or agent',none:'Not FCA regulated'};
const reg=n=>'https://register.fca.org.uk/s/search?q='+n+'&type=Companies';
const P=[
{n:'Amal Invest',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/6c66278-0642-dbac-e031-f547876efe8d_logo-amal-invest.png',c:'Investing',s:'none',url:'https://amalinvest.com',
w:'Software that rebuilds popular funds using only Shariah-screened holdings, invested through your own brokerage account.',
f:'Amal Invest (not a broker or adviser)',
r:'Amal says it is not a broker or financial adviser and never holds client money. In the UK, the investments sit in your own Trading 212 account.',
p:'Depends on the broker account you hold, Trading 212 in the UK.'},
{n:'Ansari Financial Planning',cta:'Visit Ansari FP',dark:1,c:'Financial advice',s:'auth',frn:'429142',url:'https://www.ansarifp.co.uk',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148868657/images/0bd0bf-2ae0-1e4a-035-31e657f2ff5_Ansari_Wealth_Management_1_.png',
w:'Regulated financial advice specialising in halal investing.',
f:'Corbel Partners Limited, of which Ansari Financial Planning is a trading name',
r:'Ansari Financial Planning is a trading name of Corbel Partners Limited, which is authorised and regulated by the FCA.',
p:'If a complaint cannot be settled with the firm, you may be able to refer it to the Financial Ombudsman Service.',
aff:'Ansari Financial Planning is run by Ahmad, co-founder of Nisba.'},
{n:'Bayuti',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/10bdf62-4db0-8288-c408-8130e1c4e78_logo-bayuti.png',c:'Property investment',s:'auth',frn:'822039',url:'https://bayuti.com',
w:'Fractional investment in UK rental property, with shares in individual property deals.',
f:'Elite Capital and Management Services Limited, trading as Bayuti',
r:'Offers are made by Bayutiful Ltd through the Bayuti platform.',
p:'Bayuti\'s own risk warning says you are unlikely to be protected if something goes wrong.'},
{n:'Cocoa Invest',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/eaf7ac3-f8d-54a7-daf-003564bc86fa_logo-cocoa-invest-white.png',dark:1,c:'Investing',s:'auth',frn:'1017814',url:'https://www.cocoainvest.com',
w:'App offering fixed-term Shariah-compliant investments, including a GBP government certificate (Mudarabah) and a one-month Murabaha.',
f:'COCOA Invest Ltd',
r:'Authorised and regulated by the FCA.',
p:'Cocoa\'s FAQ says the government certificate and one-month Murabaha are not covered by the FSCS.'},
{n:'Cur8 Capital',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/e4451e6-e631-760c-cfc-0442600d183_logo-cur8-capital.png',c:'Investing',s:'auth',frn:'943736',url:'https://cur8.capital',
w:'Private market investing: an EIS venture fund, private equity, real estate, fixed income and an Innovative Finance ISA.',
f:'IFG.VC Limited, a subsidiary of Islamicfinanceguru Limited',
r:'Authorised and regulated by the FCA.',
p:'FSCS cover is not stated on its website.'},
{n:'Kestrl',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/6486ec2-b6-0217-1fad-3d10df7427_logo-kestrl-white.png',dark:1,c:'Money app',s:'ar',url:'https://www.kestrl.io',
w:'Muslim money app with budgeting, an e-money account and card, and a halal stock screener.',
f:'Kestrl Ltd, which is not authorised itself',
r:'The account and card are issued by AF Payments Limited (e-money, FRN 900440). Bank connections are provided by TrueLayer, with Kestrl acting as its agent.',
p:'Money in the account is safeguarded by AF Payments. E-money is not covered by the FSCS.',regn:'900440'},
{n:'Musaffa',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/45a5d55-f173-11a-7d02-dd3a66dd10fb_logo-musaffa.png',c:'Investing',s:'none',url:'https://musaffa.com',
w:'Shariah screening and research app for stocks and ETFs, with US trading through Alpaca Securities.',
f:'Musaffa LLC, a US SEC-registered investment adviser',
r:'We found no FCA authorisation. Its services come from US firms.',
p:'UK protections such as the FSCS and the Financial Ombudsman would not apply.'},
{n:'Nester',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/257e368-78d1-32b3-6d13-4c4b7e430cd_logo-nester.png',c:'Property investment',s:'auth',frn:'915346',url:'https://www.nester.com',
w:'Peer-to-peer platform for Shariah-compliant finance secured on UK property, including an Innovative Finance ISA.',
f:'Nester Platform Ltd',
r:'Authorised and regulated by the FCA.',
p:'Peer-to-peer investments are generally not covered by the FSCS.'},
{n:'Offa',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/eeda1-f287-c57-623a-aa6b3672d1e5_logo-offa.png',c:'Home finance',s:'auth',frn:'1000573',url:'https://www.offa.co.uk',
w:'Islamic home finance: residential Home Purchase Plans, plus buy-to-let and bridging finance.',
f:'Offa Money Limited',
r:'Home Purchase Plans are FCA regulated. Bridge, buy-to-let and bridge-to-let products come from other Offa group firms and are not.',
p:'FCA protections apply to the Home Purchase Plan only.'},
{n:'Pfida',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/f1bc533-063d-113-5af8-6083d482fa6_logo-pfida.png',c:'Home finance',s:'ar',frn:'1053702',url:'https://www.pfida.com',
w:'Co-ownership home finance (OwnTogether and OwnToLet) and property-backed savings and investments.',
f:'Pfida Ltd, an appointed representative of Leela Regulatory Solutions Limited (FRN 845185) for arranging deals in investments',
r:'Pfida\'s website says none of its products are FCA regulated.',
p:'Pfida says FCA protections, the Financial Ombudsman and the FSCS do not apply to its products.'},
{n:'StrideUp',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/6a10f11-768a-e212-2a10-5087457e3f3_logo-strideup.png',c:'Home finance',s:'auth',frn:'785299',url:'https://www.strideup.co',
w:'Islamic home finance: residential Home Purchase Plans and buy-to-let purchase plans.',
f:'StrideUp Homes Limited',
r:'Residential Home Purchase Plans are FCA regulated. Buy-to-let purchase plans are not.',
p:'FCA protections apply to the residential Home Purchase Plan only.'},
{n:'Wahed',logo:'https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/sites/2148749493/images/4e3fe4-f54d-2f1a-47c3-4afc8dd85a2_logo-wahed.png',c:'Investing',s:'auth',frn:'833225',url:'https://www.wahed.com/uk',
w:'Halal managed portfolios through a Stocks and Shares ISA, a SIPP or a General Investment Account.',
f:'Wahed Invest Ltd, with custody by WealthKernel Limited',
r:'Authorised and regulated by the FCA for discretionary investment management.',
p:'Wahed says it is a member of the FSCS. Client investments are held separately from Wahed\'s own money.'}
];
const st={c:'all',s:'all',q:''};
const cats=[...new Set(P.map(x=>x.c))].sort();
const seg=(id,opts,k)=>{document.getElementById(id).innerHTML=opts.map(([v,l])=>'<button type="button" data-k="'+k+'" data-v="'+v+'">'+l+'</button>').join('')};
seg('np-c',[['all','All'],...cats.map(c=>[c,c])],'c');
seg('np-s',[['all','All'],['auth','FCA authorised'],['ar','Representative or agent'],['none','Not FCA regulated']],'s');
const short=x=>x.f.split(',')[0].replace(/ \(.*\)$/,'');
const card=x=>{const fr=x.frn||x.regn;return '<div class="np-card"><div class="np-logo'+(x.dark?' dark':'')+'">'+(x.logo?'<img src="'+x.logo+'" alt="'+x.n+' logo" loading="lazy">':'')+'</div><div><p class="np-type">'+x.c+'</p><p class="np-name">'+x.n+'</p><p class="np-what">'+x.w+'</p>'+(x.aff?'<p class="np-aff">'+x.aff+'</p>':'')+'<div class="np-tags"><span class="np-tag'+(x.s==='auth'?' auth':'')+'">'+S[x.s]+'</span>'+(short(x)!==x.n||x.frn?'<span class="np-firm">'+short(x)+(x.frn?' · <span style="white-space:nowrap">FRN '+x.frn+'</span>':'')+'</span>':'')+'</div></div>'
+'<div class="np-fact"><span>Protection</span><b>'+x.p+'</b></div>'
+'<div class="np-ctas"><a class="np-cta" href="'+x.url+'" rel="noopener">'+(x.cta||'Visit '+x.n)+'</a>'+(fr?'<a class="np-reg" href="'+reg(fr)+'" rel="noopener">Check on FCA Register</a>':'')+'</div>'
+'<details class="np-alt"><summary>How it is regulated</summary><p>'+x.r+(x.f.includes(',')?' The firm is '+x.f+'.':'')+(x.aff?' <b>Commercial relationship:</b> '+x.aff:'')+'</p></details></div>'};
const render=()=>{const q=st.q.toLowerCase();
const r=P.filter(x=>(st.c==='all'||x.c===st.c)&&(st.s==='all'||x.s===st.s)&&(!q||(x.n+' '+x.w+' '+x.c).toLowerCase().includes(q)));
document.getElementById('np-list').innerHTML=r.length?r.map(card).join(''):'<div class="np-empty">No platforms match those filters.</div>';
document.getElementById('np-sum').innerHTML='<strong>'+r.length+' platforms</strong> shown, listed A to Z.';
document.querySelectorAll('#np-app .np-seg button').forEach(b=>b.classList.toggle('on',st[b.dataset.k]===b.dataset.v));};
document.getElementById('np-app').addEventListener('click',e=>{const b=e.target.closest('.np-seg button');if(!b)return;st[b.dataset.k]=b.dataset.v;render();});
document.getElementById('np-q').addEventListener('input',e=>{st.q=e.target.value.trim();render();});
render();
}

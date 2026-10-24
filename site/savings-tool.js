/* Built from site/savings-tool.html by site/build.py. Do not edit by hand. */
(function(){
var root=document.getElementById('nr-root');if(!root)return;
var st=document.createElement('style');st.textContent=".nr{--o:#ff8e0f;--od:#e67800;--cream:#fffbf7;--cream2:#fff5de;--ink:#1e1e1e;--mut:#6b6259;--line:#efe4d6;font-family:Poppins,system-ui,sans-serif;color:var(--ink);max-width:1120px;margin:0 auto;padding:32px;background:var(--cream);border-radius:28px;box-sizing:border-box;text-align:left}\n.nr *{box-sizing:border-box}\n.nr button{font-family:inherit}\n.nr-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:18px}\n.nr-eyebrow{margin:0 0 4px;color:var(--o);font-weight:600;font-size:13px;letter-spacing:.08em;text-transform:uppercase}\n.nr-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0;font-weight:700;color:var(--ink)}\n.nr-checked{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px;color:var(--mut)}\n.nr-dot{width:8px;height:8px;border-radius:50%;background:#bbb;flex:none}\n.nr-checked.ok .nr-dot{background:#22a35a;box-shadow:0 0 0 4px rgba(34,163,90,.15)}\n.nr-checked.warn .nr-dot{background:#e0a100}\n.nr-panel{background:var(--cream2);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:18px}\n.nr-row{display:flex;flex-direction:column;gap:8px;min-width:0}\n.nr-label{font-size:14px;font-weight:600}\n.nr-amount-wrap{display:flex;align-items:center;background:#fff;border:2px solid var(--line);border-radius:16px;padding:0 16px;max-width:360px;transition:border-color .15s}\n.nr-amount-wrap:focus-within{border-color:var(--o)}\n.nr-pound{font-family:'Playfair Display',Georgia,serif;font-size:30px;font-weight:700;color:var(--o);margin-right:6px}\n.nr-amount{border:0;outline:0;background:transparent;font:700 30px/1 'Playfair Display',Georgia,serif;color:var(--ink);width:100%;padding:12px 0;min-width:0}\n.nr-chips{display:flex;flex-wrap:wrap;gap:8px}\n.nr-chips button,.nr-seg button{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:500;cursor:pointer;transition:all .15s}\n.nr-chips button:hover,.nr-seg button:hover{border-color:var(--o)}\n.nr-seg{display:flex;flex-wrap:wrap;gap:8px}\n.nr-seg button.on,.nr-chips button.on{background:var(--ink);border-color:var(--ink);color:#fff}\n.nr-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 24px}\n.nr-select{appearance:none;-webkit-appearance:none;background:#fff url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%231e1e1e' stroke-width='2'/%3E%3C/svg%3E\") no-repeat right 14px center;border:1px solid var(--line);border-radius:999px;padding:10px 38px 10px 16px;font:500 14px Poppins,sans-serif;color:var(--ink);max-width:280px;cursor:pointer}\n.nr-check{display:flex;align-items:center;gap:10px;font-size:14px;cursor:pointer}\n.nr-check input{width:18px;height:18px;accent-color:var(--o)}\n.nr-summary{margin:22px 4px 12px;font-size:15px;color:var(--mut)}\n.nr-summary strong{color:var(--ink)}\n.nr-fscs{background:#fff;border-left:4px solid var(--o);border-radius:12px;padding:12px 16px;font-size:13px;margin-bottom:12px}\n.nr-list{display:flex;flex-direction:column;gap:12px}\n.nr-card{display:grid;grid-template-columns:72px minmax(0,1fr) 170px 190px 180px;align-items:center;gap:20px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 22px;transition:box-shadow .15s,transform .15s}\n.nr-card:hover{box-shadow:0 10px 30px rgba(30,30,30,.07);transform:translateY(-1px)}\n.nr-card.best{border:2px solid var(--o)}\n.nr-card.off{opacity:.55}\n.nr-logo{width:72px;height:48px;display:flex;align-items:center;justify-content:center}\n.nr-logo img{max-width:72px;max-height:48px;object-fit:contain}\n.nr-name{min-width:0}\n.nr-bank{font-size:13px;color:var(--mut);margin:0 0 2px}\n.nr-acc{font-weight:600;font-size:16px;margin:0 0 8px;line-height:1.3}\n.nr-tags{display:flex;flex-wrap:wrap;gap:6px}\n.nr-tag{font-size:11.5px;font-weight:500;background:var(--cream);border:1px solid var(--line);border-radius:999px;padding:3px 9px;white-space:nowrap}\n.nr-tag.isa{background:#e9d4ff;border-color:#e9d4ff}\n.nr-tag.best{background:var(--o);border-color:var(--o);color:#fff}\n.nr-rate b{display:block;font-family:'Playfair Display',Georgia,serif;font-size:32px;line-height:1;color:var(--ink)}\n.nr-rate span,.nr-profit span{font-size:12px;color:var(--mut)}\n.nr-profit b{display:block;font-size:18px;font-weight:600}\n.nr-why{display:block;font-size:12px;color:#b45309;margin-top:2px}\n.nr-stale{display:block;font-size:11.5px;color:var(--mut);margin-top:4px}\n.nr-cta{display:inline-flex;align-items:center;justify-content:center;background:var(--o);color:#fff!important;text-decoration:none!important;font-weight:600;font-size:14px;border-radius:999px;padding:12px 20px;white-space:nowrap;transition:background .15s}\n.nr-cta:hover{background:var(--od)}\n.nr-card.off .nr-cta{background:#d8cfc4}\n.nr-empty{background:#fff;border-radius:20px;padding:28px;text-align:center;color:var(--mut)}\n.nr-small{font-size:12px;color:var(--mut);margin:20px 4px 0;line-height:1.6}\n.nr-more{align-self:center;margin-top:6px;border:1px solid var(--ink);background:transparent;border-radius:999px;padding:10px 22px;font-weight:600;cursor:pointer}\n@media (max-width:860px){\n  .nr-card{grid-template-columns:56px minmax(0,1fr) minmax(0,1fr);grid-template-areas:\"logo name name\" \"rate rate profit\" \"cta cta cta\";gap:14px 16px;padding:16px}\n  .nr-logo{grid-area:logo;width:56px}.nr-logo img{max-width:56px}\n  .nr-name{grid-area:name}.nr-rate{grid-area:rate}.nr-profit{grid-area:profit}\n  .nr-cta{grid-area:cta;width:100%}\n}\n@media (max-width:640px){\n  .nr{padding:20px 14px;border-radius:20px}\n  .nr-panel{padding:18px;border-radius:20px}\n  .nr-grid{grid-template-columns:1fr}\n  .nr-select{max-width:none;width:100%}\n  .nr-amount-wrap{max-width:none}\n  .nr-head{align-items:flex-start}\n}";document.head.appendChild(st);
root.innerHTML="<div id=\"nr-app\" class=\"nr\">\n  <div class=\"nr-head\">\n    <div>\n      <p class=\"nr-eyebrow\">Live comparison</p>\n      <h2 class=\"nr-title\">Compare Islamic savings rates</h2>\n    </div>\n    <div class=\"nr-checked\" id=\"nr-checked\"><span class=\"nr-dot\"></span><span>Loading today's rates\u2026</span></div>\n  </div>\n\n  <div class=\"nr-panel\">\n    <div class=\"nr-row nr-row-amount\">\n      <label class=\"nr-label\" for=\"nr-amount\">How much do you want to save?</label>\n      <div class=\"nr-amount-wrap\">\n        <span class=\"nr-pound\">\u00a3</span>\n        <input id=\"nr-amount\" class=\"nr-amount\" type=\"text\" inputmode=\"numeric\" value=\"10,000\" aria-label=\"Deposit amount in pounds\">\n      </div>\n      <div class=\"nr-chips\" id=\"nr-presets\">\n        <button type=\"button\" data-v=\"1000\">\u00a31k</button>\n        <button type=\"button\" data-v=\"5000\">\u00a35k</button>\n        <button type=\"button\" data-v=\"10000\">\u00a310k</button>\n        <button type=\"button\" data-v=\"25000\">\u00a325k</button>\n        <button type=\"button\" data-v=\"50000\">\u00a350k</button>\n        <button type=\"button\" data-v=\"100000\">\u00a3100k</button>\n      </div>\n    </div>\n\n    <div class=\"nr-grid\">\n      <div class=\"nr-row\">\n        <span class=\"nr-label\">Account type</span>\n        <div class=\"nr-seg\" id=\"nr-type\">\n          <button type=\"button\" data-v=\"all\" class=\"on\">All</button>\n          <button type=\"button\" data-v=\"easy\">Easy access</button>\n          <button type=\"button\" data-v=\"notice\">Notice</button>\n          <button type=\"button\" data-v=\"fixed\">Fixed term</button>\n        </div>\n      </div>\n      <div class=\"nr-row\">\n        <span class=\"nr-label\">ISA</span>\n        <div class=\"nr-seg\" id=\"nr-isa\">\n          <button type=\"button\" data-v=\"all\" class=\"on\">All</button>\n          <button type=\"button\" data-v=\"isa\">Cash ISA only</button>\n          <button type=\"button\" data-v=\"non\">Not ISA</button>\n        </div>\n      </div>\n      <div class=\"nr-row\">\n        <label class=\"nr-label\" for=\"nr-term\">Longest I can lock away</label>\n        <select id=\"nr-term\" class=\"nr-select\">\n          <option value=\"999\">Any length</option>\n          <option value=\"3\">Up to 3 months</option>\n          <option value=\"6\">Up to 6 months</option>\n          <option value=\"12\">Up to 1 year</option>\n          <option value=\"24\">Up to 2 years</option>\n          <option value=\"36\">Up to 3 years</option>\n          <option value=\"60\">Up to 5 years</option>\n        </select>\n      </div>\n      <div class=\"nr-row\">\n        <label class=\"nr-label\" for=\"nr-sort\">Sort by</label>\n        <select id=\"nr-sort\" class=\"nr-select\">\n          <option value=\"rate\">Highest rate</option>\n          <option value=\"term\">Shortest term</option>\n          <option value=\"min\">Lowest minimum deposit</option>\n        </select>\n      </div>\n    </div>\n    <label class=\"nr-check\"><input type=\"checkbox\" id=\"nr-elig\" checked> Only show accounts I can open with this amount</label>\n  </div>\n\n  <div class=\"nr-summary\" id=\"nr-summary\"></div>\n  <div class=\"nr-fscs\" id=\"nr-fscs\" hidden>Deposits are protected by the FSCS up to \u00a3120,000 per person, per banking group. Above that, consider splitting your savings across different banks.</div>\n  <div class=\"nr-list\" id=\"nr-list\" aria-live=\"polite\"></div>\n\n  <p class=\"nr-small\">Rates are read from each bank's own website every morning. Raisin rates are checked by hand. Islamic banks pay an expected profit rate rather than interest. Estimated profit is a simple guide for the first year (or the full term if shorter) and is not guaranteed. Always confirm the rate and terms with the provider before opening an account. Education only, not personalised financial advice.</p>\n</div>";
})();
(function(){
  var DATA = [
    'https://raw.githubusercontent.com/nisbacode/nisba-rates/main/docs/rates.json',
    'https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@main/docs/rates.json'
  ];
  var ASSETS = 'https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@main/docs/';
  var $ = function(id){ return document.getElementById(id); };
  var state = { amount: 10000, type: 'all', isa: 'all', term: 999, sort: 'rate', elig: true, showAll: false };
  var data = null;

  function gbp(n, dp){ return '£' + Number(n).toLocaleString('en-GB', {minimumFractionDigits: dp||0, maximumFractionDigits: dp||0}); }
  function esc(s){ return String(s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function termLabel(a){
    if (a.type === 'easy') return 'Easy access';
    if (a.type === 'notice') return (a.notice_days || a.term_months*30) + ' day notice';
    var m = a.term_months;
    if (m % 12 === 0) return (m/12) + (m === 12 ? ' year fixed' : ' years fixed');
    return m + ' months fixed';
  }
  function dateLabel(iso){
    var d = new Date(iso), now = new Date();
    var t = d.toLocaleTimeString('en-GB', {hour:'numeric', minute:'2-digit', hour12:true, timeZone:'Europe/London'}).replace(/\s/g, '').toLowerCase();
    var same = d.toLocaleDateString('en-GB', {timeZone:'Europe/London'}) === now.toLocaleDateString('en-GB', {timeZone:'Europe/London'});
    return same ? 'today at ' + t : d.toLocaleDateString('en-GB', {day:'numeric', month:'short', timeZone:'Europe/London'}) + ' at ' + t;
  }

  function load(i){
    i = i || 0;
    if (i >= DATA.length) return fail();
    fetch(DATA[i] + '?t=' + Math.floor(Date.now()/300000), {cache:'no-store'})
      .then(function(r){ if(!r.ok) throw 0; return r.json(); })
      .then(function(j){ data = j; ready(); })
      .catch(function(){ load(i+1); });
  }
  function fail(){
    $('nr-checked').className = 'nr-checked warn';
    $('nr-checked').lastChild.textContent = 'Rates unavailable right now';
    $('nr-list').innerHTML = '<div class="nr-empty">We could not load today\'s rates. Please refresh in a minute, or check <a href="https://www.alrayanbank.co.uk/savings">Al Rayan</a>, <a href="https://www.gatehousebank.com/personal/savings">Gatehouse</a>, <a href="https://www.blme.com/products-and-services/savings/">BLME</a> and <a href="https://www.raisin.co.uk/">Raisin</a> directly.</div>';
  }
  function ready(){
    var c = $('nr-checked');
    var stale = data.stale_count || 0;
    c.className = 'nr-checked ' + (stale ? 'warn' : 'ok');
    c.lastChild.textContent = 'Rates checked ' + dateLabel(data.checked_at);
    render();
  }

  function eligible(a){
    if (state.amount < a.min) return 'Minimum deposit ' + gbp(a.min);
    if (state.amount > a.max) return 'Maximum deposit ' + gbp(a.max);
    return '';
  }
  function profit(a){
    var amt = Math.min(state.amount, a.max);
    var years = (a.type === 'fixed' && a.term_months < 12) ? a.term_months/12 : 1;
    return { value: amt * a.rate / 100 * years, label: years < 1 ? 'over ' + a.term_months + ' months' : 'per year' };
  }

  function render(){
    if (!data) return;
    var list = data.accounts.filter(function(a){
      if (state.type !== 'all' && a.type !== state.type) return false;
      if (state.isa === 'isa' && !a.isa) return false;
      if (state.isa === 'non' && a.isa) return false;
      if (a.type !== 'easy' && a.term_months > state.term) return false;
      if (state.elig && eligible(a)) return false;
      return true;
    });
    list.sort(function(x, y){
      var ex = eligible(x) ? 1 : 0, ey = eligible(y) ? 1 : 0;
      if (ex !== ey) return ex - ey;
      if (state.sort === 'term') return (x.term_months - y.term_months) || (y.rate - x.rate);
      if (state.sort === 'min') return (x.min - y.min) || (y.rate - x.rate);
      return y.rate - x.rate;
    });

    var openable = list.filter(function(a){ return !eligible(a); });
    var top = openable.length ? openable.slice().sort(function(a,b){ return b.rate - a.rate; })[0] : null;
    $('nr-summary').innerHTML = list.length
      ? '<strong>' + list.length + ' account' + (list.length === 1 ? '' : 's') + '</strong> match' + (list.length === 1 ? 'es' : '') +
        (top ? '. Best rate you can get with ' + gbp(state.amount) + ': <strong>' + top.rate.toFixed(2) + '%</strong>, about <strong>' + gbp(profit(top).value) + '</strong> ' + profit(top).label + '.' : '.')
      : '';
    $('nr-fscs').hidden = state.amount <= 120000;

    if (!list.length){
      $('nr-list').innerHTML = '<div class="nr-empty">No accounts match these filters. Try a longer term, a different account type, or untick "Only show accounts I can open".</div>';
      return;
    }
    var shown = state.showAll ? list : list.slice(0, 12);
    var html = shown.map(function(a){
      var b = data.banks[a.bank] || {name: a.bank};
      var why = eligible(a);
      var p = profit(a);
      var best = top && a.id === top.id && state.sort === 'rate';
      var tags = '<span class="nr-tag">' + termLabel(a) + '</span>' +
        (a.isa ? '<span class="nr-tag isa">Cash ISA</span>' : '') +
        '<span class="nr-tag">' + (a.platform === 'Raisin' ? 'Via Raisin' : 'Direct with bank') + '</span>' +
        (best ? '<span class="nr-tag best">Top rate</span>' : '');
      var note = '';
      if (a.stale) note = '<span class="nr-stale">Rate last confirmed ' + (a.last_verified ? new Date(a.last_verified).toLocaleDateString('en-GB',{day:'numeric',month:'short'}) : 'recently') + '. Check with the provider.</span>';
      else if (a.checked_by_hand) note = '<span class="nr-stale">Checked by hand on ' + new Date(a.last_verified).toLocaleDateString('en-GB',{day:'numeric',month:'short'}) + '</span>';
      return '<div class="nr-card' + (why ? ' off' : '') + (best ? ' best' : '') + '">' +
        '<div class="nr-logo">' + (b.logo ? '<img loading="lazy" alt="' + esc(b.name) + '" src="' + (/^https?:/.test(b.logo) ? '' : ASSETS) + esc(b.logo) + '">' : '') + '</div>' +
        '<div class="nr-name"><p class="nr-bank">' + esc(b.name) + '</p><p class="nr-acc">' + esc(a.name) + '</p><div class="nr-tags">' + tags + '</div></div>' +
        '<div class="nr-rate"><b>' + a.rate.toFixed(2) + '%</b><span>Expected profit rate (AER)</span>' + note + '</div>' +
        '<div class="nr-profit">' + (why ? '<b>Not available</b><span class="nr-why">' + why + '</span>' : '<b>' + gbp(p.value) + '</b><span>Est. profit ' + p.label + '</span>') +
        '<span class="nr-stale">Min ' + gbp(a.min) + ' · Max ' + gbp(a.max) + '</span></div>' +
        '<a class="nr-cta" href="' + esc(a.link) + '" target="_blank" rel="noopener nofollow">View at ' + esc(a.platform === 'Raisin' ? 'Raisin' : b.name.replace(/ Bank( Zurich)?$/,'')) + '</a>' +
      '</div>';
    }).join('');
    if (list.length > shown.length) html += '<button type="button" class="nr-more" id="nr-more">Show all ' + list.length + ' accounts</button>';
    $('nr-list').innerHTML = html;
    var more = $('nr-more');
    if (more) more.onclick = function(){ state.showAll = true; render(); };
  }

  function seg(id, key, num){
    $(id).addEventListener('click', function(e){
      var b = e.target.closest('button'); if (!b) return;
      [].forEach.call(this.children, function(x){ x.classList.toggle('on', x === b); });
      state[key] = num ? Number(b.dataset.v) : b.dataset.v; state.showAll = false; render();
    });
  }
  seg('nr-type', 'type'); seg('nr-isa', 'isa');
  function setAmount(v, fromInput){
    state.amount = Math.max(0, Math.min(10000000, v || 0));
    if (!fromInput) $('nr-amount').value = state.amount.toLocaleString('en-GB');
    [].forEach.call($('nr-presets').children, function(x){ x.classList.toggle('on', Number(x.dataset.v) === state.amount); });
    state.showAll = false; render();
  }
  $('nr-presets').addEventListener('click', function(e){ var b = e.target.closest('button'); if (b) setAmount(Number(b.dataset.v)); });
  $('nr-amount').addEventListener('input', function(){
    var raw = this.value.replace(/[^\d]/g, '');
    var n = Number(raw);
    this.value = raw ? n.toLocaleString('en-GB') : '';
    setAmount(n, true);
  });
  $('nr-term').addEventListener('change', function(){ state.term = Number(this.value); state.showAll = false; render(); });
  $('nr-sort').addEventListener('change', function(){ state.sort = this.value; render(); });
  $('nr-elig').addEventListener('change', function(){ state.elig = this.checked; state.showAll = false; render(); });
  setAmount(10000);
  load();
})();

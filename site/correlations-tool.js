/* Built from site/correlations-tool.html by site/build.py. Do not edit by hand. */
(function(){
var root=document.getElementById('nc-root');if(!root)return;
var st=document.createElement('style');st.textContent="#nc-root, #nc-root *{box-sizing:border-box}\n#nc-root{color:#1a2530;-webkit-font-smoothing:antialiased;text-align:left}\n#nc-root .nc-wrap{max-width:1240px;margin:0 auto;padding:0 20px}\n#nc-root .subtitle{font-size:13px;color:#6b7280;margin-bottom:20px}\n#nc-root .controls{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:16px;padding:14px 16px;background:#fff;border:1px solid #e8e6df;border-radius:16px}\n#nc-root .mode-btn,#nc-root .reset-btn{padding:9px 18px;border:1px solid #d4d1c7;background:#fff;border-radius:999px;cursor:pointer;font-size:13px;color:#1a2530;font-family:Poppins,sans-serif}\n#nc-root .mode-btn:hover,#nc-root .reset-btn:hover{background:#f5f4ef}\n#nc-root .mode-btn.active{background:#1e1e1e;color:#fff;border-color:#1e1e1e}\n#nc-root .reset-btn{color:#6b7280;margin-left:auto}\n#nc-root .help-text{font-size:13px;color:#1a2530;padding:12px 16px;background:#fffbf7;border:1px solid #f1e4d3;border-left:4px solid #ff8e0f;border-radius:6px;margin-bottom:16px;line-height:1.6}\n#nc-root .help-text strong{color:#e67800;font-weight:600}\n#nc-root .portfolio-panel{background:#fff;border:1px solid #e8e6df;border-radius:16px;padding:14px 16px;margin-bottom:16px}\n#nc-root .portfolio-label{font-size:12px;color:#6b7280;margin-bottom:8px}\n#nc-root .portfolio-chips{display:flex;gap:6px;flex-wrap:wrap}\n#nc-root .chip{font-size:12px;padding:5px 10px;background:#e7f0e9;border:1px solid #c7dccb;color:#1a4a2b;border-radius:999px;cursor:pointer;user-select:none}\n#nc-root .chip:hover{background:#d7e6da}\n#nc-root .chip-info{font-size:12px;padding:5px 10px;background:#f5f4ef;border:1px solid #d4d1c7;color:#6b7280;border-radius:999px}\n#nc-root .chip-empty{font-size:12px;color:#9ca3af;font-style:italic}\n#nc-root .matrix-wrap{background:#fff;border:1px solid #e8e6df;border-radius:16px;padding:16px;overflow-x:auto}\n#nc-root .nc-empty{padding:40px 10px;text-align:center;font-size:13px;color:#6b7280}\n#nc-root .grid{display:grid;gap:1px}\n#nc-root .col-header{height:180px;position:relative;min-width:44px}\n#nc-root .col-header-hit{position:absolute;inset:0;cursor:pointer}\n#nc-root .col-header-text{position:absolute;bottom:6px;left:50%;writing-mode:vertical-rl;transform:translateX(-50%) rotate(180deg);white-space:nowrap;font-size:11px;color:#1a2530;pointer-events:none;text-decoration:underline;text-decoration-color:#d4d1c7;text-decoration-style:dotted;text-underline-offset:3px}\n#nc-root .col-header.selected .col-header-text{color:#065f46;font-weight:600}\n#nc-root .col-header.highlighted .col-header-text{color:#fff;font-weight:700;background:#1e40af;padding:3px 8px;border-radius:4px;box-shadow:0 2px 6px rgba(30,64,175,.4);text-decoration:none}\n#nc-root .col-header-hit:hover ~ .col-header-text{color:#0369a1}\n#nc-root .col-header.highlighted .col-header-hit:hover ~ .col-header-text{color:#fff}\n#nc-root .col-header.selected .col-header-hit:hover ~ .col-header-text{color:#065f46}\n#nc-root .row-label{padding:0 10px;display:flex;align-items:center;font-size:11px;color:#1a2530;cursor:pointer;user-select:none;min-width:210px;white-space:nowrap;text-decoration:underline;text-decoration-color:#d4d1c7;text-decoration-style:dotted;text-underline-offset:3px}\n#nc-root .row-label.left{justify-content:flex-end}\n#nc-root .row-label.right{justify-content:flex-start}\n#nc-root .row-label:hover:not(.highlighted):not(.selected){color:#0369a1}\n#nc-root .row-label.selected{color:#065f46;font-weight:600}\n#nc-root .row-label.highlighted{color:#fff;font-weight:700;background:#1e40af;box-shadow:0 2px 6px rgba(30,64,175,.4);border-radius:4px;margin:2px 4px;padding:0 8px;min-width:0;text-decoration:none}\n#nc-root .cell{width:44px;height:32px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:500;cursor:pointer}\n#nc-root .cell:hover{filter:brightness(1.15);outline:2px solid #1a2530;outline-offset:-2px;z-index:2;position:relative}\n#nc-root .cell.diagonal{cursor:default}\n#nc-root .cell.diagonal:hover{filter:none;outline:none}\n#nc-root .cell.na{background:#f1efe9;color:#9ca3af;font-weight:400}\n#nc-root .cell.suggested{outline:3px solid #1e40af;outline-offset:-3px;box-shadow:inset 0 0 0 1px #fff;z-index:3;position:relative}\n#nc-root .cell.suggested::after{content:'';position:absolute;top:2px;right:2px;width:6px;height:6px;background:#1e40af;border-radius:50%;border:1px solid #fff}\n#nc-root .legend{display:flex;gap:14px;align-items:center;margin-top:14px;flex-wrap:wrap;font-size:11px;color:#6b7280}\n#nc-root .legend-swatch{display:flex;height:14px}\n#nc-root .legend-swatch div{width:32px;height:14px}\n#nc-root .legend-labels{display:flex;gap:18px;font-size:10px}\n#nc-root .nc-tooltip{position:fixed;background:#1a2530;color:#fff;padding:8px 12px;border-radius:6px;font-size:12px;pointer-events:none;opacity:0;transition:opacity .1s;z-index:1000;max-width:280px;line-height:1.5}\n#nc-root .nc-tooltip.visible{opacity:1}\n#nc-root .nc-tooltip strong{color:#fbbf24;font-weight:500}\n#nc-root .disclaimer{margin-top:20px;padding:12px 16px;background:#fff8e6;border:1px solid #f4d78a;border-radius:8px;font-size:11px;color:#7a5a0f;line-height:1.5}\n@media(max-width:767px){#nc-root .nc-wrap{padding:0 14px}}";document.head.appendChild(st);
root.innerHTML="<div class=\"nc-wrap\">\n  <div class=\"subtitle\" id=\"nc-sub\">Loading the latest figures\u2026</div>\n\n  <div class=\"controls\">\n    <button class=\"mode-btn active\" data-mode=\"explore\">Explore mode</button>\n    <button class=\"mode-btn\" data-mode=\"build\">Build portfolio</button>\n    <button class=\"reset-btn\" id=\"nc-reset\">Reset</button>\n  </div>\n\n  <div class=\"help-text\" id=\"nc-help\"></div>\n\n  <div class=\"portfolio-panel\" id=\"nc-panel\" style=\"display:none\">\n    <div class=\"portfolio-label\">Your portfolio \u00b7 click a chip to remove \u00b7 next suggestions outlined in blue</div>\n    <div class=\"portfolio-chips\" id=\"nc-chips\"></div>\n  </div>\n\n  <div class=\"matrix-wrap\">\n    <div id=\"nc-grid\"><div class=\"nc-empty\">Loading\u2026</div></div>\n    <div class=\"legend\">\n      <span>Correlation</span>\n      <div class=\"legend-swatch\">\n        <div style=\"background:#2a6b36\"></div>\n        <div style=\"background:#5aaa5e\"></div>\n        <div style=\"background:#a8d08a\"></div>\n        <div style=\"background:#f4e9a1\"></div>\n        <div style=\"background:#f3a86b\"></div>\n        <div style=\"background:#d85a3c\"></div>\n        <div style=\"background:#9a2020\"></div>\n      </div>\n      <div class=\"legend-labels\">\n        <span>-0.2</span><span>0.0</span><span>0.2</span><span>0.4</span><span>0.6</span><span>0.8</span><span>1.0</span>\n      </div>\n      <span style=\"margin-left:12px\">green = diversifying \u00b7 red = redundant</span>\n      <span style=\"margin-left:4px;display:inline-flex;align-items:center;gap:6px\">\n        <span style=\"display:inline-block;width:14px;height:14px;border:3px solid #1e40af;box-sizing:border-box\"></span>\n        <span>= best diversifier</span>\n      </span>\n    </div>\n  </div>\n\n  <div class=\"disclaimer\">\n    <strong>Education only, not personalised financial advice.</strong> Correlations are calculated from weekly returns in pounds over the period shown and will change as market conditions shift. <span id=\"nc-short\"></span>Average pair correlation is a simplified measure: it does not account for position sizes or volatility. Past correlations are not a guide to future ones. Always do your own research or speak to a qualified adviser before investing.\n  </div>\n</div>\n<div class=\"nc-tooltip\" id=\"nc-tooltip\"></div>";
})();
(function(){
  var DATA = [
    'https://raw.githubusercontent.com/nisbacode/nisba-rates/main/docs/correlations.json',
    'https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@main/docs/correlations.json'
  ];
  var $ = function(id){ return document.getElementById(id); };
  var root = $('nc-grid');
  if (!root) return;
  var funds = [], matrix = [], n = 0, win = null;
  var mode = 'explore', highlighted = null, portfolio = [];

  var HELP = {
    explore: '👉 <strong>Click a fund name</strong> (in the row or column labels, not the cells) to highlight its three best diversifiers. Hover any cell to see the correlation.',
    build: '👉 <strong>Click fund names</strong> (row or column labels) to add them to your portfolio. After each click, the three best next additions (lowest average correlation with your basket) are highlighted in blue.'
  };

  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function fmtDate(iso, withYear){
    return new Date(iso + 'T12:00:00Z').toLocaleDateString('en-GB', withYear === false ? {day:'numeric', month:'short'} : {day:'numeric', month:'short', year:'numeric'});
  }
  function isShort(f){ return win && f.weeks < win.weeks - 4; }
  function label(i){ return funds[i].name + (isShort(funds[i]) ? ' *' : ''); }
  function fmt(v){ return v == null ? 'n/a' : (v === 1 ? '1' : v.toFixed(2)); }

  function colorFor(v){
    if (v >= 0.95) return '#7a1616';
    if (v >= 0.85) return '#9a2020';
    if (v >= 0.75) return '#bc3a2a';
    if (v >= 0.65) return '#d85a3c';
    if (v >= 0.55) return '#e88458';
    if (v >= 0.45) return '#f3a86b';
    if (v >= 0.35) return '#f7c97e';
    if (v >= 0.25) return '#f4e9a1';
    if (v >= 0.15) return '#d4e39a';
    if (v >= 0.05) return '#a8d08a';
    if (v >= -0.05) return '#5aaa5e';
    if (v >= -0.15) return '#3d8f4a';
    return '#2a6b36';
  }
  function textColor(v){ return (v >= 0.65 || v <= 0.10) ? '#ffffff' : '#2a1810'; }

  function bestDiversifiers(sel, count){
    var ranked = [];
    for (var i = 0; i < n; i++) {
      if (i === sel || matrix[sel][i] == null) continue;
      ranked.push({ idx: i, corr: matrix[sel][i] });
    }
    ranked.sort(function(a, b){ return a.corr - b.corr; });
    return ranked.slice(0, count || 3);
  }
  function nextSuggestions(picks, count){
    if (!picks.length) return [];
    var ranked = [];
    for (var i = 0; i < n; i++) {
      if (picks.indexOf(i) > -1) continue;
      var sum = 0, c = 0;
      picks.forEach(function(p){ if (matrix[i][p] != null) { sum += matrix[i][p]; c++; } });
      if (c === picks.length) ranked.push({ idx: i, corr: sum / c });
    }
    ranked.sort(function(a, b){ return a.corr - b.corr; });
    return ranked.slice(0, count || 3);
  }
  function averageCorrelation(picks){
    var sum = 0, c = 0;
    for (var i = 0; i < picks.length; i++) for (var j = i + 1; j < picks.length; j++) {
      var v = matrix[picks[i]][picks[j]];
      if (v != null) { sum += v; c++; }
    }
    return c ? sum / c : null;
  }

  function el(cls, text){ var d = document.createElement('div'); if (cls) d.className = cls; if (text != null) d.textContent = text; return d; }

  function render(){
    var grid = el('grid');
    grid.style.gridTemplateColumns = '210px repeat(' + n + ', 44px) 210px';
    var suggested = {};
    if (mode === 'explore' && highlighted !== null) bestDiversifiers(highlighted).forEach(function(d){ suggested[d.idx] = 1; });
    else if (mode === 'build' && portfolio.length) nextSuggestions(portfolio).forEach(function(d){ suggested[d.idx] = 1; });
    function marks(node, i){
      if (portfolio.indexOf(i) > -1 || i === highlighted) node.classList.add('selected');
      if (suggested[i]) node.classList.add('highlighted');
    }

    grid.appendChild(el());
    for (var j = 0; j < n; j++) {
      var head = el('col-header'); marks(head, j);
      var hit = el('col-header-hit'); hit.dataset.type = 'header'; hit.dataset.idx = j;
      head.appendChild(hit); head.appendChild(el('col-header-text', label(j)));
      grid.appendChild(head);
    }
    grid.appendChild(el());

    for (var i = 0; i < n; i++) {
      var left = el('row-label left', label(i)); marks(left, i);
      left.dataset.type = 'header'; left.dataset.idx = i;
      grid.appendChild(left);
      for (var k = 0; k < n; k++) {
        var v = matrix[i][k], cell = el('cell', fmt(v));
        if (i === k) cell.classList.add('diagonal');
        if (v == null) cell.classList.add('na');
        else { cell.style.background = colorFor(v); cell.style.color = textColor(v); }
        if (mode === 'explore' && ((i === highlighted && suggested[k]) || (k === highlighted && suggested[i]))) cell.classList.add('suggested');
        cell.dataset.type = 'cell'; cell.dataset.i = i; cell.dataset.j = k;
        grid.appendChild(cell);
      }
      var right = el('row-label right', label(i)); marks(right, i);
      right.dataset.type = 'header'; right.dataset.idx = i;
      grid.appendChild(right);
    }
    root.innerHTML = '';
    root.appendChild(grid);
    renderPortfolio();
  }

  function renderPortfolio(){
    var panel = $('nc-panel'), chips = $('nc-chips');
    if (mode !== 'build') { panel.style.display = 'none'; return; }
    panel.style.display = 'block';
    chips.innerHTML = '';
    if (!portfolio.length) {
      var empty = document.createElement('span');
      empty.className = 'chip-empty';
      empty.textContent = 'No funds selected yet. Click a fund name to start.';
      chips.appendChild(empty);
      return;
    }
    portfolio.forEach(function(idx){
      var chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = funds[idx].name + ' ✕';
      chip.addEventListener('click', function(){ portfolio = portfolio.filter(function(p){ return p !== idx; }); render(); });
      chips.appendChild(chip);
    });
    var avg = portfolio.length > 1 ? averageCorrelation(portfolio) : null;
    if (avg != null) {
      var info = document.createElement('span');
      info.className = 'chip-info';
      info.textContent = 'Avg pair correlation: ' + avg.toFixed(2);
      chips.appendChild(info);
    }
  }

  var tip = $('nc-tooltip');
  function place(e){ tip.style.left = (e.clientX + 14) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; }
  function show(e, html){ tip.innerHTML = html; tip.classList.add('visible'); place(e); }
  function hide(){ tip.classList.remove('visible'); }
  function history(f){ return isShort(f) ? '<br>Priced since ' + esc(fmtDate(f.since)) + ' (' + f.weeks + ' weeks)' : ''; }

  root.addEventListener('click', function(e){
    var t = e.target.closest('[data-type]');
    if (!t || t.dataset.type !== 'header') return;
    var idx = parseInt(t.dataset.idx, 10);
    if (mode === 'explore') highlighted = (highlighted === idx) ? null : idx;
    else if (portfolio.indexOf(idx) > -1) portfolio = portfolio.filter(function(p){ return p !== idx; });
    else portfolio.push(idx);
    render();
  });
  root.addEventListener('mouseover', function(e){
    var t = e.target.closest('[data-type]');
    if (!t) { hide(); return; }
    if (t.dataset.type === 'cell') {
      var i = parseInt(t.dataset.i, 10), j = parseInt(t.dataset.j, 10);
      if (i === j) show(e, '<strong>' + esc(funds[i].name) + '</strong>' + history(funds[i]));
      else show(e, '<strong>' + esc(funds[i].name) + '</strong><br>↕<br><strong>' + esc(funds[j].name) + '</strong><br>' +
        (matrix[i][j] == null ? 'Not enough shared history yet' : 'Correlation: ' + matrix[i][j].toFixed(2)) +
        ((isShort(funds[i]) || isShort(funds[j])) && matrix[i][j] != null ? '<br>Based on ' + Math.min(funds[i].weeks, funds[j].weeks) + ' weeks' : ''));
    } else {
      var idx = parseInt(t.dataset.idx, 10);
      if (mode === 'explore') {
        var html = '<strong>' + esc(funds[idx].name) + '</strong>' + history(funds[idx]) + '<br>Click to highlight 3 best diversifiers:';
        bestDiversifiers(idx).forEach(function(d){ html += '<br>· ' + esc(funds[d.idx].name) + ' (' + d.corr.toFixed(2) + ')'; });
        show(e, html);
      } else {
        show(e, '<strong>' + esc(funds[idx].name) + '</strong>' + history(funds[idx]) + '<br>Click to ' + (portfolio.indexOf(idx) > -1 ? 'remove from' : 'add to') + ' portfolio');
      }
    }
  });
  root.addEventListener('mousemove', function(e){ if (tip.classList.contains('visible')) place(e); });
  root.addEventListener('mouseleave', hide);

  Array.prototype.forEach.call(document.querySelectorAll('#nc-root .mode-btn'), function(btn){
    btn.addEventListener('click', function(){
      mode = btn.dataset.mode;
      Array.prototype.forEach.call(document.querySelectorAll('#nc-root .mode-btn'), function(b){ b.classList.toggle('active', b === btn); });
      highlighted = null; portfolio = [];
      $('nc-help').innerHTML = HELP[mode];
      if (n) render();
    });
  });
  $('nc-reset').addEventListener('click', function(){ highlighted = null; portfolio = []; if (n) render(); });
  $('nc-help').innerHTML = HELP.explore;

  function ready(j){
    funds = j.funds; matrix = j.matrix; n = funds.length; win = j.window;
    var years = win.weeks === 104 ? 'two years' : win.weeks + ' weeks';
    $('nc-sub').textContent = 'Weekly returns in pounds, ' + years + ' to ' + fmtDate(win.end) + ' · Recalculated at the start of each month · Prices: Alpha Vantage';
    var short = funds.filter(isShort);
    $('nc-short').textContent = short.length ? 'Funds marked * were first priced during the period, so their figures cover a shorter history (hover a fund name to see how long). ' : '';
    render();
  }
  function load(i){
    if (i >= DATA.length) { root.innerHTML = '<div class="nc-empty">We could not load the correlation figures. Please refresh in a minute.</div>'; $('nc-sub').textContent = ''; return; }
    fetch(DATA[i] + '?t=' + Math.floor(Date.now() / 300000), {cache:'no-store'})
      .then(function(r){ if (!r.ok) throw 0; return r.json(); })
      .then(function(j){ if (!j.funds || !j.matrix) throw 0; ready(j); })
      .catch(function(){ load(i + 1); });
  }
  load(0);
})();

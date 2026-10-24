// Run on any markets.ft.com page (same origin) with javascript_tool.
// Replace FUNDS with up to 2 [ticker, xid] pairs per call (output is limited to about 1KB).
// Returns lines of "TICKER#YYMMDD price,YYMMDD price,..." covering:
//   the last 12 days, a week around 6 months ago, and a week around 1 year ago.
(async (FUNDS) => {
  const mon = {Jan:1,Feb:2,Mar:3,Apr:4,May:5,Jun:6,Jul:7,Aug:8,Sep:9,Oct:10,Nov:11,Dec:12};
  const fmt = d => d.getFullYear() + '/' + String(d.getMonth() + 1).padStart(2, '0') + '/' + String(d.getDate()).padStart(2, '0');
  const ago = n => { const d = new Date(); d.setDate(d.getDate() - n); return d; };
  const windows = [[ago(12), ago(0)], [ago(186), ago(179)], [ago(369), ago(362)]];
  const out = [];
  for (const [t, xid] of FUNDS) {
    const parts = [];
    for (const [a, b] of windows) {
      const r = await fetch('/data/equities/ajax/get-historical-prices?startDate=' + encodeURIComponent(fmt(a)) + '&endDate=' + encodeURIComponent(fmt(b)) + '&symbol=' + xid);
      if (!r.ok) { parts.push('ERR' + r.status); continue; }
      const j = await r.json();
      const tb = document.createElement('table'); tb.innerHTML = j.html || '';
      tb.querySelectorAll('tr').forEach(tr => {
        const td = tr.querySelectorAll('td'); if (td.length < 5) return;
        const s = td[0].querySelectorAll('span');
        const m = (s.length ? s[s.length - 1].innerText : td[0].innerText).trim().match(/(\w{3}) (\d{1,2}), (\d{4})/);
        if (!m) return;
        parts.push(m[3].slice(2) + String(mon[m[1]]).padStart(2, '0') + m[2].padStart(2, '0') + ' ' + td[4].innerText.replace(/,/g, '').trim());
      });
    }
    out.push(t + '#' + parts.join(','));
  }
  return out.join('\n');
})(FUNDS)

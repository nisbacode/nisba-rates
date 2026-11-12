# nisba-rates

The daily check behind the Islamic savings accounts table on [nisba.co.uk/savings-accounts](https://www.nisba.co.uk/savings-accounts).

## What it does

Every morning at about 6 to 7am UK time, GitHub runs `scraper/scrape.py`. It:

1. Opens each bank's own pages (Al Rayan, BLME, Gatehouse, Habib Bank Zurich) and Raisin (for Al Rayan, QIB and KFH accounts sold there), plus Prosper (for Al Rayan and BLME accounts sold there).
2. Reads the current rate for every account listed in `accounts.json`.
3. Checks each figure makes sense. If a rate can't be found, looks wrong, or jumps by more than 1.5 points overnight, it keeps the last confirmed figure and marks that account as not confirmed today.
4. Writes everything to `docs/rates.json`, which the website reads live on every visit.
5. If anything needs a human, opens a GitHub issue called **Savings rates need a look** (you get an email). The issue closes itself once everything reads fine again. New accounts that appear on Raisin are listed there too.

The website file is here:
`https://raw.githubusercontent.com/nisbacode/nisba-rates/main/docs/rates.json`

## Common jobs

**Add an account:** copy a similar entry in `accounts.json`, give it a new `id`, and fill in the details. The `source` block says where to read it:

| kind | how it finds the rate |
|---|---|
| `gatehouse` | `match` is a pattern for the product name on gatehousebank.com/personal/savings |
| `alrayan` | `page` is the listing page, `match` a pattern for the account name |
| `blme_premier` | uses `term_months` to pick the row from the Premier Deposit table |
| `blme_notice` | reads the "Gross AER" figure on the notice account page |
| `habib_sirat` | uses `term_months` to pick the HBZ Sirat eDeposit term |
| `raisin` | `bank_slug` and `product` are from the Raisin URL, e.g. raisin.co.uk/bank/qib/**QIB001** |
| `prosper` | `page` is the Prosper product page, e.g. prosper.co.uk/savings/blme-9-month-fixed-term-deposit. Reads the AER after "What is the interest rate?". New Al Rayan, BLME, QIB, Gatehouse, KFH or Habib products on the Prosper listing are noted in the report |

**Remove an account:** delete its entry from `accounts.json`.

**Run it now:** Actions tab, "Daily rate check", Run workflow.

**See what the scraper read:** open a run in the Actions tab and download the `debug` file at the bottom.

Rates are for information only and are not personalised financial advice.

## The website tool

The comparison table on the savings page is `site/savings-tool.html`. After editing it, run `python site/build.py` and commit both files. Kajabi holds a small loader (Site theme, Savings Accounts page, section "Savings comparison (native)") that pulls `site/savings-tool.js` from jsDelivr pinned to a commit, e.g. `https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@<commit>/site/savings-tool.js`. Update the commit in that loader to publish a new version of the tool. The rates themselves need no Kajabi change: the tool reads `docs/rates.json` live every visit.

## Fund prices

`funds/funds.json` lists the 51 funds on nisba.co.uk/funds. The "Daily fund check" workflow (about 6:20am UK) works out performance for each fund and writes `docs/funds.json`, which the funds page reads live:

- **33 ETFs and ETCs**: daily prices from Alpha Vantage (secret `ALPHA_VANTAGE_API_KEY`, premium plan). MWIX uses its USD twin MWIM.
- **16 funds** (HSBC, Schroders, Baillie Gifford, Franklin, BNP Paribas, Oasis Crescent, Mayar, plus DJIW, HBKU, HSKG, HSKD and XASB): prices from FT.com, kept in `funds/ft_prices.json`. A Claude scheduled task ("Nisba FT fund price check", 7:52am UK, runs through Ahmad's Chrome) reads the latest prices with `funds/ft_fetch.js`, merges them with `funds/ft_merge.py`, pushes, and reruns the workflow.

Returns are price returns, so income (distributing) share classes understate total return.

**Factsheets:** each fund in `funds/funds.json` has a `factsheet` field, which the page shows as a "Factsheet" link. Most point at the provider's own "latest factsheet" PDF (HSBC, iShares, Schroders, HANetf, Baillie Gifford, DWS), which updates in place each month. Where the provider has no stable PDF link the field points at the provider's fund page or factsheet listing instead (Invesco, WisdomTree, Wahed, BNP Paribas, Oasis Crescent, Mayar, the Franklin Ultra Short fund). The two Franklin Global Sukuk PDFs are dated downloads, so check them if Franklin changes its site. To change a link, edit `funds/funds.json`; it flows into `docs/funds.json` on the next daily run.

## Correlations

The table on [nisba.co.uk/correlations](https://www.nisba.co.uk/correlations) reads `docs/correlations.json` live. The "Daily fund check" workflow recalculates it once a month (the first run after a month ends) from the same daily prices it already downloads, using `funds/correlations.py`: weekly returns in pounds over the two years to the last month end. Each pair uses the weeks both funds have prices for, and needs at least 26 shared weeks.

**Change the funds shown:** edit the `FUNDS` list at the top of `funds/correlations.py` (tickers must exist in `funds/funds.json` with an Alpha Vantage code).

**Recalculate now:** Actions tab, "Daily fund check", Run workflow, and type `yes` in the correlations box.

The page tool is `site/correlations-tool.html`, built to `site/correlations-tool.js` by `python site/build.py correlations-tool`. Kajabi holds the loader (Site theme, Correlations page, "Custom Code" section) pinned to a commit, the same way as the savings tool.

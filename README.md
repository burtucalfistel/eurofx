# eurofx

ECB reference rates from the terminal — no key, no account, one XML feed.

```
$ eurofx convert 100 USD
100.00 EUR = 112.14 USD

$ eurofx compare USD 30
EUR/USD over 30 sessions
  first 2026-09-30 1.1355
  last  2026-11-10 1.1214  (-1.24%)
  min 1.1130  max 1.1355  avg 1.1208
```

Data source: [ECB euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)
(historical 90-day feed). Standard library only.

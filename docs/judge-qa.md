# Likely judge questions and short answers

For the team before the judging. Every number here is in the repo: `web/public/data/*.json`, `web/public/data/futuros_nasa.json`, [validation.md](validation.md) and [earth-engine.md](earth-engine.md). If a number changes after a re-export, update this page.

**1. Why should a farmer trust a satellite over their own experience?**
They shouldn't have to choose. The farmer view shows what happened on their own plot (bare months, fires, long dry spells), the things they already know, so they can check the tool against their memory. The options are for talking over with the extension worker; the audio says it is not an official notice.

**2. How do you know the engine is right?**
We fixed the rule first and then tested it on a year it had not seen: with data up to 2017, it flags the 2018 drought as high risk at 5 of 5 plots, and FAO GIEWS relayed a preliminary MAGA estimate of 175,126 ha of crop losses, mostly maize and beans, in Guatemala that year. We also publish its misses: 2 to 3 false alarms and 1 miss in 20 years per plot.

**3. What does "holds in 9 of 33 futures" mean?**
NASA's NEX-GDDP-CMIP6 gives daily projections from 33 climate models under intermediate emissions (34 under high). For each model we take its own change in rain and temperature for 2041-2060 against 1995-2014, apply it to the observed rain at the plot, and rerun the same water balance. "Holds" means the rotation's water score is as good as today's practice with today's climate.

**4. Why not use one climate model, or the average?**
The models disagree, and the disagreement is the point. Showing one dot per model lets the extension worker see whether a rotation holds in almost every future or only in a few. The average would hide that.

**5. Isn't the drought-tolerant option winning only because it starts higher?**
Partly, and we say it on the page. It already has a higher water score today. The useful part is the other side: today's maize and beans keeps today's water score in only 2 to 9 futures out of 33 or 34.

**6. Why CHIRPS for rain if this is a NASA challenge?**
At this scale NASA POWER rain is off by −22 % to +55 % in July and August compared with CHIRPS, and four of the five plots fall in one POWER cell. We measured that and show it. CHIRPS daily uses NASA GPM IMERG to split rain into days, and POWER still gives temperature and evapotranspiration.

**7. What happens when data is missing?**
The fact turns grey: "The satellite can't see well here". Camotán has no SMAP data of recommended quality, so its confidence is low and the screen says why. The tool never fills a gap with a guess.

**8. Does AI make up the advice?**
No AI produces any number on screen. Numbers come from the data and the rules in code; texts come from fixed templates, and a validator rejects any number that is not in the engine's output. The voice is synthetic and labelled as AI. Full statement in [ai-use.md](ai-use.md).

**9. Who checked the agronomy?**
An agronomist confirmed three facts we rely on: ICTA B-7 is the most used maize in eastern Guatemala because of its drought tolerance, postrera beans are planted in August and September, and 10 days without rain at flowering already damage maize. The scoring rules still need a full review, and we list that as a limit.

**10. Does it work without internet?**
Yes. The site is static files; the map falls back to saved NASA GIBS layers; audio and data are local. `npm run sin-red` checks it with the internet blocked; it has not been tried in the field yet. Earth Engine was used only once, offline, to precompute the climate futures.

**11. How would this reach more farmers?**
Through the people who already advise them. Extension workers can show it in the field from a laptop or phone, print the one-page sheet or share the audio on WhatsApp. Next steps: visit the plots with extension workers, agronomist review, INSIVUMEH station rain and audio in Ch'orti'.

**12. What is the biggest weakness?**
The five plots are example points chosen by satellite, not visited yet, and the thresholds were set after seeing the data. We show both on the "Where it fails" panel instead of hiding them.

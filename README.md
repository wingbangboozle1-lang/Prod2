# Prod2 · Countertop Journal (working name)

A static affiliate site for five Amazon products (air fryers and meat thermometers), published from `docs/` through GitHub Pages.

## Layout

- `data/products.json`: the product register (supplied links, observed and intended ASINs kept apart, listing titles, flags).
- `scripts/build_site.py`: generates every page in `docs/` from the register. Standard library only.
- `scripts/verify_site.py`: the verification gate (disclosure, sponsored links, tracking tag, links, sources, banned claims, sitemap, feed).
- `scripts/assets/`: stylesheet and the outbound-click counter (`tracker.js`).
- `docs/`: generated site. Do not edit by hand; run the build.
- `COORDINATION.md`: shared task board and log.

## Rebuild and verify

```sh
python3 scripts/build_site.py
python3 scripts/verify_site.py
```

## Disclosure

As an Amazon Associate I earn from qualifying purchases. This site is not endorsed by or affiliated with Amazon.

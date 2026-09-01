# VibeCurb Design Read

## Audit summary

This is a framework-free static portfolio with one high-risk dynamic surface: `portfolio.js` renders repository data, maintains filters, and updates statistics. That logic, the repository generator, the JSON contract, routes, links, IDs, ARIA attributes, and page hierarchy are sacred. The visual layer is low risk and currently relies on a floating glass header, Manrope and DM Sans, large rounded cards, gradient stand-ins, pill filters, generic shadows, and decorative motion. The redesign can be implemented as reversible CSS overrides plus additive media and reveal attributes without touching the existing application logic.

## File classification

| Area | Sacred elements | Visual changes allowed | Risk |
| --- | --- | --- | --- |
| `portfolio.js` | Fetch, state, newest-six slice, filters, rendering, errors, statistics, selector IDs | None | High |
| `index.html` | IDs, anchors, ARIA, four App Store URLs, internal product routes, social links | Copy updates approved by the brief, additive media, classes, reveal attributes | Medium |
| `portfolio.css` | Existing stylesheet remains as rollback layer | None, superseded by `gold.css` | Low |
| `data/repos.json` | Entire schema and generated content | None | High |
| `scripts/update_repos.py`, workflow, tests | Pagination, filtering, sorting, snapshot semantics | Regression tests may be added | High |
| ShadeDrop and CurtainShot pages | Routes, copy, privacy and support links, issue and email links | Additive App Store calls to action, classes, and override stylesheet | Medium |
| `style.css` | Existing shared page stylesheet remains as rollback layer | None, superseded by a product override | Low |
| `favicon.svg`, `og.png` | Correct file locations and metadata references | Visual redesign | Low |

## Functional inventory

- Homepage anchors: Apps, Projects, About, and back to top.
- Four released products with App Store actions.
- Internal product pages for ShadeDrop and CurtainShot.
- Privacy and support routes for ShadeDrop and CurtainShot.
- Daily public repository snapshot generation.
- Six most recently pushed eligible repositories.
- Full repository catalog with search, language filters, live-demo toggle, clear filters, result count, empty state, and load failure state.
- Dynamic original-project and language totals.
- GitHub, LinkedIn, Devpost, support email, and GitHub issue links.
- Automatic light and dark themes, keyboard focus, skip link, and reduced motion.

## Extraction sheet

### 1. Tokens

| Decision | Current | Target |
| --- | --- | --- |
| Canvas | `#f5f7fb` and `#090d17` | Warm paper `#f0eee8` and charcoal `#11100f` |
| Surface | White or navy cards | Mostly canvas with `#e6e2d9` or `#1c1a18` section contrast |
| Text | `#101522`, `#f1f5fb` | Ink `#171614`, warm white `#f4f0e8` |
| Muted text | `#596273`, `#9aa7ba` | `#6f6b63`, `#aaa49a` |
| Accent | Teal `#0a6e5d` and `#52d8c0` | Vermilion `#cf4427` and `#ff765a` |
| Border | Blue-gray `#dbe1ea` or `#263247` | Warm ink at 14 to 18 percent opacity |
| Radius | 18 and 28px, pills at 999px | 0, 3, and 6px only |
| Shadow | 24 by 70px floating shadows | None at rest, subtle media shadow only where needed |

### 2. Typography

| Element | Current | Target |
| --- | --- | --- |
| Display | Manrope 600 to 800 | Instrument Sans 500 to 700 |
| Body | DM Sans 400 to 700 | Instrument Sans 400 to 600 |
| Metadata | Same family as body | IBM Plex Mono 400 to 500 |
| H1 | Up to 6.5rem, 0.98 line-height | Up to 8.8rem, 0.86 to 0.92 line-height |
| H2 | Up to 4rem | Up to 5.5rem with stronger section contrast |
| Body measure | About 680px | 58 to 68ch |
| Tracking | `-0.045em` headings | `-0.055em` display, `0.08em` mono labels |

### 3. Spacing

- Current sections use 7rem repeatedly with 1rem card gaps.
- Target spacing uses a 4, 8, 12, 20, 32, 48, 72, 112, and 160px rhythm.
- Desktop container expands from 1200px to 1360px.
- Product sections receive 112 to 160px vertical separation and a 12-column grid.
- Mobile gutters remain at least 20px and touch targets remain at least 44px.

### 4. Color usage

- Remove decorative teal and purple gradients.
- Use warm neutral fields, a single vermilion action color, and product imagery for local color.
- Keep language dots as functional metadata colors.
- Dark mode mirrors the hierarchy without pure black or pure white.

### 5. Components

- Floating glass header becomes a thin solid editorial rail.
- Hero statistics card becomes a border-top information rail.
- Released apps become full-width product features with real media.
- Latest projects become six structured editorial entries.
- Full project cards become dense index rows.
- Filter pills become compact tab-like controls with restrained active states.
- Buttons use square geometry, clear hierarchy, underline or arrow motion, and no generic lift.

### 6. Atmosphere

- Use warm canvas color, hairline rules, and very subtle fixed grain below 0.025 opacity.
- No glassmorphism or decorative gradient fields.
- Alternate broad section tones only where they improve chapter separation.

### 7. Motion

- Remove the infinite signal animation and generic card lifts.
- Use `cubic-bezier(0.16, 1, 0.3, 1)` only.
- Hero entry uses 700 to 850ms opacity and vertical translation.
- Below-fold sections reveal once with opacity and 24px translation.
- Interactive feedback stays between 160 and 240ms.
- Reduced motion leaves all content immediately visible and static.

## Prescription map

| Current problem | Replacement |
| --- | --- |
| Glass nav | Solid top rail with a single bottom rule |
| Generic hero plus decorative dashboard | Product-first statement and simple dynamic facts |
| Gradient app placeholders | Local App Store icons and screenshots in square-edged media fields |
| Repeated rounded cards | Full-width product chapters and ruled project rows |
| Pills everywhere | Compact rectangular tabs and text actions |
| Teal SaaS palette | Warm paper, ink, and vermilion |
| Same typography for all information | Instrument Sans hierarchy plus IBM Plex Mono metadata |
| Infinite signal bars | Removed |
| Hover lift and large shadows | Underline, arrow, border, and image-scale feedback |
| Dense three-column catalog | Readable editorial index with metadata columns |

## Pre-implementation quality gate

- [x] Every tracked application file and route was inspected.
- [x] Sacred logic, selectors, routes, links, and data contracts are documented.
- [x] Baselines exist at 1440, 768, and 390 in light and dark modes.
- [x] Seven award references and twelve useful captures are stored in the benchmark folder.
- [x] Current tokens and all seven visual layers are extracted with exact values.
- [x] The target token system and component prescription are specified.
- [x] All current interactive behaviors have regression cases.
- [x] Approved private products expose only public product copy and App Store links.
- [x] No private repository URLs are scheduled for the public site.

Gate result: PASS. Visual surgery may begin through reversible override files. `portfolio.js`, the repository data contract, and synchronization logic remain untouched.

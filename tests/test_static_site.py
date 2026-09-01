import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")


class StaticSiteRegressionTests(unittest.TestCase):
    def test_javascript_contract_ids_are_preserved(self):
        required_ids = {
            "main-content",
            "project-stat",
            "language-stat",
            "latest-projects",
            "project-search",
            "demo-filter",
            "language-filters",
            "results-count",
            "clear-filters",
            "project-grid",
        }
        for element_id in required_ids:
            self.assertIn(f'id="{element_id}"', HOME)

    def test_homepage_has_required_public_actions(self):
        required_urls = {
            "https://apps.apple.com/us/app/shadedrop/id6802923512?mt=12",
            "https://apps.apple.com/us/app/curtainshot/id6803316414?mt=12",
            "https://apps.apple.com/us/app/ramayana-vaani/id6800575063",
            "https://apps.apple.com/us/app/call-a-hero/id6797733811",
            "https://github.com/vinayanand3",
            "https://www.linkedin.com/in/vinayanand2",
            "https://devpost.com/vinayanand2",
            "/shadedrop/",
            "/curtainshot/",
        }
        for url in required_urls:
            self.assertIn(url, HOME)

    def test_private_repository_identifiers_are_not_published(self):
        public_files = [
            ROOT / "index.html",
            ROOT / "portfolio.js",
            ROOT / "gold.css",
            ROOT / "product-gold.css",
            ROOT / "data" / "repos.json",
        ]
        forbidden = (
            "github.com/vinayanand3/ramayana-vaani",
            "github.com/vinayanand3/call-a-hero-ios-app",
        )
        for path in public_files:
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                self.assertNotIn(value, text)

    def test_override_assets_and_product_routes_exist(self):
        self.assertIn('<link rel="stylesheet" href="/gold.css">', HOME)
        self.assertIn('<script src="/motion.js" defer></script>', HOME)
        for path in (
            "shadedrop/index.html",
            "shadedrop/privacy/index.html",
            "shadedrop/support/index.html",
            "curtainshot/index.html",
            "curtainshot/privacy/index.html",
            "curtainshot/support/index.html",
        ):
            page = ROOT / path
            self.assertTrue(page.is_file())
            text = page.read_text(encoding="utf-8")
            self.assertIn('/product-gold.css', text)
            self.assertIn('class="utility-skip"', text)
            self.assertIn('id="main-content"', text)
            self.assertIn('class="utility-header"', text)
            self.assertIn('class="utility-footer"', text)
            self.assertIn('aria-label="Portfolio navigation"', text)
            self.assertIn('href="/#featured"', text)
            self.assertIn('href="/#projects"', text)
            self.assertIn('https://github.com/vinayanand3', text)

        product_actions = {
            "shadedrop/index.html": "https://apps.apple.com/us/app/shadedrop/id6802923512?mt=12",
            "curtainshot/index.html": "https://apps.apple.com/us/app/curtainshot/id6803316414?mt=12",
        }
        for path, url in product_actions.items():
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertEqual(text.count(url), 2)

    def test_latest_six_contract_and_repository_order(self):
        script = (ROOT / "portfolio.js").read_text(encoding="utf-8")
        self.assertIn("state.projects.slice(0, 6)", script)
        projects = json.loads((ROOT / "data" / "repos.json").read_text(encoding="utf-8"))
        pushed = [project["pushedAt"] for project in projects]
        self.assertEqual(pushed, sorted(pushed, reverse=True))
        self.assertEqual(len(projects[:6]), 6)

    def test_app_store_media_is_local_and_optimized(self):
        names = (
            "shadedrop-icon.webp",
            "shadedrop-screen.webp",
            "curtainshot-icon.webp",
            "curtainshot-screen.webp",
            "ramayana-vaani-icon.webp",
            "ramayana-vaani-screen.webp",
            "call-a-hero-icon.webp",
            "call-a-hero-screen.webp",
        )
        for name in names:
            path = ROOT / "assets" / "apps" / name
            self.assertTrue(path.is_file())
            self.assertLess(path.stat().st_size, 350 * 1024)

    def test_mobile_presentation_stays_light_and_catalog_stays_visible(self):
        homepage_styles = (ROOT / "gold.css").read_text(encoding="utf-8")
        product_styles = (ROOT / "product-gold.css").read_text(encoding="utf-8")
        self.assertIn("color-scheme: light", homepage_styles)
        self.assertIn("color-scheme: light", product_styles)
        self.assertNotIn("prefers-color-scheme: dark", homepage_styles)
        self.assertNotIn("prefers-color-scheme: dark", product_styles)
        self.assertIn(".motion-ready #projects[data-reveal]", homepage_styles)
        self.assertIn('<meta name="theme-color" content="#f0eee8">', HOME)


if __name__ == "__main__":
    unittest.main()

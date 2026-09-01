(() => {
    "use strict";

    const DATA_URL = "/data/repos.json";
    const FALLBACK_DESCRIPTION = "Explore the source, implementation details, and latest updates on GitHub.";
    const LANGUAGE_COLORS = {
        Astro: "#ff5d01",
        "C++": "#659ad2",
        CSS: "#7b61ff",
        HTML: "#e85d35",
        JavaScript: "#d5b830",
        Python: "#3776ab",
        Swift: "#f05138",
        TypeScript: "#3178c6",
    };
    const SPECIAL_WORDS = new Map([
        ["ai", "AI"], ["api", "API"], ["dfmea", "DFMEA"], ["html", "HTML"],
        ["ios", "iOS"], ["macos", "macOS"], ["ml", "ML"], ["pdf", "PDF"],
        ["ui", "UI"], ["url", "URL"], ["ux", "UX"],
    ]);

    const state = { projects: [], query: "", language: "All", liveOnly: false };
    const elements = {
        latest: document.querySelector("#latest-projects"),
        grid: document.querySelector("#project-grid"),
        search: document.querySelector("#project-search"),
        demoFilter: document.querySelector("#demo-filter"),
        languageFilters: document.querySelector("#language-filters"),
        resultsCount: document.querySelector("#results-count"),
        clearFilters: document.querySelector("#clear-filters"),
        projectStat: document.querySelector("#project-stat"),
        languageStat: document.querySelector("#language-stat"),
    };

    function humanizeName(name) {
        return name
            .split(/[-_]+/)
            .filter(Boolean)
            .map((word) => SPECIAL_WORDS.get(word.toLowerCase()) || `${word.charAt(0).toUpperCase()}${word.slice(1)}`)
            .join(" ");
    }

    function formatDate(value) {
        if (!value) return "Recently updated";
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) return "Recently updated";
        return `Updated ${new Intl.DateTimeFormat("en", { month: "short", year: "numeric" }).format(date)}`;
    }

    function makeElement(tag, className, text) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (text !== undefined) element.textContent = text;
        return element;
    }

    function externalLink(label, url, className) {
        const link = makeElement("a", className);
        link.href = url;
        link.target = "_blank";
        link.rel = "noreferrer";
        link.append(document.createTextNode(`${label} `));
        const arrow = makeElement("span", "external-arrow", "↗");
        arrow.setAttribute("aria-hidden", "true");
        link.append(arrow);
        return link;
    }

    function createProjectCard(project, featured = false) {
        const card = makeElement("article", `project-card${featured ? " project-card-latest" : ""}`);
        const top = makeElement("div", "project-card-top");
        const language = makeElement("span", "project-language", project.language || "Other");
        const dot = makeElement("span", "language-dot");
        dot.style.backgroundColor = LANGUAGE_COLORS[project.language] || "var(--accent)";
        dot.setAttribute("aria-hidden", "true");
        language.prepend(dot);
        top.append(language, makeElement("span", "project-date", formatDate(project.pushedAt || project.updatedAt)));

        const title = makeElement("h3", null, humanizeName(project.name));
        const description = makeElement("p", "project-description", project.description || FALLBACK_DESCRIPTION);

        const topics = makeElement("div", "project-topics");
        (project.topics || []).slice(0, 3).forEach((topic) => topics.append(makeElement("span", null, topic)));

        const actions = makeElement("div", "project-actions");
        if (project.homepageUrl) actions.append(externalLink("Open app", project.homepageUrl, "project-action project-action-primary"));
        actions.append(externalLink("View code", project.repositoryUrl, `project-action${project.homepageUrl ? "" : " project-action-primary"}`));

        card.append(top, title, description);
        if (topics.childElementCount) card.append(topics);
        card.append(actions);
        return card;
    }

    function renderLatest() {
        elements.latest.replaceChildren();
        state.projects.slice(0, 6).forEach((project) => elements.latest.append(createProjectCard(project, true)));
    }

    function filteredProjects() {
        const query = state.query.trim().toLowerCase();
        return state.projects.filter((project) => {
            const searchable = [project.name, project.description || "", project.language || "", ...(project.topics || [])].join(" ").toLowerCase();
            const matchesQuery = !query || searchable.includes(query);
            const matchesLanguage = state.language === "All" || project.language === state.language;
            const matchesLive = !state.liveOnly || Boolean(project.homepageUrl);
            return matchesQuery && matchesLanguage && matchesLive;
        });
    }

    function renderCatalog() {
        const projects = filteredProjects();
        elements.grid.replaceChildren();
        projects.forEach((project) => elements.grid.append(createProjectCard(project)));

        if (!projects.length) {
            const empty = makeElement("div", "empty-state");
            empty.append(makeElement("h3", null, "No matching projects"), makeElement("p", null, "Try a different search or clear the active filters."));
            elements.grid.append(empty);
        }

        elements.resultsCount.textContent = `${projects.length} ${projects.length === 1 ? "project" : "projects"}`;
        elements.clearFilters.hidden = !state.query && state.language === "All" && !state.liveOnly;
    }

    function selectLanguage(language) {
        state.language = language;
        elements.languageFilters.querySelectorAll("button").forEach((button) => {
            button.setAttribute("aria-pressed", String(button.dataset.language === language));
        });
        renderCatalog();
    }

    function renderLanguageFilters() {
        const counts = new Map();
        state.projects.forEach((project) => {
            const language = project.language || "Other";
            counts.set(language, (counts.get(language) || 0) + 1);
        });
        const languages = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
        elements.languageFilters.replaceChildren();
        [["All", state.projects.length], ...languages].forEach(([language, count]) => {
            const button = makeElement("button", "language-filter", `${language} · ${count}`);
            button.type = "button";
            button.dataset.language = language;
            button.setAttribute("aria-pressed", String(language === state.language));
            button.addEventListener("click", () => selectLanguage(language));
            elements.languageFilters.append(button);
        });
    }

    function resetFilters() {
        state.query = "";
        state.language = "All";
        state.liveOnly = false;
        elements.search.value = "";
        elements.demoFilter.setAttribute("aria-pressed", "false");
        selectLanguage("All");
    }

    function bindControls() {
        elements.search.addEventListener("input", (event) => {
            state.query = event.target.value;
            renderCatalog();
        });
        elements.demoFilter.addEventListener("click", () => {
            state.liveOnly = !state.liveOnly;
            elements.demoFilter.setAttribute("aria-pressed", String(state.liveOnly));
            renderCatalog();
        });
        elements.clearFilters.addEventListener("click", resetFilters);
    }

    function renderFailure() {
        const message = makeElement("div", "empty-state load-error");
        message.append(makeElement("h3", null, "The project catalog could not load"));
        const copy = makeElement("p");
        copy.append(document.createTextNode("Browse every repository directly on "), externalLink("GitHub", "https://github.com/vinayanand3?tab=repositories", "inline-link"), document.createTextNode("."));
        message.append(copy);
        elements.latest.replaceChildren(message.cloneNode(true));
        elements.grid.replaceChildren(message);
        elements.resultsCount.textContent = "Catalog unavailable";
    }

    async function initialize() {
        bindControls();
        try {
            const response = await fetch(DATA_URL, { cache: "no-cache" });
            if (!response.ok) throw new Error(`Repository data returned ${response.status}`);
            const projects = await response.json();
            if (!Array.isArray(projects)) throw new TypeError("Repository data must be an array");
            state.projects = projects;
            const languages = new Set(projects.map((project) => project.language).filter(Boolean));
            elements.projectStat.textContent = String(projects.length);
            elements.languageStat.textContent = String(languages.size);
            renderLatest();
            renderLanguageFilters();
            renderCatalog();
        } catch (error) {
            console.error("Unable to load project catalog", error);
            renderFailure();
        }
    }

    initialize();
})();

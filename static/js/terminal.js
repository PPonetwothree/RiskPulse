/**
 * terminal.js — Terminal feed manager
 * Manages the scrolling event feed with color coding and auto-scroll
 */

const Terminal = (() => {
    const MAX_LINES = 200;

    const SRC_CLASS = {
        'GDELT':  'src-gdelt',
        'ACLED':  'src-acled',
        'Reddit': 'src-reddit',
        'SYSTEM': 'src-system',
    };

    function now() {
        return '[' + new Date().toISOString().substring(11, 19) + ']';
    }

    function severityClass(sev) {
        const s = (sev || '').toLowerCase();
        if (s === 'critical') return 'sev-critical';
        if (s === 'high')     return 'sev-high';
        if (s === 'medium')   return 'sev-medium';
        return 'sev-low';
    }

    function createLine(source, country, location, summary, severity) {
        const line = document.createElement('div');
        line.className = 't-line';

        const srcCls = SRC_CLASS[source] || 'src-system';
        const sevCls = severityClass(severity);

        line.innerHTML =
            `<span class="t-time dim">${now()}</span>` +
            `<span class="t-source ${srcCls}">${source.padEnd(6)}</span>` +
            `<span class="t-country">${(country || '').padEnd(3)}</span>` +
            `<span class="t-loc">${(location || '').substring(0, 12).padEnd(12)}</span>` +
            `<span class="t-msg ${sevCls}">${summary || ''}</span>`;

        return line;
    }

    function appendToFeed(feedEl, source, country, location, summary, severity) {
        const shouldScroll = feedEl.scrollTop + feedEl.clientHeight >= feedEl.scrollHeight - 10;

        const line = createLine(source, country, location, summary, severity);
        feedEl.appendChild(line);

        // Trim old lines
        while (feedEl.children.length > MAX_LINES) {
            feedEl.removeChild(feedEl.firstChild);
        }

        if (shouldScroll) {
            feedEl.scrollTop = feedEl.scrollHeight;
        }
    }

    function appendSystem(feedEl, message, cls = 'dim') {
        const line = document.createElement('div');
        line.className = `t-line ${cls}`;
        line.innerHTML = `<span class="t-time">[SYS]</span><span class="t-source src-system">SYSTEM</span><span class="t-msg">${message}</span>`;
        feedEl.appendChild(line);
        feedEl.scrollTop = feedEl.scrollHeight;
    }

    return { appendToFeed, appendSystem, severityClass };
})();

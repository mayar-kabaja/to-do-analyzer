// ── STATE ──────────────────────────────
let tasks = [], nextId = 1, currentFilter = 'all';

// ── DATE ───────────────────────────────
document.getElementById('topbarDate').textContent = new Date().toLocaleDateString('en-US',{
    weekday:'long', month:'short', day:'numeric', year:'numeric'
});

// ── BOTTOM NAV (tablet & mobile) ───────
(function() {
    var ws = document.querySelector('.workspace');
    var nav = document.getElementById('bottomNav');
    if (!ws || !nav) return;
    ws.setAttribute('data-mobile-view', 'add');
    nav.querySelectorAll('.bottom-nav-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var tab = this.getAttribute('data-mobile-tab');
            ws.setAttribute('data-mobile-view', tab);
            nav.querySelectorAll('.bottom-nav-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
        });
    });
})();

// ── TEXTAREA COUNTERS ──────────────────
const bulkEl = document.getElementById('bulkInput');
bulkEl.addEventListener('input', () => {
    const val = bulkEl.value;
    const lines = val.split('\n').filter(l => l.trim()).length;
    document.getElementById('lineCount').textContent = lines;
    document.getElementById('charCount').textContent = val.length;
    const hint = document.getElementById('detectHint');
    if (hint) { hint.style.opacity = lines > 0 ? '1' : '0'; }
});

// ── ANALYZE BULK ──────────────────────
const API_BASE = (typeof window !== 'undefined' && window.API_BASE) || '';

async function analyzeBulk() {
    const raw = bulkEl.value;
    const lines = raw.split('\n')
        .map(l => l.replace(/^[-•*\d.]\s*/,'').trim())
        .filter(Boolean);
    if (!lines.length) return;

    const btn = document.querySelector('.btn-analyze');
    const origText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Analyzing…';

    try {
        const url = API_BASE ? `${API_BASE}/api/predict_bulk` : '/api/predict_bulk';
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texts: lines }),
        });
        const data = await res.json();
        if (res.ok && data.results && data.results.length) {
            data.results.forEach(r => pushTask(r.text, r.priority, r.category, ''));
        } else {
            // ML API down or error — fallback to local rules
            lines.forEach(line => {
                pushTask(line, inferPriority(line), inferCategory(line), '');
            });
        }
    } catch (_) {
        lines.forEach(line => {
            pushTask(line, inferPriority(line), inferCategory(line), '');
        });
    }

    bulkEl.value = '';
    document.getElementById('lineCount').textContent = '0';
    document.getElementById('charCount').textContent = '0';
    var dh = document.getElementById('detectHint'); if (dh) dh.style.opacity = '0';
    btn.disabled = false;
    btn.textContent = origText;
    render();
}

function inferPriority(line) {
    if (/urgent|asap|critical|today|deadline|report|meeting|presentation|client/i.test(line)) return 'high';
    if (/optional|someday|maybe|weekend|eventually|later|low|nice/i.test(line)) return 'low';
    return 'medium';
}

function inferCategory(line) {
    if (/meeting|report|client|email|project|work|office|present|deliver|sprint/i.test(line)) return 'Work';
    if (/buy|groceri|home|clean|cook|shop|family|house|fix|repair/i.test(line)) return 'Personal';
    if (/doctor|dentist|gym|exercise|health|medicine|workout|run|diet/i.test(line)) return 'Health';
    if (/study|learn|read|course|tutorial|book|class|research|practice/i.test(line)) return 'Learning';
    if (/pay|bank|tax|budget|invoice|finance|bill|subscription|money/i.test(line)) return 'Finance';
    return 'Other';
}

function clearAll() {
    bulkEl.value = '';
    document.getElementById('lineCount').textContent = '0';
    document.getElementById('charCount').textContent = '0';
    var dh = document.getElementById('detectHint'); if (dh) dh.style.opacity = '0';
}

function pushTask(title, priority, category, deadline) {
    tasks.push({ id: nextId++, title, priority, category, deadline, done: false });
}

// ── FILTER ────────────────────────────
function setFilter(f, btn) {
    currentFilter = f;
    document.querySelectorAll('.f-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    render();
}

function toggleDone(id) {
    const t = tasks.find(t => t.id === id);
    if (t) t.done = !t.done;
    render();
}

function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    render();
}

// ── RENDER ────────────────────────────
function render() { renderTasks(); renderStats(); }

function renderTasks() {
    const list = document.getElementById('taskList');
    document.getElementById('rBadge').textContent = tasks.length;

    const visible = tasks.filter(t => {
        if (currentFilter === 'all')    return true;
        if (currentFilter === 'done')   return t.done;
        if (currentFilter === 'active') return !t.done;
        if (currentFilter === 'high')   return t.priority === 'high';
        return true;
    });

    if (!visible.length) {
        list.innerHTML = `<div class="empty-state"><div class="es-icon">📋</div><p>No tasks here.<br>Add one using the<br>center panel.</p></div>`;
        return;
    }

    const pcls = { high:'ph', medium:'pm', low:'pl' };
    list.innerHTML = visible.map(t => {
        const dl = t.deadline ? new Date(t.deadline + 'T00:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric'}) : '';
        return `
        <div class="task-card ${pcls[t.priority]} ${t.done?'done':''}">
            <div class="tc-top">
                <div class="tc-title">${esc(t.title)}</div>
                <div class="tc-actions">
                    <button class="act-btn act-done" onclick="toggleDone(${t.id})" title="Complete">✓</button>
                    <button class="act-btn act-del"  onclick="deleteTask(${t.id})" title="Delete">✕</button>
                </div>
            </div>
            <div class="tc-tags">
                <span class="ttag ${pcls[t.priority]}">${t.priority}</span>
                <span class="ttag cat">${catEmoji(t.category)} ${t.category}</span>
                ${dl ? `<span class="ttag date">📅 ${dl}</span>` : ''}
            </div>
        </div>`;
    }).join('');
}

function renderStats() {
    const total = tasks.length;
    const high  = tasks.filter(t => t.priority === 'high').length;
    const med   = tasks.filter(t => t.priority === 'medium').length;
    const low   = tasks.filter(t => t.priority === 'low').length;
    const done  = tasks.filter(t => t.done).length;

    const todayStr = new Date().toISOString().split('T')[0];
    const today = tasks.filter(t => t.deadline === todayStr).length;

    const now = new Date(); const end7 = new Date(); end7.setDate(now.getDate()+7);
    const week = tasks.filter(t => { if (!t.deadline) return false; const d=new Date(t.deadline+'T00:00:00'); return d>=now&&d<=end7; }).length;
    const over = tasks.filter(t => { if (!t.deadline||t.done) return false; return new Date(t.deadline+'T00:00:00')<now; }).length;

    document.getElementById('sTotal').textContent = total;
    document.getElementById('sToday').textContent = today;
    document.getElementById('sWeek').textContent  = week;
    document.getElementById('sOver').textContent  = over;
    document.getElementById('nH').textContent = high;
    document.getElementById('nM').textContent = med;
    document.getElementById('nL').textContent = low;

    const mx = Math.max(high,med,low,1);
    document.getElementById('bH').style.width = (high/mx*100)+'%';
    document.getElementById('bM').style.width = (med/mx*100)+'%';
    document.getElementById('bL').style.width = (low/mx*100)+'%';

    const cats = { Work:0, Personal:0, Health:0, Learning:0, Finance:0, Other:0 };
    tasks.forEach(t => { if (cats[t.category]!==undefined) cats[t.category]++; });
    document.getElementById('cW').textContent = cats.Work;
    document.getElementById('cP').textContent = cats.Personal;
    document.getElementById('cH').textContent = cats.Health;
    document.getElementById('cL').textContent = cats.Learning;
    document.getElementById('cF').textContent = cats.Finance;
    document.getElementById('cO').textContent = cats.Other;
}

function catEmoji(c) {
    return {Work:'💼',Personal:'🏠',Health:'💪',Learning:'📚',Finance:'💰',Other:'🎯'}[c]||'🎯';
}
function esc(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

render();

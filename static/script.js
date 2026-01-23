async function calculatePoints() {
    const urlInput = document.getElementById('matchUrl');
    const btn = document.getElementById('calculateBtn');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error-message');
    const url = urlInput.value.trim();

    if (!url) return;

    // Reset state
    btn.classList.add('loading');
    btn.disabled = true;
    errorDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to calculate points');
        }

        renderTable('homeTable', data.home);
        renderTable('awayTable', data.away);
        resultsDiv.classList.remove('hidden');

    } catch (err) {
        errorDiv.textContent = err.message;
        errorDiv.classList.remove('hidden');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

function renderTable(tableId, players) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = '';

    players.forEach(p => {
        const tr = document.createElement('tr');

        // Format detailed stats string
        const details = [
            p.Performance_Gls > 0 ? `⚽ Goals: ${p.Performance_Gls}` : '',
            p.Performance_Ast > 0 ? `🅰️ Assists: ${p.Performance_Ast}` : '',
            p.Performance_Tkl > 0 ? `Tackles: ${p.Performance_Tkl}` : '',
            p.Performance_Int > 0 ? `Int: ${p.Performance_Int}` : '',
            p['Unnamed: 20_level_0_Clr'] > 0 ? `Clear: ${p['Unnamed: 20_level_0_Clr']}` : '',
            p.goals_conceded === 0 ? `🛡️ Clean Sheet` : `Conc: ${p.goals_conceded}`,
            p['Unnamed: 5_level_0_Min'] ? `Min: ${p['Unnamed: 5_level_0_Min']}` : ''
        ].filter(Boolean).join(', ');

        tr.innerHTML = `
            <td>
                <div style="font-weight: 600;">${p.name}</div>
            </td>
            <td><span class="pos-tag">${p.pos}</span></td>
            <td class="score-cell">${p.score}</td>
            <td class="details-cell">${details}</td>
        `;
        tbody.appendChild(tr);
    });
}

with open("ui/stitch/hybrid.html", "r") as f:
    html = f.read()

# Replace Execution Mode
mode_html = """        <!-- Mode Selection -->
        <div class="flex flex-col gap-2">
            <label class="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Execution Mode</label>
            <div class="flex p-1 bg-surface-container-highest rounded-full border border-outline-variant/30" id="mode-group">
                <button id="mode-single" class="mode-btn flex-1 py-1 rounded-full bg-primary text-black text-xs font-bold shadow-sm active-mode">Single</button>
                <button id="mode-hybrid" class="mode-btn flex-1 py-1 rounded-full text-on-surface-variant hover:text-white text-xs font-bold transition-colors">Hybrid</button>
            </div>
        </div>"""

if "<!-- Mode Selection -->" not in html:
    html = html.replace('<!-- Algorithm Selection -->', mode_html + '\n\n        <!-- Algorithm Selection -->')

# Add PHASE 1/2 selectors
phase_html = """
        <!-- PHASE 1 CONFIG -->
        <div class="flex flex-col gap-4">
            <h3 class="text-sm font-bold text-primary">Phase 1 / Single: Algorithm</h3>
            <select id="algo1-select" class="bg-surface-container-highest border border-outline-variant/30 rounded-lg text-sm p-2 text-on-surface focus:outline-none focus:border-primary">
                <option value="GA">Genetic Algorithm (GA)</option>
                <option value="PSO">Particle Swarm (PSO)</option>
                <option value="GWO">Grey Wolf (GWO)</option>
                <option value="BCO">Bee Colony (BCO)</option>
                <option value="WOA">Whale Optimization (WOA)</option>
            </select>
        </div>

        <!-- PHASE 2 CONFIG (Hidden by default) -->
        <div id="phase2-section" class="flex flex-col gap-4 hidden border-t border-outline-variant/20 pt-4">
            <h3 class="text-sm font-bold text-secondary">Phase 2: Local Refinement</h3>
            <select id="algo2-select" class="bg-surface-container-highest border border-outline-variant/30 rounded-lg text-sm p-2 text-on-surface focus:outline-none focus:border-secondary">
                <option value="PSO">Particle Swarm (PSO)</option>
                <option value="GA">Genetic Algorithm (GA)</option>
                <option value="GWO">Grey Wolf (GWO)</option>
                <option value="BCO">Bee Colony (BCO)</option>
                <option value="WOA">Whale Optimization (WOA)</option>
            </select>
            
            <div class="flex items-center justify-between">
                <label class="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Phase 2 Iterations</label>
                <input id="iter2-input" type="number" value="50" class="w-16 input-glass text-center text-sm font-mono text-on-surface rounded-sm py-1">
            </div>
        </div>"""

if "<!-- PHASE 1 CONFIG -->" not in html:
    html = html.replace('<!-- Algorithm Selection -->', phase_html + '\n\n        <!-- Old Algorithm Selection (Hidden) -->\n        <div class="hidden">')
    html = html.replace('<!-- Population Size -->', '</div>\n        <!-- Population Size -->')

js_mode = """        let currentMode = 'Single';
        const modeSingle = document.getElementById('mode-single');
        const modeHybrid = document.getElementById('mode-hybrid');
        const phase2Section = document.getElementById('phase2-section');

        if(modeSingle && modeHybrid) {
            const setMode = (mode) => {
                currentMode = mode;
                if(mode === 'Single') {
                    modeSingle.className = 'mode-btn flex-1 py-1 rounded-full bg-primary text-black text-xs font-bold shadow-sm active-mode';
                    modeHybrid.className = 'mode-btn flex-1 py-1 rounded-full text-on-surface-variant hover:text-white text-xs font-bold transition-colors';
                    phase2Section.classList.add('hidden');
                } else {
                    modeHybrid.className = 'mode-btn flex-1 py-1 rounded-full bg-primary text-black text-xs font-bold shadow-sm active-mode';
                    modeSingle.className = 'mode-btn flex-1 py-1 rounded-full text-on-surface-variant hover:text-white text-xs font-bold transition-colors';
                    phase2Section.classList.remove('hidden');
                }
            };
            modeSingle.addEventListener('click', () => setMode('Single'));
            modeHybrid.addEventListener('click', () => setMode('Hybrid'));
        }"""

if "let currentMode =" not in html:
    html = html.replace("window.switchTab = (tab) => {", js_mode + "\n\n        window.switchTab = (tab) => {")

# Modify JS payload
old_payload = """                const popSize = document.getElementById('pop-input').value;
                const iterations = document.getElementById('iter-input').value;
                const seed = document.getElementById('seed-input').value;
                
                // Get Hyperparameters
                let hyperparams = {};
                hyperparams.ext_freq = document.getElementById('ext-freq-input').value;
                hyperparams.cost_weight = document.getElementById('weight-input').value;
                hyperparams.ext_percent = document.getElementById('ext-pct-input').value;
                if (selectedAlgo === 'GA') {
                    hyperparams.pc = document.getElementById('ga-pc').value;
                    hyperparams.pm = document.getElementById('ga-pm').value;
                } else if (selectedAlgo === 'PSO') {
                    hyperparams.w = document.getElementById('pso-w').value;
                    hyperparams.c1 = document.getElementById('pso-c1').value;
                    hyperparams.c2 = document.getElementById('pso-c2').value;
                } else if (selectedAlgo === 'BCO') {
                    hyperparams.b = document.getElementById('bco-b').value;
                    hyperparams.nc = document.getElementById('bco-nc').value;
                } else if (selectedAlgo === 'WOA') {
                    hyperparams.woa_b = document.getElementById('woa-b').value;
                }

                const results = await window.pywebview.api.run_simulation(popSize, iterations, selectedAlgo, seed, hyperparams);"""

new_payload = """                const popSize = document.getElementById('pop-input').value;
                const iterations = document.getElementById('iter-input').value;
                const seed = document.getElementById('seed-input').value;
                
                const algo1 = document.getElementById('algo1-select') ? document.getElementById('algo1-select').value : selectedAlgo;
                const algo2 = document.getElementById('algo2-select') ? document.getElementById('algo2-select').value : 'PSO';
                const iter2 = document.getElementById('iter2-input') ? document.getElementById('iter2-input').value : 50;

                let hyperparams = {};
                hyperparams.ext_freq = document.getElementById('ext-freq-input').value;
                hyperparams.cost_weight = document.getElementById('weight-input').value;
                hyperparams.ext_percent = document.getElementById('ext-pct-input').value;
                
                // Read global params into both for simplicity in this hybrid patch
                if (document.getElementById('ga-pc')) hyperparams.pc = document.getElementById('ga-pc').value;
                if (document.getElementById('ga-pm')) hyperparams.pm = document.getElementById('ga-pm').value;
                if (document.getElementById('pso-w')) hyperparams.w = document.getElementById('pso-w').value;
                if (document.getElementById('pso-c1')) hyperparams.c1 = document.getElementById('pso-c1').value;
                if (document.getElementById('pso-c2')) hyperparams.c2 = document.getElementById('pso-c2').value;
                if (document.getElementById('bco-b')) hyperparams.b = document.getElementById('bco-b').value;
                if (document.getElementById('bco-nc')) hyperparams.nc = document.getElementById('bco-nc').value;
                if (document.getElementById('woa-b')) hyperparams.woa_b = document.getElementById('woa-b').value;

                let payload = {
                    mode: currentMode,
                    pop_size: popSize,
                    seed: seed,
                    algo1: algo1,
                    iter1: iterations,
                    params1: hyperparams,
                    algo2: algo2,
                    iter2: iter2,
                    params2: hyperparams // Reuse global params for Phase 2 for simplicity
                };

                const results = await window.pywebview.api.run_simulation(payload);"""

if "let payload =" not in html:
    html = html.replace(old_payload, new_payload)

with open("ui/stitch/hybrid.html", "w") as f:
    f.write(html)


        // ==========================================
        // GLOBAL STATE
        // ==========================================
        let currentModule = 1;
        const totalModules = 9;

        // ==========================================
        // NAVIGATION
        // ==========================================
        function startExperience(mode) {
            if (mode === 'ar') {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(stream => {
                        stream.getTracks().forEach(t => t.stop());
                        alert('Realidad aumentada activada. En un dispositivo compatible, la experiencia se proyectará en tu entorno. Por ahora, se muestra el modo de pantalla.');
                        showApp();
                    })
                    .catch(() => {
                        alert('No se pudo acceder a la cámara. Continuarás en modo pantalla.');
                        showApp();
                    });
            } else {
                showApp();
            }
        }

        function showApp() {
            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('main-header').classList.remove('hidden');
            loadModule(1);
        }

        function loadModule(n) {
            if (n < 1 || n > totalModules) return;
            // Hide all
            for (let i = 1; i <= totalModules; i++) {
                document.getElementById('mod-' + i).classList.remove('active');
            }
            currentModule = n;
            document.getElementById('mod-' + n).classList.add('active');
            document.getElementById('mod-num').textContent = n;
            document.getElementById('btn-prev').disabled = (n === 1);
            document.getElementById('btn-next').disabled = (n === totalModules);
            window.scrollTo({ top: 0, behavior: 'smooth' });

            // Module-specific initialization
            if (n === 3) m3UpdateTemp();
            if (n === 4) m4Setup();
            if (n === 9) m9Setup();
        }

        function nextModule() { loadModule(currentModule + 1); }
        function prevModule() { loadModule(currentModule - 1); }

        // ==========================================
        // MODULE 1: Entrada al laboratorio
        // ==========================================
        function m1SendQuestion() {
            document.getElementById('m1-send-btn').disabled = true;
            document.getElementById('m1-send-btn').textContent = 'Enviando...';
            setTimeout(() => {
                document.getElementById('m1-pipeline').classList.remove('hidden');
                document.getElementById('m1-send-btn').textContent = 'Enviado ✓';
            }, 800);
        }

        function m1Answer(isSi) {
            const fb = document.getElementById('m1-feedback');
            fb.classList.remove('hidden');
            if (!isSi) {
                fb.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-emerald-900/30 border border-emerald-500/30 text-emerald-200';
                fb.innerHTML = '<strong>Correcto.</strong> El LLM genera una respuesta probable. Por eso, cuando la información es importante, debe verificarse.';
            } else {
                fb.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-amber-900/30 border border-amber-500/30 text-amber-200';
                fb.innerHTML = '<strong>No exactamente.</strong> Un LLM no funciona como un buscador tradicional. Genera texto a partir de patrones aprendidos y del contexto recibido.';
            }
        }

        // ==========================================
        // MODULE 2: Tokenización
        // ==========================================
        const tokenColors = ['bg-violet-600', 'bg-blue-600', 'bg-cyan-600', 'bg-teal-600', 'bg-emerald-600', 'bg-indigo-600', 'bg-purple-600', 'bg-fuchsia-600'];

        function m2Tokenize() {
            const phrase = document.getElementById('m2-phrase').textContent;
            m2RenderTokens(phrase);
            document.getElementById('m2-tokens-area').classList.remove('hidden');
            document.getElementById('m2-btn-tokenize').classList.add('hidden');
        }

        function m2RenderTokens(phrase) {
            const tokens = phrase.split(/\s+/);
            const container = document.getElementById('m2-tokens');
            container.innerHTML = '';
            tokens.forEach((t, i) => {
                const chip = document.createElement('div');
                chip.className = 'token-chip ' + tokenColors[i % tokenColors.length] + ' text-white anim-slide';
                chip.style.animationDelay = (i * 0.1) + 's';
                chip.textContent = t;
                chip.onclick = () => {
                    // Show vectors
                    document.getElementById('m2-vectors').classList.remove('hidden');
                    m2ShowVectors(tokens);
                };
                container.appendChild(chip);
            });
        }

        function m2ShowVectors(tokens) {
            const container = document.getElementById('m2-vector-display');
            container.innerHTML = '';
            tokens.forEach((t, i) => {
                const vec = document.createElement('div');
                vec.className = 'token-chip bg-slate-700 text-slate-300 text-xs border border-slate-600';
                const v1 = (Math.random() * 2 - 1).toFixed(2);
                const v2 = (Math.random() * 2 - 1).toFixed(2);
                const v3 = (Math.random() * 2 - 1).toFixed(2);
                vec.innerHTML = '<span class="text-indigo-400 font-bold mr-1">' + t + '</span> [' + v1 + ', ' + v2 + ', ' + v3 + ', …]';
                container.appendChild(vec);
            });
        }

        function m2AnalyzeCustom() {
            const phrase = document.getElementById('m2-custom-input').value.trim();
            if (!phrase) return;
            document.getElementById('m2-phrase').textContent = phrase;
            m2RenderTokens(phrase);
            document.getElementById('m2-vectors').classList.add('hidden');
        }

        // ==========================================
        // MODULE 3: Predicción
        // ==========================================
        function m3Select(word, fits) {
            const fb = document.getElementById('m3-feedback');
            fb.classList.remove('hidden');
            if (fits) {
                fb.className = 'p-4 rounded-xl text-sm font-medium mb-6 bg-emerald-900/30 border border-emerald-500/30 text-emerald-200';
                fb.innerHTML = '<strong>"' + word + '"</strong> — Esta palabra tiene sentido porque se relaciona con educación, IA y apoyo al aprendizaje.';
            } else {
                fb.className = 'p-4 rounded-xl text-sm font-medium mb-6 bg-rose-900/30 border border-rose-500/30 text-rose-200';
                fb.innerHTML = '<strong>"' + word + '"</strong> — Esta opción tiene baja probabilidad porque no encaja bien con el contexto académico.';
            }
        }

        function m3UpdateTemp() {
            const val = parseInt(document.getElementById('m3-temp').value);
            const display = document.getElementById('m3-temp-display');
            const states = [
                { title: 'Temperatura baja', desc: 'Respuesta más segura, ordenada y predecible.', color: 'border-blue-500 bg-blue-900/20 text-blue-200', active: val === 0 },
                { title: 'Temperatura media', desc: 'Respuesta equilibrada entre precisión y creatividad.', color: 'border-amber-500 bg-amber-900/20 text-amber-200', active: val === 1 },
                { title: 'Temperatura alta', desc: 'Respuesta más creativa, pero con mayor riesgo de incoherencia o error.', color: 'border-rose-500 bg-rose-900/20 text-rose-200', active: val === 2 }
            ];
            display.innerHTML = states.map(s =>
                '<div class="border rounded-xl p-4 text-sm transition-all ' + s.color + (s.active ? ' ring-2 ring-white/30 scale-105' : ' opacity-50') + '">' +
                '<p class="font-bold mb-1">' + s.title + '</p>' +
                '<p class="text-xs">' + s.desc + '</p></div>'
            ).join('');
        }

        // ==========================================
        // MODULE 4: Transformer / Atención
        // ==========================================
        const m4Sentence = ['El', 'estudiante', 'usa', 'IA', 'para', 'mejorar', 'su', 'aprendizaje'];
        const m4Attention = {
            'El': { related: ['estudiante'], weights: { 'estudiante': 0.9 } },
            'estudiante': { related: ['usa', 'mejorar', 'aprendizaje'], weights: { 'usa': 0.7, 'mejorar': 0.6, 'aprendizaje': 0.9 } },
            'usa': { related: ['IA', 'estudiante'], weights: { 'IA': 0.9, 'estudiante': 0.7 } },
            'IA': { related: ['usa', 'mejorar', 'aprendizaje'], weights: { 'usa': 0.8, 'mejorar': 0.9, 'aprendizaje': 0.7 } },
            'para': { related: ['mejorar'], weights: { 'mejorar': 0.8 } },
            'mejorar': { related: ['IA', 'aprendizaje'], weights: { 'IA': 0.8, 'aprendizaje': 0.95 } },
            'su': { related: ['estudiante', 'aprendizaje'], weights: { 'estudiante': 0.7, 'aprendizaje': 0.8 } },
            'aprendizaje': { related: ['estudiante', 'mejorar', 'IA'], weights: { 'estudiante': 0.8, 'mejorar': 0.9, 'IA': 0.7 } }
        };

        function m4Setup() {
            const container = document.getElementById('m4-words');
            container.innerHTML = '';
            m4Sentence.forEach(word => {
                const el = document.createElement('span');
                el.className = 'attention-word bg-slate-700 text-slate-200';
                el.textContent = word;
                el.onclick = () => m4Highlight(word);
                container.appendChild(el);
            });
        }

        function m4Highlight(word) {
            const words = document.querySelectorAll('#m4-words .attention-word');
            const info = m4Attention[word];
            words.forEach(w => {
                const t = w.textContent;
                if (t === word) {
                    w.className = 'attention-word bg-indigo-600 text-white ring-2 ring-indigo-400';
                } else if (info && info.related.includes(t)) {
                    const weight = info.weights[t] || 0.5;
                    const opacity = Math.round(weight * 100);
                    w.className = 'attention-word bg-purple-600 text-white';
                    w.style.opacity = Math.max(0.5, weight);
                    w.style.transform = 'scale(' + (1 + weight * 0.2) + ')';
                } else {
                    w.className = 'attention-word bg-slate-800 text-slate-500';
                    w.style.opacity = '0.4';
                    w.style.transform = 'scale(1)';
                }
            });

            const expl = document.getElementById('m4-explanation');
            expl.classList.remove('hidden');
            if (info && info.related.length > 0) {
                expl.innerHTML = 'Al analizar <strong>"' + word + '"</strong>, el modelo presta mayor atención a: <strong>' + info.related.join(', ') + '</strong>. Estas palabras ayudan a construir el significado contextual.';
            } else {
                expl.innerHTML = '<strong>"' + word + '"</strong> tiene relaciones débiles con las demás palabras en este contexto.';
            }
        }

        // ==========================================
        // MODULE 5: Buscador vs LLM
        // ==========================================
        let m5Correct = 0;

        function m5Drop(event, zone) {
            event.preventDefault();
            event.target.classList.remove('drag-over');
            const cardType = event.dataTransfer.getData('text');
            const fb = document.getElementById('m5-feedback');
            fb.classList.remove('hidden');

            let correct = false;
            if (cardType === 'fuente' && zone === 'buscador') correct = true;
            if (cardType === 'redactar' && zone === 'llm') correct = true;

            if (correct) {
                fb.className = 'p-4 rounded-xl text-sm font-medium mb-6 bg-emerald-900/30 border border-emerald-500/30 text-emerald-200';
                if (cardType === 'fuente') {
                    fb.innerHTML = '<strong>Correcto.</strong> Cuando necesitas evidencia verificable, autores reales, fecha, revista o DOI, conviene usar un buscador académico o una base de datos.';
                } else {
                    fb.innerHTML = '<strong>Correcto.</strong> Cuando necesitas ordenar ideas, generar un borrador, comparar enfoques o reformular una explicación, un LLM puede ser útil.';
                }
                const card = document.getElementById('card-' + cardType);
                if (card) card.style.opacity = '0.4';
                event.target.innerHTML = '<span class="text-emerald-400 font-semibold text-sm">✓ Asignado correctamente</span>';
                m5Correct++;
                if (m5Correct >= 2) document.getElementById('m5-table').classList.remove('hidden');
            } else {
                fb.className = 'p-4 rounded-xl text-sm font-medium mb-6 bg-rose-900/30 border border-rose-500/30 text-rose-200';
                fb.innerHTML = '<strong>Intenta de nuevo.</strong> Piensa en qué herramienta es más adecuada para cada necesidad.';
            }
        }

        // ==========================================
        // MODULE 6: Alucinaciones
        // ==========================================
        let m6Count = 0;

        function m6Alert(el, msg) {
            el.style.background = '#fef3c7';
            el.style.borderBottomColor = '#f59e0b';
            el.style.cursor = 'default';
            el.onclick = null;

            const container = document.getElementById('m6-alerts');
            const alert = document.createElement('div');
            alert.className = 'flex items-start gap-2 bg-amber-900/30 border border-amber-500/30 rounded-lg p-3 text-sm text-amber-200 fade-in';
            alert.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 flex-shrink-0 text-amber-400"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>' + msg;
            container.appendChild(alert);

            m6Count++;
            if (m6Count >= 3) {
                document.getElementById('m6-corrected').classList.remove('hidden');
            }
        }

        // ==========================================
        // MODULE 7: Prompt builder
        // ==========================================
        function m7Build() {
            const tema = document.getElementById('m7-tema').value || 'inteligencia artificial generativa';
            const publico = document.getElementById('m7-publico').value || 'estudiantes de maestría';
            const nivel = document.getElementById('m7-nivel').value || 'lenguaje claro';
            const formato = document.getElementById('m7-formato').value || 'tres ejemplos aplicados';
            const ejemplos = document.getElementById('m7-ejemplos').value || 'aplicados a la enseñanza';
            const restriccion = document.getElementById('m7-restriccion').value || 'una advertencia sobre privacidad de datos';

            const result = 'Explícame el uso de ' + tema + ' en instituciones educativas para ' + publico + ', usando ' + nivel + ', ' + formato + ' ' + ejemplos + ' y ' + restriccion + '.';

            const el = document.getElementById('m7-result');
            el.classList.remove('hidden');
            el.innerHTML = '<p class="font-bold text-indigo-300 mb-2">Prompt mejorado:</p><p class="text-white italic">"' + result + '"</p>';
        }

        // ==========================================
        // MODULE 8: Verificación
        // ==========================================
        function m8Verify() {
            document.getElementById('m8-btn').disabled = true;
            document.getElementById('m8-btn').textContent = 'Verificando...';
            setTimeout(() => {
                document.getElementById('m8-steps').classList.remove('hidden');
                document.getElementById('m8-btn').classList.add('hidden');
            }, 600);
            setTimeout(() => {
                document.getElementById('m8-status').classList.remove('hidden');
            }, 1200);
        }

        // ==========================================
        // MODULE 9: Mapa final
        // ==========================================
        const m9Details = [
            'El usuario escribe una pregunta o instrucción. Esta es la entrada que el LLM recibe como contexto inicial.',
            'La frase se divide en tokens — unidades mínimas de texto que el modelo puede procesar matemáticamente.',
            'Cada token se transforma en un vector numérico (embedding) que captura su significado semántico en un espacio multidimensional.',
            'El mecanismo de atención del Transformer analiza las relaciones entre todos los tokens para entender el contexto completo.',
            'El modelo calcula la probabilidad de cada posible siguiente token y selecciona el más probable (según la temperatura).',
            'Se genera la respuesta token por token, construyendo una secuencia coherente basada en los cálculos de probabilidad.',
            'La respuesta generada debe ser revisada por un humano. El LLM puede producir alucinaciones: información falsa presentada con seguridad.'
        ];

        function m9Show(index) {
            const el = document.getElementById('m9-detail');
            el.classList.remove('hidden');
            el.innerHTML = '<strong>Etapa ' + (index + 1) + ':</strong> ' + m9Details[index];
            // Highlight active node
            const nodes = document.querySelectorAll('#m9-pipeline .pipeline-node');
            nodes.forEach((n, i) => {
                n.style.opacity = i === index ? '1' : '0.4';
                n.style.transform = i === index ? 'scale(1.05)' : 'scale(1)';
            });
        }

        const m9QuizData = [
            { text: 'Buscar artículo con DOI', answer: 'Buscador académico', options: ['Buscador académico', 'LLM', 'Verificación de fuentes'] },
            { text: 'Crear una explicación inicial', answer: 'LLM', options: ['Buscador académico', 'LLM', 'Triangulación'] },
            { text: 'Comprobar una cita', answer: 'Verificación de fuentes', options: ['LLM', 'Mejora de instrucciones', 'Verificación de fuentes'] },
            { text: 'Corregir un prompt vago', answer: 'Mejora de instrucciones', options: ['Buscador académico', 'Mejora de instrucciones', 'Triangulación'] },
            { text: 'Revisar un dato dudoso', answer: 'Triangulación', options: ['Triangulación', 'LLM', 'Buscador académico'] }
        ];

        function m9Setup() {
            const container = document.getElementById('m9-quiz');
            container.innerHTML = '';
            m9QuizData.forEach((q, i) => {
                const div = document.createElement('div');
                div.className = 'flex flex-col sm:flex-row items-start sm:items-center gap-3 bg-slate-800/60 rounded-xl p-3';
                div.innerHTML = '<span class="text-white font-semibold text-sm flex-shrink-0 min-w-[200px]">"' + q.text + '"</span>' +
                    '<select id="m9-q' + i + '" class="bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-white text-sm flex-1 focus:outline-none focus:border-indigo-500">' +
                    '<option value="">Selecciona...</option>' +
                    q.options.map(o => '<option value="' + o + '">' + o + '</option>').join('') +
                    '</select>';
                container.appendChild(div);
            });
        }

        function m9Check() {
            let correct = 0;
            m9QuizData.forEach((q, i) => {
                const sel = document.getElementById('m9-q' + i);
                if (sel && sel.value === q.answer) {
                    correct++;
                    sel.style.borderColor = '#10b981';
                } else if (sel) {
                    sel.style.borderColor = '#f43f5e';
                }
            });
            const el = document.getElementById('m9-result');
            el.classList.remove('hidden');
            if (correct === m9QuizData.length) {
                el.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-emerald-900/30 border border-emerald-500/30 text-emerald-200';
                el.innerHTML = '<strong>¡Excelente!</strong> Ahora puedes distinguir cuándo usar un buscador, cuándo usar un LLM y por qué toda respuesta generada necesita criterio humano.';
            } else {
                el.className = 'mt-4 p-4 rounded-xl text-sm font-medium bg-amber-900/30 border border-amber-500/30 text-amber-200';
                el.innerHTML = '<strong>' + correct + '/' + m9QuizData.length + ' correctas.</strong> Revisa las opciones marcadas en rojo e intenta nuevamente.';
            }
        }
    
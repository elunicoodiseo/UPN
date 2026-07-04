import sys

filepath = 'd:/Proyectos/Arquitectura-Semana 5/UPN/S5/xai/xai.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

html_start = '<!-- 6. SECCIÓN RETO DE LA CAJA NEGRA (ACTIVIDAD CENTRAL) -->'
html_end = '<!-- === PIE DE PÁGINA === -->'
js_start = '// === ACTIVIDAD DIDÁCTICA: RETO CAJA NEGRA ==='
js_end = '</script>'

html_new = '''<!-- 6. SECCIÓN RETO DE LA CAJA NEGRA (ACTIVIDAD CENTRAL) -->
            <section id="tab-actividades" class="tab-content animate-fadeIn hidden space-y-8">
                <div class="space-y-4">
                    <h2 class="text-2xl md:text-3xl font-black">Reto Final: Reescriba la Caja Negra</h2>
                    <div class="bg-rose-950/20 border border-rose-500/20 p-5 rounded-2xl space-y-3">
                        <p class="text-slate-300 text-base leading-relaxed">
                            Esta notificación llegó ayer al correo de un estudiante de su institución:
                        </p>
                        <div class="bg-rose-950/40 p-4 rounded-xl font-mono text-sm text-rose-300 border border-rose-900/30">
                            "SISTEMA: Estudiante ID-4929 categorizado en RIESGO CRÍTICO de deserción. Becas: RECHAZADO preventivamente. Proceso inapelable."
                        </div>
                        <p class="text-slate-300 text-base leading-relaxed">
                            Su tarea como directivo: reescribirla para que sea ética, explicable y respetuosa de los derechos del estudiante. Responda las 5 preguntas y observe cómo se construye la nueva carta en tiempo real.
                        </p>
                        <div class="bg-amber-500/10 border border-amber-500/20 p-3 rounded-lg text-amber-300 text-sm flex items-start space-x-2">
                            <span class="text-lg">⚠</span>
                            <p><strong>Cuidado:</strong> algunas opciones parecen razonables pero esconden problemas éticos o legales. Elija con criterio.</p>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    <!-- Panel del Diseñador (Izquierda) -->
                    <div class="lg:col-span-6 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6 shadow-xl">
                        <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider block border-b border-slate-800 pb-2">Construya la Nueva Comunicación</span>

                        <div class="space-y-4" id="reto-form">
                            <div class="space-y-2">
                                <label class="text-xs text-slate-300 font-bold block uppercase">1. ¿Qué información respalda esta alerta?</label>
                                <select id="reto-select-data" onchange="updateRetoPreview()" class="w-full bg-slate-950 border border-slate-800 text-sm p-3 rounded-xl focus:border-cyan-500/50 text-slate-200 outline-none">
                                    <option value="">Elija una opción...</option>
                                    <option value="asistencia_notas">"Asistencia acumulada del 65% y promedio de notas de 10.5 en el trimestre."</option>
                                    <option value="codigo_postal">"Residencia del estudiante en una zona con altos índices de abandono."</option>
                                    <option value="ninguno">"Variables internas del sistema, no especificadas por confidencialidad."</option>
                                </select>
                            </div>

                            <div class="space-y-2">
                                <label class="text-xs text-slate-300 font-bold block uppercase">2. ¿Qué fue lo que disparó el riesgo?</label>
                                <select id="reto-select-factor" onchange="updateRetoPreview()" class="w-full bg-slate-950 border border-slate-800 text-sm p-3 rounded-xl focus:border-cyan-500/50 text-slate-200 outline-none">
                                    <option value="">Elija una opción...</option>
                                    <option value="caida_asistencia">"Caída del 30% en los ingresos al Aula Virtual en las últimas dos semanas."</option>
                                    <option value="historial_pagos">"Atrasos en los pagos de pensiones del ciclo académico vigente."</option>
                                </select>
                            </div>

                            <div class="space-y-2">
                                <label class="text-xs text-slate-300 font-bold block uppercase">3. ¿Cuánta certeza tiene el sistema?</label>
                                <select id="reto-select-score" onchange="updateRetoPreview()" class="w-full bg-slate-950 border border-slate-800 text-sm p-3 rounded-xl focus:border-cyan-500/50 text-slate-200 outline-none">
                                    <option value="">Elija una opción...</option>
                                    <option value="confianza_92">"El sistema estimó esta alerta con un 92% de precisión, por lo que puede haber margen de error."</option>
                                    <option value="infalible">"La decisión cuenta con garantía absoluta de infalibilidad del algoritmo."</option>
                                </select>
                            </div>

                            <div class="space-y-2">
                                <label class="text-xs text-slate-300 font-bold block uppercase">4. ¿Qué hará la universidad al respecto?</label>
                                <select id="reto-select-action" onchange="updateRetoPreview()" class="w-full bg-slate-950 border border-slate-800 text-sm p-3 rounded-xl focus:border-cyan-500/50 text-slate-200 outline-none">
                                    <option value="">Elija una opción...</option>
                                    <option value="intervencion_tutoria">"Programar una tutoría personalizada para coordinar acompañamiento académico."</option>
                                    <option value="suspension">"Retirar o suspender preventivamente los beneficios de matrícula."</option>
                                </select>
                            </div>

                            <div class="space-y-2">
                                <label class="text-xs text-slate-300 font-bold block uppercase">5. ¿Qué derechos tiene el estudiante?</label>
                                <select id="reto-select-right" onchange="updateRetoPreview()" class="w-full bg-slate-950 border border-slate-800 text-sm p-3 rounded-xl focus:border-cyan-500/50 text-slate-200 outline-none">
                                    <option value="">Elija una opción...</option>
                                    <option value="derecho_apelacion">"Derecho a apelar y solicitar una revisión humana en un plazo de 5 días."</option>
                                    <option value="inapelable">"Ninguno: las decisiones del sistema son definitivas e inapelables."</option>
                                </select>
                            </div>

                            <div class="flex flex-wrap gap-3 pt-2" id="reto-actions">
                                <button onclick="checkReto()" class="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-slate-950 font-extrabold text-sm py-3.5 rounded-xl transition shadow">
                                    Evaluar mi comunicación
                                </button>
                                <button onclick="resetReto()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-bold text-sm px-6 py-3.5 rounded-xl transition">
                                    Empezar de nuevo
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Panel de Previsualización (Derecha) -->
                    <div class="lg:col-span-6 space-y-6 flex flex-col">
                        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4 shadow-xl flex-1 flex flex-col">
                            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                                <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider block">Su Nueva Carta</span>
                                <span id="reto-badge" class="text-sm font-bold px-2 py-0.5 rounded bg-slate-950 text-slate-450 hidden">Score: -</span>
                            </div>

                            <div class="bg-slate-950 p-6 rounded-xl text-base leading-relaxed space-y-4 flex-1 border border-slate-850 text-slate-300 shadow-inner">
                                <p>Estimado estudiante:</p>
                                <p>
                                    El sistema de análisis académico de la institución ha generado una alerta sobre tu situación, basada en: <span id="preview-1" class="inline-block min-w-[200px] border-b-2 border-dashed border-slate-700 text-cyan-400 font-medium px-1">[respuesta 1: ¿qué información?]</span>
                                </p>
                                <p>
                                    El factor principal que activó esta alerta fue: <span id="preview-2" class="inline-block min-w-[200px] border-b-2 border-dashed border-slate-700 text-cyan-400 font-medium px-1">[respuesta 2: ¿qué la disparó?]</span>, con un nivel de certeza de: <span id="preview-3" class="inline-block min-w-[200px] border-b-2 border-dashed border-slate-700 text-indigo-400 font-medium px-1">[respuesta 3: ¿cuánta confianza?]</span>
                                </p>
                                <p>
                                    Como siguiente paso, la universidad procederá a: <span id="preview-4" class="inline-block min-w-[200px] border-b-2 border-dashed border-slate-700 text-emerald-400 font-medium px-1">[respuesta 4: ¿qué acción?]</span>
                                </p>
                                <p>
                                    Finalmente, te recordamos que cuentas con: <span id="preview-5" class="inline-block min-w-[200px] border-b-2 border-dashed border-slate-700 text-indigo-300 font-medium px-1">[respuesta 5: ¿qué derechos?]</span>
                                </p>
                                <div class="pt-4">
                                    <p>Atentamente,</p>
                                    <p class="font-bold">Dirección Académica</p>
                                </div>
                            </div>
                        </div>
                        
                        <div id="reto-feedback-container" class="hidden space-y-4">
                            <div id="reto-feedback" class="p-6 rounded-2xl text-sm md:text-base leading-relaxed">
                                <!-- Feedback de JS -->
                            </div>
                            <button id="btn-corregir" onclick="corregirReto()" class="w-full bg-amber-500/20 hover:bg-amber-500/30 text-amber-400 border border-amber-500/50 font-bold text-sm px-6 py-3.5 rounded-xl transition shadow">
                                Corregir mis respuestas
                            </button>
                        </div>
                    </div>
                </div>
            </section>

        </div>

    </main>
'''

js_new = '''// === ACTIVIDAD DIDÁCTICA: RETO CAJA NEGRA ===
        function updateRetoPreview() {
            const dataVal = document.getElementById('reto-select-data').value;
            const factorVal = document.getElementById('reto-select-factor').value;
            const scoreVal = document.getElementById('reto-select-score').value;
            const actionVal = document.getElementById('reto-select-action').value;
            const rightVal = document.getElementById('reto-select-right').value;

            const p1 = document.getElementById('preview-1');
            const p2 = document.getElementById('preview-2');
            const p3 = document.getElementById('preview-3');
            const p4 = document.getElementById('preview-4');
            const p5 = document.getElementById('preview-5');

            const setPreview = (el, val, map, defaultText) => {
                if(val && map[val]) {
                    el.textContent = map[val];
                    el.classList.remove('border-dashed', 'border-slate-700', 'text-slate-500');
                } else {
                    el.textContent = defaultText;
                    el.classList.add('border-dashed', 'border-slate-700', 'text-slate-500');
                }
            };

            setPreview(p1, dataVal, {
                'asistencia_notas': 'asistencia acumulada del 65% y promedio de notas de 10.5 en el trimestre.',
                'codigo_postal': 'residencia en una zona con altos índices de abandono.',
                'ninguno': 'variables internas del sistema (confidenciales).'
            }, '[respuesta 1: ¿qué información?]');

            setPreview(p2, factorVal, {
                'caida_asistencia': 'la caída del 30% en los ingresos al Aula Virtual en las últimas dos semanas',
                'historial_pagos': 'los atrasos en los pagos de pensiones del ciclo académico vigente'
            }, '[respuesta 2: ¿qué la disparó?]');

            setPreview(p3, scoreVal, {
                'confianza_92': 'un 92% de precisión (sujeto a margen de error).',
                'infalible': 'garantía absoluta de infalibilidad algorítmica.'
            }, '[respuesta 3: ¿cuánta confianza?]');

            setPreview(p4, actionVal, {
                'intervencion_tutoria': 'programar una tutoría personalizada para coordinar acompañamiento académico.',
                'suspension': 'retirar o suspender preventivamente los beneficios de matrícula.'
            }, '[respuesta 4: ¿qué acción?]');

            setPreview(p5, rightVal, {
                'derecho_apelacion': 'el derecho a apelar y solicitar una revisión humana en un plazo de 5 días.',
                'inapelable': 'ningún recurso, al ser decisiones definitivas e inapelables.'
            }, '[respuesta 5: ¿qué derechos?]');
        }

        function checkReto() {
            const dataVal = document.getElementById('reto-select-data').value;
            const factorVal = document.getElementById('reto-select-factor').value;
            const scoreVal = document.getElementById('reto-select-score').value;
            const actionVal = document.getElementById('reto-select-action').value;
            const rightVal = document.getElementById('reto-select-right').value;

            if (!dataVal || !factorVal || !scoreVal || !actionVal || !rightVal) {
                alert("Por favor, responda las 5 preguntas antes de evaluar.");
                return;
            }

            let score = 0;
            let feedbackItems = [];

            // 1. Información
            if (dataVal === 'asistencia_notas') {
                score += 20;
                feedbackItems.push('<p class="text-emerald-400"><span class="font-bold">✓ Información: Correcto</span> — usaste evidencia académica verificable, no datos que discriminan por origen.</p>');
            } else {
                feedbackItems.push('<p class="text-amber-400"><span class="font-bold">✗ Información:</span> La zona de residencia es un indicador indirecto del nivel socioeconómico — usarla discrimina sin decirlo. Y ocultar las variables "por confidencialidad" es exactamente la caja negra que intentamos desmontar.</p>');
            }

            // 2. Factor
            if (factorVal === 'caida_asistencia') {
                score += 20;
                feedbackItems.push('<p class="text-emerald-400"><span class="font-bold">✓ Factor: Correcto</span> — señalaste una causa académica concreta que el tutor puede abordar.</p>');
            } else {
                feedbackItems.push('<p class="text-amber-400"><span class="font-bold">✗ Factor:</span> Los atrasos de pago describen la economía familiar, no el compromiso académico. Mezclarlo estigmatiza al estudiante.</p>');
            }

            // 3. Certeza
            if (scoreVal === 'confianza_92') {
                score += 20;
                feedbackItems.push('<p class="text-emerald-400"><span class="font-bold">✓ Certeza: Correcto</span> — reconocer el margen de error es honesto y legalmente prudente.</p>');
            } else {
                feedbackItems.push('<p class="text-amber-400"><span class="font-bold">✗ Certeza:</span> Ningún sistema es infalible. Prometer certeza absoluta es falso y deja a la institución sin defensa cuando el sistema se equivoque.</p>');
            }

            // 4. Acción
            if (actionVal === 'intervencion_tutoria') {
                score += 20;
                feedbackItems.push('<p class="text-emerald-400"><span class="font-bold">✓ Acción: Correcto</span> — la respuesta institucional es de acompañamiento, no de castigo.</p>');
            } else {
                feedbackItems.push('<p class="text-amber-400"><span class="font-bold">✗ Acción:</span> Una alerta predictiva es una probabilidad, no un veredicto. Castigar (suspender la beca) en base a una predicción es la falla ética más grave de este ejercicio.</p>');
            }

            // 5. Derechos
            if (rightVal === 'derecho_apelacion') {
                score += 20;
                feedbackItems.push('<p class="text-emerald-400"><span class="font-bold">✓ Derechos: Correcto</span> — garantizaste la revisión humana, el pilar central de la IA responsable.</p>');
            } else {
                feedbackItems.push('<p class="text-amber-400"><span class="font-bold">✗ Derechos:</span> Toda decisión asistida por IA debe poder apelarse ante un ser humano. "Inapelable" vulnera derechos básicos del estudiante.</p>');
            }

            const feedbackBox = document.getElementById('reto-feedback');
            const feedbackContainer = document.getElementById('reto-feedback-container');
            const badge = document.getElementById('reto-badge');
            const btnCorregir = document.getElementById('btn-corregir');

            badge.textContent = `Score: ${score}/100`;
            badge.classList.remove('hidden');
            feedbackContainer.classList.remove('hidden');

            let headerHTML = '';

            if (score === 100) {
                badge.className = "text-sm font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400";
                feedbackBox.className = "p-6 rounded-2xl text-sm md:text-base leading-relaxed bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 shadow-lg space-y-3";
                headerHTML = "<p class='font-semibold text-lg text-emerald-400 mb-4'>🎓 Comunicación aprobada. Tu carta cumple los 5 pilares: evidencia legítima, causa concreta, honestidad sobre el margen de error, acción de apoyo y derecho a revisión humana. Compárala con la notificación original de arriba: mismos datos, misma alerta — pero una destruye la confianza y la otra la construye.</p>";
                btnCorregir.classList.add('hidden'); // Ocultar si está perfecto
                
                // Deshabilitar selects
                ['data', 'factor', 'score', 'action', 'right'].forEach(id => {
                    document.getElementById(`reto-select-${id}`).disabled = true;
                });
            } else {
                badge.className = "text-sm font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400";
                feedbackBox.className = "p-6 rounded-2xl text-sm md:text-base leading-relaxed bg-slate-900 border border-slate-700 shadow-lg space-y-3";
                headerHTML = `<p class='font-semibold text-lg text-slate-200 mb-4'>Tu carta aún tiene brechas éticas o legales (${score}/100). Revisa los puntos marcados y usa "Corregir mis respuestas" para ajustar solo lo necesario.</p>`;
                btnCorregir.classList.remove('hidden');
                
                // Deshabilitar selects temporalmente
                ['data', 'factor', 'score', 'action', 'right'].forEach(id => {
                    document.getElementById(`reto-select-${id}`).disabled = true;
                });
            }

            feedbackBox.innerHTML = headerHTML + '<div class="space-y-3 p-4 bg-slate-950 rounded-xl border border-slate-800">' + feedbackItems.join('') + '</div>';

            // Scroll al feedback
            setTimeout(() => {
                feedbackContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        }

        function corregirReto() {
            document.getElementById('reto-feedback-container').classList.add('hidden');
            
            // Rehabilitar selects
            ['data', 'factor', 'score', 'action', 'right'].forEach(id => {
                document.getElementById(`reto-select-${id}`).disabled = false;
            });

            // Scroll arriba
            document.getElementById('reto-form').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        function resetReto() {
            ['data', 'factor', 'score', 'action', 'right'].forEach(id => {
                const el = document.getElementById(`reto-select-${id}`);
                el.value = "";
                el.disabled = false;
            });

            document.getElementById('reto-badge').classList.add('hidden');
            document.getElementById('reto-feedback-container').classList.add('hidden');

            updateRetoPreview();
            document.getElementById('reto-form').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

'''

s1 = content.find(html_start)
e1 = content.find(html_end)
s2 = content.find(js_start)
e2 = content.find(js_end)

if s1!=-1 and e1!=-1 and s2!=-1 and e2!=-1:
    content = content[:s1] + html_new + '\n    ' + content[e1:s2] + js_new + '\n    ' + content[e2:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Reemplazo OK")
else:
    print("No se encontraron los tags")

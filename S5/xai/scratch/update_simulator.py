import re
import sys

filepath = 'd:/Proyectos/Arquitectura-Semana 5/UPN/S5/xai/xai.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new Javascript for the simulator
new_js = r'''// === SIMULADOR DIRECTIVO ===
        let showingConsequence = false;
        let consequenceData = null;

        function renderSimMetrics() {
            const container = document.getElementById('sim-metrics-container');

            const getMetricColor = (val) => {
                if (val > 70) return 'text-emerald-400';
                if (val > 40) return 'text-amber-400';
                return 'text-rose-500';
            };

            const metrics = [
                { name: 'Precisión Académica', desc: 'Qué tan bien el sistema detecta a los estudiantes en riesgo real.', value: simMetrics.academic },
                { name: 'Viabilidad Presupuestaria', desc: 'Recursos financieros disponibles para el proyecto.', value: simMetrics.economic },
                { name: 'Confianza Social', desc: 'Qué tanto docentes y estudiantes aceptan y usan el sistema.', value: simMetrics.trust },
                { name: 'Cumplimiento Legal (Ley de Protección de Datos)', desc: 'Riesgo de sanciones, demandas o reclamos por derechos de datos.', value: simMetrics.legal }
            ];

            container.innerHTML = metrics.map(m => `
                <div class="space-y-1">
                    <div class="flex justify-between text-sm font-semibold">
                        <span>${m.name}</span>
                        <span class="${getMetricColor(m.value)}">${m.value}%</span>
                    </div>
                    <p class="text-xs text-slate-400">${m.desc}</p>
                    <div class="w-full bg-slate-950 h-3 rounded-full overflow-hidden relative border border-slate-800 mt-1">
                        <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-rose-500/50 z-10"></div>
                        <div class="absolute left-1/2 top-0 bottom-0 text-[8px] text-rose-500/80 font-bold -ml-8 flex items-center">umbral mínimo</div>
                        <div class="bg-gradient-to-r from-cyan-500 to-indigo-500 h-full transition-all duration-500 relative z-0" style="width: ${m.value}%"></div>
                    </div>
                </div>
            `).join('');
        }

        function renderSimStage() {
            const container = document.getElementById('sim-stage-content');

            if (simStage === 0) {
                container.innerHTML = `
                    <div class="space-y-6 flex flex-col justify-center h-full">
                        <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider block">Su Nuevo Cargo: Dirección Académica</span>
                        <div class="space-y-4">
                            <p class="text-base text-slate-300 leading-relaxed">
                                Usted acaba de asumir la Dirección Académica de la institución. El Consejo Directivo le encargó implementar un sistema de Inteligencia Artificial para reducir la deserción estudiantil.
                            </p>
                            <p class="text-base text-slate-300 leading-relaxed">
                                Tomará 4 decisiones sobre el diseño del sistema. Cada una afectará su Tablero de Gestión.
                            </p>
                            <p class="text-base text-slate-300 leading-relaxed font-semibold text-rose-200 bg-rose-950/20 p-4 border border-rose-900/50 rounded-xl">
                                Su misión: que al finalizar, ninguna métrica caiga por debajo del 50%. Si la Confianza Social o el Cumplimiento Legal colapsan, el proyecto será cancelado y su gestión quedará cuestionada.
                            </p>
                            <p class="text-base text-slate-400 italic">
                                No hay opciones perfectas. Hay decisiones con consecuencias.
                            </p>
                        </div>
                        <button onclick="startSimulator()" class="mt-4 w-full md:w-auto bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-slate-950 font-extrabold text-base px-8 py-3.5 rounded-xl transition shadow flex items-center justify-center space-x-2">
                            <span>Asumir el cargo</span>
                            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                        </button>
                    </div>
                `;
                return;
            }

            if (showingConsequence) {
                const deltaFormat = (val) => val > 0 ? `<span class="text-emerald-400">+${val}</span>` : val < 0 ? `<span class="text-rose-400">${val}</span>` : `<span class="text-slate-400\">0</span>`;
                
                container.innerHTML = `
                    <span class="text-sm font-bold text-amber-400 uppercase tracking-wider bg-amber-500/10 py-1 px-2.5 rounded-full block w-fit mb-4">Consecuencia de su Decisión</span>
                    <div class="space-y-6 flex flex-col justify-center h-full">
                        <p class="text-lg text-slate-200 leading-relaxed italic border-l-4 border-amber-500/50 pl-4 py-2">
                            "${consequenceData.text}"
                        </p>
                        <div class="bg-slate-950 border border-slate-800 p-4 rounded-xl flex flex-wrap gap-4 text-sm font-bold justify-between">
                            <div>Precisión: ${deltaFormat(consequenceData.delta.academic)}</div>
                            <div>Presupuesto: ${deltaFormat(consequenceData.delta.economic)}</div>
                            <div>Confianza: ${deltaFormat(consequenceData.delta.trust)}</div>
                            <div>Legal: ${deltaFormat(consequenceData.delta.legal)}</div>
                        </div>
                        <button onclick="nextSimStage()" class="mt-4 w-full md:w-auto bg-slate-800 hover:bg-slate-700 text-white font-bold text-base px-8 py-3.5 rounded-xl transition flex items-center justify-center space-x-2">
                            <span>Continuar</span>
                            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                        </button>
                    </div>
                `;
                return;
            }

            const progressDots = [1, 2, 3, 4].map(i => i === simStage ? '●' : i < simStage ? '○' : '○').join(' ');

            if (simStage === 1) {
                container.innerHTML = `
                    <div class="flex items-center space-x-3 mb-4">
                        <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider bg-cyan-500/10 py-1 px-2.5 rounded-full">Decisión 1 de 4</span>
                        <span class="text-slate-500 tracking-[0.2em]">${progressDots}</span>
                    </div>
                    <div class="space-y-2">
                        <h3 class="text-xl md:text-2xl font-bold">Arquitectura de IA</h3>
                        <p class="text-base text-slate-400 leading-relaxed">¿Qué modelo implementará para la detección temprana de deserción?</p>
                    </div>
                    <div class="space-y-3">
                        <button onclick="makeSimDecision('model', 'A', { academic: 25, economic: 15, trust: -25, legal: -25 }, 'Tres meses después: las alertas son precisas, pero los tutores no pueden explicarlas. Los estudiantes reclaman decisiones que nadie sabe justificar.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-rose-400 block font-bold text-lg mb-2">Opción A: Sistema Complejo (Caja Negra)</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Máxima precisión (96%) y bajo costo inicial</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Nadie podrá explicar por qué se generó una alerta</p>
                            </div>
                        </button>
                        <button onclick="makeSimDecision('model', 'B', { academic: 20, economic: -15, trust: 25, legal: 25 }, 'El desarrollo tomó más presupuesto del previsto, pero cada alerta llega con sus razones. Los tutores empiezan a confiar en el sistema.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-cyan-400 block font-bold text-lg mb-2">Opción B: Modelo con Capa de Explicación (XAI)</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Alta precisión (92%) y cada alerta llega traducida a razones comprensibles</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Requiere presupuesto adicional de desarrollo</p>
                            </div>
                        </button>
                        <button onclick="makeSimDecision('model', 'C', { academic: -15, economic: 10, trust: 20, legal: 15 }, 'El sistema es comprensible para todos, pero se le escapan casos complejos y genera falsos positivos que irritan a algunos tutores.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-emerald-400 block font-bold text-lg mb-2">Opción C: Modelo Simple y Transparente</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Cualquier docente entiende cómo funciona de inmediato</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Precisión modesta (75%): más falsos positivos en alumnos atípicos</p>
                            </div>
                        </button>
                    </div>
                `;
            } else if (simStage === 2) {
                container.innerHTML = `
                    <div class="flex items-center space-x-3 mb-4">
                        <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider bg-cyan-500/10 py-1 px-2.5 rounded-full">Decisión 2 de 4</span>
                        <span class="text-slate-500 tracking-[0.2em]">${progressDots}</span>
                    </div>
                    <div class="space-y-2">
                        <h3 class="text-xl md:text-2xl font-bold">Datos del Sistema</h3>
                        <p class="text-base text-slate-400 leading-relaxed">¿Qué información alimentará al algoritmo?</p>
                    </div>
                    <div class="space-y-3">
                        <button onclick="makeSimDecision('data', 'A', { academic: 15, economic: 15, trust: -30, legal: -30 }, 'Auditoría interna detecta que el sistema penaliza sistemáticamente a estudiantes de distritos periféricos. El caso llega a oídos de la prensa universitaria.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-rose-400 block font-bold text-lg mb-2">Opción A: Todos los datos disponibles</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Mayor precisión al incluir código postal y colegio de procedencia</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Esas variables reflejan el nivel socioeconómico: riesgo de discriminación indirecta</p>
                            </div>
                        </button>
                        <button onclick="makeSimDecision('data', 'B', { academic: 10, economic: -5, trust: 25, legal: 25 }, 'El comité de ética aprueba el diseño. El sistema pierde algo de capacidad predictiva, pero ninguna alerta puede atribuirse al origen del estudiante.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-cyan-400 block font-bold text-lg mb-2">Opción B: Solo comportamiento académico</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Asistencia, notas y actividad en el Aula Virtual; sin variables sensibles</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Pierde algo de precisión predictiva</p>
                            </div>
                        </button>
                    </div>
                `;
            } else if (simStage === 3) {
                container.innerHTML = `
                    <div class="flex items-center space-x-3 mb-4">
                        <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider bg-cyan-500/10 py-1 px-2.5 rounded-full">Decisión 3 de 4</span>
                        <span class="text-slate-500 tracking-[0.2em]">${progressDots}</span>
                    </div>
                    <div class="space-y-2">
                        <h3 class="text-xl md:text-2xl font-bold">Comunicación a los Estudiantes</h3>
                        <p class="text-base text-slate-400 leading-relaxed">¿Cómo informará sobre el uso de la IA?</p>
                    </div>
                    <div class="space-y-3">
                        <button onclick="makeSimDecision('transparency', 'A', { academic: 10, economic: 15, trust: -35, legal: -35 }, 'Un estudiante descubre por casualidad que su perfil era analizado sin su conocimiento. Presenta un reclamo formal por sus derechos de datos y otros lo siguen.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-rose-400 block font-bold text-lg mb-2">Opción A: Implementación silenciosa</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Los estudiantes no alteran su conducta para &quot;engañar&quot; al sistema</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Se vulnera su derecho a saber que son analizados</p>
                            </div>
                        </button>
                        <button onclick="makeSimDecision('transparency', 'B', { academic: 5, economic: -5, trust: 30, legal: 30 }, 'La transparencia genera confianza: los estudiantes consultan su propio panel y varios buscan apoyo antes de que el sistema los alerte.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-cyan-400 block font-bold text-lg mb-2">Opción B: Aviso visible y consentimiento</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Aviso en matrícula y panel donde cada estudiante ve su propio reporte</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Algunos estudiantes podrían modificar su comportamiento</p>
                            </div>
                        </button>
                    </div>
                `;
            } else if (simStage === 4) {
                container.innerHTML = `
                    <div class="flex items-center space-x-3 mb-4">
                        <span class="text-sm font-bold text-cyan-400 uppercase tracking-wider bg-cyan-500/10 py-1 px-2.5 rounded-full">Decisión 4 de 4</span>
                        <span class="text-slate-500 tracking-[0.2em]">${progressDots}</span>
                    </div>
                    <div class="space-y-2">
                        <h3 class="text-xl md:text-2xl font-bold">¿Quién ejecuta las alertas?</h3>
                        <p class="text-base text-slate-400 leading-relaxed">Defina el protocolo cuando el sistema detecta riesgo alto.</p>
                    </div>
                    <div class="space-y-3">
                        <button onclick="makeSimDecision('process', 'A', { academic: 15, economic: 20, trust: -30, legal: -30 }, 'El sistema suspendió la beca de una estudiante cuya inactividad era una hospitalización. La familia inicia acciones legales y el caso se hace público.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-rose-400 block font-bold text-lg mb-2">Opción A: Automatización total</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> Respuesta inmediata sin carga de trabajo para los docentes</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> El sistema suspende becas y emite cartas sin que nadie revise el contexto</p>
                            </div>
                        </button>
                        <button onclick="makeSimDecision('process', 'B', { academic: 10, economic: -5, trust: 35, legal: 25 }, 'Los tutores validan cada alerta con contexto humano. Detectan dos falsos positivos por fallas de conectividad y una emergencia familiar. El sistema se percibe como apoyo, no como amenaza.')" class="w-full p-4 rounded-xl border border-slate-800 bg-slate-950 text-left hover:border-cyan-500/30 transition text-sm space-y-1 block">
                            <strong class="text-cyan-400 block font-bold text-lg mb-2">Opción B: Validación docente (Human-in-the-loop)</strong>
                            <div class="text-slate-300 space-y-1.5">
                                <p class="flex items-start"><span class="text-emerald-400 mr-2\">✓</span> La IA alerta con las causas; un docente valida antes de actuar</p>
                                <p class="flex items-start"><span class="text-rose-400 mr-2\">⚠</span> Requiere tiempo docente y las alertas podrían acumularse</p>
                            </div>
                        </button>
                    </div>
                `;
            } else {
                // Resultados finales del Simulador
                document.getElementById('sim-reset-container').classList.remove('hidden');

                const hasCriticalIssue = simMetrics.trust < 50 || simMetrics.legal < 50;
                let dictamenHTML = '';

                if (hasCriticalIssue) {
                    dictamenHTML = `
                        <div class="bg-rose-500/10 border border-rose-500/30 p-5 rounded-xl text-rose-300 space-y-3">
                            <div class="flex items-center space-x-2">
                                <span class="text-2xl">🚨</span>
                                <strong class="font-extrabold text-lg">Proyecto Cancelado por el Consejo</strong>
                            </div>
                            <p class="text-base leading-relaxed">
                                Sus decisiones priorizaron en exceso la eficiencia técnica y la automatización silenciosa. Ha implementado una solución "Caja Negra" vulnerable a demandas legales y con fuerte rechazo estudiantil. Debe replantear su gobernanza hacia una "IA Explicable" con un enfoque centrado en las personas.
                            </p>
                        </div>
                    `;
                } else {
                    dictamenHTML = `
                        <div class="bg-emerald-500/10 border border-emerald-500/30 p-5 rounded-xl text-emerald-300 space-y-3">
                            <div class="flex items-center space-x-2">
                                <span class="text-2xl">✓</span>
                                <strong class="font-extrabold text-lg">Gestión Reconocida: IA Ética y Auditable</strong>
                            </div>
                            <p class="text-base leading-relaxed">
                                ¡Felicitaciones Directivo! Ha logrado un diseño robusto bajo los principios de ética por diseño, transparencia operativa y "Human-in-the-loop". Su sistema es auditable, legalmente sólido y cuenta con la confianza de docentes y alumnos.
                            </p>
                        </div>
                    `;
                }

                container.innerHTML = `
                    <span class="text-sm font-bold text-emerald-400 uppercase tracking-wider bg-emerald-500/10 py-1 px-2.5 rounded-full block w-fit mb-4">Dictamen Técnico Emitido</span>
                    <div class="space-y-2">
                        <h3 class="text-xl md:text-3xl font-black">Reporte Final de la Simulación</h3>
                        <p class="text-base text-slate-400 leading-relaxed">Análisis de viabilidad institucional de sus elecciones de política institucional.</p>
                    </div>

                    ${dictamenHTML}

                    <div class="space-y-3 pt-4 border-t border-slate-800 mt-4">
                        <h4 class="text-base font-bold text-slate-300">Bitácora de Decisiones:</h4>
                        <div class="space-y-2 max-h-[200px] overflow-y-auto pr-2 text-xs text-slate-400 leading-relaxed">
                            ${simHistory.map((h, i) => `
                                <div class="bg-slate-950 p-3 rounded-lg border border-slate-850">
                                    <strong class="text-cyan-400 block text-sm mb-1">${i + 1}. ${h.category}:</strong>
                                    <span class="text-sm">${h.decision}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }
        }
        
        function startSimulator() {
            simStage = 1;
            renderSimStage();
        }

        function makeSimDecision(category, option, metricsChange, consequenceText) {
            simDecisions[category] = option;

            // Actualizar métricas
            simMetrics.academic = Math.min(100, Math.max(0, simMetrics.academic + metricsChange.academic));
            simMetrics.economic = Math.min(100, Math.max(0, simMetrics.economic + metricsChange.economic));
            simMetrics.trust = Math.min(100, Math.max(0, simMetrics.trust + metricsChange.trust));
            simMetrics.legal = Math.min(100, Math.max(0, simMetrics.legal + metricsChange.legal));

            // Guardar historial
            const optionLabels = {
                model: option === 'A' ? 'Sistema Complejo (Caja Negra)' : option === 'B' ? 'Modelo con Capa de Explicación (XAI)' : 'Modelo Simple y Transparente',
                data: option === 'A' ? 'Todos los datos disponibles' : 'Solo comportamiento académico',
                transparency: option === 'A' ? 'Implementación silenciosa' : 'Aviso visible y consentimiento',
                process: option === 'A' ? 'Automatización total' : 'Validación docente (Human-in-the-loop)'
            };

            simHistory.push({
                category: category === 'model' ? 'Arquitectura de IA' : category === 'data' ? 'Datos del Sistema' : category === 'transparency' ? 'Comunicación a los Estudiantes' : '¿Quién ejecuta las alertas?',
                decision: optionLabels[category]
            });

            // Preparar consecuencia
            consequenceData = {
                text: consequenceText,
                delta: metricsChange
            };
            showingConsequence = true;

            renderSimMetrics();
            renderSimStage();
        }
        
        function nextSimStage() {
            showingConsequence = false;
            simStage++;

            if (simStage === 5) {
                // Prevent crash if userProgress isn't fully defined yet, though we patched it
                if (typeof userProgress !== 'undefined') {
                    userProgress.simCompleted = true;
                    if (typeof saveProgress === 'function') saveProgress();
                    if (typeof updateProgressUI === 'function') updateProgressUI();
                }
            }

            renderSimStage();
        }

        function resetSimulator() {
            simStage = 0;
            showingConsequence = false;
            simMetrics = { academic: 50, economic: 70, trust: 40, legal: 50 };
            simHistory = [];
            document.getElementById('sim-reset-container').classList.add('hidden');
            renderSimMetrics();
            renderSimStage();
        }'''

# Extract the block to replace
start_marker = '// === SIMULADOR DIRECTIVO ==='
end_marker = '// === ACTIVIDAD DIDÁCTICA: RETO CAJA NEGRA ==='

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_js + '\n\n        ' + content[end_idx:]
    
    # Also change simStage = 1 to simStage = 0 in the global vars at the top of script
    content = content.replace("let simStage = 1;", "let simStage = 0;")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Reemplazo JS exitoso")
else:
    print("No se encontraron los marcadores")

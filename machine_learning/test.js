



        AFRAME.registerComponent('mouse-pan-zoom', {
            schema: {
                panSpeed: {type: 'number', default: 0.005},
                zoomSpeed: {type: 'number', default: 0.005},
                minZoom: {type: 'number', default: 1},
                maxZoom: {type: 'number', default: 10}
            },
            init: function () {
                this.isDragging = false;
                this.previousMousePosition = {x: 0, y: 0};
                this.onMouseDown = this.onMouseDown.bind(this);
                this.onMouseUp = this.onMouseUp.bind(this);
                this.onMouseMove = this.onMouseMove.bind(this);
                this.onWheel = this.onWheel.bind(this);

                window.addEventListener('mousedown', this.onMouseDown);
                window.addEventListener('mouseup', this.onMouseUp);
                window.addEventListener('mousemove', this.onMouseMove);
                window.addEventListener('wheel', this.onWheel, {passive: false});
            },
            remove: function () {
                window.removeEventListener('mousedown', this.onMouseDown);
                window.removeEventListener('mouseup', this.onMouseUp);
                window.removeEventListener('mousemove', this.onMouseMove);
                window.removeEventListener('wheel', this.onWheel);
            },
            onMouseDown: function (evt) {
                if (evt.button !== 0 || isARMode) return; 
                if (evt.target.closest('.interactive-ui')) return; // No hacer pan si hacemos click en la UI
                this.isDragging = true;
                this.previousMousePosition = {x: evt.clientX, y: evt.clientY};
            },
            onMouseUp: function () {
                this.isDragging = false;
            },
            onMouseMove: function (evt) {
                if (!this.isDragging || isARMode) return;

                const deltaX = evt.clientX - this.previousMousePosition.x;
                const deltaY = evt.clientY - this.previousMousePosition.y;

                this.previousMousePosition = {x: evt.clientX, y: evt.clientY};

                const position = this.el.getAttribute('position');
                position.x -= deltaX * this.data.panSpeed;
                position.y += deltaY * this.data.panSpeed;
                this.el.setAttribute('position', position);
            },
            onWheel: function (evt) {
                if(isARMode) return;
                const position = this.el.getAttribute('position');
                position.z += evt.deltaY * this.data.zoomSpeed;
                position.z = Math.max(this.data.minZoom, Math.min(this.data.maxZoom, position.z));
                this.el.setAttribute('position', position);
            }
        });

        // --- 1. GENERACIÓN DE DATOS (NO SUPERVISADO) ---
        // Generamos 80 estudiantes con variables continuas y categóricas.
        // No existe etiqueta de éxito/fracaso.
        const students = [];
        // Mapeo lógico:
        // X = Interacción (Participación, Tiempo, Consultas, Recursos)
        // Y = Cumplimiento (Asistencia, Tareas, Puntualidad)

        for (let i = 1; i <= 80; i++) {
            // Distribuimos equitativamente en 4 "tendencias" o clusters naturales (sin decírselo al modelo)
            const cluster = (i % 4) + 1;
            let x, y;

            // Generación de coordenadas en el plano cartesiano (-2.5 a 2.5)
            // Cluster 1: Alta Int (+X), Alto Cump (+Y)
            if (cluster === 1) { x = 0.5 + Math.random() * 1.8; y = 0.5 + Math.random() * 1.8; }
            // Cluster 2: Baja Int (-X), Alto Cump (+Y)
            else if (cluster === 2) { x = -2.3 + Math.random() * 1.8; y = 0.5 + Math.random() * 1.8; }
            // Cluster 3: Alta Int (+X), Bajo Cump (-Y)
            else if (cluster === 3) { x = 0.5 + Math.random() * 1.8; y = -2.3 + Math.random() * 1.8; }
            // Cluster 4: Baja Int (-X), Bajo Cump (-Y)
            else { x = -2.3 + Math.random() * 1.8; y = -2.3 + Math.random() * 1.8; }

            // Generación de variables basadas puramente en las coordenadas
            // Eje X (Interacción)
            const participacion = x > 0 ? (x > 1.2 ? "Alta" : "Media") : "Baja";
            const tiempo = (Math.max(1, (x + 2.5) * 1.5 + Math.random())).toFixed(1) + " horas";
            const consultas = Math.floor(Math.max(0, (x + 2.5) * 1.2 + Math.random() * 2));
            const recursos = x > 0 ? "Frecuente" : "Escaso";

            // Eje Y (Cumplimiento)
            const asistenciaNum = Math.min(100, Math.max(30, Math.floor((y + 2.5) * 20 + Math.random() * 10)));
            const asistencia = (y > 0 ? "Alta" : "Baja") + ` (${asistenciaNum}%)`;
            const tareas = y > 0.5 ? "Completas" : (y > -1 ? "Parciales" : "Incompletas");
            const puntualidad = y > 0 ? "Alta" : "Baja";

            students.push({
                id: "E" + String(i).padStart(3, '0'),
                x: x, y: y,
                cluster: cluster,
                vars: { asistencia, tareas, participacion, tiempo, puntualidad, consultas, recursos }
            });
        }

        // --- 2. MÓDULOS EDUCATIVOS ---
        const modules = [
            {
                id: 1,
                title: "Módulo 1: Datos Sin Etiquetas",
                html: `
                    <p>En el <strong>Machine Learning No Supervisado</strong> no existen respuestas conocidas ni datos etiquetados históricamente.</p>
                    <p>En el plano frente a ti, cada punto representa a un estudiante. La IA no sabe quién aprueba o desaprueba, porque nadie le ha dado esa información.</p>
                    <p>El algoritmo solo observa características puras: asistencia, participación, tareas, consultas y uso de recursos digitales.</p>
                    <div class="p-3 bg-indigo-900/50 border border-indigo-400 rounded-lg mt-4 text-indigo-200">
                        <strong>Cierre:</strong> El modelo no predice resultados. Primero, simplemente observa y distribuye los datos.
                    </div>
                `,
                onEnter: () => { showAllPoints(); hideAxesHighlight(); hideNeighbors(); hideClusters(); closeStudentPanel(); document.getElementById('comparison-panels').classList.add('hidden'); }
            },
            {
                id: 2,
                title: "Módulo 2: Comprender los Ejes",
                html: `
                    <p>Para visualizar a los estudiantes, hemos reducido sus múltiples variables en dos dimensiones principales:</p>
                    <ul class="list-disc pl-5 mt-2 space-y-2">
                        <li><strong class="text-blue-400">Eje X (Horizontal): Nivel de interacción académica.</strong><br>Calculado analizando participación, tiempo en plataforma, consultas al docente y uso de recursos digitales.</li>
                        <li><strong class="text-emerald-400">Eje Y (Vertical): Nivel de cumplimiento académico.</strong><br>Calculado analizando asistencia, tareas entregadas y puntualidad.</li>
                    </ul>
                    <div class="p-3 bg-indigo-900/50 border border-indigo-400 rounded-lg mt-4 text-indigo-200">
                        <strong>Cierre:</strong> Los ejes convierten datos abstractos de comportamiento en una representación visual y espacial comprensible.
                    </div>
                `,
                onEnter: () => { highlightAxes(); hideNeighbors(); hideClusters(); closeStudentPanel(); document.getElementById('comparison-panels').classList.add('hidden'); }
            },
            {
                id: 3,
                title: "Módulo 3: Cercanía entre Datos",
                html: `
                    <p>En el plano, la distancia entre dos puntos indica matemáticamente qué tan similares son sus comportamientos.</p>
                    <p>Selecciona cualquier punto en el plano para ver líneas que lo conectan con sus 4 "vecinos" más cercanos.</p>
                    <p>Esta cercanía espacial permite que el algoritmo encuentre patrones y afinidades, sin necesidad de saber el resultado final de los estudiantes.</p>
                    <div class="p-3 bg-indigo-900/50 border border-indigo-400 rounded-lg mt-4 text-indigo-200">
                        <strong>Cierre:</strong> La IA no necesita etiquetas previas para detectar similitudes entre los individuos.
                    </div>
                `,
                onEnter: () => { showAllPoints(); unhighlightAxes(); enableNeighborMode(); hideClusters(); closeStudentPanel(); document.getElementById('comparison-panels').classList.add('hidden'); }
            },
            {
                id: 4,
                title: "Módulo 4: Segmentación (Clustering)",
                html: `
                    <p>La técnica más común no supervisada es el <strong>Clustering</strong>.</p>
                    <p>Presiona el botón <strong class="text-white">"Mostrar Clusters"</strong> (abajo a la derecha) para ver cómo la IA agrupa automáticamente los 80 puntos en 4 zonas o perfiles, basándose únicamente en su cercanía.</p>
                    <ul class="text-xs space-y-1 mt-3">
                        <li><span class="text-emerald-400 font-bold">Z1 (Sup. Der):</span> Alta interacción, alto cumplimiento.</li>
                        <li><span class="text-blue-400 font-bold">Z2 (Sup. Izq):</span> Baja interacción, alto cumplimiento.</li>
                        <li><span class="text-amber-400 font-bold">Z3 (Inf. Der):</span> Alta interacción, bajo cumplimiento.</li>
                        <li><span class="text-rose-400 font-bold">Z4 (Inf. Izq):</span> Baja interacción, bajo cumplimiento.</li>
                    </ul>
                    <div class="p-3 bg-indigo-900/50 border border-indigo-400 rounded-lg mt-4 text-indigo-200">
                        <strong>Cierre:</strong> El clustering agrupa por similitud, no emite una sentencia definitiva sobre el estudiante. El nombre e interpretación del grupo los da el docente humano.
                    </div>
                `,
                onEnter: () => { disableNeighborMode(); showClusterControls(); hidePanelsExceptControls(); }
            },
            {
                id: 5,
                title: "Módulo 5: Interpretación Humana",
                html: `
                    <p>El algoritmo es útil, pero ciego ante la realidad externa.</p>
                    <p>Hemos seleccionado automáticamente al estudiante <strong>E027</strong> (ubicado en la zona inferior izquierda de baja interacción y bajo cumplimiento).</p>
                    <div class="grid grid-cols-2 gap-2 mt-4 text-xs">
                        <div class="bg-indigo-900/40 p-2 border border-indigo-500 rounded">
                            <strong class="text-indigo-300">Lo que la IA observa:</strong><br>
                            Asistencia baja, tareas incompletas, 0 consultas, poca participación.
                        </div>
                        <div class="bg-rose-900/40 p-2 border border-rose-500 rounded">
                            <strong class="text-rose-300">Lo que la IA NO sabe:</strong><br>
                            Problemas familiares, falta de conectividad, carga laboral extrema o salud emocional.
                        </div>
                    </div>
                    <div class="p-3 bg-indigo-900/50 border border-indigo-400 rounded-lg mt-4 text-indigo-200">
                        <strong>Cierre:</strong> La IA agrupa y visualiza patrones, pero el docente debe interpretar el contexto éticamente antes de tomar decisiones.
                    </div>
                `,
                onEnter: () => { toggleClusters(true); hideClusterControls(); selectStudentE027(); }
            },
            {
                id: 6,
                title: "Módulo 6: Supervisado vs No Supervisado",
                html: `
                    <p>Para concluir, visualicemos la diferencia fundamental entre ambos enfoques en la pantalla principal.</p>
                    <p>Mientras que el aprendizaje <strong>Supervisado</strong> requiere conocer los resultados históricos para predecir el futuro, el <strong>No Supervisado</strong> trabaja a ciegas descubriendo la estructura y los patrones ocultos de los datos actuales.</p>
                    <div class="p-3 bg-indigo-900/50 border border-indigo-400 rounded-lg mt-4 text-indigo-200">
                        <strong>Cierre final:</strong> El aprendizaje no supervisado sirve para descubrir grupos similares y apoyar la reflexión docente, no para automatizar juicios o calificaciones.
                    </div>
                `,
                onEnter: () => { toggleClusters(false); closeStudentPanel(); document.getElementById('comparison-panels').classList.remove('hidden'); }
            }
        ];

        let currentModuleIndex = 0;
        let isARMode = false;
        let neighborMode = false;
        let sceneBuilt = false;
        
        let camPosition = { x: 0, y: 0, z: 4 };

        // --- 3. INICIALIZACIÓN ---
        function requestAR() {
            // Solicitar cámara explicitamente solo al pedir AR
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    // Detenemos el stream temporalmente, AR.js lo volverá a pedir internamente
                    stream.getTracks().forEach(track => track.stop());
                    document.getElementById('btn-toggle-ar').style.display = 'none';
                    initExperience('ar');
                })
                .catch(function (err) {
                    alert("No se pudo activar la cámara o el permiso fue denegado. Puedes continuar usando el modo simulación.");
                    initExperience('sim');
                });
        }

        function initExperience(mode) {
            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('start-screen').classList.remove('flex');
            document.getElementById('ui-layer').classList.remove('hidden');
            document.getElementById('ui-layer').style.display = 'flex';
            
            if (sceneBuilt) {
                // Ya estaba construido, no reconstruimos
                return;
            }

            isARMode = (mode === 'ar');
            
            if (isARMode) {
                const script = document.createElement('script');
                script.src = "https://raw.githack.com/AR-js-org/AR.js/master/aframe/build/aframe-ar.js";
                script.onload = () => buildScene();
                document.head.appendChild(script);
            } else {
                buildScene();
            }
        }

        function buildScene() {
            sceneBuilt = true;
            const container = document.getElementById('scene-container');
            let html = '';

            if (isARMode) {
                html = `
                    <a-scene embedded arjs="sourceType: webcam; debugUIEnabled: false;" vr-mode-ui="enabled: false" raycaster="objects: .clickable" cursor="rayOrigin: mouse">
                        <a-marker preset="hiro">
                            <a-entity id="content-anchor" rotation="-90 0 0" scale="0.6 0.6 0.6">
                                <!-- Contenido dinámico -->
                            </a-entity>
                        </a-marker>
                        <a-entity id="camera-rig"><a-entity camera></a-entity></a-entity>
                    </a-scene>
                `;
            } else {
                html = `
                    <a-scene embedded vr-mode-ui="enabled: false" raycaster="objects: .clickable" cursor="rayOrigin: mouse" background="color: #0f172a">
                        <!-- Luces -->
                        <a-light type="ambient" color="#fff" intensity="0.6"></a-light>
                        <a-light type="directional" position="-1 2 1" intensity="0.4"></a-light>
                        
                        <a-entity id="camera-rig" position="0 0 4.5" mouse-pan-zoom>
                            <a-entity camera look-controls="enabled: false" wasd-controls="enabled: false"></a-entity>
                        </a-entity>
                        
                        <a-entity id="content-anchor" position="0 0 0">
                            <!-- Contenido dinámico -->
                        </a-entity>
                    </a-scene>
                `;
            }
            container.innerHTML = html;

            setTimeout(() => {
                setupCartesianPlane();
                loadModule(0);
                
                // Listener global para clics en puntos
                document.querySelector('a-scene').addEventListener('click', function(e) {
                    if (e.detail.intersection && e.detail.intersection.object.el.classList.contains('point')) {
                        handlePointClick(e.detail.intersection.object.el);
                    }
                });
            }, 500);
        }

        // --- 4. CONSTRUCCIÓN DEL PLANO CARTESIANO Y PUNTOS ---
        function setupCartesianPlane() {
            const anchor = document.getElementById('content-anchor');
            if (!anchor) return;

            const group = document.createElement('a-entity');
            group.setAttribute('id', 'plane-group');

            // Grid
            const grid = document.createElement('a-plane');
            grid.setAttribute('width', '5.5');
            grid.setAttribute('height', '5.5');
            grid.setAttribute('color', '#1e293b');
            grid.setAttribute('position', '0 0 -0.05');
            group.appendChild(grid);

            // Ejes (sin tildes - A-Frame MSDF no las soporta)
            const axisX = document.createElement('a-entity');
            axisX.setAttribute('id', 'axis-x');
            axisX.setAttribute('line', 'start: -2.8 0 0; end: 2.8 0 0; color: #94a3b8; opacity: 0.5');

            const labelX = document.createElement('a-text');
            labelX.setAttribute('id', 'label-x');
            labelX.setAttribute('value', 'Interaccion Academica ->');
            labelX.setAttribute('align', 'center');
            labelX.setAttribute('position', '0 -3.1 0');
            labelX.setAttribute('color', '#60a5fa');
            labelX.setAttribute('width', '4');
            axisX.appendChild(labelX);

            group.appendChild(axisX);

            const axisY = document.createElement('a-entity');
            axisY.setAttribute('id', 'axis-y');
            axisY.setAttribute('line', 'start: 0 -2.8 0; end: 0 2.8 0; color: #94a3b8; opacity: 0.5');

            const labelY = document.createElement('a-text');
            labelY.setAttribute('id', 'label-y');
            labelY.setAttribute('value', 'Cumplimiento Academico ->');
            labelY.setAttribute('align', 'center');
            labelY.setAttribute('position', '-3.5 0 0');
            labelY.setAttribute('rotation', '0 0 90');
            labelY.setAttribute('color', '#34d399');
            labelY.setAttribute('width', '4');
            axisY.appendChild(labelY);

            group.appendChild(axisY);

            // Capa para líneas de vecinos
            const linksLayer = document.createElement('a-entity');
            linksLayer.setAttribute('id', 'links-layer');
            group.appendChild(linksLayer);

            // Capa de zonas (Clusters)
            const clustersLayer = document.createElement('a-entity');
            clustersLayer.setAttribute('id', 'clusters-layer');
            clustersLayer.setAttribute('visible', 'false');
            
            const zones = [
                { id: 'c1', pos: '1.25 1.25 -0.05', color: '#10b981' }, // Emerald
                { id: 'c2', pos: '-1.25 1.25 -0.05', color: '#3b82f6' }, // Blue
                { id: 'c3', pos: '1.25 -1.25 -0.05', color: '#f59e0b' }, // Amber
                { id: 'c4', pos: '-1.25 -1.25 -0.05', color: '#f43f5e' }  // Rose
            ];
            
            zones.forEach(z => {
                const p = document.createElement('a-plane');
                p.setAttribute('position', z.pos);
                p.setAttribute('width', '2.5');
                p.setAttribute('height', '2.5');
                p.setAttribute('color', z.color);
                p.setAttribute('opacity', '0.15');
                p.setAttribute('material', 'transparent: true; side: double');
                clustersLayer.appendChild(p);
            });
            group.appendChild(clustersLayer);

            // Puntos (Estudiantes)
            const pointsLayer = document.createElement('a-entity');
            pointsLayer.setAttribute('id', 'points-layer');
            
            students.forEach(st => {
                const pt = document.createElement('a-circle');
                pt.setAttribute('id', st.id);
                pt.setAttribute('class', 'clickable point');
                pt.setAttribute('radius', '0.06');
                pt.setAttribute('color', '#cbd5e1');
                pt.setAttribute('position', `${st.x} ${st.y} 0.01`);
                
                // Texto código estudiante
                const txt = document.createElement('a-text');
                txt.setAttribute('value', st.id);
                txt.setAttribute('align', 'center');
                txt.setAttribute('position', '0 -0.12 0');
                txt.setAttribute('scale', '0.4 0.4 0.4');
                txt.setAttribute('color', '#94a3b8');
                pt.appendChild(txt);

                pointsLayer.appendChild(pt);
            });
            group.appendChild(pointsLayer);

            anchor.appendChild(group);
        }

        // --- 5. LOGICA DE MÓDULOS Y UI ---
        function loadModule(index) {
            currentModuleIndex = index;
            const mod = modules[index];

            document.getElementById('mod-indicator').innerText = mod.id;
            document.getElementById('mod-title').innerText = mod.title;
            document.getElementById('mod-content').innerHTML = mod.html;

            document.getElementById('btn-prev').disabled = (index === 0);
            document.getElementById('btn-next').disabled = (index === modules.length - 1);

            if (mod.onEnter) mod.onEnter();
        }

        function nextModule() {
            if (currentModuleIndex < modules.length - 1) loadModule(currentModuleIndex + 1);
        }

        function prevModule() {
            if (currentModuleIndex > 0) loadModule(currentModuleIndex - 1);
        }

        // --- 6. FUNCIONES DE VIZUALIZACIÓN (ACCIONES MÓDULOS) ---
        function hideAxesHighlight() { unhighlightAxes(); }
        function hideClusters() { toggleClusters(false); }

        function showAllPoints() {
            const points = document.querySelectorAll('.point');
            points.forEach(p => {
                p.setAttribute('color', '#cbd5e1'); // Reset color
                p.setAttribute('scale', '1 1 1');
            });
        }

        function highlightAxes() {
            document.getElementById('axis-x').setAttribute('line', 'color: #60a5fa; opacity: 1'); // Resaltar X
            document.getElementById('axis-y').setAttribute('line', 'color: #34d399; opacity: 1'); // Resaltar Y
            document.getElementById('label-x').setAttribute('color', '#93c5fd');
            document.getElementById('label-y').setAttribute('color', '#6ee7b7');
            document.getElementById('label-x').setAttribute('scale', '1.2 1.2 1.2');
            document.getElementById('label-y').setAttribute('scale', '1.2 1.2 1.2');
        }

        function unhighlightAxes() {
            document.getElementById('axis-x').setAttribute('line', 'color: #94a3b8; opacity: 0.5');
            document.getElementById('axis-y').setAttribute('line', 'color: #94a3b8; opacity: 0.5');
            document.getElementById('label-x').setAttribute('color', '#60a5fa');
            document.getElementById('label-y').setAttribute('color', '#34d399');
            document.getElementById('label-x').setAttribute('scale', '1 1 1');
            document.getElementById('label-y').setAttribute('scale', '1 1 1');
        }

        function enableNeighborMode() {
            neighborMode = true;
        }

        function disableNeighborMode() {
            neighborMode = false;
            hideNeighbors();
        }

        function hideNeighbors() {
            const layer = document.getElementById('links-layer');
            if(layer) layer.innerHTML = '';
        }

        function showClusterControls() {
            document.getElementById('cluster-controls').classList.remove('hidden');
        }

        function hideClusterControls() {
            document.getElementById('cluster-controls').classList.add('hidden');
        }

        function hidePanelsExceptControls() {
            closeStudentPanel();
            document.getElementById('comparison-panels').classList.add('hidden');
        }

        function toggleClusters(show) {
            const layer = document.getElementById('clusters-layer');
            if (layer) layer.setAttribute('visible', show ? 'true' : 'false');

            const points = document.querySelectorAll('.point');
            points.forEach(p => {
                if (show) {
                    const st = students.find(s => s.id === p.getAttribute('id'));
                    if (st) {
                        let col = '#cbd5e1';
                        if (st.cluster === 1) col = '#10b981'; // Emerald
                        if (st.cluster === 2) col = '#3b82f6'; // Blue
                        if (st.cluster === 3) col = '#f59e0b'; // Amber
                        if (st.cluster === 4) col = '#f43f5e'; // Rose
                        p.setAttribute('color', col);
                    }
                } else {
                    p.setAttribute('color', '#cbd5e1');
                }
            });
        }

        // Simula la selección de E027 en el módulo 5
        function selectStudentE027() {
            // Buscamos un estudiante del cluster 4 forzadamente para el ejemplo didáctico
            let st = students.find(s => s.cluster === 4);
            if(st) {
                st.id = 'E027'; // Forzamos id para alinear con la historia
                const pt = document.getElementById(st.id);
                if(pt) {
                    pt.setAttribute('scale', '1.5 1.5 1.5');
                    pt.setAttribute('color', '#fff');
                    openStudentPanel(st);
                }
            }
        }

        // --- 7. INTERACCIÓN Y PANEL DE ESTUDIANTE ---
        function handlePointClick(el) {
            const stId = el.getAttribute('id');
            const st = students.find(s => s.id === stId);
            if (!st) return;

            // Reset scale of all
            document.querySelectorAll('.point').forEach(p => p.setAttribute('scale', '1 1 1'));
            // Highlight clicked
            el.setAttribute('scale', '1.5 1.5 1.5');

            if (neighborMode) {
                drawNeighbors(st);
            }

            openStudentPanel(st);
        }

        function drawNeighbors(centerSt) {
            const layer = document.getElementById('links-layer');
            layer.innerHTML = ''; // Clear old links

            // Calcular distancias euclidianas a todos
            let dists = students.map(s => {
                return {
                    id: s.id,
                    d: Math.sqrt(Math.pow(s.x - centerSt.x, 2) + Math.pow(s.y - centerSt.y, 2))
                };
            });

            // Ordenar y tomar los 5 más cercanos (excluyendo a sí mismo que es d=0)
            dists.sort((a,b) => a.d - b.d);
            const neighbors = dists.slice(1, 6);

            neighbors.forEach(n => {
                const targetSt = students.find(s => s.id === n.id);
                const line = document.createElement('a-entity');
                line.setAttribute('line', `start: ${centerSt.x} ${centerSt.y} 0.01; end: ${targetSt.x} ${targetSt.y} 0.01; color: #fbbf24; opacity: 0.8`);
                layer.appendChild(line);
                
                // Resaltar vecino ligeramente
                const np = document.getElementById(n.id);
                if(np) np.setAttribute('scale', '1.2 1.2 1.2');
            });
        }

        function openStudentPanel(st) {
            document.getElementById('st-id').innerText = `Estudiante ${st.id}`;
            document.getElementById('st-x-desc').innerText = st.x > 0 ? "Alto" : "Bajo";
            document.getElementById('st-x-desc').className = `font-semibold ${st.x > 0 ? 'text-blue-600' : 'text-slate-500'}`;
            document.getElementById('st-y-desc').innerText = st.y > 0 ? "Alto" : "Bajo";
            document.getElementById('st-y-desc').className = `font-semibold ${st.y > 0 ? 'text-emerald-600' : 'text-slate-500'}`;

            const ul = document.getElementById('st-vars');
            ul.innerHTML = `
                <li class="flex justify-between"><span>Asistencia:</span> <strong>${st.vars.asistencia}</strong></li>
                <li class="flex justify-between"><span>Tareas entregadas:</span> <strong>${st.vars.tareas}</strong></li>
                <li class="flex justify-between"><span>Participación:</span> <strong>${st.vars.participacion}</strong></li>
                <li class="flex justify-between"><span>Tiempo en plataforma:</span> <strong>${st.vars.tiempo}</strong></li>
                <li class="flex justify-between"><span>Puntualidad:</span> <strong>${st.vars.puntualidad}</strong></li>
                <li class="flex justify-between"><span>Consultas al docente:</span> <strong>${st.vars.consultas}</strong></li>
                <li class="flex justify-between"><span>Uso de recursos:</span> <strong>${st.vars.recursos}</strong></li>
            `;

            let interp = "";
            if (st.x > 0 && st.y > 0) interp = "Este punto aparece en la zona superior derecha porque tiene alto nivel de interacción y alto cumplimiento. La IA lo agrupa con perfiles similares.";
            else if (st.x < 0 && st.y > 0) interp = "Este punto aparece en la zona superior izquierda porque cumple con tareas/asistencia, pero su interacción es baja.";
            else if (st.x > 0 && st.y < 0) interp = "Este punto aparece en la zona inferior derecha porque interactúa mucho, pero su cumplimiento normativo (tareas/asistencia) es bajo.";
            else interp = "Este punto aparece en la zona inferior izquierda porque tiene bajo nivel de interacción y bajo nivel de cumplimiento. La IA no está prediciendo que el estudiante desaprobará, solo lo ubica cerca de estudiantes similares.";

            document.getElementById('st-interpretation').innerText = `Interpretación: "${interp}"`;
            
            document.getElementById('student-panel').classList.remove('hidden');
        }

        function closeStudentPanel() {
            document.getElementById('student-panel').classList.add('hidden');
        }

        


        // Asignación segura de eventos
        document.addEventListener('DOMContentLoaded', () => {
            const bindEvent = (id, fn) => {
                const el = document.getElementById(id);
                if (el) el.addEventListener('click', fn);
            };

            bindEvent('btn-init-sim', () => initExperience('sim'));
            bindEvent('btn-init-ar', () => requestAR());
            bindEvent('btn-toggle-ar', () => requestAR());
            bindEvent('btn-prev', () => prevModule());
            bindEvent('btn-next', () => nextModule());
            bindEvent('btn-close-student', () => closeStudentPanel());
            bindEvent('btn-show-clusters', () => toggleClusters(true));
            bindEvent('btn-hide-clusters', () => toggleClusters(false));
            });
    
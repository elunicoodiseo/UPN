import sys
import re

filepath = r'd:\Proyectos\Arquitectura-Semana 5\UPN\UPN\S3\ai_evaluacion\ai_evaluacion.html'
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError:
    with open(filepath, 'r', encoding='utf-16') as f:
        content = f.read()

start_marker = "<!-- 4. MagicSchool AI -->"
end_marker = "<!-- 5. Gradescope -->"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print("Markers not found")
    sys.exit()

replacement = """<!-- 4. Gradescope — Feedback Estructurado -->
                <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-lg flex flex-col justify-between mb-8">
                    <div>
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-xl font-bold text-gray-800"><i
                                    class="fa-solid fa-check-double text-blue-700 mr-2"></i>Gradescope — Feedback</h3>
                            <span
                                class="text-xs font-bold bg-blue-100 text-blue-800 px-3 py-1 rounded-full border border-blue-200">Feedback
                                Estructurado</span>
                        </div>

                        <!-- Panel de Explicación Visible -->
                        <div
                            class="bg-blue-50 p-4 rounded-lg border border-blue-200 mb-4 text-sm text-gray-800 space-y-2">
                            <h4 class="font-bold text-blue-900 border-b border-blue-200 pb-1 mb-2"><i
                                    class="fa-solid fa-circle-info mr-1"></i> Explicación Pedagógica</h4>
                            <p><strong>Para qué sirve:</strong> Generar comentarios formativos sobre el informe entregado, vinculados a una rúbrica de evaluación.</p>
                            <p><strong>Uso docente:</strong> Calificar y comentar el trabajo real del estudiante de forma más rápida y consistente entre secciones.</p>
                            <p><strong>Resultado esperado:</strong> Informe devuelto con observaciones específicas por criterio (claridad, evidencias, viabilidad).</p>
                            <p class="text-red-700"><strong>Riesgo:</strong> Estandarizar el comentario y perder matices del trabajo individual del estudiante.</p>
                            <p class="text-green-700"><strong>Cuidado ético:</strong> El docente revisa y ajusta cada comentario antes de enviarlo; la IA no entrega la nota final.</p>
                            <p
                                class="mt-2 pt-2 border-t border-blue-200 text-blue-600 font-bold text-xs uppercase tracking-wider">
                                <a href="https://www.gradescope.com/" target="_blank"
                                    class="hover:underline flex items-center"><i
                                        class="fa-solid fa-arrow-up-right-from-square mr-1"></i> Visitar sitio
                                    oficial</a></p>
                        </div>

                        <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
                            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block">Simulación
                                Práctica</span>
                            <div class="bg-white p-3 rounded border border-gray-200 mb-2">
                                <span class="text-[10px] font-bold text-gray-500 uppercase">Texto del estudiante</span>
                                <p class="text-xs text-gray-800 mt-1 italic">"Se propone mejorar la gestión educativa usando tecnología para que los docentes trabajen mejor... Esta propuesta es importante porque existen problemas."</p>
                            </div>
                            <div class="bg-blue-50 p-3 rounded border border-blue-100 mb-3">
                                <span class="text-[10px] font-bold text-blue-500 uppercase">Prompt del docente</span>
                                <p class="text-xs text-gray-800 mt-1 font-medium italic">"Revisa este informe entregado usando la rúbrica (Claridad, Evidencias, Viabilidad). No coloques nota. Entrega: 1. Fortalezas, 2. Por mejorar, 3. Recomendaciones."</p>
                            </div>
                            <button onclick="simulateMagicSchool()"
                                class="w-full bg-blue-700 text-white px-5 py-2 rounded font-semibold hover:bg-blue-800 transition shadow flex items-center justify-center">
                                <i class="fa-solid fa-bolt mr-2"></i> Generar feedback sobre el informe
                            </button>
                            <div id="magicschool-feedback"
                                class="mt-4 hidden overflow-hidden rounded border border-gray-300 shadow-sm">
                                <div class="bg-white p-4 text-sm">
                                    <h5 class="font-bold text-blue-700 mb-1">1. Fortalezas</h5>
                                    <p class="text-gray-700 mb-2">Identifica correctamente el uso de tecnología en gestión educativa como eje de mejora.</p>
                                    <h5 class="font-bold text-blue-700 mb-1">2. Por mejorar</h5>
                                    <p class="text-gray-700 mb-2">Falta de evidencias concretas. ¿Cuáles son los problemas exactos? ¿Cómo trabajan mejor los docentes?</p>
                                    <h5 class="font-bold text-blue-700 mb-1">3. Recomendaciones</h5>
                                    <p class="text-gray-700">Incluye datos cuantitativos o citas que respalden la existencia de los "problemas" mencionados.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                """

content = content[:idx_start] + replacement + content[idx_end:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated successfully")

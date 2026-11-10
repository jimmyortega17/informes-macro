# Instrucciones permanentes (MBA CENTRUM PUCP, curso de Macroeconomía, prof. Sergio Julio Chión Chacón)

**Idioma: responde SIEMPRE en español**, tanto en el chat como en los commits y en los documentos.

## ¿Qué tipo de trabajo es?

- **Informe macroeconómico de UNA EMPRESA** (por ejemplo, Universidad Científica del Sur, Ferreycorp, Saga Falabella): sigue `INSTRUCCIONES_INFORME_EMPRESA.md` y NO las reglas de ensayo de abajo, salvo las de estilo (sin narración, sin Phillips ni isopérdida, cifras verificadas, versionado).
- **Ensayo colaborativo sobre la economía peruana** basado en el Reporte de Inflación: sigue las reglas de este archivo.

# Reglas del ensayo macroeconómico (economía peruana)

## Documento de referencia (obligatorio)

`plantillas/ensayo_macro_referencia.docx` es el modelo aprobado. Antes de escribir, ábrelo y léelo completo. Cada nuevo ensayo debe tener la MISMA estructura, estilo, profundidad y formato. Solo cambian el periodo, el Reporte de Inflación (RI) base, las cifras y las fuentes. Redacta con palabras nuevas (cero plagio frente a la referencia o a versiones anteriores).

## Estilo de redacción (lo más importante)

- PROHIBIDO narrar lo que el documento va a hacer: nada de "este ensayo", "este trabajo busca", "a continuación", "en esta sección", "se procede", "primero/segundo/tercero", "pregunta guía", "tesis central", "alcance y criterios de lectura".
- Estilo de informe técnico: cada párrafo empieza con el DATO o la AFIRMACIÓN, luego la causa y después la consecuencia. Párrafos de 3 a 5 líneas.
- Cada cifra lleva su fuente y fecha: (BCRP, 2026b), (INEI, citado por …), (BCRPData).
- Usa "→" dentro del párrafo para la consecuencia: "… → El origen es de oferta, no de demanda."
- Cadenas de razonamiento en línea aparte, en negrita, con flechas ↑ ↓ → en 16 pt e incluyendo la elasticidad cuando aplique:
  "↑ El Niño → ↓ oferta de pescado (−17,33 %) → demanda inelástica (ε = −0,59) → ↑ precio → ↑ inflación"
- Razonamiento crítico: rótulo "Razonamiento crítico:" y el párrafo completo en negrita NEGRA.
- Razonamiento estratégico: rótulo "Razonamiento estratégico:" y el párrafo completo en negrita ROJA (C00000).
- Al menos un razonamiento (crítico o estratégico) por sección, y los dos en las conclusiones.
- Las 4 variables de orientación siempre interconectadas: PBI, inflación, tasa de referencia y tipo de cambio.
- Sin viñetas en el resumen ejecutivo, el análisis ni las conclusiones: todo en prosa.
- Incluye un análisis costo-beneficio de la recomendación de política (por ejemplo, del alza o recorte de tasa).

## Lo que NO se incluye

- NO usar la curva de Phillips (ni ecuación, ni gráfico, ni descomposición). Es demasiado compleja.
- NO usar curvas de isopérdida ni funciones de pérdida del banco central.
- NO dejar placeholders entre corchetes, salvo los nombres de los integrantes en la carátula.
- NO escribir "Elaboración propia" ni "Gráfico generado en Python" en las notas.

## Estructura obligatoria

1. Carátula: Pontificia Universidad Católica del Perú / Escuela de Posgrado / MBA / curso / título / Integrantes del grupo / Profesor / Lima, mes y año. Nunca "CENTRUM PUCP Business School".
2. Declaración de Uso de Inteligencia Artificial (la exige el sílabo; su ausencia baja mucho la nota): Tabla 1 con herramienta, modalidad, rubros y temas específicos, y luego la declaración de originalidad en prosa (el uso de IA no afectó la interpretación, el análisis ni las conclusiones).
3. Cap. 1 Situación macroeconómica y modelo de análisis:
   - 1.1 Resumen ejecutivo en prosa: un párrafo de diagnóstico y uno por cada variable (dato del RI → último dato → hacia dónde va), con una cadena y un razonamiento estratégico.
   - 1.2 Qué cambió entre el RI anterior y el actual (tabla + gráfico + interpretación).
   - 1.3 Lectura encadenada de los incisos del Resumen del RI: un párrafo por vínculo (i)→(ii)→…, con el dato del RI, el dato actualizado y por qué empuja al siguiente inciso. Cierra con un razonamiento crítico.
   - 1.4 Modelo de análisis: identidad del gasto Y = C + I + G + (X − M) (debe cuadrar con el PBI oficial), elasticidades de demanda (fórmula ε = %ΔQ / %ΔP y tabla de 5-6 elasticidades: calculadas con cifras reales cuando se pueda y marcadas como "supuesto del grupo" cuando no), regla de Taylor con suavizamiento, paridad descubierta de tasas (UIP) y ecuación de Fisher. Después de CADA ecuación va un párrafo que diga qué significa ese número para el banco central.
4. Entorno internacional (crecimiento mundial, Fed, China y commodities).
5. Choque de oferta, inflación y tasa (canal de costos, aritmética del cierre del año).
6. Términos de intercambio, PBI y tipo de cambio (calidad del crecimiento, contribuciones al PBI, isocuantas de producción).
7. Tasa real, crédito y modelo IS-MP.
8. El nudo cambiario (mercado de divisas, Mundell-Fleming, reservas, traspaso).
9. Síntesis: matriz de transmisión, determinantes, diagramas de Ishikawa por variable, y la sección "Análisis por variable: elasticidades y cadenas de transmisión", con una subsección para cada una de las 4 variables (cifras, cadena con elasticidad, cálculo de sensibilidad y razonamiento).
10. Escenarios base, favorable y adverso con probabilidades y valores de las 4 variables para el año actual y el siguiente, más una tabla de señales tempranas.
11. Resumen integrado y perspectivas de las 4 variables (tabla y un párrafo por variable).
12. Conclusiones en prosa (no viñetas), con un razonamiento crítico y uno estratégico.
13. Recomendaciones por actor (BCRP, MEF, empresas, exportadores).
14. Cadenas de razonamiento de cierre (una por variable).
15. Referencias en APA 7 (solo las fuentes citadas en el texto).

## Cifras

- Usa siempre el RI vigente del BCRP y los datos más recientes: inflación del INEI del último mes, Programa Monetario del BCRP, BCRPData (tipo de cambio, RIN, crédito, expectativas), PBI mensual del INEI y decisiones de la Fed.
- Busca cada cifra en bcrp.gob.pe, estadisticas.bcrp.gob.pe, inei.gob.pe o federalreserve.gov. No inventes cifras. Si una cifra no está publicada a la fecha de corte, dilo y usa indicadores adelantados.
- Una sola cifra por concepto en todo el documento (por ejemplo, un solo valor de expectativas de inflación, con su mes), y todo lo que dependa de ella debe ser coherente (tasa real, Taylor, etc.).
- Comprueba toda la aritmética (sumas de la identidad, Taylor, cocientes de elasticidades, escenarios) con código antes de escribirla.

## Gráficos

- Hechos en Python con datos reales de BCRPData/INEI cuando existan; los diagramas conceptuales se señalan como tales en la nota.
- Incluye: las cadenas causales como diagramas, un Ishikawa por variable, IS-MP, mercado de divisas (oferta-demanda de dólares), Mundell-Fleming, isocuantas de producción, tasa real ex ante/ex post y escenarios.

## Formato Word

- Times New Roman 12, todo en negro salvo el razonamiento estratégico en rojo. Texto alineado a la izquierda (sin justificar).
- Tablas APA 7: tres líneas horizontales, sin relleno ni color, letra 9, encabezados de columna sin negrita.
- "Tabla N" / "Figura N" en negrita y el título en cursiva, en mayúsculas y minúsculas. Numeración consecutiva sin saltos.
- Notas: "Nota." en cursiva + "Adaptado de [fuente]".
- Número de página arriba a la derecha.

## Versiones

- Cada corrección sube el número de versión en el nombre del archivo (V1, V2, V3…); nunca sobrescribas la versión anterior.
- Si el usuario pide corregir una parte, toca SOLO esa parte y confirma que el resto quedó idéntico.

## Verificación antes de entregar

1. Convierte el .docx a PDF y revisa visualmente cada página.
2. Busca en el texto las frases prohibidas de narración, "Elaboración propia", "Phillips" e "isopérdida": no debe aparecer ninguna.
3. Confirma que estén la carátula, la declaración de IA, todas las secciones y los razonamientos con el color correcto, que los gráficos se vean y que la numeración de tablas y figuras sea consecutiva.
4. Haz commit y push.

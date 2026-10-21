# TEAM International × tempo.io - Senior Frontend Developer (Growth)
## Análisis fiscal: cuánto valen realmente USD 5.000/mes brutos en Argentina (contractor)

**Fecha del análisis:** 21 de octubre de 2026
**Modalidad asumida:** contractor full-time, facturando desde Argentina a un cliente del exterior (EE.UU.), sin relación de dependencia.
**Régimen asumido:** Monotributo, categoría determinada por facturación anual.

> **Nota de método:** todos los montos que cambian en el tiempo fueron abiertos contra la fuente oficial el 21/10/2026. Lo que no pude verificar está listado en la sección INCERTIDUMBRE y **no** fue rellenado con estimaciones presentadas como datos.

---

## 1. Tipo de cambio

| Dato | Valor | Fecha del dato | Fuente |
|---|---|---|---|
| Dólar minorista (promedio vendedor) | **ARS 1.545,01** | 20/10/2026 | BCRA, API Estadísticas v4.0, variable 4 `Tipo de cambio minorista (promedio vendedor)` |
| Dólar mayorista de referencia | **ARS 1.524,8401** | 20/10/2026 | BCRA, API Estadísticas v4.0, variable 5 `Tipo de cambio mayorista de referencia` |

- Fuente: `https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/4` y `/5` (consultadas 21/10/2026 12:50 ART).
- La API v3.0 está deprecada (devuelve HTTP 410); la v4.0 es la vigente.
- **Criterio usado en la tabla principal: minorista 1.545,01.** Es el tipo de cambio que se acerca más a lo que efectivamente se recibe al liquidar dólares en una cuenta local. El mayorista se usa solo como sensibilidad.

**Conversión de la oferta:**
- USD 5.000/mes × 1.545,01 = **ARS 7.725.050/mes**
- USD 60.000/año × 1.545,01 = **ARS 92.700.600/año**

---

## 2. Monotributo: categoría y cuota

### 2.1. ¿La tabla de ARCA ya incluye el ajuste del 16,8%?

**Sí. Verificado, no asumido.** La página de ARCA publica "Valores de aplicación desde el 1/08/2026". Comparé esa tabla contra el PDF oficial del período anterior (01/02/2026 al 31/07/2026):

| Categoría A | Monto | Fuente |
|---|---|---|
| Tope de ingresos brutos, feb-jul 2026 | ARS 10.277.988,13 | PDF ARCA `monotributo-categorias-febrero-julio-2026.pdf` |
| Tope de ingresos brutos, desde 01/08/2026 | ARS 12.009.410,45 | `arca.gob.ar/monotributo/categorias.asp` |

12.009.410,45 / 10.277.988,13 = **1,1684 → +16,84%**.

Además, los valores de octubre que publica Ámbito (15/10/2026) coinciden **exactamente** con la tabla de ARCA desde 01/08/2026 (A $49.527,18; B $56.379,08; … K $1.614.446,04). Conclusión: **la tabla de arca.gob.ar ya está ajustada y es la que rige los pagos de octubre 2026. No hay que aplicar ningún factor extra.** Aplicar un 16,8% adicional sería un error de doble conteo.

### 2.2. Categoría que corresponde

Con ARS 92.700.600 anuales, corresponde la **categoría J** (tope J = ARS 105.012.519,20; tope I = ARS 91.699.761,90). Queda dentro del régimen: el tope máximo de servicios (K) es ARS 126.610.838,75.

> **Aclaración sobre un dato que suele confundirse:** en el HTML de ARCA la columna "Actividad" está comentada (código legacy) y la tabla lista "Venta de Bs. muebles" en las filas I, J y K. Eso **no** significa que un prestador de servicios no pueda estar en J o K: la propia página de ARCA de exportación de servicios dice que los monotributistas pueden exportar servicios "sin superar los límites de facturación de la categoría máxima correspondiente a su actividad", y la columna de cuota de servicios existe hasta K. **Un prestador de servicios de software puede y debe usar la columna "Locaciones y prestaciones de servicios".**

### 2.3. Composición de la cuota - Categoría J (servicios)

| Componente | ARS/mes | USD/mes (@1.545,01) | % del bruto |
|---|---|---|---|
| Impuesto integrado | 977.510,14 | 632,69 | 12,65% |
| Aportes al SIPA (jubilación) | 112.892,16 | 73,07 | 1,46% |
| Aportes obra social | 76.897,46 | 49,77 | 1,00% |
| **Total cuota J (servicios)** | **1.167.299,76** | **755,53** | **15,11%** |

Fuente: `https://arca.gob.ar/monotributo/categorias.asp`, valores desde 01/08/2026 (abierta 21/10/2026).

**Lectura importante:** a esta altura del régimen, el 84% de la cuota es **impuesto integrado**, no aportes. El monotributo deja de ser "barato" en las categorías altas: la cuota se lleva 15,11% del bruto, muy por encima del ~5% que se paga en categorías bajas.

### 2.4. Riesgo de categoría: es un borde, no un centro

| Umbral | FX de equilibrio (USD 60.000/año) | Situación |
|---|---|---|
| Salir de I → entrar en J | ARS 1.528,33 | Ya superado (estamos en J) |
| Salir de J → entrar en K | ARS 1.750,21 | +13,3% de devaluación |
| Salir del monotributo (tope K) | ARS 2.110,18 | +36,6% de devaluación |

Detalle no menor: con el **mayorista** (1.524,84) la facturación anualizada da ARS 91.490.406, que cae **por debajo** del tope de I (91.699.761,90) y daría categoría **I** (cuota ARS 963.747,86 = USD 623,78). La categoría cambia según qué tipo de cambio se use para valuar la facturación. En la práctica ARCA toma la conversión de cada factura E, así que la posición real queda entre I y J.

---

## 3. Costos que la oferta NO cubre

### 3.1. ART - corrección de una premisa del brief

**El brief asume que un contractor monotributista paga "cuota fija de ART + ~3% sobre la masa de Wage Segurables". Eso no aplica a este caso y hay que decirlo con claridad.**

Verificado: la Ley 24.557 (art. 3) obliga a afiliarse a una ART al **empleador que tiene trabajadores en relación de dependencia**. Un monotributista que trabaja solo no es empleado de nadie y **no tiene un trámite estándar para afiliarse a una ART para cubrirse a sí mismo**. La obligación nace recién cuando contrata su primer empleado, y en ese caso la ART cubre al empleado, no al titular.
Fuente: `https://aylingseguros.com.ar/blog/un-monotributista-necesita-art-que-dice-la-ley-en-2026` (abierta 21/10/2026). Ver INCERTIDUMBRE: es una fuente secundaria de un productor de seguros, no el texto de la ley.

**Consecuencia para el cálculo:** **ART = ARS 0.** El "3% sobre masa salarial" no existe para un contratista individual: no hay masa salarial porque no hay sueldos.

**Lo que sí existe como costo opcional:** seguro de **accidentes personales**, que no es ART ni la reemplaza. Referencia de mercado: La Caja, Plan A, **ARS 9.124/mes** (`https://seguros.lacaja.com.ar/personas-seguro-de-accidentes-personales`, consultada 21/10/2026). Lo incluyo en el cálculo como costo prudente, marcado como opcional.

**Riesgo real que esto deja abierto:** si te lesionás, no hay ART que responda. Un contractor sin cobertura de accidentes personales asume el riesgo completo. Esto es un costo económico aunque no sea una factura.

### 3.2. Salud: el aporte de obra social no alcanza para una prepaga

- Aporte de obra social incluido en la cuota J: **ARS 76.897,46/mes**.
- Prepagas económicas en CABA (30-60 años, contratación particular, octubre 2026): **desde ~ARS 77.000 (Mundo Médico Flex) hasta ~ARS 189.000-416.000** para planes tipo Premedic 400. Planes intermedios desde ~ARS 263.000 (Galeno Azul 200) y ~ARS 290.000-471.000 (OSDE 210).
  Fuente: `https://www.comparaprepagas.com/blog/precio-de-las-prepagas` (cuadros tarifarios SSSalud, Res. 645/2025; actualizado 07/10/2026).
- **Faltante estimado:** con un plan económico el aporte casi cubre la cuota (faltante ≈ ARS 0-30.000). Con un plan intermedio (OSDE 210) el faltante es de **~ARS 185.000-215.000/mes** (≈ USD 120-140).
- Dato útil: los monotributistas pueden **derivar los aportes a la prepaga y pagar solo la diferencia**, y esos planes no llevan IVA (misma fuente).

En el cálculo principal asumo el plan económico (faltante ≈ 0) y lo expongo como supuesto.

### 3.3. Contador

- Abono de mercado para monotributista: **desde ARS 60.000/mes** (septiembre 2026). Recategorización: mínimo sugerido CPCE CABA ARS 92.520 (baja complejidad), dos veces por año.
- Un caso con **cliente del exterior, Factura E y cobros en otra moneda** es explícitamente listado como factor que encarece el servicio.
- Fuente: `https://lannis.app/blog/cuanto-cobra-un-contador-monotributista` (actualizado octubre 2026).
- **Supuesto usado: ARS 75.000/mes** (por encima del piso de mercado, por la complejidad de Factura E).

### 3.4. Costo de transferencia / cobro internacional

**No verificado.** No encontré una fuente oficial con la comisión exacta del canal que usaría TEAM ni del banco/billetera receptora. **Supuesto: 1,0% del bruto** (USD 50/mes), consistente con billeteras tipo Wise para recibir USD y convertir a ARS. Está en SUPUESTOS y en INCERTIDUMBRE.

También puede haber costo de **certificación de ingresos del exterior** si el banco la exige para justificar fondos: no verificado, no cuantificado.

---

## 4. Facturación al cliente del exterior

### 4.1. Comprobante: Factura E, no Factura C

Verificado en dos páginas de ARCA:
- "Deberán emitir comprobantes tipo 'C', **a excepción de que se trate de una operación de exportación, en cuyo caso corresponderá emitir comprobantes tipo 'E'**." - `https://www.afip.gob.ar/facturacion/monotributo/comprobantes.asp`
- "Las operaciones de exportación deben respaldarse mediante la emisión de una **factura tipo 'E'**, que puede hacerse tanto en moneda extranjera como en pesos, considerando el tipo de cambio comprador del Banco Nación al día anterior al de la emisión." - `https://www.arca.gob.ar/monotributo/exportacion-servicios/`

**Implicancias prácticas:**
1. Hay que **habilitar un punto de venta** específico para "Comprobantes de exportación - Comprobante en línea" antes de facturar.
2. Se factura con el **CUIT del país de destino** en el campo del prestatario (ARCA publica tabla de CUIT por país).
3. La factura **puede emitirse en USD**. No es obligatorio pesificar la factura; sí hay que valúa al tipo de cambio comprador del BNA del día anterior.
4. Es un **trámite distinto** al de Factura C y requiere configuración previa: no se resuelve el primer día.

### 4.2. Derechos de exportación de servicios

Verificado en ARCA: sobre las exportaciones de servicios recae el **Derecho de exportación**, pero **los monotributistas inscriptos en el Registro MiPyME con certificado vigente están exentos**. Además, los monotributistas no están obligados a inscribirse en el Registro de exportadores.
Fuente: `https://www.arca.gob.ar/monotributo/exportacion-servicios/`

**Acción concreta:** tramitar el **certificado MiPyME** antes/ni bien se empieza a facturar. Sin ese certificado, el derecho de exportación es un costo que la oferta no cubre.

### 4.3. La retención del 10%: NO verificada

**No pude confirmar la vigencia ni la aplicación de una retención del 10% sobre exportación de servicios a un monotributista.** La página de ARCA sobre exportación de servicios para monotributistas **no menciona ninguna retención**; solo habla de derechos de exportación y de la exención MiPyME. Las búsquedas sobre RG 2286/2007 no devolvieron una fuente que pueda abrir y citar con el porcentaje vigente para este caso.

**No invento el dato.** Lo dejo como incertidumbre explícita y **no lo descuento** del cálculo. Si existiera una retención del 10%, el impacto sería de USD ~500/mes brutos (o un crédito fiscal recuperable, según el caso), lo que movería el neto de forma material. **Es el punto que hay que preguntar al contador antes de aceptar.**

### 4.4. Moneda y forma de pago de TEAM

**No verificado.** La oferta dice USD 5.000 brutos, pero no tengo confirmación de si TEAM paga en USD a una cuenta argentina, a una cuenta en el exterior, o vía plataforma con conversión obligatoria. Eso cambia el costo de transferencia y la exposición al spread cambiario.

### 4.5. Reembolso de benefits en la misma invoice

La oferta describe los benefits como **reembolso contra factura** (el contractor elige aseguradora y TEAM le reembolsa). Si ese reembolso se suma a la invoice mensual:
- **Aumenta la base facturada** y por lo tanto **cuenta como ingreso bruto** para el monotributo → puede empujar de categoría.
- Mezcla un **reembolso de gastos** con una **prestación de servicios** en el mismo comprobante de exportación, lo que complica la trazabilidad ante ARCA.
- **Recomendación:** mantener el reembolso como **documento separado** (nota de crédito / rendición de gastos) en lugar de inflar la Factura E.

---

## 5. Cálculo del neto

### 5.1. Tabla principal - Categoría J (servicios), FX 1.545,01

| Concepto | ARS/mes | USD/mes |
|---|---|---|
| **Bruto oferta** | 7.725.050,00 | **5.000,00** |
| (−) Monotributo - impuesto integrado | 977.510,14 | 632,69 |
| (−) Monotributo - aportes SIPA | 112.892,16 | 73,07 |
| (−) Monotributo - obra social | 76.897,46 | 49,77 |
| **Subtotal monotributo** | **1.167.299,76** | **755,53** |
| (−) ART | 0,00 | **0,00** |
| (−) Seguro accidentes personales (opcional) | 9.124,00 | 5,91 |
| (−) Contador | 75.000,00 | 48,54 |
| (−) Costo de transferencia (1%) | 77.250,50 | 50,00 |
| **NETO EN MANOS** | **6.396.376,00** | **≈ 4.140** |

**Neto por hora** (160 h/mes): **USD 25,88/h**
**Tasa efectiva de descuento sobre el bruto: 17,2%**

### 5.2. Escenario alternativo - Categoría I (si ARCA valúa con mayorista)

| Concepto | ARS/mes | USD/mes |
|---|---|---|
| Bruto | 7.725.050,00 | 5.000,00 |
| (−) Monotributo total (I: 814.591,79 + 80.637,26 + 68.518,81) | 963.747,86 | 623,78 |
| (−) ART | 0,00 | 0,00 |
| (−) Accidentes personales | 9.124,00 | 5,91 |
| (−) Contador | 75.000,00 | 48,54 |
| (−) Transferencia (1%) | 77.250,50 | 50,00 |
| **NETO EN MANOS** | **6.599.928,00** | **≈ 4.272** |

**Neto por hora: USD 26,70/h**

### 5.3. Sensibilidad al tipo de cambio

| Escenario FX | Facturación anual ARS | Categoría | Neto USD/mes | Neto USD/h |
|---|---|---|---|---|
| 1.390,51 (−10%) | 83.430.600 | I | ≈ 4.196 | 26,23 |
| **1.545,01 (base)** | **92.700.600** | **J** | **≈ 4.140** | **25,88** |
| 1.699,51 (+10%) | 101.970.600 | J | ≈ 4.214 | 26,34 |
| 2.110,18 (+36,6%) | 126.610.800 | K (borde) | ≈ 4.145 | 25,91 |
| > 2.110,18 | > tope K | **Exclusión → Régimen General** | cae fuerte | - |

Hallazgo relevante: **el neto en USD es notablemente estable frente al FX** (±10% de tipo de cambio mueve el neto menos de 2%), porque la cuota del monotributo está fijada en pesos y se licúa con la devaluación. El riesgo real no es la erosión gradual: es **cruzar el tope de la categoría K y quedar excluido del régimen**.

### 5.4. El costo silencioso: PTO y licencias

La oferta promete 20 días de PTO el primer año, pero como **contractor facturás por lo que trabajás**. Si esos días no se pagan, el ingreso anual real no es USD 60.000 sino aproximadamente:

USD 60.000 − (USD 5.000 × 20/21 días hábiles) ≈ **USD 55.238/año**

Eso reduce el neto mensual equivalente a **≈ USD 3.810** (−8%). Lo mismo aplica a los 5 días por fallecimiento y a las 2 semanas por enfermedad grave: son **días sin factura**, no beneficios pagos.

**Esto no está confirmado:** depende de si TEAM paga el PTO a contractors o no. Ver INCERTIDUMBRE. **Si no lo paga, es el recorte más grande de toda la oferta y no aparece en ningún lado del contrato.**

---

## 6. Comparación con las referencias de Gonzo

Supuesto común: 160 h/mes. USD 5.000/mes = **USD 31,25/h brutos**.

| Referencia | Bruto USD/h | Bruto USD/mes | Neto estimado USD/h | Neto USD/mes |
|---|---|---|---|---|
| **Infjini** (22/h all-inclusive) | 22,00 | 3.520 | ~22,00 (si all-inclusive no tiene costos extra) | ~3.520 |
| **TEAM / tempo.io** | **31,25** | **5.000** | **25,88 - 26,70** | **4.140 - 4.272** |
| **Staffy** (30-35/h) | 30,00 - 35,00 | 4.800 - 5.600 | ~26 - 30 | ~4.200 - 4.800 |

**Lecturas:**
- **Contra Infjini:** TEAM está **+42% en bruto** y **+18% a +21% en neto**. Ganador claro.
- **Contra Staffy:** TEAM (31,25/h bruto) cae **dentro del rango** de Staffy (30-35), en la parte media-baja. En neto, TEAM (~25,9-26,7) queda en el **borde inferior** del rango neto de Staffy (~26-30). **Es un empate técnico, no una mejora.**
- **El punto que casi nadie calcula:** TEAM paga **USD 5.000 fijos por mes**, no por hora. Si el puesto "Senior Frontend (Growth)" termina demandando 45-50 h/semana -habitual en equipos de growth con cliente único- el valor/hora real cae a **USD 25-27 brutos** y **USD 21-22 netos**, es decir **por debajo de Infjini**. El riesgo no está en la tarifa: está en las horas no declaradas.

---

## 7. INCERTIDUMBRE

Lo que **no** pude verificar y por qué:

1. **Retención del 10% sobre exportación de servicios.** No encontré fuente abrible que confirme vigencia ni aplicabilidad a monotributistas. La página oficial de ARCA para monotributistas no la menciona. **No la desconté.** Impacto potencial: ~USD 500/mes. *Pregunta obligatoria al contador.*
2. **Moneda y canal de pago de TEAM.** No confirmado si paga en USD a cuenta argentina, cuenta exterior, o vía plataforma con conversión. El costo de transferencia del 1% es un supuesto, no un dato.
3. **Si TEAM paga el PTO a contractors.** Es la variable de mayor impacto no resuelta (±8% del neto anual). El texto de la oferta habla de "PTO 20 días" sin aclarar si es pago o no.
4. **ART - fuente secundaria.** La conclusión de que un monotributista individual no puede/no debe afiliarse a una ART proviene de un blog de productor de seguros, no del texto de la Ley 24.557 ni de la SRT. Es consistente con el diseño del sistema (la ART cubre el vínculo empleador-empleado) y con la ausencia de un trámite estándar, pero conviene confirmarlo con un contador.
5. **Categoría exacta (I vs J).** Depende del tipo de cambio con el que ARCA valore cada Factura E. Con minorista da J; con mayorista da I. Diferencia: ~USD 132/mes.
6. **Prepaga concreta.** Asumí plan económico (faltante ≈ 0). Si Gonzo quiere OSDE 210, el neto baja ~USD 120-140/mes.
7. **Ajuste del 16,8%.** Verificado que la tabla vigente ya lo incluye (comparación contra el PDF feb-jul 2026), pero la página de ARCA **no dice explícitamente** "ajuste 16,8%": la coincidencia es aritmética y contra la nota de Ámbito del 15/10/2026.
8. **Ingresos Brutos.** No evaluado. Convenio Multilateral puede aplicar según jurisdicción; para exportación de servicios suele haber exención, pero **no lo verifiqué**.
9. **Escenario de exclusión del monotributo.** Si el FX supera ~2.110, el cálculo cambia a Régimen General (autónomo categoría máxima ARS 939.240,20/mes según PDF ARCA oct-2026 + Ganancias + IVA). **No desarrollé ese escenario en profundidad** porque requiere la escala de Ganancias 2026 completa, que no abrí.

---

## 8. SUPUESTOS

1. **Contractor individual**, sin empleados, sin sociedad. Monotributo categoría J (servicios de software/IT).
2. **Tipo de cambio minorista BCRA 1.545,01** del 20/10/2026, sostenido durante todo el período.
3. **160 h/mes** para la conversión a valor hora.
4. **Sin ART** (no aplica legalmente a un monotributista sin empleados). Se incluye seguro de accidentes personales de ARS 9.124/mes como costo prudente.
5. **Prepaga económica** con derivación de aportes de obra social → faltante ≈ ARS 0. Si se elige un plan intermedio, restar USD 120-140/mes.
6. **Contador ARS 75.000/mes**, por encima del piso de mercado de ARS 60.000 por la complejidad de Factura E.
7. **Costo de transferencia 1,0%** del bruto (USD 50/mes). Supuesto no verificado.
8. **Sin retención del 10%** aplicada (no verificada). Si aplica, restar ~USD 500/mes o computarla como crédito fiscal.
9. **PTO pagado.** Si no lo está, restar ~8% (neto ≈ USD 3.810).
10. **Sin aportes a jubilación adicionales** más allá del SIPA del monotributo, y **sin inversión** de excedentes.
11. **Certificado MiPyME vigente** → derechos de exportación de servicios = 0.
12. **Sin Ingresos Brutos** (no evaluado).

---

## 9. VEREDICTO

> **USD 5.000/mes brutos de TEAM son ≈ USD 4.140 - 4.270 netos por mes (≈ USD 25,9 - 26,7/h), lo que supera claramente a Infjini (USD 22/h) pero empata -sin mejorar- el rango de Staffy (USD 30-35/h), y cae a ≈ USD 3.810/mes si el PTO no se paga.**

---

## 10. Fuentes

| # | Fuente | URL | Fecha de consulta |
|---|---|---|---|
| 1 | BCRA - Tipo de cambio minorista (var. 4) | `https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/4` | 21/10/2026 |
| 2 | BCRA - Tipo de cambio mayorista (var. 5) | `https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/5` | 21/10/2026 |
| 3 | ARCA - Montos y categorías vigentes (desde 01/08/2026) | `https://arca.gob.ar/monotributo/categorias.asp` | 21/10/2026 |
| 4 | ARCA - Cuadro de categorías feb-jul 2026 (PDF, para verificar el ajuste) | `https://www.afip.gob.ar/monotributo/documentos/categorias/monotributo-categorias-febrero-julio-2026.pdf` | 21/10/2026 |
| 5 | Ámbito - Ajuste 16,8% monotributo octubre 2026 | `https://www.ambito.com/informacion-general/ajuste-el-monotributo-la-suba-del-168-que-aplica-arca-octubre-y-que-pasa-si-superas-los-topes-n6333461` | 21/10/2026 (publicado 15/10/2026) |
| 6 | ARCA - Exportación de servicios (Monotributo) | `https://www.arca.gob.ar/monotributo/exportacion-servicios/` | 21/10/2026 |
| 7 | ARCA - Comprobantes del monotributista (C vs E) | `https://www.afip.gob.ar/facturacion/monotributo/comprobantes.asp` | 21/10/2026 |
| 8 | ARCA - Valores autónomos desde octubre 2026 (PDF escenario exclusión) | `https://www.arca.gob.ar/autonomos/documentos/Valores-autonomos-desde-octubre-2026.pdf` | 21/10/2026 |
| 9 | Ayling Seguros - ¿Un monotributista necesita ART? (fuente secundaria) | `https://aylingseguros.com.ar/blog/un-monotributista-necesita-art-que-dice-la-ley-en-2026` | 21/10/2026 |
| 10 | La Caja - Seguro de Accidentes Personales (precio) | `https://seguros.lacaja.com.ar/personas-seguro-de-accidentes-personales` | 21/10/2026 |
| 11 | Compara Prepagas - Precios octubre 2026 (SSSalud Res. 645/2025) | `https://www.comparaprepagas.com/blog/precio-de-las-prepagas` | 21/10/2026 |
| 12 | Lannis - Honorarios contador monotributista 2026 (CPCE CABA) | `https://lannis.app/blog/cuanto-cobra-un-contador-monotributista` | 21/10/2026 |
| 13 | Monito - Categoría H (desglose de componentes, verificación cruzada) | `https://monito.ar/monotributo-categoria-h` | 21/10/2026 |

---

### Checklist de preguntas para el recruiter / contador antes de firmar

1. ¿El PTO de 20 días se **paga** a contractors o son días sin factura?
2. ¿En qué **moneda y por qué canal** se paga? ¿Quién absorbe la comisión de transferencia?
3. ¿El reembolso de benefits va en la **misma invoice** o como documento separado?
4. ¿TEAM exige **exclusividad** o permite otro cliente en paralelo (relevante para el tope de categoría)?
5. Al contador: ¿aplica **retención** sobre esta exportación de servicios? ¿Conviene certificado MiPyME antes de la primera factura?
6. Al contador: ¿la categoría se calcula con minorista o mayorista, y qué pasa si el FX cruza 1.750 o 2.110?

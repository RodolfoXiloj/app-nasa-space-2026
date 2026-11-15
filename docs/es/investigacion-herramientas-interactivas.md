# Investigación de Herramientas y Tecnologías para Interactividad Avanzada y Efecto "WOW"

**Fecha de elaboración:** 14 de noviembre de 2026  
**Objetivo:** Identificar, evaluar y diseñar la integración de librerías y patrones de interacción que transformen a **Milpa Resiliente** en una experiencia visualmente impactante ("efecto guau"), inmersiva y memorable, preservando al 100 % los principios de integridad científica, operación estática/sin red y presupuesto estricto de peso web (JS inicial ≤ 172 kB).

> **Aviso (sábado 14 nov 2026, 20:20).** Algunas afirmaciones de este documento no se sostienen tal como están escritas. El SRTM del pipeline solo tiene altitud y pendiente de 5 puntos, no teselas. El peso de menos de 2 MB de las teselas de terreno no se ha medido. Las capas guardadas comparan época seca con época de lluvias, no un año normal con la sequía de 2026. Los futuros no traen un puntaje por modelo para un eje Z. El motor no calcula la «probabilidad de soportar la canícula» ni el «ahorro de humedad en 30 cm». La decisión sobre cada herramienta está en [plan-version-interactiva.md](plan-version-interactiva.md).

---

## 1. Diagnóstico del Estado Actual de la Web

* **Stack actual:** React 18, Leaflet (`react-leaflet`), Recharts, Vite 6, CSS puro.
* **Puntos fuertes actuales:**
  * Carga ultra rápida y funciona sin internet con capas GIBS cacheadas.
  * Accesibilidad sobresaliente (semáforo que no depende del color, pictogramas SVG, audio con subtítulos en ES y EN).
  * Peso optimizado (JS inicial dentro del límite de 172 kB).
* **Limitaciones visuales e interactivas:**
  * El mapa Leaflet 2D es estático y plano; no transmite la topografía montañosa y accidentada de las laderas de Chiquimula y Zacapa.
  * Los gráficos de Recharts son correctos pero estáticos; carecen de micro-animaciones fluidas, exploración por arrastre (brushing) o comparativas temporales directas.
  * El reproductor de audio es un botón con una etiqueta de texto; no muestra la onda de sonido ni sincroniza visualmente las palabras mientras se reproduce la voz.
  * La comparación entre un año normal y la sequía histórica de 2026 se presenta en tablas y texto, sin un comparador visual directo tipo "antes y después".

---

## 2. Catálogo de Herramientas para el Efecto "Guau"

A continuación se analizan las mejores librerías del ecosistema de visualización de datos y ciencias de la Tierra:

### 2.1. Mapas e Infraestructura Geoespacial de Próxima Generación

#### A. MapLibre GL JS + 3D Terrain (SRTM DEM)
* **Qué hace:** Renderizador de mapas basado en WebGL/WebGPU con soporte nativo de relieve y terreno tridimensional mediante elevación ráster (DEM).
* **Impacto visual:** Permite al usuario inclinar la cámara (pitch/bearing) y volar en perspectiva 3D sobre la cuenca del Río Grande de Zacapa o las laderas de Jocotán y Camotán. Se aprecia de inmediato la pendiente del terreno y por qué el suelo sin cobertura vegetal sufre una erosión catastrófica.
* **Integración técnica:** Utiliza los datos de elevación de NASA SRTM (ya presentes en el pipeline del proyecto) convertidos a formato Terrarium o Mapbox Terrain-RGB.
* **Modo sin red:** Los tiles de terreno de las 5 parcelas ocupan menos de 2 MB y se pueden almacenar en `web/public/data/terrain/`.

#### B. deck.gl + `deck.gl-raster` (Development Seed)
* **Qué hace:** Framework de visualización geoespacial acelerado por hardware para grandes volúmenes de datos. Su extensión ráster permite ejecutar operaciones de álgebra de bandas (como NDVI) directamente en los shaders de la tarjeta gráfica (GPU).
* **Impacto visual:** 
  * Deslizador en tiempo real para modificar la paleta de colores del NDVI o la humedad del suelo sin recargar imágenes.
  * Capas de extrusión 3D (columnas hexagonales H3 o prismas) donde la altura representa el déficit de lluvia y el color la cobertura del suelo.
* **Integración técnica:** Se acopla de forma transparente sobre MapLibre mediante `@deck.gl/maplibre` (`MapLibreOverlay`).

#### C. Deslizador de Pantalla Dividida "Before / After" (Swipe Slider)
* **Qué hace:** Divide el mapa en dos mitades con una barra vertical deslizable.
* **Impacto visual:** Permite comparar cara a cara:
  * **Lado izquierdo:** Cobertura vegetal normal en un año lluvioso (MODIS NDVI mediana).
  * **Lado derecho:** El impacto devastador de la sequía de julio-agosto 2026 (al 20-26 % de la lluvia normal).
  * El usuario desliza con el dedo o el ratón y "revela" la sequía de forma cinematográfica.
* **Librerías:** `leaflet-side-by-side` (para Leaflet actual, peso < 8 kB) o control deslizante nativo en MapLibre.

#### D. Capa de Partículas de Viento y Frentes de Humedad (WebGL Weather Flow)
* **Qué hace:** Anima miles de partículas que se mueven sobre el mapa siguiendo la dirección de los vientos alisios o las corrientes de humedad durante la temporada de canícula (estilo *Windy* o *earth.nullschool*).
* **Impacto visual:** Hace que el mapa se sienta vivo y dinámico, ilustrando de dónde vienen las masas de aire seco que bloquean la lluvia en el Corredor Seco.
* **Librerías:** `leaflet-velocity` o capas de partículas con shaders WebGL.

---

### 2.2. Exploración Dinámica de Datos y Escenarios

#### A. Observable Plot / D3.js con Brushing & Zooming Sincronizado
* **Qué hace:** Motor declarativo de gráficos de alta fidelidad creado por el equipo de D3.
* **Impacto visual:**
  * En la serie diaria de 25 años de CHIRPS (2001–2025), el usuario puede seleccionar con el ratón o el dedo una ventana de tiempo (ej. la sequía de 2018 o la de 2026) y ver cómo todos los gráficos de la página se adaptan y filtran simultáneamente con transiciones suaves.
  * Resaltado visual interactivo de los períodos con **más de 15 días secos consecutivos** (la canícula que dispara la alarma del motor).

#### B. Visualizador 3D de Futuros Climáticos NASA NEX-GDDP-CMIP6
* **Qué hace:** En lugar de una tabla de texto con los 33 y 34 modelos climáticos, renderiza un gráfico de superficie o dispersión 3D interactivo con Apache ECharts o Three.js.
* **Impacto visual:**
  * Eje X: Cambio de precipitación (%)
  * Eje Y: Aumento de temperatura (°C)
  * Eje Z: Puntaje de agua del cultivo
  * Cada modelo es una esfera que orbita en 3D. El agricultor/extensionista ve en un segundo cómo las 34 esferas del maíz caen al fondo del abismo (solo 2 a 9 modelos sostienen el puntaje), mientras las esferas del sorgo/caupí o Kuxur Rum flotan en la zona segura (32 a 34 modelos).

#### C. Constructor Interactivo de Rotaciones ("Lego Agronómico")
* **Qué hace:** Una interfaz táctil interactiva tipo "drag & drop" o selector por pasos donde el extensionista y el agricultor pueden configurar su propia propuesta de rotación:
  * Elegir el cultivo principal: Maíz / Frijol.
  * Arrastrar o seleccionar la leguminosa de cobertura: *Kuxur Rum*, Canavalia o Sorgo tolerante.
  * Al soltar el cultivo, un medidor animado tipo velocímetro recalcula al instante:
    * Cobertura de suelo protegida en meses secos.
    * Probabilidad de soportar una canícula de 15 días.
    * Ahorro estimado de humedad en los primeros 30 cm de suelo.

---

### 2.3. Experiencia Sensorial y Multimedia (Audio y Tacto)

#### A. Onda de Sonido Interactiva (Wavesurfer.js o SVG Audio Waveform)
* **Qué hace:** Reemplaza el botón plano de audio por una onda sonora animada que oscila en tiempo real mientras el audio sintetizado lee los tres hechos de la parcela.
* **Impacto visual y de accesibilidad:**
  * Las barras de la onda de audio se colorean al compás de la voz.
  * **Efecto Karaoke:** Las palabras y subtítulos se resaltan en pantalla sincronizadas con la reproducción.
  * El usuario puede tocar cualquier punto de la onda para rebobinar o repetir la frase clave ("Suelo desnudo", "Fuego cerca", "Canícula larga").
* **Peso:** Una onda SVG basada en la Web Audio API nativa ocupa **menos de 4 kB**, sin necesidad de librerías externas pesadas.

#### B. Micro-animaciones Biofílicas SVG
* **Qué hace:** Pequeñas animaciones SVG sutiles que reaccionan al estado del semáforo:
  * Si la cobertura del suelo es "Buena", brotan hojas verdes animadas en el pictograma.
  * Si hay sequía o fuego, las partículas de humo o el sol radiante pulsan suavemente con CSS keyframes.
  * **Cero sobrecosto de JS:** Se implementa íntegramente con CSS y SVG ya presentes en el proyecto.

---

## 3. Caso de Estudio y Referente Maestro: OpenET Data Explorer (`explore.etdata.org`)

El explorador de datos de **OpenET** ([explore.etdata.org](https://explore.etdata.org/?back=1#16/38.3800/-97.0510)) es una iniciativa conjunta de la **NASA**, el Servicio Geológico de EE.UU. (USGS), el Desert Research Institute (DRI), Environmental Defense Fund (EDF) y Google Earth Engine. Es considerado a nivel mundial como el estándar de oro en interfaces satelitales para la toma de decisiones agrícolas y gestión hídrica.

### 3.1. Anatomía Visual y Patrones de Interacción en OpenET
Al analizar la experiencia en `explore.etdata.org` en una parcela agrícola (coordenadas 38.3800, -97.0510):

1. **Modo Dual: Límite de Parcela (*Field Boundary*) vs. Ráster Continuo (*Pixel View*):**
   * *El mapa no es un bloque ciego:* Permite visualizar la parcela como un polígono vectorial nítido con métricas consolidadas o alternar a la malla de píxeles satelitales continuos de 30 m (Landsat/Sentinel).
   * *Slider de Opacidad/Transparencia:* El usuario puede atenuar el mapa térmico de evapotranspiración para ver la infraestructura real, caminos y terreno satelital debajo.
2. **Sincronización Bidireccional Mapa ↔ Gráfico Temporal:**
   * Al hacer clic en una parcela, se despliega instantáneamente un panel inferior con la serie temporal interactiva.
   * Al deslizar el cursor sobre la curva de evapotranspiración o lluvia, el mapa actualiza visualmente la capa temporal y muestra el punto exacto en el tiempo.
3. **Curvas Acumuladas de Temporada Agrícola (*Cumulative Water Use*):**
   * No solo muestra barras mensuales aisladas; traza la curva acumulativa del consumo de agua a lo largo del ciclo vegetativo, permitiendo detectar el momento exacto en que la demanda del cultivo supera la oferta hídrica.
4. **Transparencia Multimodelo (*Ensemble Breakdown*):**
   * Muestra la estimación del ensamble conjunto (el promedio robusto) y permite al usuario técnico desglosar los 6 modelos satelitales subyacentes (METRIC, SSEBop, DisALEXI, geeSEBAL, PT-JPL y SIMS).
5. **Comparativa Multianual y Estacional:**
   * Selector directo para contrastar el año actual contra años históricos secos o húmedos precedentes.

### 3.2. Cómo Aplicar la Filosofía OpenET en Milpa Resiliente

Aunque la cobertura satelital de OpenET actualmente se concentra en Estados Unidos (CONUS), sus lecciones de arquitectura visual son 100 % transferibles a Milpa Resiliente en el Corredor Seco:

| Característica de OpenET | Adaptación Directa en Milpa Resiliente | Beneficio para el Extensionista / Agricultor |
|---|---|---|
| **Límite de Parcela Vectorial** | Superponer el contorno de la celda MODIS (250 m) y el radio de fuego (500 m) como vectores SVG/Leaflet con opacidad graduable sobre la foto satelital real. | El agricultor reconoce su parcela y entiende exactamente qué porción de tierra está observando el satélite. |
| **Curva de Agua Acumulada** | Graficar la lluvia acumulada CHIRPS/IMERG frente al requerimiento hídrico acumulado del cultivo (ETc FAO-56) de mayo a noviembre, coloreando en rojo el área de déficit durante la canícula. | Explica visualmente por qué el maíz se marchita en julio-agosto aunque haya llovido en mayo. |
| **Ensamble de 6 Modelos** | Adaptar el selector de modelos para los 33/34 modelos climáticos de NASA NEX-GDDP-CMIP6, mostrando el consenso y la dispersión ante los escenarios SSP2-4.5 y SSP5-8.5. | Demuestra rigor científico sin abrumar: muestra primero la tendencia mayoritaria y permite desglosar el detalle técnico. |
| **Comparativa Estacional Rápida** | Pestaña de comparación directa que enfrente la campaña de 2026 frente a la mediana 2001–2025 y a los años con sequía severa documentada (2018 y 2019). | Valida la recomendación con la memoria histórica de la comunidad. |

---

## 4. Estrategia de Arquitectura: "Efecto WOW" sin Romper el Presupuesto de Peso ni el Modo Offline

El reto técnico más crítico de Milpa Resiliente es que **el JS inicial de la pantalla rápida del agricultor debe pesar 172 kB o menos** y el sitio debe funcionar 100 % sin conexión a internet en el campo.

### 3.1. Arquitectura de Carga Diferida (Code-Splitting Inteligente)

```
                 PANTALLA DEL AGRICULTOR (Inicio)
              ┌────────────────────────────────────┐
              │  Bundle Inicial: React + Vite +    │  < 170 kB
              │  Pictogramas SVG + Audio Nativo    │  (Carga instantánea)
              └─────────────────┬──────────────────┘
                                │ Click en "Evidence" / "Explorador 3D"
                                ▼
                   CARGA DINÁMICA BAJO DEMANDA
              ┌────────────────────────────────────┐
              │  Lazy Chunk: MapLibre 3D / Shaders │  Cargado solo
              │  Librería de Comparación Swipe     │  cuando se
              │  ECharts 3D / Futuros NASA         │  solicita
              └────────────────────────────────────┘
```

1. **La Vista del Agricultor permanece intacta y ultraligera:**
   * La primera pantalla que ve el productor en su teléfono sigue pesando menos de 172 kB.
   * Utiliza micro-animaciones CSS y la onda de audio nativa con Canvas/SVG, que no agregan peso de librerías.
2. **Las herramientas pesadas se confinan a la pestaña "Evidence":**
   * Se importan usando `React.lazy()` y `Suspense`:
     ```jsx
     const Terreno3D = React.lazy(() => import('./components/Terreno3D'));
     const ComparadorSwipe = React.lazy(() => import('./components/ComparadorSwipe'));
     const GraficoFuturos3D = React.lazy(() => import('./components/GraficoFuturos3D'));
     ```
   * Si el usuario nunca abre el explorador 3D, ese código jamás se descarga.

### 3.2. Garantía 100 % Offline-First

* Todos los modelos de terreno (DEM SRTM) y tiles de comparación se procesan previamente durante la exportación (`python -m motor.exportar`) y se almacenan en `web/public/data/`.
* Ninguna herramienta dependerá de CDNs externas, tokens de Mapbox o llamadas a servidores en la nube.

---

## 5. Hoja de Ruta de Implementación Recomendada

### Fase 1: Quick Wins Inmediatos (Bajo riesgo, alto impacto visual)
1. **Deslizador "Before / After" en la pestaña Evidence:**
   * Comparador interactivo de pantalla dividida que contrasta el satélite en un año normal contra el extremo seco de julio-agosto 2026.
   * Implementable con `leaflet-side-by-side` o un contenedor CSS split con slider nativo (peso: < 5 kB).
2. **Visualizador de Onda Sonora en el botón de Audio:**
   * Canvas interactivo que dibuja la onda mientras se reproduce el mp3 de la tarjeta del agricultor, con resaltado de la frase activa.
   * Peso: 0 kB de dependencias externas (usa la Web Audio API estándar del navegador).
3. **Micro-interacciones táctiles en los tres hechos:**
   * Al tocar un hecho (suelo, fuego, canícula), la tarjeta se expande con una transición suave y muestra el gráfico anual específico de los 25 años.

### Fase 2: Inmersión 3D y Relieve (Pestaña Evidence Avanzada)
1. **Vista de Relieve 3D con Elevación SRTM:**
   * Módulo dinámico cargado con `React.lazy()` que permite rotar e inclinar la ladera de la parcela en 3D.
2. **Navegador del Catálogo de 34 Modelos Climáticos NASA:**
   * Gráfico de dispersión interactivo con micro-animaciones para comparar SSP2-4.5 vs SSP5-8.5.

### Fase 3: Simulador Agronómico Táctil
1. **Constructor interactivo de rotaciones ("Lego Agronómico"):**
   * El extensionista prueba combinaciones en vivo con feedback inmediato de puntajes y balance de agua.

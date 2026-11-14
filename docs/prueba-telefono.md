# Prueba en un teléfono real

Actualización documental: 14 nov 2026, 09:00 (Guatemala, UTC−6).

Milpa Resiliente es un **prototipo local de referencia**: no se publica ni se entrega. Esta prueba sirve la web desde la laptop por la red Wi-Fi de la casa u oficina y la abre en un teléfono.

## 1. Levantar la web en la red local (laptop, PowerShell)

```powershell
cd web
npm run build
npx vite preview --host 0.0.0.0 --port 4173 --strictPort
```

Para detenerla: `Ctrl+C`.

## 2. URL para el teléfono

**http://192.168.0.17:4173/** (IP anotada en el plan, sin comprobar)

- Usar la IP que imprime Vite en la línea `Network: http://192.168.x.x:4173/`. No usar las que empiezan con `169.254.` ni con `172.22.`.
- El teléfono debe estar **en la misma red Wi-Fi** que la laptop.
- Si Windows pregunta, **permitir Node.js en redes privadas**. Si el teléfono no abre la página, revisar que el perfil de esa red Wi-Fi sea «Privada».

**Sin comprobar todavía** (no hay corrida real registrada en `docs/pruebas.md`). Desde la laptop, contra su IP local, revisar que:
- la página, los JSON, los mp3 y las capas respondan;
- los mp3 acepten pedidos por partes (206), que el iPhone necesita para reproducir audio.

Después, probarlo desde el teléfono: el firewall solo se nota ahí.

## 3. Qué revisar en el teléfono

Anotar el modelo del teléfono, el navegador, ✅ o ❌ en cada punto, y una captura de cada falla.

### Primera pantalla
- [ ] Abre en pocos segundos.
- [ ] Arriba aparece «Observación preliminar: julio-agosto 2026» con su resumen.
- [ ] «Ver detalle y límites» lleva a la pestaña Validación, a la tabla de 2026.

### Mapa
- [ ] Se ve el mapa base (OpenStreetMap; necesita internet).
- [ ] Zoom con dos dedos y arrastre.
- [ ] Los 5 círculos de las parcelas, con su color de confianza; al tocar uno, cambia la parcela.
- [ ] En el control de capas (icono de hojas, arriba a la derecha) cargan «Color real MODIS (sin red)», «NDVI época seca» y «NDVI época de lluvia».

### Tarjetas
- [ ] El selector «Parcela» muestra las 5 y cada una carga sus 3 rotaciones.
- [ ] Cultivo, prioridad, lluvia y temperatura cambian los puntajes.
- [ ] La tarjeta para el agricultor se lee sin hacer zoom.
- [ ] «Imprimir o guardar PDF» funciona:
  - Android: Chrome → Compartir → Imprimir → Guardar como PDF.
  - iPhone: Compartir → Imprimir.
- [ ] Las tablas de Validación se desplazan dentro de su cuadro, sin mover la página de lado.
- [ ] Con el teléfono en horizontal no se corta nada.

### Audio
- [ ] El reproductor de la tarjeta suena y se pausa, con el volumen de medios subido.
- [ ] Debajo del reproductor se lee que es **voz sintética generada con IA** (edge-tts, voz es-GT-MartaNeural).
- [ ] Cada audio dura unos 72 s. ¿Es demasiado largo para el agricultor? Anotar la opinión.
- [ ] En Camotán, el texto dice que SMAP no tiene mediciones de buena calidad.

### Modo sin conexión
- **En el teléfono no hay modo sin conexión:** la web no tiene *service worker*. Si se corta el Wi-Fi, lo ya abierto sigue visible, pero no carga parcelas nuevas.
- **Sin internet, pero con la laptop en la misma red:** desconectar el cable de internet del router y dejar su Wi-Fi encendido. La web sigue abriendo desde la laptop, y el mapa debe pasar solo a la capa guardada con el aviso «Sin internet: se muestra la capa guardada…». Es opcional.
- **La prueba sin red completa se hace en la laptop.** Pasó 14 de 14 el 14 nov 2026 a las 12:10 (Guatemala; ver `docs/pruebas.md`):

  ```powershell
  cd web
  npm run build
  npm run sin-red
  ```

  Abre la web en Edge sin interfaz y sin acceso a internet, con la copia local servida en la misma laptop. Recorre:
  - las 5 parcelas, con su audio y el rótulo de IA;
  - el cambio automático de capa del mapa;
  - las pestañas Validación y Glosario;
  - la impresión a PDF.

## 4. Resultado

| Punto | Android | iPhone | Nota |
|---|---|---|---|
| Primera pantalla | | | |
| Mapa | | | |
| Tarjetas | | | |
| Audio | | | |
| Sin internet (opcional) | | | |

Al terminar, pasar los resultados a `docs/pruebas.md`.

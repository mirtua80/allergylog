# Polen&Yo

Diario personal de alergia: registra cómo te sientes cada día y crúzalo automáticamente
con los niveles de polen y esporas de Catalunya publicados por el
[Punt d'Informació Aerobiològica (XAC–UAB)](https://aerobiologia.cat/pia/es/).

## Cómo funciona

- **`index.html`** — la app. Se lee sola, no necesita build ni backend. Tus registros
  se guardan en `localStorage`, solo en tu navegador.
- **`data/pollen.json`** — niveles actuales por estación, generado automáticamente.
  La app lo lee con una petición al mismo origen (sin problemas de CORS).
- **`scripts/fetch_pollen.py`** — script que visita las páginas públicas de predicción
  de cada estación y extrae los niveles.
- **`.github/workflows/update-pollen.yml`** — GitHub Action que ejecuta el script
  dos veces al día y hace commit de `data/pollen.json` si cambia.

Así, tu navegador nunca llama directamente a aerobiologia.cat (evita el bloqueo CORS);
es GitHub quien hace esa llamada por ti, de forma programada.

## Publicarlo en GitHub Pages

1. Sube este contenido a un repositorio nuevo (público o privado).
2. **Settings → Actions → General → Workflow permissions** → marca
   "Read and write permissions" (para que el Action pueda hacer commit del JSON).
3. **Settings → Pages** → Source: rama `main`, carpeta `/ (root)`.
4. Ve a la pestaña **Actions**, abre "Actualizar datos de polen" y pulsa
   **Run workflow** una vez, manualmente, para generar el primer `data/pollen.json`
   real con las 9 estaciones (el que viene en el repo es una semilla de ejemplo
   solo con Barcelona, para que la app no se rompa mientras tanto).
5. Tu app quedará en `https://tu-usuario.github.io/tu-repositorio/`.

A partir de ahí, el Action se ejecuta solo cada día (06:30 y 18:30 UTC — edita el
cron en el workflow si quieres otra frecuencia) y mantiene los datos frescos sin que
tengas que hacer nada.

## Si el scraper deja de funcionar

Las páginas de aerobiologia.cat pueden cambiar de estructura HTML con el tiempo.
Si ves en la pestaña Actions que el job falla o que `data/pollen.json` deja de
actualizarse, revisa `scripts/fetch_pollen.py` — la función `parse_station_page`
es la que interpreta la tabla de la web. Mientras tanto, la app sigue funcionando
con los últimos datos guardados, y siempre puedes corregir un valor a mano desde
"Corregir un valor manualmente" en la propia app.

## Licencia de los datos

Los niveles de polen y esporas son de PIA (XAC–UAB), bajo licencia
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Si publicas esta app en algún sitio, PIA pide (no es obligatorio, pero lo agradecen)
que les avises en aerobiologia.pia@uab.cat.

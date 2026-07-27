name: Actualizar datos de polen

on:
  schedule:
    # 06:30 y 18:30 UTC todos los días (ajusta si quieres otra frecuencia)
    - cron: "30 6 * * *"
    - cron: "30 18 * * *"
  workflow_dispatch: {}  # permite ejecutarlo manualmente desde la pestaña Actions

permissions:
  contents: write

jobs:
  update-data:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependencias
        run: pip install requests beautifulsoup4

      - name: Ejecutar scraper
        run: python scripts/fetch_pollen.py

      - name: Commit si hay cambios
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/pollen.json
          git diff --staged --quiet || git commit -m "Actualizar niveles de polen ($(date -u +'%Y-%m-%d %H:%M UTC'))"
          git push

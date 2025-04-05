# 🗑️ Raccolta Rifiuti per Home Assistant

![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue)
![Platform](https://img.shields.io/badge/Platform-Home%20Assistant-41BDF5)

Integrazione personalizzata per visualizzare la Raccolta dei rifiuti nel tuo Home Assistant, con supporto ad icone grafiche e visualizzazione in Lovelace.

---

## 📦 Funzionalità

✅ Crea il sensore `sensor.prossima_raccolta_rifiuti`  
✅ Include attributo `collection_types` (es: `"Plastica", "Carta"`)  
✅ Compatibile con template e card HTML personalizzate  
✅ Supporta immagini per ogni tipo di rifiuto

---

## ⚙️ Installazione tramite HACS

> 💡 Se non hai HACS, segui [questa guida](https://hacs.xyz/docs/setup/download)

1. Vai su **HACS > Integrazioni > Menu (⋮) > Repositories personalizzati**
2. Inserisci l'URL del repository GitHub: https://github.com/DomoticaFacile/raccolta_rifiuti
3. Tipo: `Integrazione`
4. Cerca "Raccolta Rifiuti" tra le integrazioni e clicca su "Installa"
5. Riavvia Home Assistant

---

## 🧾 Configurazione

Aggiungi nel tuo `configuration.yaml`:

```yaml
sensor:
  - platform: raccolta_rifiuti
    calendar_entity_id: calendar.raccolta_rifiuti
```

Riavvia Home Assistant

---

📆 **Creazione del calendario locale**   (manuale)

Per far funzionare correttamente l'integrazione, è necessario creare manualmente un calendario:

1. Vai su **Impostazioni > Dispositivi e Servizi**
2. Clicca su **Aggiungi Integrazione**
3. Seleziona **"Calendario Locale"**
4. Assegna il nome **`raccolta_rifiuti`** (esattamente così)

5. - Inserire nel calendario (il giorno prima della raccolta) i rifiuti che verranno raccolti e l'orario 
quando la card deve mostrare i contenitori (E' possibile inserire: Carta, Plastica, Vetro, Umido, Indifferenziato).

La logica è: se ogni lunedi raccolgono carta e vetro, crea due eventi la domenica,
uno carta e uno vetro, metti orario 19:00 - 23:59 e poi seleziona il lunedi di ogni settimana.

---

🖼️ Immagini (manuale)

Per visualizzare le icone nel tuo template, è necessario:

    Copiare la cartella **images**:
    da
    config\custom_components\raccolta_rifiuti\
    a
    config\www\
	
---

🧠 Esempio di Template HTML in Lovelace

```yaml
type: conditional
conditions:
  - condition: state
    entity: calendar.raccolta_rifiuti
    state: "on"
card:
  type: markdown
  content: >-
    {% set raccolta = state_attr('sensor.prossima_raccolta_rifiuti', 'collection_types') %}

    Domani si raccoglie:

    <div style="display: flex; justify-content: space-evenly; align-items: center;">

    {% if 'Plastica' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/plastica.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Carta' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/carta.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Vetro' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/vetro.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Umido' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/umido.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Indifferenziata' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/indifferenziata.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    </div>
```

---

👨‍💻 Sviluppatore

Realizzato con ❤️ da www.domoticafacile.it

Hai suggerimenti o vuoi contribuire?
Apri una issue, una pull request o contattaci tramite i nostri canali social che trovi sul sito.

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT**.  
Puoi usarlo, modificarlo e distribuirlo liberamente, purché venga mantenuto il copyright originario.

Leggi il file [LICENSE](LICENSE) per i dettagli completi.

---

## ☕ Offrimi un caffè

Se questo progetto ti è stato utile e vuoi supportarmi, puoi offrirmi un caffè cliccando qui sotto! 😊

[![Buy Me A Coffee](https://github.com/appcraftstudio/buymeacoffee/raw/master/Images/snapshot-bmc-button.png)](https://www.buymeacoffee.com/domoticafacile)

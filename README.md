# 🗑️ Raccolta Rifiuti per Home Assistant

Integrazione personalizzata per visualizzare la Raccolta dei rifiuti nel tuo Home Assistant, con supporto ad icone grafiche e visualizzazione in Lovelace.

![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue)
![Platform](https://img.shields.io/badge/Platform-Home%20Assistant-41BDF5)
![Maintainer](https://img.shields.io/badge/Maintainer-DomoticaFacile-blueviolet)
[![Donate](https://img.shields.io/badge/Buy_Me_A_Coffee-%E2%98%95-yellow)](https://www.buymeacoffee.com/domoticafacile)
![GitHub stars](https://img.shields.io/github/stars/DomoticaFacile/raccolta_rifiuti?style=social)
[![Home Assistant installs](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=HA%20installs&suffix=%20users&cacheSeconds=14400&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.raccolta_rifiuti.total)](https://analytics.home-assistant.io/custom_integrations.json)

[![Gruppo Facebook](https://img.shields.io/badge/Gruppo-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/groups/domoticafacile)
[![Pagina Facebook](https://img.shields.io/badge/Pagina-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/domoticafacile)
[![YouTube](https://img.shields.io/badge/YouTube-Channel-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@DomoticaFacile-it)

[![Instagram](https://img.shields.io/badge/Instagram-Profilo-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/domoticafacile.it)
[![TikTok](https://img.shields.io/badge/TikTok-Profilo-000000?style=for-the-badge&logo=tiktok&logoColor=white)](https://www.tiktok.com/@domoticafacile)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Canale-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029Vb5qW5O4o7qPGrFbRm1T)

**Ti piace questa integrazione?** ⭐ Clicca sulla stella per supportare il progetto!

![image](https://github.com/user-attachments/assets/2647835f-7981-4974-98c8-f82dcfe85b48)

Video Tutorial YouTube: https://www.youtube.com/watch?v=v-wM2uAQTRg
---

## 📦 Funzionalità

✅ Crea il sensore `sensor.raccolta_rifiuti`  
✅ Include attributo `collection_types` (es: `"Plastica", "Carta"`)  
✅ Compatibile con template e card HTML personalizzate  
✅ Supporta immagini per ogni tipo di rifiuto

---

## ⚙️ Installazione tramite HACS

> 💡 Se non hai HACS, segui [questa guida](https://hacs.xyz/docs/setup/download)

1. Vai su **HACS**
2. Cerca "Raccolta Rifiuti" tra le integrazioni e clicca su "Installa"
3. Riavvia Home Assistant

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

5. Inserire nel calendario (il giorno prima della raccolta) i rifiuti che verranno raccolti e l'orario 
quando la card deve mostrare i contenitori (E' possibile inserire: Carta, Plastica, Vetro, Umido, Indifferenziato).

La logica è: se ogni lunedi raccolgono carta e vetro, crea due eventi la domenica,
uno carta e uno vetro, metti orario 19:00 - 23:59 e poi seleziona il lunedi di ogni settimana.
	
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
    {% set raccolta = state_attr('sensor.raccolta_rifiuti', 'collection_types') %}

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
🖼️ Immagini (manuale)

Dopo aver completato l'installazione, verifica che sia stata creata la seguente cartella, contenente le immagini:

``` config\www\images\img_raccolta_rifiuti ```

Se la cartella non è presente, puoi crearla manualmente seguendo questi semplici passaggi:

```
Copia la cartella images da:
config\custom_components\raccolta_rifiuti\
a:
config\www\
    
```
Riavvia Home Assistant
---
### 📘 Blueprint (facoltativo ma consigliati)

Per usare i blueprint inclusi:

1. Crea la cartella:
   `config/blueprints/automation/raccolta_rifiuti/`

2. Copia  e incolla nella cartella creata il file YAML che trovi qui:
   [`blueprints/automation/raccolta_rifiuti/`](https://github.com/DomoticaFacile/raccolta_rifiuti/tree/main/blueprints/automation/raccolta_rifiuti)

3. Riavvia Home Assistant o ricarica le automazioni.

👉 Dopo il riavvio, troverai l'automazione disponibile in:
**Impostazioni > Automazioni e Scenari > + Crea automazione**

---
🖼️Screenshots

![image](https://github.com/user-attachments/assets/3b0a8c7b-7e09-4b59-b57e-f7fd8e57a3ae)

![image](https://github.com/user-attachments/assets/bd05df5b-f3ab-4b87-b041-7eba9fef88be)

---

📘 GUIDA DI CONFIGURAZIONE ANNUNCIO VOCALE ALEXA



1️⃣ Creare l’helper (commutatore)

- Vai su: Impostazioni → Dispositivi e servizi → Aiutanti → Crea Aiutante → Commutatore
- Dai al commutatore il seguente nome "Avvia Annuncio Raccolta" (otterrai input_boolean.avvia_annuncio_raccolta)
- Seleziona l'icona "Trash"

2️⃣ Esporre l’helper ad Alexa

Vai su:

- Impostazioni → Assistenti vocali → Esponi
- Cerca "Avvio Annuncio Raccolta"
- Assicurati che il commutatore creato sia esposto ad Alexa

<img width="1155" height="438" alt="image" src="https://github.com/user-attachments/assets/794a6f01-05b9-47d8-8cb9-1be08b78dfaf" />

3️⃣ Crea la routine in Alexa

Apri l'app Amazon Alexa sul tuo smartphone
→ Routine → +

Trigger → Comando vocale
→ "Quali rifiuti devo mettere fuori"
(metti altri trigger a tuo piacimento)

Aggiungi Azione → Casa Intelligente
→ Attiva Avvia Annuncio Raccolta

Salva.

4️⃣ Creare una nuova automazione usando il blueprint "Avvia Annuncio raccolta tramite Alexa"

<img width="1025" height="389" alt="image" src="https://github.com/user-attachments/assets/0ab3005a-73f7-4308-8020-fd371b091282" />


🎉 RISULTATO

Come funziona:

Tu: “Alexa, quali rifiuti devo mettere fuori?”

- Alexa accende il commutatore
- Il blueprint avvia la tua automazione originale
- L’annuncio parte con la tua voce/echo preferito
- Il toggle si spegne automaticamente
  
---

👨‍💻 Sviluppatore

Realizzato con ❤️ da www.domoticafacile.it

Hai suggerimenti o vuoi contribuire?
Apri una issue, una pull request o contattaci tramite i nostri canali social che trovi sul sito.

---

💖 Ringraziamenti:

Un enorme grazie a:

👤 **Bilo2110** – per il prezioso supporto come tester 🧪  
👤 **DaniloGP-91** – per i preziosi suggerimenti nella creazione del blueprint che permette a Google Home di annunciare la raccolta rifiuti 🔊

...e a tutti coloro che supportano e contribuiscono a questo progetto!

Ogni feedback, segnalazione o contributo è sempre benvenuto 😊  
Insieme rendiamo la domotica più facile e divertente!

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT**.  
Puoi usarlo, modificarlo e distribuirlo liberamente, purché venga mantenuto il copyright originario.

Leggi il file [LICENSE](LICENSE) per i dettagli completi.

---

## ☕ Offrimi un caffè

Se questo progetto ti è stato utile e vuoi supportarmi, puoi offrirmi un caffè cliccando qui sotto! 😊

[![Buy Me A Coffee](https://github.com/appcraftstudio/buymeacoffee/raw/master/Images/snapshot-bmc-button.png)](https://www.buymeacoffee.com/domoticafacile)

-----------------------------------------------------------------------------------

ENGLISH

# 🗑️ Waste Collection for Home Assistant

Custom integration to display your waste collection schedule in Home Assistant, with support for graphic icons and Lovelace visualization.

![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue)
![Platform](https://img.shields.io/badge/Platform-Home%20Assistant-41BDF5)
![Maintainer](https://img.shields.io/badge/Maintainer-DomoticaFacile-blueviolet)
[![Donate](https://img.shields.io/badge/Buy_Me_A_Coffee-%E2%98%95-yellow)](https://www.buymeacoffee.com/domoticafacile)
![GitHub stars](https://img.shields.io/github/stars/DomoticaFacile/raccolta_rifiuti?style=social)

[![Facebook Group](https://img.shields.io/badge/Group-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/groups/domoticafacile)
[![Facebook Page](https://img.shields.io/badge/Page-Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/domoticafacile)
[![YouTube](https://img.shields.io/badge/YouTube-Channel-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@DomoticaFacile-it)

[![Instagram](https://img.shields.io/badge/Instagram-Profile-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/domoticafacile.it)
[![TikTok](https://img.shields.io/badge/TikTok-Profile-000000?style=for-the-badge&logo=tiktok&logoColor=white)](https://www.tiktok.com/@domoticafacile)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Channel-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029Vb5qW5O4o7qPGrFbRm1T)

**Do you like this integration?** ⭐ Click the star to support the project!

![image](https://github.com/user-attachments/assets/2647835f-7981-4974-98c8-f82dcfe85b48)

YouTube Tutorial Video: https://www.youtube.com/watch?v=v-wM2uAQTRg

---

## 📦 Features

✅ Creates the sensor `sensor.raccolta_rifiuti`  
✅ Includes attribute `collection_types` (e.g. `"Plastic", "Paper"`)  
✅ Compatible with templates and custom HTML cards  
✅ Supports images for each waste type  

---

## ⚙️ Installation via HACS

> 💡 If you don’t have HACS yet, follow [this guide](https://hacs.xyz/docs/setup/download)

1. Go to **HACS**
2. Search for “Raccolta Rifiuti” in integrations and click **Install**
3. Restart Home Assistant

---

## 🧾 Configuration

Add this to your `configuration.yaml`:

```yaml
sensor:
  - platform: raccolta_rifiuti
    calendar_entity_id: calendar.raccolta_rifiuti
```

Restart Home Assistant.

📆 Creating the Local Calendar (manual setup)

To ensure the integration works correctly, you must manually create a calendar:

Go to Settings > Devices & Services
Click Add Integration
Select “Local Calendar”
Set the name to raccolta_rifiuti (exactly like this)

Add to the calendar (the day before collection) the waste types that will be collected and the time when the card should display the bins.
Allowed values: Paper, Plastic, Glass, Organic, Mixed Waste

Example logic:

If every Monday they collect paper and glass:
Create two events on Sunday
One event for paper, one for glass
Set the time between 19:00–23:59
Repeat weekly for Monday

🧠 Example of HTML Template in Lovelace
```yaml
type: conditional
conditions:
  - condition: state
    entity: calendar.raccolta_rifiuti
    state: "on"
card:
  type: markdown
  content: >-
    {% set raccolta = state_attr('sensor.raccolta_rifiuti', 'collection_types') %}

    Tomorrow the collection includes:

    <div style="display: flex; justify-content: space-evenly; align-items: center;">

    {% if 'Plastic' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/plastica.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Paper' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/carta.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Glass' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/vetro.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Organic' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/umido.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    {% if 'Mixed' in raccolta %}
      <img src="/local/images/img_raccolta_rifiuti/indifferenziata.png" style="max-width: 50px; max-height: 50px;" />
    {% endif %}

    </div>
```
🖼️ Images (manual)

After installation, ensure that the following folder exists and contains the images:

```yaml
config\www\images\img_raccolta_rifiuti
```

If the folder is missing, create it manually:

```yaml
Copy the "images" folder from:
config\custom_components\raccolta_rifiuti\
to:
config\www\
```

Restart Home Assistant.

📘 Blueprints (optional but recommended)

To use the included blueprints:

Create the folder:

```swift
config/blueprints/automation/raccolta_rifiuti/
```

Copy into that folder the YAML file from:
https://github.com/DomoticaFacile/raccolta_rifiuti/tree/main/blueprints/automation/raccolta_rifiuti

Restart Home Assistant or reload automations.

👉 After restarting, you’ll find the automation in:
Settings > Automations & Scenes > + Create Automation

🖼️ Screenshots

---
🖼️Screenshots

![image](https://github.com/user-attachments/assets/3b0a8c7b-7e09-4b59-b57e-f7fd8e57a3ae)

![image](https://github.com/user-attachments/assets/bd05df5b-f3ab-4b87-b041-7eba9fef88be)

---

📘 ALEXA VOICE ANNOUNCEMENT CONFIGURATION GUIDE

1️⃣ Create the Helper (Toggle)

Go to: Settings → Devices & Services → Helpers → Create Helper → Toggle

Name the toggle "Avvia Annuncio Raccolta" (this will create input_boolean.avvia_annuncio_raccolta)

Select the "Trash" icon

2️⃣ Expose the Helper to Alexa

Go to:

Settings → Voice Assistants → Expose

Search for "Avvia Annuncio Raccolta"

Make sure the toggle you created is exposed to Alexa

<img width="1155" height="438" alt="image" src="https://github.com/user-attachments/assets/794a6f01-05b9-47d8-8cb9-1be08b78dfaf" />
3️⃣ Create the Routine in Alexa

Open the Amazon Alexa app on your smartphone
→ Routines → +

Trigger → Voice Command
→ "Quali rifiuti devo mettere fuori"
(feel free to add any other trigger you prefer)

Add Action → Smart Home
→ Activate “Avvia Annuncio Raccolta”

Save the routine.

4️⃣ Create a New Automation Using the Blueprint
"Avvia Annuncio raccolta tramite Alexa"
<img width="1025" height="389" alt="image" src="https://github.com/user-attachments/assets/0ab3005a-73f7-4308-8020-fd371b091282" />
🎉 RESULT

How it works:

You: “Alexa, quali rifiuti devo mettere fuori?”

Alexa turns on the helper toggle

The blueprint triggers your main automation

The announcement is played through your preferred Alexa device

The toggle automatically turns itself off

---

👨‍💻 Developer

Created with ❤️ by www.domoticafacile.it

Do you have suggestions or want to contribute?
Open an issue, a pull request, or contact us through our social channels listed on the website.

💖 Acknowledgements

A huge thank you to:

👤 Bilo2110 – for valuable support as a tester 🧪

👤 DaniloGP-91 – for great suggestions in building the Google Home announcement blueprint 🔊

…and thanks to everyone who supports and contributes to this project!

Your feedback, reports, and contributions are always welcome 😊
Together we make home automation easier and more fun!

📄 License

This project is distributed under the MIT license.
You may use, modify, and distribute it freely, as long as the original copyright is preserved.

Read the LICENSE file for full details.

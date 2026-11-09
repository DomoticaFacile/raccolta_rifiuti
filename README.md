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
✅ Configurazione da interfaccia, in italiano e inglese  
✅ Notifiche serali su Telegram (facoltative)

---

## ⚙️ Installazione tramite HACS

> 💡 Se non hai HACS, segui [questa guida](https://hacs.xyz/docs/setup/download)

1. Vai su **HACS**
2. Cerca "Raccolta Rifiuti" tra le integrazioni e clicca su "Installa"
3. Riavvia Home Assistant

---

## 🧾 Configurazione

1. Crea il calendario locale (vedi **Creazione del calendario locale** più sotto)
2. Vai su **Impostazioni > Dispositivi e servizi > Aggiungi integrazione**, cerca **Raccolta Rifiuti** e scegli il calendario
3. In qualsiasi momento puoi cambiare le impostazioni da **Impostazioni > Dispositivi e servizi > Raccolta Rifiuti > Configura**

Impostazioni disponibili:
- **Nome del sensore** (facoltativo, lascia vuoto per il nome automatico)
- **Giorni in cui cercare la prossima raccolta** (`lookahead_days`, default 7)
- **Lingua del sensore**: automatica (segue la lingua di Home Assistant), italiano o inglese
- **Notifiche Telegram** (vedi più sotto)

> ♻️ **Se usavi la configurazione YAML** (`platform: raccolta_rifiuti` in `configuration.yaml`) non devi fare nulla: al primo avvio dopo l'aggiornamento il sensore viene importato automaticamente, con lo stesso `entity_id` e lo stesso storico. Home Assistant ti mostrerà un avviso in Riparazioni. Dopo aver verificato in **Dispositivi e servizi** che l'integrazione sia presente, rimuovi dal YAML l'intera voce del sensore (`platform: raccolta_rifiuti`, `calendar_entity_id` e le altre opzioni della stessa voce; se `sensor:` resta vuoto, togli anche quella riga) e riavvia. L'intervallo di aggiornamento (`scan_interval`) non è più configurabile: il sensore si aggiorna ogni 30 minuti.

🌍 **Multi-lingua**: puoi scrivere gli eventi del calendario in italiano o in inglese (es. "Carta" o "Paper"), vengono riconosciuti entrambi. L'opzione lingua controlla solo la lingua di *visualizzazione* dello stato e degli attributi del sensore (default: segue la lingua configurata in Home Assistant). È disponibile anche l'attributo `collection_type_codes`, con valori stabili in inglese (es. `"paper"`, `"glass"`), utile per chi vuole scrivere template Lovelace indipendenti dalla lingua.

📅 **Prossima raccolta (`lookahead_days`)**: `state` e `collection_types` descrivono solo la raccolta di **oggi**. In più, se oggi non c'è nulla, il sensore cerca in avanti entro `lookahead_days` giorni e popola:
- `days_remaining`: giorni mancanti alla prossima raccolta trovata (`0` se è oggi)
- `next_collection_date`: data della prossima raccolta (`YYYY-MM-DD`)
- `next_collection_types` / `next_collection_type_codes`: tipi previsti in quella data

---

📲 **Notifiche Telegram**

Ogni sera ricevi su Telegram i rifiuti da mettere fuori, con una emoji per ogni tipo:

```
🗑️ Raccolta rifiuti
Domani verrà raccolto:
📄 Carta
🍾 Vetro
```

**Requisiti**: l'integrazione [**Telegram bot**](https://my.home-assistant.io/redirect/config_flow_start/?domain=telegram_bot) di Home Assistant (clicca per aggiungerla), configurata da interfaccia, con la tua chat tra gli ID chat consentiti.

> 💡 Le chat che puoi scegliere come destinatari sono quelle aggiunte in **Telegram bot** con il pulsante **+ Aggiungi ID chat consentito** (l'ID numerico della chat lo ottieni, ad esempio, scrivendo a @userinfobot). Se l'elenco è vuoto, Home Assistant non ha ancora nessuna chat: aggiungila lì e riapri **Configura**.

**Attivazione**: **Impostazioni > Dispositivi e servizi > Raccolta Rifiuti > Configura > Notifiche Telegram**, poi scegli:
- **Attiva le notifiche Telegram**
- **Destinatari**: una o più chat del tuo bot
- **Orario della notifica** (default 20:00) ed eventualmente una **seconda notifica** (default 20:30)
- **Lingua del messaggio** (automatica, italiano o inglese), **emoji** e **titolo** personalizzato

Le notifiche sono disattivate finché non le attivi. Il messaggio parte solo se c'è una raccolta in programma. Usa gli stessi dati del sensore (gli eventi inseriti nel calendario il giorno prima), per questo dice sempre "Domani verrà raccolto". Il testo usa solo caratteri semplici, quindi funziona con qualsiasi formattazione impostata sul bot; se usi Markdown evita i caratteri `. ! - ( )` nel titolo personalizzato.

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
✅ Set up from the UI, in Italian and English  
✅ Optional evening notifications on Telegram  

---

## ⚙️ Installation via HACS

> 💡 If you don’t have HACS yet, follow [this guide](https://hacs.xyz/docs/setup/download)

1. Go to **HACS**
2. Search for “Raccolta Rifiuti” in integrations and click **Install**
3. Restart Home Assistant

---

## 🧾 Configuration

1. Create the local calendar (see **Creating the Local Calendar** below)
2. Go to **Settings > Devices & services > Add integration**, search for **Raccolta Rifiuti** and choose the calendar
3. You can change the settings at any time from **Settings > Devices & services > Raccolta Rifiuti > Configure**

Available settings:
- **Sensor name** (optional, leave empty for the automatic name)
- **Days to look ahead for the next collection** (`lookahead_days`, default 7)
- **Sensor language**: automatic (follows Home Assistant's language), Italian or English
- **Telegram notifications** (see below)

> ♻️ **If you used the YAML configuration** (`platform: raccolta_rifiuti` in `configuration.yaml`) you don't need to do anything: on the first start after the update the sensor is imported automatically, with the same `entity_id` and history. Home Assistant will show a notice under Repairs. After checking in **Devices & services** that the integration is there, remove the whole sensor entry from the YAML (`platform: raccolta_rifiuti`, `calendar_entity_id` and any other options of the same entry; if `sensor:` is left empty, remove that line too) and restart. The update interval (`scan_interval`) is no longer configurable: the sensor updates every 30 minutes.

🌍 **Multi-language**: calendar events can be written in Italian or English (e.g. "Carta" or "Paper"), both are recognized. The language option only controls the *display* language of the sensor's state and attributes (default: follows Home Assistant's configured language). A `collection_type_codes` attribute is also available, with stable English identifiers (e.g. `"paper"`, `"glass"`), handy for building Lovelace templates that shouldn't depend on the display language.

📅 **Next collection (`lookahead_days`)**: `state` and `collection_types` describe only **today's** collection. In addition, if nothing is scheduled today, the sensor looks ahead up to `lookahead_days` days and populates:
- `days_remaining`: days until the next collection found (`0` if it's today)
- `next_collection_date`: date of the next collection (`YYYY-MM-DD`)
- `next_collection_types` / `next_collection_type_codes`: expected types on that date

---

📲 **Telegram notifications**

Every evening you get a Telegram message with the waste to put out, with one emoji per type:

```
🗑️ Waste collection
Tomorrow's collection:
📄 Paper
🍾 Glass
```

**Requirements**: Home Assistant's [**Telegram bot**](https://my.home-assistant.io/redirect/config_flow_start/?domain=telegram_bot) integration (click to add it), set up from the UI, with your chat among the allowed chat IDs.

> 💡 The chats you can pick as recipients are the ones added in **Telegram bot** with the **+ Add allowed chat ID** button (you can get a chat's numeric ID, for example, by messaging @userinfobot). If the list is empty, Home Assistant has no chat yet: add it there and reopen **Configure**.

**How to enable**: **Settings > Devices & services > Raccolta Rifiuti > Configure > Telegram notifications**, then choose:
- **Enable Telegram notifications**
- **Recipients**: one or more chats of your bot
- **Notification time** (default 20:00) and optionally a **second notification** (default 20:30)
- **Message language** (automatic, Italian or English), **emojis** and a custom **title**

Notifications are off until you enable them. The message is only sent if a collection is scheduled. It uses the same data as the sensor (the calendar events entered the day before), which is why it always says "Tomorrow's collection". The text only uses simple characters, so it works with any formatting set on the bot; if you use Markdown, avoid the characters `. ! - ( )` in a custom title.

---

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

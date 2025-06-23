# 🚀 SEO E-E-A-T Content Optimizer

Un potente strumento per ottimizzare i contenuti secondo gli standard **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness) di Google, sviluppato con Streamlit e OpenAI.

## 📋 Panoramica

Questo tool analizza e ottimizza automaticamente i contenuti testuali per migliorare il posizionamento SEO secondo i criteri di qualità E-E-A-T richiesti da Google. Non solo fornisce analisi e suggerimenti, ma **genera il contenuto finale completamente ottimizzato e pronto per la pubblicazione**.

## ✨ Caratteristiche Principali

### 🔍 **Analisi Completa E-E-A-T**
- **Experience**: Valuta esempi pratici e applicabilità nel mondo reale
- **Expertise**: Analizza competenza tecnica e accuratezza delle informazioni
- **Authoritativeness**: Controlla presenza di fonti affidabili e citazioni
- **Trustworthiness**: Verifica trasparenza, obiettività e affidabilità

### 📊 **Funzionalità Avanzate**
- **Analisi competitor automatica** da URL o contenuto manuale
- **Estrazione automatica sitemap.xml** per link interni ottimizzati
- **Punteggi dettagliati** per ogni criterio E-E-A-T (1-10)
- **Suggerimenti specifici** per ogni area di miglioramento
- **Contenuto finale ottimizzato** pronto per pubblicazione
- **Conteggio parole automatico** e metriche di performance

### 🎯 **Input Richiesti**
- Nome del brand e URL del sito
- Contenuto da ottimizzare
- Tone of voice del brand
- Estratto della pagina "Chi Siamo"
- Sitemap.xml (URL o contenuto diretto)
- 3 URL competitor per analisi comparativa

## 🛠️ Installazione e Setup

### **Prerequisiti**
- Python 3.8+
- Account OpenAI con API Key
- Account GitHub (per deployment)

### **1. Clona il Repository**
```bash
git clone https://github.com/tuo-username/seo-eeat-optimizer.git
cd seo-eeat-optimizer
```

### **2. Installa le Dipendenze**
```bash
pip install -r requirements.txt
```

### **3. File requirements.txt**
Crea un file `requirements.txt` con:
```
streamlit==1.29.0
requests==2.31.0
beautifulsoup4==4.12.2
openai==1.3.0
lxml==4.9.3
```

### **4. Esecuzione Locale**
```bash
streamlit run app.py
```

## 🌐 Deploy su Streamlit Cloud

### **1. Setup Repository GitHub**
1. Carica il codice su GitHub
2. Assicurati di avere `app.py` e `requirements.txt` nella root

### **2. Deploy su Streamlit Cloud**
1. Vai su [share.streamlit.io](https://share.streamlit.io)
2. Connetti il tuo repository GitHub
3. Specifica:
   - **Repository**: `tuo-username/seo-eeat-optimizer`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click "Deploy!"

### **3. Configurazione API Key**
- Inserisci la tua OpenAI API Key direttamente nell'app
- **Non committare mai** le API keys nel codice

## 📖 Come Utilizzare

### **Step 1: Configurazione**
1. Apri l'applicazione
2. Inserisci la tua **OpenAI API Key** nella sidebar
3. Verifica la connessione (✅ dovrebbe apparire)

### **Step 2: Informazioni Brand**
- **Nome del Brand**: Il nome della tua azienda/brand
- **URL del Sito**: Link principale del sito web
- **Tone of Voice**: Seleziona lo stile comunicativo
- **Chi Siamo**: Incolla estratto della pagina aziendale

### **Step 3: Contenuto da Analizzare**
- Incolla il testo che vuoi ottimizzare
- Può essere un articolo, pagina prodotto, landing page, etc.

### **Step 4: Sitemap e Competitor**
- **Sitemap**: URL della sitemap.xml o contenuto diretto
- **Competitor**: 3 URL di concorrenti ben posizionati
- Se gli URL non sono accessibili, usa il campo manuale

### **Step 5: Analisi e Ottimizzazione**
1. Click "🚀 Avvia Analisi Completa"
2. Attendi l'elaborazione (2-3 minuti)
3. Ricevi:
   - **Analisi E-E-A-T dettagliata** con punteggi
   - **Suggerimenti specifici** per ottimizzazione
   - **Contenuto finale ottimizzato** pronto per pubblicazione

## 📊 Output Generati

### **1. Analisi E-E-A-T**
```
PUNTEGGI E-E-A-T (da 1 a 10)
- Experience: 7/10
- Expertise: 8/10
- Authoritativeness: 6/10
- Trustworthiness: 7/10
PUNTEGGIO TOTALE: 28/40
```

### **2. Suggerimenti di Ottimizzazione**
- Miglioramenti specifici per ogni criterio E-E-A-T
- Link interni consigliati dalla sitemap
- Struttura contenuto ottimizzata
- Call-to-action efficaci

### **3. Contenuto Finale Ottimizzato**
- **Testo completo** revisionato e ottimizzato
- **1500-2000 parole** ottimali per SEO
- **Formattazione markdown** pronta per web
- **Integrazione automatica** di tutti i miglioramenti

## 🔧 Configurazione Avanzata

### **Personalizzazione Prompts**
Puoi modificare i prompt OpenAI nelle funzioni:
- `analyze_eeat_content()` - per personalizzare l'analisi
- `generate_optimization_suggestions()` - per i suggerimenti
- `generate_optimized_content()` - per il contenuto finale

### **Aggiunta Lingue**
Il tool supporta contenuti in italiano per default. Per altre lingue, modifica i prompt nelle funzioni principali.

### **Limits e Rate Limiting**
- **OpenAI API**: Rispetta i limiti del tuo piano
- **Web Scraping**: Include delay automatici tra richieste
- **Timeout**: 15 secondi per il caricamento pagine

## 🚨 Troubleshooting

### **Errori Comuni**

**❌ "Errore nella configurazione OpenAI"**
- Verifica che l'API Key sia corretta
- Controlla i crediti disponibili nel tuo account OpenAI

**❌ "Errore nell'estrazione della sitemap"**
- Verifica che l'URL della sitemap sia accessibile
- Usa il campo "Contenuto XML diretto" come alternativa

**❌ "Errore nel caricamento del contenuto competitor"**
- Alcuni siti bloccano il web scraping
- Usa il campo "Contenuto Manuale Competitor"

### **Performance Tips**
- **Contenuti lunghi**: Limita a 5000 caratteri per ottimizzare i tempi
- **Sitemap grandi**: Il tool usa automaticamente i primi 20 URL
- **Competitor**: Se possibile, fornisci URL di pagine specifiche piuttosto che homepage

## 📈 Metriche di Successo

Dopo l'ottimizzazione, monitora:
- **Posizionamento SEO** per le keyword target
- **Tempo di permanenza** sulla pagina
- **Tasso di conversione** dalle call-to-action
- **Engagement social** se condiviso

---

**Sviluppato da Daniele Pisciottano 🦕**

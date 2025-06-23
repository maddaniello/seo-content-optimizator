import streamlit as st
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import openai
import re
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime

# Configurazione della pagina
st.set_page_config(
    page_title="SEO E-E-A-T Content Optimizer",
    page_icon="🚀",
    layout="wide"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #2e8b57;
        border-bottom: 2px solid #2e8b57;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inizializzazione dello stato della sessione
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'optimization_complete' not in st.session_state:
    st.session_state.optimization_complete = False

def init_openai_client(api_key):
    """Inizializza il client OpenAI"""
    try:
        openai.api_key = api_key
        # Test della connessione
        openai.models.list()
        return True
    except Exception as e:
        st.error(f"Errore nella configurazione OpenAI: {str(e)}")
        return False

def extract_sitemap_urls(sitemap_content):
    """Estrae gli URL dalla sitemap XML"""
    urls = []
    try:
        if sitemap_content.startswith('http'):
            # È un URL, scarica il contenuto
            response = requests.get(sitemap_content, timeout=10)
            content = response.text
        else:
            # È il contenuto XML diretto
            content = sitemap_content
        
        root = ET.fromstring(content)
        
        # Namespace comuni per sitemap
        namespaces = {
            'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
        }
        
        # Cerca URL nelle sitemap
        for url_elem in root.findall('.//sitemap:url/sitemap:loc', namespaces):
            urls.append(url_elem.text)
        
        # Se non trova nulla, prova senza namespace
        if not urls:
            for url_elem in root.findall('.//loc'):
                urls.append(url_elem.text)
                
    except Exception as e:
        st.error(f"Errore nell'estrazione della sitemap: {str(e)}")
    
    return urls

def scrape_website_content(url):
    """Scrappa il contenuto di una pagina web"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Rimuovi script, style e altri elementi non necessari
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
        
        # Estrai il testo principale
        text = soup.get_text()
        
        # Pulisci il testo
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text[:5000]  # Limita a 5000 caratteri
        
    except Exception as e:
        return f"Errore nel caricamento del contenuto: {str(e)}"

def analyze_eeat_content(content, brand_info, openai_client):
    """Analizza il contenuto secondo i criteri E-E-A-T"""
    
    prompt = f"""
    Analizza il seguente contenuto secondo i criteri E-E-A-T di Google per il brand "{brand_info['nome']}":

    CONTENUTO DA ANALIZZARE:
    {content}

    INFORMAZIONI SUL BRAND:
    - Nome: {brand_info['nome']}
    - URL: {brand_info['url']}
    - Tone of Voice: {brand_info['tone_of_voice']}
    - Chi Siamo: {brand_info['chi_siamo']}

    Valuta il contenuto secondo questi 4 criteri E-E-A-T e assegna un punteggio da 1 a 10 per ciascuno:

    1. EXPERIENCE (Esperienza):
    - Presenza di esempi pratici e diversificati
    - Applicabilità nel mondo reale
    - Dettagli specifici e contestualizzati
    - Casi studio o esperienze dirette

    2. EXPERTISE (Competenza):
    - Dimostrazione di conoscenza approfondita
    - Accuratezza tecnica delle informazioni
    - Insight originali o ricerche proprietarie
    - Uso di terminologia specialistica appropriata

    3. AUTHORITATIVENESS (Autorevolezza):
    - Citazioni di fonti affidabili
    - Riferimenti a studi e ricerche
    - Collegamenti a risorse autorevoli
    - Riconoscimenti nel settore

    4. TRUSTWORTHINESS (Affidabilità):
    - Trasparenza delle informazioni
    - Obiettività del punto di vista
    - Menzione di limiti o conflitti di interesse
    - Presenza di dati e prove a supporto

    Fornisci l'analisi in questo formato:
    
    ## PUNTEGGI E-E-A-T (da 1 a 10)
    - Experience: [punteggio]/10
    - Expertise: [punteggio]/10
    - Authoritativeness: [punteggio]/10
    - Trustworthiness: [punteggio]/10
    - **PUNTEGGIO TOTALE: [somma]/40**

    ## ANALISI DETTAGLIATA
    
    ### Experience
    [Analisi dettagliata della componente Experience con esempi specifici dal contenuto]
    
    ### Expertise
    [Analisi dettagliata della componente Expertise con esempi specifici dal contenuto]
    
    ### Authoritativeness
    [Analisi dettagliata della componente Authoritativeness con esempi specifici dal contenuto]
    
    ### Trustworthiness
    [Analisi dettagliata della componente Trustworthiness con esempi specifici dal contenuto]
    
    ## PUNTI DI FORZA
    [Elenco dei punti di forza identificati]
    
    ## AREE DI MIGLIORAMENTO
    [Elenco delle aree che necessitano miglioramento]
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore nell'analisi E-E-A-T: {str(e)}"

def generate_optimization_suggestions(content, brand_info, competitor_analysis, sitemap_urls, eeat_analysis, openai_client):
    """Genera suggerimenti di ottimizzazione basati sull'analisi E-E-A-T"""
    
    prompt = f"""
    Basandoti sull'analisi E-E-A-T precedente, genera suggerimenti specifici per ottimizzare il contenuto:

    CONTENUTO ATTUALE:
    {content}

    BRAND INFO:
    - Nome: {brand_info['nome']}
    - URL: {brand_info['url']}
    - Tone of Voice: {brand_info['tone_of_voice']}

    ANALISI E-E-A-T PRECEDENTE:
    {eeat_analysis}

    ANALISI COMPETITOR:
    {competitor_analysis}

    URL INTERNI DISPONIBILI (primi 20):
    {sitemap_urls[:20]}

    Genera suggerimenti di ottimizzazione strutturati in questo formato:

    ## STRATEGIA DI OTTIMIZZAZIONE E-E-A-T

    ### 1. MIGLIORAMENTI EXPERIENCE
    - [Suggerimento specifico 1 con esempio pratico]
    - [Suggerimento specifico 2 con esempio pratico]
    - [Suggerimento specifico 3 con esempio pratico]

    ### 2. MIGLIORAMENTI EXPERTISE
    - [Suggerimento specifico 1 per dimostrare competenza]
    - [Suggerimento specifico 2 per dimostrare competenza]
    - [Suggerimento specifico 3 per dimostrare competenza]

    ### 3. MIGLIORAMENTI AUTHORITATIVENESS
    - [Suggerimento specifico 1 per aumentare autorevolezza]
    - [Suggerimento specifico 2 per aumentare autorevolezza]
    - [Suggerimento specifico 3 per aumentare autorevolezza]

    ### 4. MIGLIORAMENTI TRUSTWORTHINESS
    - [Suggerimento specifico 1 per aumentare affidabilità]
    - [Suggerimento specifico 2 per aumentare affidabilità]
    - [Suggerimento specifico 3 per aumentare affidabilità]

    ## LINK INTERNI CONSIGLIATI
    [Suggerisci 5-8 URL interni dalla sitemap che sarebbero rilevanti per questo contenuto]

    ## STRUTTURA CONTENUTO OTTIMIZZATA
    [Suggerisci una struttura migliorata per il contenuto con H2, H3, etc.]

    ## CONTENUTI AGGIUNTIVI DA INCLUDERE
    [Suggerisci paragrafi, sezioni o elementi specifici da aggiungere]

    ## CALL-TO-ACTION E CONVERSIONI
    [Suggerisci CTA ottimizzate per questo contenuto]

    Mantieni il tone of voice "{brand_info['tone_of_voice']}" in tutti i suggerimenti.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore nella generazione dei suggerimenti: {str(e)}"

def generate_optimized_content(original_content, brand_info, competitor_analysis, sitemap_urls, eeat_analysis, optimization_suggestions, openai_client):
    """Genera il contenuto completamente ottimizzato pronto per la pubblicazione"""
    
    prompt = f"""
    Ora devi creare la versione FINALE e OTTIMIZZATA del contenuto, pronto per essere pubblicato.
    Applica TUTTI i suggerimenti di ottimizzazione E-E-A-T per creare un contenuto di qualità superiore.

    CONTENUTO ORIGINALE:
    {original_content}

    BRAND INFO:
    - Nome: {brand_info['nome']}
    - URL: {brand_info['url']}
    - Tone of Voice: {brand_info['tone_of_voice']}
    - Chi Siamo: {brand_info['chi_siamo']}

    ANALISI E-E-A-T:
    {eeat_analysis}

    SUGGERIMENTI DI OTTIMIZZAZIONE:
    {optimization_suggestions}

    COMPETITOR INSIGHTS:
    {competitor_analysis}

    URL INTERNI DISPONIBILI:
    {sitemap_urls[:15]}

    ISTRUZIONI PER IL CONTENUTO OTTIMIZZATO:

    1. **EXPERIENCE**: Integra esempi concreti, casi studio, dati specifici, esperienze pratiche
    2. **EXPERTISE**: Dimostra competenza tecnica, usa terminologia appropriata, includi insight originali
    3. **AUTHORITATIVENESS**: Cita fonti autorevoli, riferimenti a studi, link a risorse credibili
    4. **TRUSTWORTHINESS**: Mantieni trasparenza, obiettività, includi disclaimers quando necessario

    STRUTTURA IL CONTENUTO CON:
    - Titolo principale ottimizzato SEO
    - Introduzione coinvolgente
    - Sottotitoli H2, H3 ben strutturati
    - Paragrafi con esempi pratici e dati
    - Citazioni e riferimenti autorevoli
    - Link interni rilevanti integrati naturalmente
    - Call-to-action efficaci
    - Conclusione che sintetizza e invita all'azione

    MANTIENI:
    - Tone of voice: {brand_info['tone_of_voice']}
    - Lunghezza minima: 1500-2000 parole
    - Formattazione markdown per web
    - SEO-friendly ma naturale
    - TITOLI: usa solo la prima lettera maiuscola (es: "Contattaci per scoprire le nostre soluzioni" NON "Contattaci per Scoprire le Nostre Soluzioni")

    Crea un contenuto che sia:
    ✅ Pronto per la pubblicazione
    ✅ Ottimizzato per E-E-A-T
    ✅ SEO-friendly
    ✅ Coinvolgente per l'utente
    ✅ Allineato al brand
    ✅ Con titoli in formato corretto (solo prima lettera maiuscola)

    GENERA IL CONTENUTO OTTIMIZZATO COMPLETO:
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore nella generazione del contenuto ottimizzato: {str(e)}"

def main():
    st.markdown('<h1 class="main-header">🚀 SEO E-E-A-T Content Optimizer</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong style="color: #1f77b4;">Ottimizza i tuoi contenuti secondo gli standard E-E-A-T di Google:</strong><br>
    • <strong style="color: #2e8b57;">Experience</strong>: Esempi pratici e diversificati<br>
    • <strong style="color: #2e8b57;">Expertise</strong>: Conoscenza approfondita e accurata<br>
    • <strong style="color: #2e8b57;">Authoritativeness</strong>: Fonti affidabili e citazioni<br>
    • <strong style="color: #2e8b57;">Trustworthiness</strong>: Trasparenza e obiettività
    </div>
    """, unsafe_allow_html=True)

    # Sidebar per la configurazione
    with st.sidebar:
        st.header("⚙️ Configurazione")
        
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Inserisci la tua chiave API OpenAI"
        )
        
        if openai_api_key:
            if init_openai_client(openai_api_key):
                st.success("✅ OpenAI configurato correttamente")
            else:
                st.error("❌ Errore nella configurazione OpenAI")
                return

    if not openai_api_key:
        st.warning("⚠️ Inserisci la tua OpenAI API Key nella sidebar per continuare")
        return

    # Sezione 1: Informazioni del Brand
    st.markdown('<h2 class="section-header">📋 Informazioni del Brand</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_brand = st.text_input("🏢 Nome del Brand", placeholder="Es: Azienda XYZ")
        url_sito = st.text_input("🌐 URL del Sito", placeholder="https://www.esempio.com")
        
    with col2:
        tone_of_voice = st.selectbox(
            "🎯 Tone of Voice",
            ["Professionale", "Amichevole", "Tecnico", "Casual", "Formale", "Innovativo", "Autorevole"]
        )

    chi_siamo = st.text_area(
        "ℹ️ Estratto della pagina 'Chi Siamo'",
        height=150,
        placeholder="Inserisci un estratto della pagina Chi Siamo per fornire contesto sul brand..."
    )

    # Sezione 2: Contenuto da Analizzare
    st.markdown('<h2 class="section-header">📝 Contenuto da Ottimizzare</h2>', unsafe_allow_html=True)
    
    contenuto_da_analizzare = st.text_area(
        "Inserisci il contenuto da revisionare",
        height=300,
        placeholder="Incolla qui il contenuto testuale che vuoi ottimizzare secondo gli standard E-E-A-T..."
    )

    # Sezione 3: Sitemap
    st.markdown('<h2 class="section-header">🗺️ Sitemap per Link Interni</h2>', unsafe_allow_html=True)
    
    sitemap_option = st.radio(
        "Come vuoi fornire la sitemap?",
        ["URL della Sitemap", "Contenuto XML diretto"]
    )
    
    if sitemap_option == "URL della Sitemap":
        sitemap_input = st.text_input(
            "URL Sitemap.xml",
            placeholder="https://www.esempio.com/sitemap.xml"
        )
    else:
        sitemap_input = st.text_area(
            "Contenuto Sitemap.xml",
            height=200,
            placeholder="Incolla qui il contenuto del tuo file sitemap.xml..."
        )

    # Sezione 4: Competitor
    st.markdown('<h2 class="section-header">🏆 Analisi Competitor</h2>', unsafe_allow_html=True)
    
    st.info("Inserisci 3 URL di competitor ben posizionati per analizzare i loro contenuti")
    
    competitor_urls = []
    for i in range(3):
        url = st.text_input(f"URL Competitor {i+1}", key=f"competitor_{i}", placeholder=f"https://competitor{i+1}.com/pagina-rilevante")
        if url:
            competitor_urls.append(url)

    # Opzione per contenuto manuale dei competitor
    st.subheader("💡 Alternative: Contenuto Manuale Competitor")
    competitor_content_manual = st.text_area(
        "Se gli URL non sono accessibili, incolla qui il contenuto dei competitor",
        height=150,
        placeholder="Incolla qui il contenuto testuale dei principali competitor..."
    )

    # Pulsante di Analisi
    st.markdown('<h2 class="section-header">🔍 Avvia Analisi E-E-A-T</h2>', unsafe_allow_html=True)
    
    if st.button("🚀 Avvia Analisi Completa", type="primary", use_container_width=True):
        
        # Validazione input
        if not all([nome_brand, url_sito, contenuto_da_analizzare, chi_siamo]):
            st.error("❌ Compila tutti i campi obbligatori del brand e il contenuto da analizzare")
            return
        
        # Prepare brand info
        brand_info = {
            'nome': nome_brand,
            'url': url_sito,
            'tone_of_voice': tone_of_voice,
            'chi_siamo': chi_siamo
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Estrazione Sitemap
            status_text.text("🗺️ Estrazione URL dalla sitemap...")
            progress_bar.progress(20)
            
            sitemap_urls = []
            if sitemap_input:
                sitemap_urls = extract_sitemap_urls(sitemap_input)
                if sitemap_urls:
                    st.success(f"✅ Estratti {len(sitemap_urls)} URL dalla sitemap")
                else:
                    st.warning("⚠️ Nessun URL estratto dalla sitemap")
            
            # Step 2: Analisi Competitor
            status_text.text("🏆 Analisi dei competitor...")
            progress_bar.progress(40)
            
            competitor_analysis = "ANALISI COMPETITOR:\n"
            
            if competitor_content_manual:
                competitor_analysis += f"Contenuto competitor fornito manualmente:\n{competitor_content_manual}\n\n"
            
            for i, url in enumerate(competitor_urls):
                if url:
                    content = scrape_website_content(url)
                    competitor_analysis += f"COMPETITOR {i+1} ({url}):\n{content}\n\n"
                    time.sleep(1)  # Rate limiting
            
            # Step 3: Analisi E-E-A-T
            status_text.text("🔍 Analisi E-E-A-T del contenuto...")
            progress_bar.progress(60)
            
            eeat_analysis = analyze_eeat_content(contenuto_da_analizzare, brand_info, openai)
            
            # Step 4: Generazione Suggerimenti
            status_text.text("💡 Generazione suggerimenti di ottimizzazione...")
            progress_bar.progress(80)
            
            optimization_suggestions = generate_optimization_suggestions(
                contenuto_da_analizzare, 
                brand_info, 
                competitor_analysis, 
                sitemap_urls, 
                eeat_analysis, 
                openai
            )
            
            # Step 5: Generazione Contenuto Ottimizzato
            status_text.text("✨ Creazione contenuto ottimizzato finale...")
            progress_bar.progress(90)
            
            optimized_content = generate_optimized_content(
                contenuto_da_analizzare,
                brand_info,
                competitor_analysis,
                sitemap_urls,
                eeat_analysis,
                optimization_suggestions,
                openai
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Analisi e ottimizzazione completate!")
            
            # Risultati
            st.markdown('<h2 class="section-header">📊 Risultati Analisi E-E-A-T</h2>', unsafe_allow_html=True)
            
            with st.expander("📈 Analisi E-E-A-T Dettagliata", expanded=True):
                st.markdown(eeat_analysis)
            
            st.markdown('<h2 class="section-header">🎯 Suggerimenti di Ottimizzazione</h2>', unsafe_allow_html=True)
            
            with st.expander("💡 Piano di Ottimizzazione Completo", expanded=True):
                st.markdown(optimization_suggestions)
            
            # NUOVA SEZIONE: Contenuto Ottimizzato
            st.markdown('<h2 class="section-header">✨ Contenuto Ottimizzato - Pronto per Pubblicazione</h2>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="success-box">
            <strong>🎉 Contenuto Finale Ottimizzato!</strong><br>
            Il contenuto seguente è stato completamente revisionato applicando tutti i suggerimenti E-E-A-T.
            È pronto per essere copiato e pubblicato sul tuo sito web.
            </div>
            """, unsafe_allow_html=True)
            
            # Contenuto ottimizzato in un expander
            with st.expander("📝 CONTENUTO FINALE OTTIMIZZATO", expanded=True):
                st.markdown(optimized_content)
            
            # Pulsanti per copiare il contenuto
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copia Contenuto Ottimizzato", use_container_width=True):
                    st.code(optimized_content, language="markdown")
                    st.info("💡 Seleziona tutto il testo sopra e copialo (Ctrl+A, Ctrl+C)")
                    
            with col2:
                # Conteggio parole
                word_count = len(optimized_content.split())
                st.metric("📊 Parole Totali", word_count)
            
            # Informazioni aggiuntive
            if sitemap_urls:
                with st.expander(f"🔗 URL Interni Trovati ({len(sitemap_urls)})"):
                    for url in sitemap_urls[:50]:  # Mostra primi 50
                        st.write(f"• {url}")
            
            # Riepilogo finale
            st.markdown('<h2 class="section-header">📋 Riepilogo Ottimizzazione</h2>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Experience", "Migliorata", delta="↗️")
            with col2:
                st.metric("🧠 Expertise", "Potenziata", delta="↗️")
            with col3:
                st.metric("👑 Authority", "Rafforzata", delta="↗️")
            with col4:
                st.metric("🔒 Trust", "Incrementata", delta="↗️")
                        
            st.markdown("""
            <div class="success-box">
            <strong>✅ Ottimizzazione Completata!</strong><br>
            Il tuo contenuto è ora ottimizzato secondo gli standard E-E-A-T di Google e pronto per la pubblicazione.
            <br><br>
            <strong>Prossimi Passi:</strong><br>
            1. Copia il contenuto ottimizzato<br>
            2. Sostituisci il contenuto originale sul tuo sito<br>
            3. Aggiungi i link interni suggeriti<br>
            4. Monitora le performance SEO nei prossimi mesi
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Errore durante l'analisi: {str(e)}")
            
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    <strong>SEO E-E-A-T Content Optimizer</strong> - Ottimizza i tuoi contenuti per Google secondo gli standard Experience, Expertise, Authoritativeness e Trustworthiness
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

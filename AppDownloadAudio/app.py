import os
import tempfile
import streamlit as st
import yt_dlp

# Configuração da página
st.set_page_config(
    page_title="Audio Downloader",
    page_icon="🎧",
    layout="centered"
)

# Estilização CSS customizada
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        color: #f8fafc !important;
        margin-bottom: 0.2rem !important;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .video-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .video-title {
        font-weight: 600;
        font-size: 1.05rem;
        color: #f1f5f9;
        margin-top: 8px;
    }

    .channel-name {
        font-size: 0.85rem;
        color: #38bdf8;
    }

    div.stButton > button, div.stDownloadButton > button {
        width: 100%;
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.title("Audio Downloader")
st.markdown("<p class='subtitle'>Converta e baixe áudios do YouTube diretamente pelo navegador.</p>", unsafe_allow_html=True)

# Input de URL
link_usuario = st.text_input("Cole o link do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

def obter_info_video(url):
    ydl_opts_info = {
        'quiet': True,
        'no_warnings': True,
        'source_address': '0.0.0.0',
        'nocheckcertificate': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'audio'),
                'thumbnail': info.get('thumbnail', None),
                'uploader': info.get('uploader', 'Canal desconhecido'),
            }
    except Exception:
        return None

if link_usuario.strip():
    with st.spinner("Buscando informações do vídeo..."):
        info_video = obter_info_video(link_usuario)

    if info_video:
        st.markdown(f"""
            <div class="video-card">
                <img src="{info_video['thumbnail']}" style="width:100%; border-radius:8px; object-fit: cover; max-height: 280px;">
                <div class="video-title">{info_video['title']}</div>
                <div class="channel-name">📺 {info_video['uploader']}</div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            formato = st.radio("Formato de saída:", ["MP3", "WAV"], horizontal=True)

        with col2:
            st.write("")
            st.write("")
            botao_preparar = st.button("Preparar Download")

        # Processa e disponibiliza o arquivo via navegador
        if botao_preparar:
            extensao = formato.lower()
            
            # Usar pasta temporária do sistema
            with tempfile.TemporaryDirectory() as temp_dir:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'source_address': '0.0.0.0',
                    'nocheckcertificate': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': extensao,
                        'preferredquality': '192' if extensao == "mp3" else None,
                    }],
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                }

                with st.spinner("Processando o áudio e convertendo..."):
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([link_usuario])

                        # Encontra o arquivo gerado dentro da pasta temporária
                        arquivos = os.listdir(temp_dir)
                        if arquivos:
                            caminho_arquivo = os.path.join(temp_dir, arquivos[0])
                            nome_arquivo = arquivos[0]

                            with open(caminho_arquivo, "rb") as file:
                                bytes_audio = file.read()

                            st.session_state['download_pronto'] = {
                                'data': bytes_audio,
                                'file_name': nome_arquivo,
                                'mime': f"audio/{extensao}"
                            }
                            st.success("✓ Áudio convertido!")
                    except Exception as e:
                        st.error(f"Erro ao converter: {e}")

        # Se o arquivo estiver pronto na sessão, exibe o botão do navegador
        if 'download_pronto' in st.session_state:
            dados = st.session_state['download_pronto']
            st.download_button(
                label="⬇️ Baixar Arquivo no Navegador",
                data=dados['data'],
                file_name=dados['file_name'],
                mime=dados['mime']
            )

    else:
        st.error("Não foi possível carregar as informações deste link. Verifique a URL.")
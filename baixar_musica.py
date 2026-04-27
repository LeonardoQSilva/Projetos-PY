import streamlit as st
import yt_dlp
import os

# Configuração da página
st.set_page_config(page_title="Baixador pro Moises", page_icon="🎸")

st.title("🎸 Baixador de Áudio (WAV) para Moises")
st.markdown("Cole o link do YouTube abaixo para converter em alta qualidade.")

# Interface do Streamlit
url = st.text_input("Link do vídeo do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Converter e Baixar"):
    if url:
        try:
            with st.spinner("Processando áudio... Aguarde."):
                # Opções do yt-dlp para o servidor
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                    }],
                    'outtmpl': 'musica_download.wav',
                    # --- NOVO: Truques para evitar o Erro 403 ---
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'ignoreerrors': False,
                    'logtostderr': False,
                    'addheader': [
                        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                    ],
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web', 'mweb', 'tv'],
                        }
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Oferece o arquivo para o usuário baixar no PC/Tablet
                with open("musica_download.wav", "rb") as f:
                    st.success("Conversão concluída!")
                    st.download_button(
                        label="Clique aqui para baixar seu .WAV",
                        data=f,
                        file_name="musica_para_moises.wav",
                        mime="audio/wav"
                    )
                
                # Limpa o arquivo do servidor após o uso
                os.remove("musica_download.wav")

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, cole um link válido.")

st.info("Dica: Use esse site no seu Tab S10 Lite para baixar direto para o tablet!")

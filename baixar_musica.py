import yt_dlp
import os

def baixar():
    # 1. Cria a pasta se ela não existir
    pasta_destino = "Musicas_Moises"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta '{pasta_destino}' criada com sucesso!")

    link = input("Cole o link do YouTube: ")

    # 2. Configurações com o caminho da pasta
    opcoes = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        # O segredo está aqui: salvando dentro da pasta destino
        'outtmpl': f'{pasta_destino}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([link])
        print(f"\nPronto! Sua música está na pasta: {pasta_destino}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    baixar()
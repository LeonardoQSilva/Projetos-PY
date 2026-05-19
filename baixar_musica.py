import yt_dlp
import os

def iniciar_baixador():
    pasta_raiz = "Musicas_Baixadas"
    if not os.path.exists(pasta_raiz):
        os.makedirs(pasta_raiz)

    link_usuario = input("Cole o link do YouTube: ").strip()
    
    print("\nQual formato você quer?")
    print("1 - WAV ")
    print("2 - MP3 ")
    escolha = input("Digite 1 ou 2: ")

    extensao = "wav" if escolha == "1" else "mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': extensao,
            'preferredquality': '192' if extensao == "mp3" else None,
        }],
        'outtmpl': f'{pasta_raiz}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n[INFO] Iniciando download em {extensao.upper()}...")
            ydl.download([link_usuario]) 
        print(f"\n[SUCESSO] Arquivo salvo na pasta: {pasta_raiz}")
    except Exception as e:
        print(f"\n[ERRO] Algo deu errado: {e}")

if __name__ == "__main__":
    iniciar_baixador()

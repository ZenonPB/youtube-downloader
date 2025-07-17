# DadTunes - Youtube Downloader

![DadTunes Logo](dadtunes.ico)

## Sobre

**DadTunes** é um aplicativo minimalista e intuitivo para baixar músicas do YouTube em MP3, criado em apenas 2 dias como um presente de aniversário para o meu pai.  
Eu estava devendo a ele um pendrive com as músicas que ele mais gosta (isso já faz alguns BONS anos, desculpa), e decidi ir além: criei este app para facilitar o processo, exercitar minha criatividade e minha paixão por programação.

Além das músicas, também coloquei no pendrive mensagens carinhosas para o meu pai, para que ele sempre se lembre desse momento especial.

---

## Funcionalidades

- Baixe músicas do YouTube em MP3 com apenas alguns cliques.
- Interface moderna, escura e fácil de usar.
- Suporte a múltiplos downloads e gerenciamento de setlist.
- Download automático do FFmpeg (não precisa instalar nada manualmente!).
- Executável pronto para Windows (não precisa instalar Python).

---

## Como usar

### Usuário final (Windows)

1. Baixe o arquivo `DadTunes - Youtube Downloader.exe` na pasta `dist`.
2. Dê dois cliques para abrir o aplicativo.
3. Cole a URL do vídeo do YouTube, clique no botão de busca e adicione à sua setlist.
4. Clique em "Baixar Todas" para salvar as músicas no seu computador ou pendrive.

### Desenvolvedores

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/youtube-downloader.git
   cd youtube-downloader
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode o app:
   ```bash
   python main.py
   ```
4. Para gerar o executável:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --icon=dadtunes.ico --name="DadTunes - Youtube Downloader" main.py
   ```
   O executável estará em `dist/DadTunes - Youtube Downloader.exe`.

---

## Requisitos

- Windows 10+ (para o executável)
- Python 3.8+ (apenas para desenvolvedores)
- FFmpeg é baixado automaticamente pelo app

---

## Licença

MIT License. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Nota pessoal

---

**Este projeto nasceu de uma mistura de amor, preguiça e vontade de aprender.**
Tudo começou com uma ideia simples: colocar algumas músicas em um pendrive para que meu pai pudesse escutar no carro. Algo tão pequeno — mas que, por alguma razão, eu fui adiando por anos.

Agora, prestes a completar 18 anos, e ele 47 (sim, fazemos aniversário na mesma data), finalmente decidi fazer isso por ele. Quis criar algo que fosse mais do que só um presente; queria que ele conseguisse sentir, de alguma forma, o quanto eu o amo. Mais do que isso, queria mostrar que todo apoio que ele sempre me deu na minha jornada — especialmente na área da tecnologia — está começando a dar frutos.

Espero que esse projetinho simples sirva como inspiração ou lembrete para quem estiver lendo: nunca subestime o valor das pequenas coisas. Faça, crie, experimente. E, acima de tudo, demonstre seu amor pelas pessoas que estão ao seu lado.

---

> _Feito por Zenon Parelli Bergamo_

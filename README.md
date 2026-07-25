# Keylogger Educacional em Python

> **Aviso**
>
> Este projeto foi desenvolvido **exclusivamente para fins educacionais**, como parte de uma disciplina de Segurança da Informação. Seu objetivo é demonstrar o funcionamento de técnicas de captura de eventos do teclado e mouse, integração com APIs assíncronas e concorrência no Python.
>
> **Não utilize este projeto em computadores de terceiros sem autorização explícita.** O uso indevido pode violar leis e políticas de segurança.

---

# Objetivo

Este projeto demonstra como um programa pode:

- Capturar eventos do teclado e cliques do mouse utilizando a biblioteca `pynput`;
- Integrar a escuta de eventos em threads com um loop de eventos assíncrono (`asyncio`);
- Armazenar temporariamente o texto digitado;
- Enviar os dados de forma assíncrona e não-bloqueante para a API do Telegram utilizando `httpx`;
- Utilizar variáveis de ambiente para armazenar informações sensíveis, como o Token do Bot.

---

# Tecnologias utilizadas

- Python 3.10+
- **pynput** (Captura de eventos de entrada)
- **httpx** (Cliente HTTP assíncrono)
- **asyncio** (Programação assíncrona nativa do Python)
- **python-dotenv** (Gerenciamento de variáveis de ambiente)

---

# Estrutura do projeto

```text
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# Como funciona

O programa roda um loop de eventos do `asyncio` em segundo plano e inicia os escutadores do `pynput` em threads separadas para não travar a execução.

## Captura das teclas e mouse

A biblioteca `pynput` registra as teclas pressionadas e cliques do mouse em tempo real.

- As letras e caracteres são acumulados na memória temporária.
- Ao pressionar **Enter** ou **clicar com o mouse**, o texto acumulado é formatado e agendado para envio.

---

## Integração Thread-Safe (pynput + asyncio)

Como o `pynput` roda suas callbacks em threads separadas, o projeto utiliza a função `asyncio.run_coroutine_threadsafe()` para enviar as tarefas de envio HTTP para o loop de eventos principal do `asyncio`. Isso garante que a captura de teclas continue rápida e sem interrupções enquanto as requisições de rede ocorrem em segundo plano.

---

## Limite de caracteres por mensagem

O projeto possui a constante:

```python
CHAR_MAX_TO_SEND = 50
```

Essa constante define o número máximo de caracteres que uma mensagem pode possuir para ser enviada ao Telegram. Caso o texto capturado ultrapasse esse limite, ele é descartado antes do envio.

---

## Formatação da mensagem

Para tratar marcas de controle capturadas (como a tecla `caps_lock`), o texto passa por uma etapa de formatação via expressão regular (Regex) antes de ser transmitido.

```python
regex = r"Key\.caps_lock(.*?)Key\.caps_lock"
```

---

## Envio Assíncrono para o Telegram

O envio é feito utilizando o cliente assíncrono do `httpx`. As mensagens são transmitidas de forma não-bloqueante para o endpoint oficial do Telegram:

```text
https://api.telegram.org/bot<TOKEN>/sendMessage
```

---

## Variáveis de ambiente

As credenciais ficam armazenadas em um arquivo `.env`.

Exemplo:

```env
BOT_TOKEN=SEU_TOKEN
CHAT_ID=SEU_CHAT_ID
```

---

# Como executar o projeto

## 1. Clone o repositório e acesse a pasta

```bash
git clone <URL_DO_REPOSITORIO>
cd nome-do-projeto
```

---

## 2. Crie e ative o ambiente virtual

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configure o arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```env
BOT_TOKEN=SEU_TOKEN
CHAT_ID=SEU_CHAT_ID
```

---

## 5. Execute o programa

```bash
python main.py
```

---

# Gerando um executável

O projeto pode ser convertido em um executável utilizando o **PyInstaller**.

Primeiro instale:

```bash
pip install pyinstaller
```

## O comando de execução pode ser feito de duas formas:

### 1. A primeira é trazer os valores que foi definido nas variaveis de ambiente para o codigo no `main.py`

```python
# Traga os valores da .env para dentro do main.py

BOT_TOKEN = "VALOR_DA_ENV"
CHAT_ID = "VALOR_DA_ENV"
```

Depois rode o comando abaixo

```bash
pyinstaller --onefile --noconsole main.py
```

### 2. A segunda maneira é empacotar o arquivo .env dentro do executavel gerado

Windows

```bash
pyinstaller --onefile --noconsole --add-data ".env;." main.py
```

Linux/macOS

```bash
pyinstaller --onefile --noconsole --add-data ".env:." main.py
```

---

Ao finalizar usando alguma das formas acima, será criada a pasta:

```
dist/
```

Dentro dela estará o executável.

---

# Importante sobre Windows e PyInstaller

> **O executável para Windows deve ser gerado em um ambiente Windows.**

O PyInstaller empacota dependências C e DLLs específicas do sistema operacional onde o comando é executado.

---

# Fluxo de funcionamento

```text
Usuário digita ou clica
        │
        ▼
pynput captura os eventos (Thread secundária)
        │
        ▼
Texto é acumulado / formatado
        │
        ▼
asyncio.run_coroutine_threadsafe() (Ponte entre Threads)
        │
        ▼
Event Loop do asyncio (Thread principal)
        │
        ▼
Envio assíncrono via httpx.AsyncClient (Telegram API)
```

---

# Dependências (`requirements.txt`)

```text
pynput
httpx
python-dotenv
```

---

# Observações

Este projeto foi desenvolvido estritamente para demonstrar conceitos de:

- Programação assíncrona em Python com `asyncio` e `httpx`;
- Comunicação thread-safe entre escutadores de eventos e o loop de eventos assíncrono;
- Integração com APIs REST via HTTP/HTTPS;
- Gerenciamento de variáveis de ambiente e empacotamento com PyInstaller.
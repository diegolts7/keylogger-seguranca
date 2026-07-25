# Keylogger Educacional em Python

> **Aviso**
>
> Este projeto foi desenvolvido **exclusivamente para fins educacionais**, como parte de uma disciplina de Segurança da Informação. Seu objetivo é demonstrar o funcionamento de técnicas de captura de eventos do teclado e mouse, além da integração com APIs.
>
> **Não utilize este projeto em computadores de terceiros sem autorização explícita.** O uso indevido pode violar leis e políticas de segurança.

---

# Objetivo

Este projeto demonstra como um programa pode:

- Capturar eventos do teclado utilizando a biblioteca `pynput`;
- Detectar cliques do mouse;
- Armazenar temporariamente o texto digitado;
- Enviar os dados utilizando a API do Telegram;
- Utilizar variáveis de ambiente para armazenar informações sensíveis, como o Token do Bot.

---

# Tecnologias utilizadas

- Python 3.10+
- pynput
- python-dotenv
- pyTelegramBotAPI
- requests

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

O programa permanece executando em segundo plano aguardando eventos do teclado e do mouse.

## Captura das teclas

A biblioteca `pynput` registra cada tecla pressionada.

Durante a digitação:

- letras são adicionadas à palavra atual;
- espaço adiciona um espaço em branco;
- Backspace remove o último caractere;
- Enter finaliza a captura da palavra/frase.

---

## Captura do mouse

Sempre que ocorre um clique do mouse e existe texto pendente, esse conteúdo é enviado ao Telegram.

Essa lógica simula o comportamento de registrar o que foi digitado antes da troca de foco para outra janela ou interação com o mouse.

---

## Limite de caracteres por mensagem

O projeto possui a constante:

```python
CHAR_MAX_TO_SEND = 50
```

Essa constante define o número máximo de caracteres que uma mensagem pode possuir para ser enviada ao Telegram.

Antes do envio, o programa verifica o tamanho do texto capturado. Caso a quantidade de caracteres ultrapasse esse limite, a mensagem é descartada e não é enviada.

---

## Formatação da mensagem

A biblioteca `pynput` captura os eventos do teclado, porém não preserva automaticamente a diferença entre letras maiúsculas e minúsculas. Quando o **Caps Lock** está ativado, em vez de registrar diretamente os caracteres em caixa alta, a biblioteca registra eventos indicando que a tecla `caps_lock` foi pressionada.

Para tornar a mensagem enviada mais legível, foi implementada uma etapa de formatação utilizando uma expressão regular (Regex).

```python
regex = r"Key\.caps_lock(.*?)Key\.caps_lock"
```

Em seguida, o trecho encontrado é substituído pela sua versão em caixa alta utilizando o método `.upper()`, fazendo com que a mensagem final fique mais próxima do que o usuário realmente digitou.

---

## Envio para o Telegram

O envio ocorre através da API HTTP oficial do Telegram.

Cada mensagem enviada contém:

- nome da máquina;
- usuário do sistema;
- texto capturado.

Esses dados são enviados utilizando uma requisição HTTP para:

```
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

O projeto utiliza a biblioteca `python-dotenv` para carregar essas informações.

---

# Como executar o projeto

## 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta:

```bash
cd nome-do-projeto
```

---

## 2. Crie um ambiente virtual

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Instale as dependências

Como o projeto possui um arquivo `requirements.txt`, basta executar:

```bash
pip install -r requirements.txt
```

---

## 4. Configure o arquivo `.env`

Crie um arquivo chamado:

```
.env
```

Adicione:

```env
BOT_TOKEN=SEU_TOKEN
CHAT_ID=SEU_CHAT_ID
```

## 5. Execute

```bash
python main.py
```

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

# Importante sobre Windows

> **O executável do Windows deve ser gerado no próprio Windows.**

Um executável criado no Linux **não funciona** no Windows.

Da mesma forma:

- Linux gera executáveis Linux;
- Windows gera executáveis Windows.

Isso acontece porque o PyInstaller empacota bibliotecas específicas do sistema operacional em que ele está sendo executado.

Caso o objetivo seja obter um `.exe`, todo o processo de geração deve ser realizado em um ambiente Windows (Windows físico ou máquina virtual).

---

# Fluxo de funcionamento

```text
Usuário digita
        │
        ▼
pynput captura as teclas
        │
        ▼
Texto é armazenado temporariamente
        │
        ├──────────────► Clique do mouse
        │                     │
        │                     ▼
        └──────────────► Pressiona Enter
                              │
                              ▼
                     Texto é formatado
                              │
                              ▼
                 Envio pela API do Telegram
```

---

# Dependências

As principais bibliotecas utilizadas são:

- `pynput`
- `python-dotenv`
- `requests`
- `pyTelegramBotAPI`

Todas podem ser instaladas automaticamente através do arquivo:

```text
requirements.txt
```

---

# Observações

Este projeto foi desenvolvido apenas para demonstrar conceitos de:

- captura de eventos do teclado;
- captura de eventos do mouse;
- integração com APIs;
- utilização de variáveis de ambiente;
- empacotamento de aplicações Python.

O projeto não deve ser utilizado para monitoramento não autorizado ou qualquer atividade que viole a privacidade de terceiros.

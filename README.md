
# Projeto de Autenticação Facial com Captura de Medidas

Este é um projeto de autenticação facial que utiliza **MediaPipe** e **OpenCV** para capturar medidas faciais e autenticar usuários de forma precisa e eficiente. O sistema permite registrar novos usuários e realizar login com base em características faciais, tudo integrado com um banco de dados Firebase.

---

## **Funcionalidades**

- **Registro de Usuários**:
  - Captura medidas faciais e registra no banco de dados.
  - Interface gráfica simples para entrada de nome e CPF.
  
- **Login com Reconhecimento Facial**:
  - Autentica o usuário com base em medidas faciais previamente registradas.
  
- **Integração com Firebase**:
  - Armazena os dados do usuário e realiza autenticações de forma segura.
  
- **Feedback Visual**:
  - Retângulo dinâmico que muda de cor durante a captura facial.
  - Mensagens de orientação para posicionamento correto do rosto.

---

## **Tecnologias Utilizadas**

- **Python 3.10+**
- **OpenCV**
- **MediaPipe**
- **Tkinter** (Interface Gráfica)
- **Firebase** (Banco de Dados)
- **dotenv** (Gerenciamento de Variáveis de Ambiente)

---

## **Pré-requisitos**

Certifique-se de que sua máquina possui as seguintes ferramentas instaladas:

1. **Python 3.10 ou superior**
2. **Git**
3. **Pip** para gerenciamento de pacotes Python

---

## **Passo a Passo para Instalar e Testar o Projeto**

### 1. **Clone o Repositório**

Abra o terminal e execute o comando abaixo para clonar o projeto:

```bash
git clone https://github.com/daniel-santos92/IoT_facial_bio.git
cd seu-repositorio
```

### 2. **Crie um Ambiente Virtual**

Crie e ative um ambiente virtual para isolar as dependências do projeto:

- **Linux/Mac**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

- **Windows**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

### 3. **Instale as Dependências**

Use o `pip` para instalar as dependências do projeto listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. **Configure o Firebase**

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:
    ```env
    FIREBASE_URL=https://seu-projeto.firebaseio.com/
    DEBUG_MODE=True
    ```
2. Substitua `https://seu-projeto.firebaseio.com/` pela URL do seu banco Firebase.

---

### 5. **Execute o Projeto**

No terminal, inicie o projeto executando o arquivo principal:

```bash
python main.py
```

---

## **Como Usar**

### **Registro de Usuários**

1. Clique no botão **Registrar**.
2. Insira o nome e CPF.
3. Posicione o rosto dentro do retângulo e aguarde a captura das medidas.
4. Confirme o registro.

### **Login com Reconhecimento Facial**

1. Clique no botão **Login**.
2. Posicione o rosto dentro do retângulo.
3. Aguarde a autenticação. Se bem-sucedida, você verá uma mensagem de boas-vindas.

---

## **Estrutura do Projeto**


.
├── firebase/
│   ├── firebase_utils.py  # Funções para interação com o Firebase
├── gui/
│   ├── login.py           # Tela de login
│   ├── registro.py        # Tela de registro
├── utils/
│   ├── camera.py          # Função para captura de medidas faciais
│   ├── logger.py          # Configuração de logs
│   ├── validation.py      # Funções de validação (ex.: CPF)
│   ├── window_utils.py    # Funções para centralizar janelas
├── main.py                # Arquivo principal
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
├── .env                   # Configurações de ambiente
```

---

## **Possíveis Problemas e Soluções**

- **Erro ao acessar a webcam**:
  - Certifique-se de que sua câmera está conectada e funcionando corretamente.
  
- **Erro `No module named ...`**:
  - Certifique-se de que instalou todas as dependências com `pip install -r requirements.txt`.

- **Erro ao conectar ao Firebase**:
  - Verifique se a variável `FIREBASE_URL` está configurada corretamente no arquivo `.env`.


---



## **Contato**

Caso tenha dúvidas ou sugestões, entre em contato:

- **Nome**: Daniel Santos
- **Email**: daniel.elias.dos.santos@gmail.com

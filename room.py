import requests
import telebot
import time

# Configurações do bot
telegram_token = ""
chat_id = ""

# Configurações do jogo
API_URL = "https://casino.betfair.com/api/tables-details"
MARTINGALE_STEPS = 2

# Inicialização do bot
bot = telebot.TeleBot(telegram_token)

# Mensagem de início do jogo
bot.send_message(chat_id=chat_id,
text='''
🔥 ATENÇÃO VAMOS INICIAR 🔥
                 
➡️ ENTRE NA ↙️↙️↙️

💰ROLETA IMMERSIVE ROULETTE💰''', parse_mode="html")

print("💰 ROLETA IMMERSIVE Roulette")

# Variáveis de controle
sinal = False
indicacao1 = 0
indicacao2 = 0
entrada = 0
todas_entradas = []
quatidade_greens = 0
quatidade_reds = 0
greens_seguidos = 0
check_dados = []

# Função para obter o resultado atual do jogo
def obter_resultado():
    headers = {"cookie": ""}
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code != 200:
            return []
        data = response.json()
        data = data["gameTables"]
        for x in data:
            if x["gameTableId"] == "r2pm25d7web554om":
                try:
                    data = x["lastNumbers"]
                    print(x["lastNumbers"])
                    time.sleep(0)
                    return data
                except KeyError:
                    continue
    except requests.exceptions.ConnectionError:
        print("Erro de conexão. Tentando reconectar...")
        time.sleep(5)
        return obter_resultado()

# Função para calcular e enviar os resultados
def enviar_resultados():
    global quatidade_greens
    global quatidade_reds
    global greens_seguidos

    total_resultados = quatidade_greens + quatidade_reds
    if total_resultados != 0:
        assertividade = (100 * quatidade_greens) / total_resultados
    else:
        assertividade = 0

    win_hate = f"{assertividade:.2f}%"

    texto = f"""
    
► PLACAR = ✅ {quatidade_greens} | 🚫 {quatidade_reds}
► Consecutivas = {greens_seguidos}
► Assertividade = {win_hate}
"""
    # Enviar mensagem com os resultados
    bot.send_message(chat_id=chat_id, text=texto)

# Função para verificar alertas e tomar ações
def verificar_alerta(data):
    global sinal
    global indicacao1
    global indicacao2
    global todas_entradas
    global greens_seguidos

    data = caracteristicas(data)
    numeros = [numero["numero"] for numero in data]
    colunas = [coluna["coluna"] for coluna in data]
    if len(numeros) > 0:
        ultimo_numero = numeros[0]

        if sinal == True:
            correcao(numeros, colunas, indicacao1, indicacao2)
        else:
            if colunas[:2] == [1, 1]:
                sinal = True
                indicacao1 = 2
                indicacao2 = 3
                enviar_sinal(indicacao1, indicacao2, ultimo_numero)
                print("SINAL ENVIADO")
            if colunas[:2] == [2, 2]:
                sinal = True
                indicacao1 = 1
                indicacao2 = 3
                enviar_sinal(indicacao1, indicacao2, ultimo_numero)
                print("SINAL ENVIADO")
            if colunas[:2] == [3, 3]:
                sinal = True
                indicacao1 = 1
                indicacao2 = 2
                enviar_sinal(indicacao1, indicacao2, ultimo_numero)
                print("SINAL ENVIADO")
                
                
        # Incrementar contador de greens seguidos se for um green
        if colunas[0] == indicacao1 or colunas[0] == indicacao2 or colunas[0] == 0:
            greens_seguidos += 1
        else:
            greens_seguidos = 0
    return

# Função para calcular as características dos números
def caracteristicas(data):
    if data is None:
        return []

    caracteristicas = [] 
    for numero in data:
        try:
            numero = int(numero)

            coluna = (
                1
                if numero in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                else (
                    2
                    if numero in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                    else (
                        3
                        if numero in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
                        else 0
                    )
                )
            )
            caracteristicas.append({"numero": numero, "coluna": coluna})
        except ValueError:
            continue
    return caracteristicas

# Função para enviar sinal ao chat


def enviar_sinal(indicacao1, indicacao2, ultimo_numero):
    texto = f"""
    
    
🎯 Entrada confirmada 🎯

🔥 Entrar na {indicacao1}º e {indicacao2}ª Coluna | Cobrir o 0️⃣

🎰 IMMERSIVE ROULETTE

➡️ ENTRADA ÚNICA 1/G 🐓

💰 Após Último número: {ultimo_numero}

🤑 CADASTRE-SE AQUI
"""

    # Enviar mensagem
    bot.send_message(
        chat_id=chat_id, text=texto, parse_mode="html", disable_web_page_preview=True
    )
    time.sleep(10)

# Função para realizar a correção após o sinal
def correcao(numeros, colunas, indicacao1, indicacao2):
    global todas_entradas
    global quatidade_greens

    if colunas[0] == indicacao1 or colunas[0] == indicacao2 or colunas[0] == 0:
        todas_entradas.append(numeros[0])
        quatidade_greens += 1
        green()
    else:
        martingale()

# Função para enviar mensagem de alerta
def alerta():
    texto = f"⚠️ AGUARDE CONFIRMAR ⚠️"
    message = bot.send_message(chat_id=chat_id, text=texto, parse_mode="html")
    time.sleep(3)
    bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    reset()

# Função para executar o sistema de martingale
def martingale():
    global entrada
    global MARTINGALE_STEPS
    entrada += 1

    if entrada <= MARTINGALE_STEPS:
        texto = f"🔁 ENTRAMOS NO {entrada}° GALE 🔁"
        bot.send_message(chat_id=chat_id, text=texto, parse_mode="html")
        print("VAMOS PARA O GALE 🐓")
    else:
        red()

# Função para lidar com vitória
def green():
    global todas_entradas
    texto = f"""✅✅✅ 💰GREEN NO {todas_entradas} 💰✅✅✅"""
    print("GREEN ✅")
    # Enviar mensagem de vitória
    bot.send_message(chat_id=chat_id, text=texto)
    enviar_resultados()
    reset()

# Função para lidar com derrota
def red():
    global quatidade_reds
    quatidade_reds += 1
    texto = f"""❌LOSS MANTENHA O GERENCIAMENTO❌"""
    print("RED 🔻")
    # Enviar mensagem de derrota
    bot.send_message(chat_id=chat_id, text=texto)
    enviar_resultados()
    reset()

# Função para resetar as variáveis
def reset():
    global sinal
    global entrada
    global todas_entradas
    entrada = 0
    todas_entradas.clear()
    sinal = False

# Loop principal
while True:
    data = obter_resultado()

    if data != check_dados:
        verificar_alerta(data)
        check_dados = data

    time.sleep(5)

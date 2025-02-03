from flask import Flask, request
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from collections import deque
import threading

app = Flask(__name__)
angulo1_queue = deque(maxlen=100)
angulo2_queue = deque(maxlen=100)
alturaN_queue = deque(maxlen=100)

plt.ion()  # Modo interativo para atualização do gráfico

# Criando a página com 3 gráficos independentes (1 coluna, 3 linhas)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))  # 3 subgráficos em uma coluna

# Configuração de cada gráfico
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 300)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 300)
ax3.set_xlim(0, 100)
ax3.set_ylim(0, 30)

# Inicializando as linhas para cada gráfico
line1, = ax1.plot([], [], 'ro-', label='Angulo 1')
line2, = ax2.plot([], [], 'go-', label='Angulo 2')
line3, = ax3.plot([], [], 'bo-', label='Altura do Nariz')

def update_graph():
    """ Atualiza os gráficos periodicamente """
    while True:
        # Converte as deques para listas
        data_list1 = list(angulo1_queue)
        data_list2 = list(angulo2_queue)
        data_list3 = list(alturaN_queue)

        # Atualiza os gráficos
        line1.set_xdata(range(len(data_list1)))
        line1.set_ydata(data_list1)

        line2.set_xdata(range(len(data_list2)))
        line2.set_ydata(data_list2)

        line3.set_xdata(range(len(data_list3)))
        line3.set_ydata(data_list3)

        # Redesenha os gráficos
        fig.canvas.draw()
        fig.canvas.flush_events()

@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    """ Recebe dados XML e atualiza as filas """
    try:
        xml_data = request.data.decode("utf-8")
        print("XML recebido:", xml_data)
        root = ET.fromstring(xml_data)

        angulo1 = float(root.find('.//Angulo1').text)
        angulo2 = float(root.find('.//Angulo2').text)
        altura = float(root.find('.//AlturaNariz').text)

        angulo1_queue.append(angulo1)
        angulo2_queue.append(angulo2)
        alturaN_queue.append(altura)

        return "OK", 200

    except Exception as e:
        print("Erro ao processar os dados:", str(e))
        return f'Erro: {str(e)}', 500

def start_server():
    """ Inicia o Flask numa thread separada """
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

# Inicia o servidor Flask numa thread separada
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Permite encerrar com Ctrl+C
server_thread.start()

# Mantém o gráfico rodando no thread principal
update_graph()

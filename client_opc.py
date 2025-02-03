import random
import time
import requests
import xml.etree.ElementTree as ET

# Função para gerar dados aleatórios (simulando dados de sensores OPC UA)
def generate_opc_data():
    angulo1 = random.uniform(0, 180)  # Ângulo 1 entre 0 e 180 graus
    angulo2 = random.uniform(0, 180)  # Ângulo 2 entre 0 e 180 graus
    altura_nariz = random.uniform(10, 20)  # Altura do nariz entre 10 e 20 cm
    return angulo1, angulo2, altura_nariz

# Função para gerar dados em formato XML
def generate_xml_data(angulo1, angulo2, altura_nariz):
    # Criação do XML usando ElementTree
    root = ET.Element("Entry")

    ang1_elem = ET.SubElement(root, "Angulo1")
    ang1_elem.text = str(angulo1)

    ang2_elem = ET.SubElement(root, "Angulo2")
    ang2_elem.text = str(angulo2)

    altura_elem = ET.SubElement(root, "AlturaNariz")
    altura_elem.text = str(altura_nariz)

    # Gerar a árvore XML e convertê-la para string
    tree = ET.ElementTree(root)
    return ET.tostring(root, encoding="unicode")

# Função para enviar dados XML via HTTP POST
def send_data_to_server(xml_data, url):
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(url, data=xml_data, headers=headers)
        if response.status_code == 200:
            print("Dados enviados com sucesso!")
        else:
            print(f"Falha ao enviar dados. Status code: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")

# Função para o cliente OPC que gera dados constantemente
def opc_client(url, interval=2):
    while True:
        # Gerar dados aleatórios
        angulo1, angulo2, altura_nariz = generate_opc_data()

        # Gerar o XML com os dados
        xml_data = generate_xml_data(angulo1, angulo2, altura_nariz)

        # Enviar os dados via HTTP
        send_data_to_server(xml_data, url)

        # Aguardar o próximo intervalo
        time.sleep(interval)

# URL do servidor que irá receber os dados (exemplo)
server_url = "http://127.0.0.1:5000/receber_dados"  # Altere para o URL do seu servidor

# Intervalo de 2 segundos para enviar os dados
opc_client(server_url, interval=2)

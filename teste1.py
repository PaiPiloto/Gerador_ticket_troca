# Parte 1
import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
import subprocess
import json
from reportlab.lib.pagesizes import mm
from barcode.writer import ImageWriter
import io
import tempfile
import datetime
from barcode import EAN13, Code128
from PIL import Image
import os
import webbrowser
import platform
import subprocess
import re



cod_venda = ""
cod_produto = ""
venda = ""


# Parte 2
class Configuracoes:
    def __init__(self):
        self.nome_empresa = ""
        self.endereco_empresa = ""
        self.telefone_empresa = ""
        self.cnpj_empresa = ""

    def salvar(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.__dict__, file)

    def carregar(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.__dict__.update(data)


config = Configuracoes()



def abrir_caixa_impressao(file_path):
    if platform.system() == "Windows":
        subprocess.Popen(['start', '', file_path], shell=True)
    elif platform.system() == "Linux":
        subprocess.Popen(['xdg-open', file_path])
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(['open', file_path])
    else:
        webbrowser.open(file_path)





# Parte 4
def salvar_configuracoes(configuracoes_window, nome_entry, endereco_entry, telefone_entry, cnpj_entry):
    config.nome_empresa = nome_entry.get()
    config.endereco_empresa = endereco_entry.get()
    config.telefone_empresa = telefone_entry.get()
    config.cnpj_empresa = cnpj_entry.get()
    config.salvar("configuracoes.json")
    configuracoes_window.destroy()




# Parte 5
def abrir_configuracoes(root, codigo_venda_entry, codigo_barras_entry, valor_entry):
    configuracoes_window = tk.Toplevel(root)
    configuracoes_window.title("Configurações")
    configuracoes_window.geometry("200x400")

    nome_label = tk.Label(configuracoes_window, text="Nome da Empresa:")
    nome_label.pack()
    nome_entry = tk.Entry(configuracoes_window, width=30)
    nome_entry.pack()

    endereco_label = tk.Label(configuracoes_window, text="Endereço:")
    endereco_label.pack()
    endereco_entry = tk.Entry(configuracoes_window, width=30)
    endereco_entry.pack()

    telefone_label = tk.Label(configuracoes_window, text="Telefone:")
    telefone_label.pack()
    telefone_entry = tk.Entry(configuracoes_window, width=30)
    telefone_entry.pack()

    cnpj_label = tk.Label(configuracoes_window, text="CNPJ:")
    cnpj_label.pack()
    cnpj_entry = tk.Entry(configuracoes_window, width=30)
    cnpj_entry.pack()

    nome_entry.insert(0, config.nome_empresa)
    endereco_entry.insert(0, config.endereco_empresa)
    telefone_entry.insert(0, config.telefone_empresa)
    cnpj_entry.insert(0, config.cnpj_empresa)

    valor_entry.bind("<KeyRelease>", lambda event: formatar_valor(event, valor_entry))

    salvar_button = tk.Button(configuracoes_window, text="Salvar",
                              command=lambda: salvar_configuracoes(configuracoes_window, nome_entry, endereco_entry,
                                                                   telefone_entry, cnpj_entry))
    salvar_button.pack()

    cancelar_button = tk.Button(configuracoes_window, text="Cancelar", command=configuracoes_window.destroy)
    cancelar_button.pack(side=tk.LEFT)




# Parte 6
# Parte 6
def gerar_codigo_barras(numero):
    barcode_obj = Code128(numero, writer=ImageWriter())
    barcode_image = barcode_obj.render()

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        barcode_image.save(tmp_file, format='PNG')
        tmp_file_path = tmp_file.name

    return tmp_file_path

def gerar_codigo_barras_tipo(numero, tipo):
    barcode_class = Code128 if tipo == 'valor' else EAN13
    barcode_obj = barcode_class(numero, writer=ImageWriter())
    barcode_image = barcode_obj.render()

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        barcode_image.save(tmp_file, format='PNG')
        tmp_file_path = tmp_file.name

    return tmp_file_path



def formatar_valor(event, valor_entry):
    valor = valor_entry.get()
    valor = re.sub(r'\D', '', valor)  # Remover caracteres não numéricos
    valor = valor.ljust(7, '0')  # Preencher com zeros à direita até ter 7 dígitos
    valor = valor[:5] + ',' + valor[5:]  # Inserir a vírgula após o quinto dígito
    valor_entry.delete(0, tk.END)  # Limpar o campo de entrada
    valor_entry.insert(0, valor)  # Inserir o valor formatado no campo de entrada






# Parte 7
def gerar_ticket(root, valor, codigo_venda, codigo_barras):
    print("Valor:", valor)
    print("Código de Venda:", codigo_venda)
    print("Código de Barras:", codigo_barras)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        file_path = tmp_file.name
        temp_file_path = tmp_file.name

        # Definir tamanho da página e ajustar coordenadas do canvas
        page_width = 80 * mm  # 80mm de largura
        page_height = 297 * mm  # Altura da página (exemplo: 297mm)
        margin = 10  # Margem de 30 pontos
        desired_length = 25  # Comprimento desejado para a sequência "======"
        equals_string = "=" * desired_length

        c = canvas.Canvas(file_path, pagesize=(page_width, page_height))
        c.setFont("Helvetica", 14)  # Tamanho da fonte dobrado

        # Ajustar coordenadas do canvas
        c.translate(0, 0)

        # Ticket de Troca
        line_width = page_width - 1 * margin
        c.drawString(margin, page_height - 15, equals_string.ljust(desired_length))
        c.drawCentredString(page_width / 2, page_height - 30, "Ticket de Troca")
        c.drawString(margin, page_height - 45, equals_string.ljust(desired_length))
        c.drawString(margin, page_height - 60, f"{config.nome_empresa}")
        c.drawString(margin, page_height - 75, f"{config.endereco_empresa}")
        c.drawString(margin, page_height - 90, f"{config.telefone_empresa}")
        c.drawString(margin, page_height - 105, f"{config.cnpj_empresa}")
        c.drawString(margin, page_height - 120, equals_string.ljust(desired_length))
        c.drawCentredString(page_width / 2, page_height - 135, "Doc. não fiscal")
        c.drawString(margin, page_height - 150, equals_string.ljust(desired_length))
        c.drawString(margin, page_height - 165, f"Cod. venda: {codigo_venda}")
        c.drawString(margin, page_height - 210, f"Val. 30 Dias")
        c.drawString(margin, page_height - 225, equals_string.ljust(desired_length))
        c.drawCentredString(page_width / 2, page_height - 240, "Produto")

        # Incluir data e hora
        data_atual = datetime.datetime.now()
        data_string = data_atual.strftime("%d/%m/%Y")
        c.drawString(margin, page_height - 180, f"Data: {data_string}")
        hora_atual = datetime.datetime.now()
        hora_string = hora_atual.strftime("%H:%M:%S")
        c.drawString(margin, page_height - 195, f"Hora: {hora_string}")

        c.drawCentredString(page_width / 2, page_height - 345, "Cod. Interno")
        c.drawString(margin, page_height - 330, equals_string.ljust(desired_length))

        barcode_path = gerar_codigo_barras_tipo(codigo_barras, 'codigo')
        valor_barcode_path = gerar_codigo_barras_tipo(valor, 'valor')

        barcode_image = Image.open(barcode_path)
        valor_barcode_image = Image.open(valor_barcode_path)

        # Obter as dimensões da imagem
        width, height1 = barcode_image.size
        width1, height = valor_barcode_image.size

        # Definir as coordenadas de corte para a primeira metade
        left = 0
        top = 0
        right = width
        bottom = height // 2
        #left1 = 0
        #top1 = 0
        right1 = width1
        #bottom1 = height // 2

        # Cortar a primeira metade da imagem
        cropped_image1 = barcode_image.crop((left, top, right, bottom))
        cropped_image3 = valor_barcode_image.crop((left, top, right1, bottom))

        # Definir as coordenadas de corte para a segunda metade
        top = height // 2
        bottom = height
        #top1 = height1 // 2
        #bottom1 = height1



        # Cortar a segunda metade da imagem
        cropped_image2 = barcode_image.crop((left, top, right, bottom))
        cropped_image4 = valor_barcode_image.crop((left, top, right1, bottom))

        # Salvar as duas imagens cortadas temporariamente
        cropped_image1_path = "barcode_half1.png"
        cropped_image2_path = "barcode_half2.png"
        cropped_image1.save(cropped_image1_path)
        cropped_image2.save(cropped_image2_path)

        valor_entry.delete(0, tk.END)
        valor_entry.insert(0, valor)

        valor_entry.bind("<KeyRelease>", lambda event: formatar_valor(event, valor_entry))

        cropped_image3_path = "barcode_half3.png"
        cropped_image4_path = "barcode_half4.png"
        cropped_image3.save(cropped_image3_path)
        cropped_image4.save(cropped_image4_path)

        barcode_x = 100  # Substitua o valor 100 pelo valor desejado para a coordenada X
        valor_barcode_x = 100  # Substitua o valor 100 pelo valor desejado para a coordenada X


        # Gerar código de barras
        barcode_width = int(line_width)  # Convertendo para inteiro
        barcode_height = 1  # Altura desejada da imagem do código de barras
        barcode_image = Image.open(barcode_path).resize((barcode_width, barcode_height), Image.LANCZOS)
        barcode_path = gerar_codigo_barras(codigo_barras)
        barcode_width, barcode_height = Image.open(barcode_path).size
        barcode_x = (page_width - barcode_width) / 2

        valor_barcode_width = barcode_width
        valor_barcode_height: int = barcode_height

        # Atualizar o tamanho do código de barras
        barcode_scale_factor_width = 0.6
        barcode_scale_factor_height = 0.25

        barcode_scaled_width = int(barcode_width * barcode_scale_factor_width)
        barcode_scaled_height = int(barcode_height * barcode_scale_factor_height)
        barcode_x = (page_width - barcode_scaled_width) / 2
        #c.drawImage(barcode_path, barcode_x, page_height - 285, width=barcode_scaled_width,
                    #height=barcode_scaled_height)

        # Desenhar a primeira metade do código de barras
        c.drawImage(cropped_image1_path, barcode_x, page_height - 278, width=barcode_scaled_width,
                    height=barcode_scaled_height // 2)

        # Desenhar a segunda metade do código de barras
        #c.drawImage(cropped_image2_path, barcode_x, page_height - 350 - barcode_scaled_height // 2,
                    #width=barcode_scaled_width, height=barcode_scaled_height // 2)

        c.drawCentredString(page_width / 2, page_height - 293, f"{codigo_barras}")

        valor_barcode_path = gerar_codigo_barras_tipo(valor, 'valor')
        valor_barcode_image = Image.open(valor_barcode_path)
        valor_barcode_width, valor_barcode_height = valor_barcode_image.size

        valor_barcode_scale_factor_width = 0.6
        valor_barcode_scale_factor_height = 0.25

        valor_barcode_scaled_width = int(valor_barcode_width * valor_barcode_scale_factor_width)
        valor_barcode_scaled_height = int(valor_barcode_height * valor_barcode_scale_factor_height)
        valor_barcode_x = (page_width - valor_barcode_scaled_width) / 2

        #c.drawImage(valor_barcode_path, valor_barcode_x, page_height - 420, width=valor_barcode_scaled_width,
                    #height=valor_barcode_scaled_height)

        # Desenhar a primeira metade do código de barras
        c.drawImage(cropped_image3_path, valor_barcode_x, page_height - 400, width=valor_barcode_scaled_width,
                    height=barcode_scaled_height // 2)

        # Desenhar a segunda metade do código de barras
        #c.drawImage(cropped_image4_path, valor_barcode_x, page_height - 480 - valor_barcode_scaled_height // 2,
                    #width=valor_barcode_scaled_width, height=barcode_scaled_height // 2)


        c.save()

        # Excluir os arquivos temporários das imagens cortadas
        os.remove(cropped_image1_path)
        os.remove(cropped_image2_path)
        os.remove(cropped_image3_path)
        os.remove(cropped_image4_path)

    abrir_caixa_impressao(file_path)

    subprocess.Popen(['start', file_path])

    os.remove(file_path)


# Parte 8
def mostrar_ticket_demo(root, codigo_venda, codigo_barras, valor):
    print("Ticket de Troca")
    print("Nome da Empresa:", config.nome_empresa)
    print("Endereço:", config.endereco_empresa)
    print("Telefone:", config.telefone_empresa)
    print("CNPJ:", config.cnpj_empresa)
    print("Código de Venda:", codigo_venda)
    print("Valor:", valor)
    print("Código de Barras:", codigo_barras)
    ticket_demo_window = tk.Toplevel(root)
    ticket_demo_window.title("Ticket de Troca")
    ticket_demo_window.geometry("300x300")

    ticket_label = tk.Label(ticket_demo_window, text="Ticket de Troca")
    ticket_label.pack()

    nome_empresa_label = tk.Label(ticket_demo_window, text=f"Nome da Empresa:\n{config.nome_empresa}")
    nome_empresa_label.pack()

    endereco_label = tk.Label(ticket_demo_window, text=f"Endereço:\n{config.endereco_empresa}")
    endereco_label.pack()

    telefone_label = tk.Label(ticket_demo_window, text=f"Telefone:\n{config.telefone_empresa}")
    telefone_label.pack()

    cnpj_label = tk.Label(ticket_demo_window, text=f"CNPJ:\n{config.cnpj_empresa}")
    cnpj_label.pack()

    codigo_venda_label = tk.Label(ticket_demo_window, text=f"Código de Venda:\n{codigo_venda}")
    codigo_venda_label.pack()

    codigo_barras_label = tk.Label(ticket_demo_window, text=f"Código de Barras:\n{codigo_barras}")
    codigo_barras_label.pack()

    valor_label = tk.Label(ticket_demo_window, text=f"Valor:\n{valor}")
    valor_label.pack()

    cancelar_button = tk.Button(ticket_demo_window, text="Cancelar", command=ticket_demo_window.destroy)
    cancelar_button.pack(side=tk.LEFT)

    imprimir_button = tk.Button(ticket_demo_window, text="Imprimir",
                                command=lambda: gerar_ticket(root, valor, codigo_venda, codigo_barras))
    imprimir_button.pack(side=tk.LEFT)


# Parte 9
def gerar_ticket_wrapper(root, codigo_venda_entry, codigo_barras_entry, valor_entry):
    codigo_venda = codigo_venda_entry.get()
    codigo_barras = codigo_barras_entry.get()
    valor = valor_entry.get()

    try:
        if codigo_venda and codigo_barras and valor:
            gerar_ticket(root, valor, codigo_venda, codigo_barras)
        else:
            print("Preencha todos os campos")
    except Exception as e:
        print("Erro ao gerar o ticket:", e)


# Parte 10
def inicializar_interface():
    root = tk.Tk()
    root.title("Gerador de Ticket de Troca")
    root.geometry("300x200")

    codigo_venda_label = tk.Label(root, text="Código de Venda:")
    codigo_venda_label.pack()
    codigo_venda_entry = tk.Entry(root, width=30)
    codigo_venda_entry.pack()

    codigo_barras_label = tk.Label(root, text="Código de Barras:")
    codigo_barras_label.pack()
    codigo_barras_entry = tk.Entry(root, width=30)
    codigo_barras_entry.pack()

    valor_label = tk.Label(root, text="Valor:")
    valor_label.pack()
    valor_entry = tk.Entry(root)
    valor_entry.pack()

    abrir_ticket_button = tk.Button(root, text="Gerar Ticket",
                                    command=lambda: gerar_ticket_wrapper(root, codigo_venda_entry, codigo_barras_entry, valor_entry))
    abrir_ticket_button.pack()

    abrir_configuracoes_button = tk.Button(root, text="Configurações",
                                           command=lambda: abrir_configuracoes(root, codigo_venda_entry, codigo_barras_entry, valor_entry))
    abrir_configuracoes_button.pack()

    # Teste
    config = Configuracoes()
    config.nome_empresa = "Nome da Empresa"
    config.endereco_empresa = "Endereço da Empresa"
    config.telefone_empresa = "Telefone da Empresa"
    config.cnpj_empresa = "CNPJ da Empresa"

    root = tk.Tk()

    codigo_venda_entry = tk.Entry(root)
    codigo_venda_entry.pack()

    codigo_barras_entry = tk.Entry(root)
    codigo_barras_entry.pack()

    valor_entry = tk.Entry(root)
    valor_entry.pack()
    valor_entry.bind("<KeyRelease>", lambda event: formatar_valor(event, valor_entry))

    gerar_ticket_button = tk.Button(root, text="Gerar Ticket", command=lambda: gerar_ticket(root, valor_entry.get(),
                                                                                            codigo_venda_entry.get(),
                                                                                            codigo_barras_entry.get()))
    gerar_ticket_button.pack()

    mostrar_ticket_demo_button = tk.Button(root, text="Mostrar Ticket Demo", command=lambda: mostrar_ticket_demo(root,
                                                                                                                 codigo_venda_entry.get(),
                                                                                                                 codigo_barras_entry.get(),
                                                                                                                 valor_entry.get()))
    mostrar_ticket_demo_button.pack()

    root.mainloop()


# Parte 11
config.carregar("configuracoes.json")
inicializar_interface()


import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
import subprocess
import json
from reportlab.lib.pagesizes import mm
import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
import io
import tempfile
import datetime
from barcode import EAN13, Code128
from PIL import Image
import os




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
    subprocess.Popen(["start", file_path], shell=True)


def salvar_configuracoes(configuracoes_window, nome_entry, endereco_entry, telefone_entry, cnpj_entry):
    config.nome_empresa = nome_entry.get()
    config.endereco_empresa = endereco_entry.get()
    config.telefone_empresa = telefone_entry.get()
    config.cnpj_empresa = cnpj_entry.get()
    config.salvar("configuracoes.json")
    configuracoes_window.destroy()


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

    valor_label = tk.Label(configuracoes_window, text="Valor:")
    valor_label.pack()
    valor_entry = tk.Entry(configuracoes_window, width=30)
    valor_entry.pack()

    salvar_button = tk.Button(configuracoes_window, text="Salvar",
                              command=lambda: salvar_configuracoes(configuracoes_window, nome_entry, endereco_entry,
                                                                   telefone_entry, cnpj_entry))
    salvar_button.pack()

    cancelar_button = tk.Button(configuracoes_window, text="Cancelar", command=configuracoes_window.destroy)
    cancelar_button.pack(side=tk.LEFT)

    abrir_ticket_button = tk.Button(configuracoes_window, text="Abrir Ticket",
                                    command=lambda: gerar_ticket(root, codigo_venda_entry.get(),
                                                                 codigo_barras_entry.get(), valor_entry.get()))
    abrir_ticket_button.pack()


def gerar_ticket(root, codigo_venda, codigo_barras, valor):
    config.carregar("configuracoes.json")

    pdf_name = f"ticket_{codigo_venda}.pdf"
    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=pdf_name)
    if pdf_path:
        c = canvas.Canvas(pdf_path, pagesize=(80 * mm, 150 * mm))
        c.setFont("Helvetica", 8)

        # Código de barras
        barcode_image = generate_barcode(codigo_barras)

        with tempfile.NamedTemporaryFile(suffix=".png", dir=".") as tmp_file:
            barcode_image.save(tmp_file.name, format="PNG")
            tmp_file.seek(0)

            # Desenhar o código de barras no PDF
            c.drawImage(tmp_file.name, 5 * mm, 130 * mm, width=70 * mm, height=10 * mm)


        # Salvar o código de barras em um arquivo temporário
        # Salvar o código de barras em um arquivo temporário
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", dir=r"C:\Nova pasta\GeradordeTicket")
        barcode_image.save(tmp_file.name, format="PNG")
        tmp_file.seek(0)

        # Desenhar o código de barras no PDF
        c.drawImage(tmp_file.name, 5 * mm, 130 * mm, width=70 * mm, height=10 * mm)

        # Informações da empresa
        c.drawString(5 * mm, 120 * mm, config.nome_empresa)
        c.drawString(5 * mm, 115 * mm, config.endereco_empresa)
        c.drawString(5 * mm, 110 * mm, f"Telefone: {config.telefone_empresa}")
        c.drawString(5 * mm, 105 * mm, f"CNPJ: {config.cnpj_empresa}")

        # Informações da venda
        c.drawString(5 * mm, 95 * mm, f"Código da Venda: {codigo_venda}")
        c.drawString(5 * mm, 90 * mm, f"Valor: R$ {valor}")

        c.save()

        abrir_caixa_impressao(pdf_path)


def generate_barcode(barcode_data):
    barcode_class = Code128 if len(barcode_data) > 12 else EAN13
    barcode_writer = ImageWriter()
    barcode_image = barcode_class(barcode_data, writer=barcode_writer).render()
    return barcode_image




root = tk.Tk()
root.title("Gerador de Tickets")
root.geometry("300x200")

codigo_venda_label = tk.Label(root, text="Código da Venda:")
codigo_venda_label.pack()
codigo_venda_entry = tk.Entry(root)
codigo_venda_entry.pack()

codigo_barras_label = tk.Label(root, text="Código de Barras:")
codigo_barras_label.pack()
codigo_barras_entry = tk.Entry(root)
codigo_barras_entry.pack()

valor_label = tk.Label(root, text="Valor:")
valor_label.pack()
valor_entry = tk.Entry(root)
valor_entry.pack()

config_button = tk.Button(root, text="Configurações",
                          command=lambda: abrir_configuracoes(root, codigo_venda_entry, codigo_barras_entry,
                                                              valor_entry))
config_button.pack()

gerar_ticket_button = tk.Button(root, text="Gerar Ticket",
                                command=lambda: gerar_ticket(root, codigo_venda_entry.get(), codigo_barras_entry.get(),
                                                             valor_entry.get()))
gerar_ticket_button.pack()

root.mainloop()

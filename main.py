import time
from pycomm3 import LogixDriver
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv
import os
import xml.etree.ElementTree as ET
import threading

class Tela():
  
    def texto(self):
        self.label_inicio = Label(self.main, text="Aguardando...", font="Arial 16")
        self.label_inicio.place(x=215, y=50)
      
    def componentes(self):
        self.texto()

        with LogixDriver('192.168.0.10') as self.micro:
            self.sinal_abastecimento = self.micro.read('SIS_FINALIZANDO')
            print(f"Status da bomba: {self.sinal_abastecimento[1]}")
          
            if self.sinal_abastecimento[1] == True:
                self.label_inicio.destroy()
                self.label_abas = Label(self.main, text="Coletando informações", font="Arial 16")
                self.label_abas.place(x=165, y=50)
                time.sleep(1)
                self.label_abastecendo = Label(self.main, text="Aguarde...", font="Arial 16")
                self.label_abastecendo.place(x=225, y=90)
                time.sleep(1)
                self.conecta_clp()
                time.sleep(2)
                #km_novo = self.micro.write('SP_KM',km2)
                #bool2 = self.micro.write('Grava', False)
                self.micro.close()
                self.componentes()
                time.sleep(10)
            else:
                self.micro.close()
                time.sleep(3)
                self.componentes()
              
    def conecta_clp(self):
        id_motorista = self.micro.read('ID_MOT_FORM')
        id_motorista2 = id_motorista[1].replace('\x00', '')
        km_form = self.micro.read('KM_FORM')
        km_form2 = km_form[1].replace('\x00', '')
        placa_form = self.micro.read('PLACA_FORM')
        placa_form2 = placa_form[1].replace('\x00', '')
        qtd_litros_abastecido = self.micro.read('QTD_LITROS_ABASTECIDO')
        qtd_litros_abastecido2 = str(qtd_litros_abastecido[1])
        tanque_cheio = self.micro.read('TANQUE_CHEIO')
        tanque_cheio2 = tanque_cheio[1]
        tanque_cheio3 = ""
      
        if tanque_cheio2 == True:
            tanque_cheio3 = "SIM"
        else:
            tanque_cheio3 = "NAO"

        with open('Names.csv', 'a') as csvfile:
            csvfile.write(",".join([id_motorista2, km_form2, placa_form2, qtd_litros_abastecido2, tanque_cheio3,'\n']))
          
        self.gerar_xml()
        #var_string = micro.write('Placa_Caminhao1', self.placa_completa)
        # var = micro.read('Placa_Caminhao')
  
    def gerar_xml(self):
        f = open('Names.csv')
        csv_f = csv.reader(f)
        data = []

        for row in csv_f:
            data.append(row)
        f.close()
      
        with open('output.xml') as myfile:
            total_lines = sum(1 for line in myfile)

        linha_especifica = total_lines - 1
        print(linha_especifica)
        texto = """     <abastecimento>
            <ID_MOTORISTA>%s</ID_MOTORISTA>
            <KM>%s</KM>
            <PLACA>%s</PLACA>
            <LITROS>%s</LITROS>
            <TANQUE_CHEIO>%s</TANQUE_CHEIO>
    </abastecimento> \n """ % (row[0], row[1], row[2], row[3], row[4])

        file = open('output.xml', 'r')
        lines = file.readlines()
        file.close()
        lines.insert(linha_especifica, texto + "\n")
        file = open('output.xml', 'w')
        file.writelines(lines)
        file.close()
        self.imgrodape = PhotoImage(file="bomba_suc.png")
        self.l_rodape = Label(self.main, image=self.imgrodape)
        self.l_rodape.place(x=220, y=160)
        self.micro.write('FINALIZA_PYTON', True)
        time.sleep(3)
        self.label_abas.destroy()
        self.label_abastecendo.destroy()
        self.l_rodape.destroy()
        self.micro.close()
      
    def __init__(self):
        self.main = Tk()
        self.main.title('Controle de Combustível')
        self.main.geometry('550x400')
        threading.Thread(target=self.componentes).start()
        self.main.mainloop()

if __name__== "__main__":

    Tela()

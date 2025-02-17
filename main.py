# Importando bibliotecas necessárias
import random
from twilio.rest import Client
import customtkinter as ctk
from tkinter import messagebox
import dev  # Importando as credenciais


class VerificacaoSMS(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela
        self.title("Verificação por SMS")
        self.geometry("400x500")
        self.configure(fg_color="#2b2b2b")
        
        # Variáveis
        self.codigo = None
        
        # Criando widgets
        self.criar_widgets()
        
    def criar_widgets(self):
        # Título
        ctk.CTkLabel(self, 
                     text="Verificação por SMS",
                     font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Frame para entrada do número
        self.frame_numero = ctk.CTkFrame(self)
        self.frame_numero.pack(pady=20, padx=40, fill="x")
        
        self.entrada_numero = ctk.CTkEntry(
            self.frame_numero,
            placeholder_text="Digite seu número (+5511999999999)",
            width=300)
        self.entrada_numero.pack(pady=10)
        
        # Botão enviar código
        self.btn_enviar = ctk.CTkButton(
            self,
            text="Enviar Código",
            command=self.enviar_codigo,
            width=200)
        self.btn_enviar.pack(pady=10)
        
        # Frame para verificação
        self.frame_verificacao = ctk.CTkFrame(self)
        self.frame_verificacao.pack(pady=20, padx=40, fill="x")
        self.frame_verificacao.pack_forget()
        
        self.entrada_codigo = ctk.CTkEntry(
            self.frame_verificacao,
            placeholder_text="Digite o código recebido",
            width=300)
        self.entrada_codigo.pack(pady=10)
        
        self.btn_verificar = ctk.CTkButton(
            self.frame_verificacao,
            text="Verificar Código",
            command=self.verificar_codigo,
            width=200)
        self.btn_verificar.pack(pady=10)
        
        # Label para tentativas
        self.label_tentativas = ctk.CTkLabel(
            self,
            text="Tentativas restantes: 3")
        self.label_tentativas.pack()
        self.label_tentativas.pack_forget()
        
        self.tentativas = 3

    def enviar_codigo(self):
        numero = self.entrada_numero.get()
        self.codigo = gerar_codigo_verificacao()
        mensagem = f"Seu código de verificação é: {self.codigo}"
        
        if enviar_sms(numero, mensagem):
            messagebox.showinfo("Sucesso", "Código enviado com sucesso!")
            self.frame_verificacao.pack(pady=20, padx=40, fill="x")
            self.label_tentativas.pack()
            self.btn_enviar.configure(state="disabled")
        else:
            messagebox.showerror("Erro", "Falha ao enviar o código")
    
    def verificar_codigo(self):
        codigo_usuario = self.entrada_codigo.get()
        
        if codigo_usuario == self.codigo:
            messagebox.showinfo("Sucesso", "Número verificado com sucesso!")
            self.destroy()
        else:
            self.tentativas -= 1
            self.label_tentativas.configure(text=f"Tentativas restantes: {self.tentativas}")
            
            if self.tentativas > 0:
                messagebox.showwarning("Erro", f"Código incorreto. Você tem mais {self.tentativas} tentativas.")
            else:
                messagebox.showerror("Erro", "Número máximo de tentativas excedido.")
                self.destroy()

def gerar_codigo_verificacao():
    """Gera um código de verificação de 6 dígitos"""
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

def enviar_sms(numero_telefone, mensagem):
    """
    Função para enviar SMS usando Twilio
    
    Parâmetros:
    numero_telefone (str): Número do telefone no formato +5511999999999
    mensagem (str): Mensagem a ser enviada
    """
    try:
        # Criando cliente Twilio usando as credenciais do dev.py
        client = Client(dev.TWILIO_ACCOUNT_SID, dev.TWILIO_AUTH_TOKEN)
        
        # Enviando mensagem
        message = client.messages.create(
            body=mensagem,
            from_=dev.TWILIO_PHONE_NUMBER,
            to=numero_telefone
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar SMS: {e}")
        return False

if __name__ == "__main__":
    # Para usar o sistema, primeiro instale as bibliotecas:
    # pip install twilio customtkinter
    
    app = VerificacaoSMS()
    app.mainloop()

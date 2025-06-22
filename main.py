import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

# Cargar API key desde .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Leer y extraer texto del PDF
def leer_pdf(ruta):
    texto = ""
    with fitz.open(ruta) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto.strip()

# Preguntar al modelo de Hugging Face con enfoque en NCs
def generar_respuesta_nc(contexto, no_conformidad):
    prompt = (
        "[INST] Eres un experto técnico en certificación de proyectos de I+D. "
        "A partir del siguiente texto extraído de una memoria técnica, redacta una respuesta formal, completa e impersonal que responda claramente a la siguiente no conformidad o requerimiento de la certificadora."
        "\n\nMEMORIA:\n" + contexto +
        "\n\nNO CONFORMIDAD:\n" + no_conformidad +
        "\n\nRESPUESTA: [/INST]"
    )

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.4, "max_new_tokens": 1000}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].split("RESPUESTA:")[-1].strip()
        else:
            return "[Error]: Respuesta inesperada."
    except Exception as e:
        return f"[Error]: {str(e)}"

# Interfaz
contexto_pdf = ""

def cargar_pdf():
    global contexto_pdf
    ruta = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if ruta:
        contexto_pdf = leer_pdf(ruta)
        messagebox.showinfo("Éxito", "PDF cargado correctamente.")

def enviar_nc():
    global contexto_pdf
    nc_text = entrada_nc.get("1.0", tk.END).strip()
    if not nc_text:
        messagebox.showwarning("Aviso", "Por favor, escribe la no conformidad a responder.")
        return
    if not contexto_pdf:
        messagebox.showwarning("Aviso", "Primero carga un archivo PDF.")
        return

    texto_respuesta.config(state="normal")
    texto_respuesta.delete("1.0", tk.END)
    texto_respuesta.insert(tk.END, "Generando respuesta...")
    texto_respuesta.update()

    respuesta = generar_respuesta_nc(contexto_pdf, nc_text)

    texto_respuesta.delete("1.0", tk.END)
    texto_respuesta.insert(tk.END, respuesta)
    texto_respuesta.config(state="disabled")

# GUI
ventana = tk.Tk()
ventana.title("Respuestas a No Conformidades - Proyectos I+D")
ventana.geometry("800x600")

frame_pdf = ttk.Frame(ventana)
frame_pdf.pack(pady=10)

btn_cargar = ttk.Button(frame_pdf, text="Cargar Memoria (PDF)", command=cargar_pdf)
btn_cargar.pack()

ttk.Label(ventana, text="No Conformidad o Pregunta de la Certificadora:").pack()
entrada_nc = tk.Text(ventana, height=6)
entrada_nc.pack(fill="x", padx=10)

ttk.Button(ventana, text="Generar Respuesta", command=enviar_nc).pack(pady=10)

ttk.Label(ventana, text="Respuesta generada:").pack()
texto_respuesta = tk.Text(ventana, height=20, state="disabled", wrap="word")
texto_respuesta.pack(fill="both", expand=True, padx=10, pady=5)

ventana.mainloop()

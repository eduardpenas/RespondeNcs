# RespondeNC – Generador de Respuestas a No Conformidades en Proyectos I+D

Este programa permite generar respuestas técnicas automáticas a no conformidades o requerimientos que emite una certificadora, a partir del contenido de memorias técnicas en PDF. Usa inteligencia artificial (modelo Mistral Instruct 7B alojado en Hugging Face) para sintetizar la información del documento y generar una respuesta clara, formal y fundamentada.

## 🧠 ¿Para qué sirve?

Ideal para empresas que gestionan proyectos de I+D y desean:

- Reducir devoluciones de las certificadoras.
- Ahorrar tiempo redactando respuestas técnicas.
- Justificar aspectos como salto tecnológico, interoperabilidad, sostenibilidad, etc.

## 🚀 Funcionalidades

- Interfaz gráfica sencilla en Tkinter.
- Carga de memorias técnicas en PDF.
- Entrada de la no conformidad (o requerimiento).
- Generación automática de una respuesta técnica y redactada.
- Integración con modelo Mistral-7B Instruct (Hugging Face).

## 🛠️ Requisitos

- Python 3.10 o superior
- Cuenta gratuita en [Hugging Face](https://huggingface.co/)
- Token de acceso de Hugging Face (tipo `hf_xxx`)

## 📦 Instalación

1. Clona este repositorio o descarga los archivos:

```bash
git clone https://github.com/tuusuario/responde-nc.git
cd responde-nc

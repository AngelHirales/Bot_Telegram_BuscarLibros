#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import logging
import pyodbc
import Levenshtein
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Database connection
def connect_db():
    server = 'LAPODEROSA\\SQLEXPRESS'
    database = 'Biblioteca'

    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("🛠️Instrucciones de uso:🛠️\n"
                                    "Este bot está diseñado para ayudar al usuario a buscar libros de dos maneras:\n\n"
                                    "1. Búsqueda por título:\n        Escribe 'buscar - título del libro'.\n"
                                    "Ejemplo: buscar - el alquimista\n\n"
                                    "2. Búsqueda por autor:\n        Escribe 'autor - nombre del autor'.\n"
                                    "Ejemplo: autor - Miguel de Cervantes\n\n"
                                    "También, puedes utilizar los siguientes comandos:\n\n"
                                    "/menu - abre un menú con las opciones disponibles para un uso más cómodo\n"
                                    "/librerias - muestra un enlace para ver las librerías de Ensenada\n\n"
                                    "¡Esperamos que encuentres lo que buscas!")

async def librerias_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the link to libraries in Ensenada."""
    maps_link = "https://www.google.com/maps/search/librerías+Ensenada"
    await update.message.reply_text(f"Aquí tienes un enlace para ver las librerías en Ensenada: {maps_link}")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the menu options."""
    keyboard = [
        [InlineKeyboardButton('Busqueda por Titulo', callback_data='busqueda_titulo')],
        [InlineKeyboardButton('Busqueda por Autor', callback_data='busqueda_autor')],
        [InlineKeyboardButton('Ver librerias', callback_data='ver_librerias')],
        [InlineKeyboardButton('Contactanos', callback_data='contactanos')],
        [InlineKeyboardButton('Salir', callback_data='salir')]
    ]
    menu_choices = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Menu de opciones:", reply_markup=menu_choices)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    mensaje = update.message.text

    # List of bad words
    groserias = ['estupido','estupida',
                 'tonto', 'tonta',
                 'nigga']

    # Check for bad words
    if any(groseria in mensaje.lower() for groseria in groserias):
        await update.message.reply_text("NO SEA GROSERO!!")
        return

    if mensaje.lower() == 'hola':
        mensaje = ("Hola soy tu asistente de búsqueda de libros, "
                   "Por favor revisa las instrucciones de uso con el comando: /ayuda\n\n"
                   "Si ya estás listo puedes comenzar a usar el bot!")

    elif mensaje.startswith('buscar - '):
        query = mensaje[9:].lower()
        db = connect_db()
        try:
            with db.cursor() as cursor:
                sql = "SELECT * FROM Tabla_libros"
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                # Find the closest match using Levenshtein distance
                best_match = None
                min_distance = float('inf')
                
                for row in rows:
                    distance = Levenshtein.distance(query, row.titulo.lower())
                    if distance < min_distance:
                        min_distance = distance
                        best_match = row
                
                maps_link = "https://www.google.com/maps/search/librerías+Ensenada" 
                
                if best_match:
                    mensaje = (f"Titulo: {best_match.titulo}\n"
                               f"Autor: {best_match.autor}\n"
                               f"Genero: {best_match.genero}\n"
                               f"Editorial: {best_match.editorial}\n"
                               f"Año: {best_match.año}\n"
                               f"{best_match.portada}\n\n"          
                               f"podrias encontrar el libro en alguna de estas Librerias: ({maps_link})")
                else:
                    mensaje = "No se encontraron resultados para tu búsqueda."
        except Exception as e:
            mensaje = f"Error al buscar en la base de datos: {e}"
        finally:
            db.close()

    elif mensaje.startswith('autor - '):
        query = mensaje[8:].lower()
        db = connect_db()
        try:
            with db.cursor() as cursor:
                sql = "SELECT * FROM Tabla_libros"
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                # encotrar coincidencias en los nombres usando Levenshtein
                best_match = None
                min_distance = float('inf')
                
                for row in rows:
                    distance = Levenshtein.distance(query, row.autor.lower())
                    if distance < min_distance:
                        min_distance = distance
                        best_match = row

                maps_link = "https://www.google.com/maps/search/librerías+Ensenada" 
                
                if best_match:
                    mensaje = (f"Titulo: {best_match.titulo}\n"
                               f"Autor: {best_match.autor}\n"
                               f"Genero: {best_match.genero}\n"
                               f"Editorial: {best_match.editorial}\n"
                               f"Año: {best_match.año}\n"
                               f"{best_match.portada}\n\n"          
                               f"podrias encontrar el libro en alguna de estas Librerias: ({maps_link})")
                else:
                    mensaje = "No se encontraron resultados para tu búsqueda."
        except Exception as e:
            mensaje = f"Error al buscar en la base de datos: {e}"
        finally:
            db.close()
    
    else:
        mensaje = "Aún no estoy programado para eso"

    await update.message.reply_text(mensaje)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button press from inline keyboard."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'busqueda_titulo':
        mensaje = "1. Búsqueda por título:\n        Escribe 'buscar - título del libro'.\n"

    elif query.data == 'busqueda_autor':
        mensaje = "2. Búsqueda por autor:\n        Escribe 'autor - nombre del autor'.\n"

    elif query.data == 'ver_librerias':
        maps_link = "https://www.google.com/maps/search/librerías+Ensenada"
        mensaje = f"Aquí tienes un enlace para ver las librerías en Ensenada: [enlace]({maps_link})"
        await query.edit_message_text(text=mensaje, parse_mode='Markdown')
        return
    
    elif query.data == 'contactanos':
        mensaje = "Para contactarnos, por favor envía un correo con tu duda/sugerencia a libro_bot@correo.com."
    
    elif query.data == 'salir':
        mensaje = "Gracias por usar el bot de búsqueda de libros. ¡Nos vemos luego!"

    await query.edit_message_text(text=mensaje)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("tu_token_bot_aqui").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", ayuda_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("librerias", librerias_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # on callback from inline buttons
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until you send a signal with Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()

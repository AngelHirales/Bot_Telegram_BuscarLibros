# Bot_Telegram_BuscarLibros
### Este proyecto es un bot de telegram que ayuda al usuario a realizar busquedas de libros en una base de datos 

## Para usarlo debes tener en cuenta esto:
#### - El lenguaje utilizado es python 3.12
#### - Para la base de datos de uso SQL Server Managment Studiom (2019)
#### - Telegram

## Para usar el codigo debes:
#### - Tener instalado python
#### - Tener instalado SQL Server o Algun otro SGDB que prefieras usar
#### - instalar las librerias de:
### pyodbc
```bash
pip install pyodbc
```
### Levenshtein
```bash
pip install python-Levenshtein
```
### telegram:
```bash
pip install python-telegram-bot
```

### En esta seccion del codigo cambia los datos a la de tu instancia de SQL
```bash
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
```

### En el main cambia la clave por la de tu bot de telegram
```bash
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("tu_clave_de_bot").build()

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
```

## Una vez que ya tengas todo listo solo crea o descarga mi base de datos y agrega o borra los libros de tu preferencia
## Despues solo pruebalo y diviertete!

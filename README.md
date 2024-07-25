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

### Para la creacion de ka tabla se uso la siguiente estructura
```bash
USE Biblioteca;

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Tabla_libros' AND xtype='U')
CREATE TABLE Tabla_libros (
    id INT PRIMARY KEY,
    titulo VARCHAR(255),
    genero VARCHAR(255),
    autor VARCHAR(255),
    editorial VARCHAR(255),
    año INT,
    portada VARCHAR(255)
);

INSERT INTO Tabla_libros (id, titulo, genero, autor, editorial, año, portada) VALUES
(1, 'El Alquimista', 'Búsqueda, Ficción de aventuras, Realismo mágico, Literatura fantástica', 'Paulo Coelho', 'Editorial del libro', 1988, 'https://proassetspdlcom.cdnstatics2.com/usuaris/libros/fotos/201/original/portada_el-alquimista_paulo-coelho_201612191218.jpg'),
(2, 'Cien años de soledad', 'Novela, Realismo mágico, Literatura latinoamericana', 'Gabriel García Márquez', 'Editorial Sudamericana', 1967, 'https://www.planetadelibros.com/usuaris/libros/fotos/50/m_libros/portada_cien-anos-de-soledad_gabriel-garcia-marquez_201711291655.jpg'),
(3, '1984', 'Distopía, Ciencia ficción, Política, Literatura inglesa', 'George Orwell', 'Secker & Warburg', 1949, 'https://images-na.ssl-images-amazon.com/images/I/41E9pyd9QBL._SX324_BO1,204,203,200_.jpg'),
(4, 'Don Quijote de la Mancha', 'Novela, Aventura, Literatura española, Satira', 'Miguel de Cervantes', 'Francisco de Robles', 1605, 'https://www.planetadelibros.com/usuaris/libros/fotos/71/m_libros/portada_don-quijote-de-la-mancha_miguel-de-cervantes_201605041619.jpg');

```

### Una vez que ya tengas todo listo solo crea o descarga mi base de datos y agrega o borra los libros de tu preferencia
## Despues solo pruebalo y diviertete!

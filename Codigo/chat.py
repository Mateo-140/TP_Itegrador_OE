import os
import logging
import sqlite3
from dotenv import load_dotenv
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import bot

# Configuración de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
ID_JEFE = int(os.getenv("ID_JEFE")) 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id_usuario = update.message.chat_id
    bot.guardar_estado(id_usuario, "INICIO")
    user_info = bot.consultar_saldo(id_usuario)
    
    if user_info:
        await update.message.reply_text(
            f"Hola {user_info[1]}. Bienvenido al Sistema de Autogestión de RRHH.\n"
            f"Tienes {user_info[0]} días de vacaciones disponibles.\n"
            "Para iniciar una solicitud, usa el comando /solicitar"
        )
    else:
        await update.message.reply_text("Error: Tu usuario no está registrado en el sistema de la empresa.")

async def solicitar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id_usuario = update.message.chat_id
    estado = bot.obtener_estado(id_usuario)
    
    if estado == "INICIO":
        bot.guardar_estado(id_usuario, "ESPERANDO_DIAS")
        await update.message.reply_text("Por favor, ingresa la cantidad de días de vacaciones que necesitas:")
    else:
        await update.message.reply_text("Ya tienes un proceso en curso. Usa /start para reiniciar.")

async def procesar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id_usuario = update.message.chat_id
    texto_recibido = update.message.text
    estado = bot.obtener_estado(id_usuario)
    
    if estado == "ESPERANDO_DIAS":
        if not texto_recibido.isdigit():
            await update.message.reply_text("❌ Entrada inválida. Debes ingresar un número entero.). Inténtalo de nuevo:")
            return
        
        dias_pedidos = int(texto_recibido)
        saldo_disponible, nombre = bot.consultar_saldo(id_usuario)
        
        if dias_pedidos > saldo_disponible:
            await update.message.reply_text(
                f"❌ Solicitud Denegada (Saldo Insuficiente).\n"
                f"Pediste {dias_pedidos} días pero solo dispones de {saldo_disponible}.\n"
                "El proceso ha finalizado. Puedes iniciar uno nuevo con /solicitar"
            )
            bot.guardar_estado(id_usuario, "INICIO")
        else:
            # --- LÓGICA DE APROBACIÓN AUTOMÁTICA ---
            # 1. Registramos la solicitud directamente
            id_sol = bot.registrar_solicitud(id_usuario, dias_pedidos)
            
            # 2. Conectamos a la BD para pasarla a APROBADO y restar los días al toque
            conn = sqlite3.connect('recursos_humanos.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE solicitudes SET estado = 'APROBADO' WHERE id_solicitud = ?", (id_sol,))
            cursor.execute("UPDATE empleados SET dias_disponibles = dias_disponibles - ? WHERE id_telegram = ?", (dias_pedidos, id_usuario))
            conn.commit()
            conn.close()
            
            # 3. Le avisamos al empleado que ya está aprobado por defecto
            await update.message.reply_text(
                f"🎉 ¡Solicitud Aprobada Automáticamente!\n\n"
                f"Como disponías de saldo, la solicitud #{id_sol} por {dias_pedidos} días fue procesada.\n"
                f"Disfrutá tus vacaciones."
            )
            
            # 4.  Al jefe solo se le manda un mensaje informativo
            await context.application.bot.send_message(
                chat_id=ID_JEFE,
                text=f"📢 NOTIFICACIÓN DE RRHH\n\n"
                     f"El empleado {nombre} solicitó {dias_pedidos} días.\n"
                     f"Se aprobó automáticamente (Solicitud #{id_sol})."
            )
            
            # Reseteamos el estado del bot para que pueda volver a usar comandos
            bot.guardar_estado(id_usuario, "INICIO")


def main():
    bot.inicializar_bd()
    
    # Estructura de inicialización 
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("solicitar", solicitar))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensajes))

    print("Bot de simulación moderno corriendo con éxito...")
    application.run_polling()

if __name__ == '__main__':
    main()

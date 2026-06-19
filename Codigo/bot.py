import sqlite3

def inicializar_bd():
    conn = sqlite3.connect('recursos_humanos.db')
    cursor = conn.cursor()
    
    # Tabla de Empleados (Corregida: se quitó el NOT EXISTS erróneo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id_telegram INTEGER PRIMARY KEY,
            nombre TEXT,
            dias_disponibles INTEGER
        )
    ''')
    
    # Tabla para la Máquina de Estados del Bot
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estados_bot (
            id_telegram INTEGER PRIMARY KEY,
            estado_actual TEXT
        )
    ''')
    
    # Tabla de solicitudes de vacaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
            id_telegram INTEGER,
            cantidad_dias INTEGER,
            estado TEXT DEFAULT 'PENDIENTE'
        )
    ''')
    
    # IMPORTANTE: Cambiá el 12345678 por tu ID real de Telegram que te dio el @userinfobot
    cursor.execute("INSERT OR IGNORE INTO empleados VALUES (973763325, 'Mateo Peralta', 14)")
    
    conn.commit()
    conn.close()

def obtener_estado(id_telegram):
    conn = sqlite3.connect('recursos_humanos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT estado_actual FROM estados_bot WHERE id_telegram = ?", (id_telegram,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else "INICIO"

def guardar_estado(id_telegram, nuevo_estado):
    conn = sqlite3.connect('recursos_humanos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO estados_bot (id_telegram, estado_actual) VALUES (?, ?)", (id_telegram, nuevo_estado))
    conn.commit()
    conn.close()

def consultar_saldo(id_telegram):
    conn = sqlite3.connect('recursos_humanos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT dias_disponibles, nombre FROM empleados WHERE id_telegram = ?", (id_telegram,))
    res = cursor.fetchone()
    conn.close()
    return res # Retorna tupla (dias, nombre) o None

def registrar_solicitud(id_telegram, dias):
    conn = sqlite3.connect('recursos_humanos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO solicitudes (id_telegram, cantidad_dias) VALUES (?, ?)", (id_telegram, dias))
    conn.commit()
    id_solicitud = cursor.lastrowid
    conn.close()
    return id_solicitud
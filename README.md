# TP_Itegrador_OE
# Sistema de Autogestión de RRHH - Bot de Telegram 🤖📊

![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)
![SQLite](https://img.shields.io/badge/database-SQLite3-lightgrey.svg)
![API](https://img.shields.io/badge/API-Telegram%20Bot%20v20.x-green.svg)

Este proyecto consiste en un **Bot de Telegram asincrónico** conectado a una base de datos relacional local (SQLite), diseñado para automatizar y optimizar el proceso de solicitud y control de licencias por vacaciones dentro de una organización. El sistema aplica reglas de negocio automatizadas utilizando un modelo de **Máquina de Estados Finitos (FSM)**.

---

## 🚀 Características Clave

- **Consulta de Saldo 24/7:** El empleado puede verificar instantáneamente sus días de vacaciones disponibles.
- **Aprobación Automática Autónoma:** Si el empleado cuenta con saldo suficiente, el sistema aprueba la solicitud, realiza el descuento en la base de datos y genera una alerta de auditoría para el supervisor en tiempo real.
- **Máquina de Estados Persistente (FSM):** El contexto de la conversación se almacena en la base de datos, garantizando tolerancia a fallos (si el script se reinicia, el bot no sufre "amnesia").
- **Compatibilidad de Vanguardia:** Totalmente adaptado para correr de forma nativa en entornos modernos utilizando **Python 3.14**.

---

## 🛠️ Arquitectura de la Base de Datos

El sistema utiliza **SQLite3** (`recursos_humanos.db`) con tres tablas principales interconectadas:

1. **`empleados`**: Datos maestros del personal (`id_telegram`, `nombre`, `dias_disponibles`).
2. **`estados_bot`**: Gestión de persistencia de la FSM (`id_telegram`, `estado_actual`).
3. **`solicitudes`**: Registro histórico y auditoría (`id_solicitud`, `id_telegram`, `cantidad_dias`, `estado`).

---

## ⚙️ Requisitos e Instalación

### 1. Clonar el repositorio y posicionarse en la carpeta
```bash
cd Codigo_TP_OE

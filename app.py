from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import smtplib
import sqlite3 # <-- Para manejar la base de datos
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='static')
# Necesitamos una 'secret_key' para manejar sesiones de login de forma segura
app.secret_key = os.getenv("SECRET_KEY", "una-llave-secreta-muy-dificil-de-adivinar")

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect('bammind_crm.db')
    cursor = conn.cursor()
    # Creamos la tabla 'leads' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT,
            empresa TEXT,
            paquete TEXT,
            mensaje TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- RUTAS PÚBLICAS (TU PÁGINA WEB) ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar_formulario():
    data = request.get_json()
    nombre = data.get('nombre')
    email_cliente = data.get('email')
    paquete = data.get('paquete')
    telefono = data.get('telefono')
    empresa = data.get('empresa')
    mensaje = data.get('mensaje', 'No se proporcionó un mensaje.')

    # TAREA 1: Guardar en la base de datos (nuestro CRM)
    try:
        conn = sqlite3.connect('bammind_crm.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO leads (nombre, email, telefono, empresa, paquete, mensaje) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, email_cliente, telefono, empresa, paquete, mensaje)
        )
        conn.commit()
        conn.close()
        print("Lead guardado en la base de datos con éxito.")
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

    # TAREA 2: Enviar correo de notificación (esto se queda igual)
    try:
        remitente = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        destinatario = os.getenv("RECIPIENT_EMAIL")
        # ... (el resto del código de envío de email se queda igual)
    except Exception as e:
        print(f"Error al enviar correo: {e}")
    
    return jsonify({"status": "success", "message": "Formulario recibido con éxito."})


# --- RUTAS PRIVADAS (TU PANEL DE CRM) ---
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Si el usuario ya inició sesión, lo dejamos pasar
    if 'logged_in' in session and session['logged_in']:
        conn = sqlite3.connect('bammind_crm.db')
        conn.row_factory = sqlite3.Row # Para acceder a los datos por nombre de columna
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leads ORDER BY fecha DESC")
        leads = cursor.fetchall()
        conn.close()
        return render_template('admin.html', leads=leads)

    # Si intenta iniciar sesión
    if request.method == 'POST':
        password = request.form['password']
        if password == os.getenv("ADMIN_PASSWORD"):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Contraseña incorrecta")
    
    # Si no ha iniciado sesión, le mostramos la pantalla de login
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

# Al iniciar la aplicación, nos aseguramos que la base de datos exista
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
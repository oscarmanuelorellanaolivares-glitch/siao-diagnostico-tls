import os
import ssl
import streamlit as st

st.title("Diagnóstico TLS - Entorno Streamlit")

rutas = [
    "/usr/lib/ssl/cert.pem",
    "/etc/ssl/certs/ca-certificates.crt",
]

for ruta in rutas:
    st.write(f"{ruta}: {'Disponible' if os.path.isfile(ruta) else 'No disponible'}")

st.write("OpenSSL:", ssl.OPENSSL_VERSION)

st.divider()
st.subheader("Diagnóstico de conexión PostgreSQL")

import psycopg
from urllib.parse import urlsplit, parse_qs

if "DATABASE_URL" not in st.secrets:
    st.warning("DATABASE_URL no está configurada en esta aplicación.")
else:
    url = st.secrets["DATABASE_URL"]
    parametros = parse_qs(urlsplit(url).query)

    st.write("Configuración SSL:", parametros.get("sslmode", ["No definido"])[0])
    st.write("Certificado configurado:", "sslrootcert" in parametros)

    if st.button("Comprobar conexión segura"):
        try:
            with psycopg.connect(
                url,
                connect_timeout=10,
                options="-c default_transaction_read_only=on",
            ) as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()

            st.success("Conexión PostgreSQL establecida correctamente.")

        except Exception as error:
            st.error("No se pudo establecer la conexión.")
            st.write("Tipo de error:", type(error).__name__)
            st.write(
                "Código SQLSTATE:",
                getattr(error, "sqlstate", None) or "No disponible"
            )

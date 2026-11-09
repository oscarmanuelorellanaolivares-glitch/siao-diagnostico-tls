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

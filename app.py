import os
os.environ["STREAMLIT_WATCHDOG_DISABLE"] = "true"
import streamlit as st
from pymongo import MongoClient

# Leer secretos desde secrets.toml
uri = st.secrets["mongo"]["uri"]
db_name = st.secrets["mongo"]["database"]
collection_name = st.secrets["mongo"]["collection"]

# Conectar con MongoDB
client = MongoClient(uri)
db = client[db_name]
collection = db[collection_name]

st.title("📋 CRUD con Streamlit + MongoDB")

# --- CREATE ---
st.subheader("Agregar nueva tarea")
titulo = st.text_input("Título de la tarea")
descripcion = st.text_area("Descripción")

if st.button("Agregar"):
    if titulo:
        collection.insert_one({"titulo": titulo, "descripcion": descripcion})
        st.success("✅ Tarea agregada con éxito")
    else:
        st.warning("⚠️ Escribe un título antes de agregar")

# --- READ ---
st.subheader("Lista de tareas")
tareas = list(collection.find())

for tarea in tareas:
    st.write(f"**{tarea['titulo']}** — {tarea.get('descripcion', '')}")

# --- UPDATE ---
st.subheader("Actualizar tarea")
tareas_nombres = [t["titulo"] for t in tareas]
if tareas_nombres:
    seleccion = st.selectbox("Selecciona tarea", tareas_nombres)
    nuevo_texto = st.text_input("Nuevo título")
    if st.button("Actualizar"):
        collection.update_one({"titulo": seleccion}, {"$set": {"titulo": nuevo_texto}})
        st.success("✏️ Tarea actualizada")

# --- DELETE ---
st.subheader("Eliminar tarea")
if tareas_nombres:
    borrar = st.selectbox("Selecciona tarea a eliminar", tareas_nombres, key="delete")
    if st.button("Eliminar"):
        collection.delete_one({"titulo": borrar})
        st.error("🗑️ Tarea eliminada")


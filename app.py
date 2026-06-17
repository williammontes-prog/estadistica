import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análisis de Frecuencias", layout="wide")

st.title("📊 Generador de Tablas de Frecuencia y Gráficos")

# Cargar archivo
archivo = st.file_uploader(
    "Seleccione un archivo CSV o Excel",
    type=["csv", "xlsx"]
)

if archivo is not None:

    # Leer archivo
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        st.success("Archivo cargado correctamente")

        st.subheader("Vista previa del Dataset")
        st.dataframe(df.head())

        # Seleccionar columna
        columna = st.selectbox(
            "Seleccione una columna para analizar",
            df.columns
        )

        if columna:

            st.subheader(f"Tabla de Frecuencias - {columna}")

            frecuencia = (
                df[columna]
                .value_counts(dropna=False)
                .reset_index()
            )

            frecuencia.columns = ["Valor", "Frecuencia"]

            frecuencia["Frecuencia Relativa (%)"] = (
                frecuencia["Frecuencia"]
                / frecuencia["Frecuencia"].sum()
                * 100
            ).round(2)

            frecuencia["Frecuencia Acumulada"] = (
                frecuencia["Frecuencia"].cumsum()
            )

            st.dataframe(frecuencia)

            # Descargar tabla
            csv = frecuencia.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Descargar Tabla de Frecuencias",
                csv,
                file_name=f"frecuencia_{columna}.csv",
                mime="text/csv"
            )

            # Gráfico de barras
            st.subheader("Gráfico de Barras")

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.bar(
                frecuencia["Valor"].astype(str),
                frecuencia["Frecuencia"]
            )

            ax.set_title(f"Frecuencia de {columna}")
            ax.set_xlabel(columna)
            ax.set_ylabel("Frecuencia")

            plt.xticks(rotation=45)

            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

else:
    st.info("Cargue un archivo para comenzar.")
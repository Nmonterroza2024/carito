import streamlit as st
st.set_page_config(page_title="Ingresos por Departamento", layout="wide")
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import seaborn as sns
import plotly.express as px


col1, col2 = st.columns([1, 1])

with col1:
    st.title("Análisis de datos de ingreso a CINTIA para el periodo 2024-2.")

with col2:
    st.image("CINTIA-LOGO.png", width=150)

with st.expander("📊Objetivo del análisis"):
    st.write(
            "Visualizar  los indicadores clave de la plataforma CINTIA de manera eficiente, facilitando la automatización de los informes semestrales y mejorando la toma de decisiones en base al uso de los recursos académicos por parte de estudiantes y profesores.")

st.expander("x")

with st.expander("Introducción"):
    st.write(
            "El Centro de Innovación en TIC para Apoyo a la Academia (CINTIA), que forma parte de la Vicerrectoría Académica, fue establecido con el objetivo de apoyar los procesos fundamentales de la institución. Su actividad se enfoca en la integración, el uso pedagógico, la apropiación, la investigación y la innovación en Tecnologías de la Información y la Comunicación (TIC). Todo ello se enmarca dentro de una estrategia institucional diseñada para mejorar la calidad de los procesos de enseñanza, investigación y extensión.")

st.expander("x")

col3, col4 = st.columns(2)
with col3:
        st.write("**Presentado por:** Ana Carolina Florez Cleto")
with col4:
        st.write("**Fuentes de datos:** Bases de datos de estudiantes y profesores.")
st.title("Indicadores de uso de la plataforma Cintia")
df =pd.read_csv("ingresos_plataforma_2024_2.csv", sep=';')

total_ingresos = len(df)
df_docentes = df[df['id'].notna()]
ingresos_docentes = len(df_docentes)

# Título
st.title("Análisis de Ingresos")

# Crear columnas con tarjetas de resumen
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total de Ingresos", value=total_ingresos)

with col2:
    st.metric(label="Ingresos por Docentes", value=ingresos_docentes)

total_ingresos = len(df)
# Solo para asegurarnos: convierte la columna a tipo fecha
df['timecreated'] = pd.to_datetime(df['timecreated'], errors='coerce')

df['mes_anio'] = df['timecreated'].dt.strftime('%b')

# Traducir meses al español
meses_traduc = {
    'Jan': 'Ene', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'May', 'Jun': 'Jun',
    'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dic'
}
df['mes_anio'] = df['mes_anio'].replace(meses_traduc, regex=True)

ingresos_por_mes = df['mes_anio'].value_counts().sort_index()


# --- Datos base ---
ingresos_por_mes = df['mes_anio'].value_counts().sort_index()
sizes = ingresos_por_mes.values
labels = ingresos_por_mes.index

# --- Paleta de colores pastel personalizada ---
colores_pastel = [
    "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFADAD", "#CAFFBF",
    "#FDFFB6", "#9BF6FF", "#FFDAC1", "#D0F4DE", "#F1C0E8"
]

# Asegurar que haya suficientes colores
while len(colores_pastel) < len(sizes):
    colores_pastel += colores_pastel

# --- Explode (separación de porciones) ---
explode = [0.05] * len(sizes)

df['timecreated'] = pd.to_datetime(df['timecreated'], errors='coerce')
df = df[df['timecreated'].notna()]
df['semana'] = df['timecreated'].dt.strftime('%U')

# Agrupar por semana y ordenar
ingresos_por_semana = df['semana'].dropna().value_counts().sort_index()
semanas = ingresos_por_semana.index.tolist()
valores = ingresos_por_semana.values.tolist()

# Paleta pastel
colores_pastel = [
    "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFADAD", "#CAFFBF",
    "#FDFFB6", "#9BF6FF", "#FFDAC1", "#D0F4DE", "#F1C0E8"
]

while len(colores_pastel) < len(semanas):
    colores_pastel += colores_pastel

# --- Ingresos por día de la semana (Treemap) ---
dias_ordenados = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
df['dia_semana'] = df['timecreated'].dt.dayofweek.map({
    0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
    3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
})

conteo_dias = df['dia_semana'].value_counts().reindex(dias_ordenados, fill_value=0)
valores_dias = conteo_dias.values
etiquetas = [f"{dia}\n{valor}" for dia, valor in zip(dias_ordenados, valores_dias)]
colores = ["#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFADAD", "#CAFFBF", "#FDFFB6", "#F1C0E8"]

df['timecreated'] = pd.to_datetime(df['timecreated'], errors='coerce')
df = df[df['timecreated'].notna()]  # eliminar filas vacías

# =================== GRAFICO 1: INGRESOS POR DÍA DE LA SEMANA ===================
dias_ordenados = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
df['dia_semana'] = df['timecreated'].dt.dayofweek.map({
    0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
    3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
})
conteo_dias = df['dia_semana'].value_counts().reindex(dias_ordenados, fill_value=0)
valores_dias = conteo_dias.values
etiquetas_dias = [f"{dia}\n{valor}" for dia, valor in zip(dias_ordenados, valores_dias)]
colores_dias = ["#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFADAD", "#CAFFBF", "#FDFFB6", "#F1C0E8"]

df['timecreated'] = pd.to_datetime(df['timecreated'], errors='coerce')
df = df[df['timecreated'].notna()]  # eliminar filas vacías

# =================== GRAFICO 1: INGRESOS POR DÍA DE LA SEMANA ===================
dias_ordenados = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
df['dia_semana'] = df['timecreated'].dt.dayofweek.map({
    0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
    3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
})
conteo_dias = df['dia_semana'].value_counts().reindex(dias_ordenados, fill_value=0)
valores_dias = conteo_dias.values
etiquetas_dias = [f"{dia}\n{valor}" for dia, valor in zip(dias_ordenados, valores_dias)]
colores_dias = ["#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFADAD", "#CAFFBF", "#FDFFB6", "#F1C0E8"]

# =================== GRAFICO 2: INGRESOS POR SEMANA ===================
df['semana'] = df['timecreated'].dt.strftime('%U')
ingresos_por_semana = df['semana'].value_counts().sort_index()
semanas = ingresos_por_semana.index.tolist()
valores_semanas = ingresos_por_semana.values.tolist()

# Asegurar que los colores coincidan
colores_semanas = [
    "#A0C4FF", "#BDB2FF", "#FFC6FF", "#FFADAD", "#CAFFBF",
    "#FDFFB6", "#9BF6FF", "#FFDAC1", "#D0F4DE", "#F1C0E8"
]
while len(colores_semanas) < len(semanas):
    colores_semanas += colores_semanas

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Ingresos por Día (Treemap)")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    squarify.plot(
        sizes=valores_dias,
        label=etiquetas_dias,
        color=colores_dias,
        alpha=0.9,
        edgecolor="white",
        text_kwargs={'fontsize': 10, 'weight': 'bold'},
        ax=ax1
    )
    ax1.set_title("Por Día de la Semana", fontsize=14)
    ax1.axis('off')
    st.pyplot(fig1)

with col2:
    st.subheader("📈 Ingresos por Semana")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(
        semanas,
        valores_semanas,
        color=colores_semanas[:len(semanas)],
        edgecolor='gray',
        linewidth=1
    )
    ax2.set_title("Por Semana del Año", fontsize=14)
    ax2.set_xlabel("Semana")
    ax2.set_ylabel("Ingresos")
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    st.pyplot(fig2)

col1, col2 = st.columns(2)

# -------- GRÁFICO 1: Ingresos por MES (Dona) --------
with col1:
    st.subheader("📆 Ingresos por Mes")
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax1.pie(
        sizes,
        labels=None,
        explode=explode,
        colors=colores_pastel[:len(sizes)],
        autopct=lambda pct: f'{int(round(pct * sum(sizes) / 100))}',
        startangle=90,
        wedgeprops=dict(width=0.5, edgecolor='black', linewidth=1.5)
    )
    ax1.legend(wedges, labels, title="Meses", loc="center left", bbox_to_anchor=(1, 0.5))
    ax1.set_title("Mensual")
    ax1.axis('equal')
    st.pyplot(fig1)

# -------- GRÁFICO 2: Ingresos por SEMANA (Barras) --------
df['timecreated'] = pd.to_datetime(df['timecreated'], errors='coerce')
df['fecha_sin_hora'] = df['timecreated'].dt.date
with col2:
    conteo_por_dia = df['fecha_sin_hora'].value_counts().sort_index()

    # Crear la gráfica interactiva con Plotly para ingresos por día
    fig_time = px.line(x=conteo_por_dia.index, y=conteo_por_dia.values,
                       labels={'x': 'Fecha', 'y': 'Número de Ingresos'},
                       title='Número de Ingresos por Día',
                       template="plotly_white",
                       color_discrete_sequence=px.colors.qualitative.Pastel
                       )
    st.plotly_chart(fig_time, use_container_width=True)

st.title("📌 Información del departamento de matematicas y estditicas")

st.subheader("📚 Ingresos registrados por docentes (filtrados por 'id')")

df.loc[
    df['user_department'].str.contains("Departamento De Matemáticas Y Estadístic|Estadística|ESTADÍSTICA|Matemáticas|MATEMATICA Y ESTADISTICA", case=False, na=False),
    'user_department'
] = "Departamento de Matemáticas y Estadística"
df_ingresos = df.groupby(['idnumber', 'user_department']).size().reset_index(
                name='num_ingresos')
data_filtrada_est_box = df_ingresos[df_ingresos['user_department'] =="Departamento de Matemáticas y Estadística"]
fig_boxplot_est = px.box(data_filtrada_est_box, x='user_department', y='num_ingresos', color='user_department',
                                     title='Distribución de Accesos por Programa (Estudiantes)',
                                     labels={'num_ingresos': 'Accesos a Plataforma', 'user_department': 'Facultad'},
                                     points='outliers', hover_data=['idnumber'],
                                     color_discrete_sequence=[px.colors.qualitative.Pastel[2]])
fig_boxplot_est.update_layout(
                showlegend=False,
                yaxis=dict(visible=True, showticklabels=True),  # Quitar eje Y
                plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
                xaxis=dict(showgrid=False)  # Quitar líneas de fondo del eje X
            )



df['timecreated'] = pd.to_datetime(df['timecreated'], errors='coerce')
df['fecha_sin_hora'] = df['timecreated'].dt.date
df.loc[
    df['user_department'].str.contains("Departamento De Matemáticas Y Estadístic|Estadística|ESTADÍSTICA|Matemáticas|MATEMATICA Y ESTADISTICA", case=False, na=False),
    'user_department'
] = "Departamento de Matemáticas y Estadística"

data_mat = df[df['user_department'] =="Departamento de Matemáticas y Estadística"]
conteo_por_dia = data_mat['fecha_sin_hora'].value_counts().sort_index()

    # Crear la gráfica interactiva con Plotly para ingresos por día
fig_time2 = px.line(x=conteo_por_dia.index, y=conteo_por_dia.values,
                       labels={'x': 'Fecha', 'y': 'Número de Ingresos'},
                       title='Número de Ingresos por Día',
                       template="plotly_white",
                       color_discrete_sequence=px.colors.qualitative.Pastel
                       )



col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_boxplot_est, use_container_width=True)

with col2:
    st.plotly_chart(fig_time2, use_container_width=True)

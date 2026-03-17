import pandas as pd
import streamlit as st
import plotly.express as px


# Carga de los datos

url = 'https://github.com/juliandariogiraldoocampo/ia_taltech/raw/refs/heads/main/aeropuerto/data_sint_oper_pred_clas.csv'

df = pd.read_csv(url)

# Análisis y procesamiento

df_tipo_vuelo = df['TIPO_VUELO'].value_counts().reset_index()
estadisticos = df_tipo_vuelo['count'].describe()
maximo = estadisticos['max']
minimo = estadisticos['min']
media = estadisticos['mean']

# Top 5 aeropuertos con mayor número de operaciones

df_top5_aeropuerto=df['AEROPUERTO_OPERACION'].value_counts().reset_index().head(5)
df_top5_aeropuerto.colums=['AEROPUERTO OPERACION','count']

# Top 10 de rutas con mayor número de operaiones

df['Ruta']=df['ORIGEN']+'→'+df['DESTINO']
df_top10_rutas=df['Ruta'].value_counts().reset_index().head(10)
df_top10_rutas.columns=['RUTA','CANTIDAD']


# CONFIGURACIÓN GENERAL DE LA APLICACIÓN STREAMLIT

# Configuración de la página

st.set_page_config(
    page_title='Operaciones aéreas Colombia',layout='centered',initial_sidebar_state='collapsed')


# Ajuste del ancho máximo del contenedor principal a 1200

st.markdown(
    '''  
    <style>  
        .block-container{
            max-width: 1200px;}  
    </style>
    ''',
    unsafe_allow_html=True
)
paleta_barras=px.colors.qualitative.Antique


# Visualización

# uso de imagen

st.image('encabezado.png',use_container_width=True)

st.title('Datos operacionales')
col1, col2, col3=st.columns(3)

with st.container(border=true)
    with col1:

        st.metric('Máximo', f'{maximo:.0f}',border=True)

    with col2:
        st.metric('Mínimo', f'{minimo:.0f}',border=True)  

    with col3:
        st.metric('Media', f'{media:.0f}',border=True)

with st.expander('Registros 2025 '):
    st.dataframe(df)

with st.expander('Top 5 de aeropuertos con mayor númerro de operaciones'):
    st.dataframe(df_top5_aeropuerto)

with st.expander('Top 10 de rutas con mayor número de operaciones'):
    st.dataframe(df_top10_rutas)

# Salidas gráficas

# Creación de la gráfica

with st.container(border=True):
    col4,col5=st.columns(2)

    with col4:
        #st.dataframe(df_top5_aeropuerto)
        fig_barras=px.bar(
            df_top5_aeropuerto,
            x='AEROPUERTO_OPERACION',
            y='count',
            title='Top 5 aeropuertos con mayor número de operaciones',
            labels={'AEROPUERTO_OPERACION': 'Aeropuerto',
                    'count': 'Número de operaciones'
            },
            color='AEROPUERTO_OPERACION',
            color_discrete_sequence=paleta_barras
        )  
        st.plotly_chart(fig_barras,use_container_width=True) 
    #fig_barras.update_layout(showlegend=False) 


    # st.dataframe(df_top5_aeropuerto)

    with col5:
        df_top10_rutas=df_top10_rutas.sort_values('CANTIDAD',ascending=True)
        fig_rutas=px.bar(
            df_top10_rutas,
            x='CANTIDAD',
            y='RUTA',
            title='Top 10 de rutas con mayor número de operaciones',
            color='CANTIDAD',
            color_continuous_scale='tealgrn'
        )
        fig_rutas.update_layout(showlegend=False) 
        st.plotly_chart(fig_rutas,use_container_width=True)

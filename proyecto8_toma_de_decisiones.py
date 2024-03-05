# %% [markdown]
# # Departamento de marketing - Test A/B
# 
# # Contexto
# Eres analista en una gran tienda en línea. Junto con el departamento de marketing has recopilado una lista de hipótesis que pueden ayudar a aumentar los ingresos. 
# Tienes que priorizar estas hipótesis, lanzar un test A/B y analizar los resultados.

# %% [markdown]
# # Contenido
# 
# * [Objetivos](#objetivos)
# * [Diccionario de Datos](#diccionario)
# * [1 Inicialización](#inicio)
# * [2 Parte 1. Priorizar hipótesis](#hipotheses)
# * [3 Parte 2. Análisis de test A/B](#test)
# 	* [3.1 Ingresos Acumulados por Grupo](#acumulado_ingreso)
# 	* [3.2 Tamaño de Pedido Promedio Acumulado por Grupo](#acumulado_pedido)
# 	* [3.3 Diferencia relativa en el tamaño de pedido promedio acumulado para el grupo B en comparación con el grupo A](#dif_rel_pedidos)
# 	* [3.4 Tasa de conversión de cada grupo como la relación entre los pedidos y el número de visitas de cada día](#conversion_acum)
# 	* [3.5 Tasas de conversión diarias de los dos grupos](#conversion_diaria)
# 	* [3.6 Valores atípicos y aumentos: valores extremos](#atipicos)
# 		* [3.6.1 Gráfico de dispersión del número de pedidos por usuario](#scatter_orders)
# 		* [3.6.2 Gráfico de dispersión de los precios de los pedidos](#scatter_price)
# 	* [3.7 Significancia estadística de la diferencia en la conversión entre los grupos con los datos en bruto](#sig_esta_conversion)
# 	* [3.8 Significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos en bruto](#sig_esta_pedidos)
# 	* [3.9 Significancia estadística de la diferencia en la conversión entre los grupos utilizando los datos filtrados](#conversion_filtrado)
# 	* [3.10 Significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos filtrados](#pedidos_filtrado)
# * [4 Resumen y Conclusión General](#end)
# 

# %% [markdown]
# # Objetivos <a id='objetivos'></a>  
# 
# * Obtener una comprensión general de los datos.  
# * Identificar tendencias y patrones importantes.  
# * Preparar los datos para el análisis.   
# * Analizar los resultados del test A/B.  

# %% [markdown]
# # Diccionario de Datos <a id='diccionario'></a>   
# 
# * DataFrame `hypotheses_us`:  
#     * `Hypotheses`: breves descripciones de las hipótesis.  
#     * `Reach`: alcance del usuario, en una escala del uno a diez.  
#     * `Impact`: impacto en los usuarios, en una escala del uno al diez.  
#     * `Confidence`: confianza en la hipótesis, en una escala del uno al diez.  
#     * `Effort`: los recursos necesarios para probar una hipótesis, en una escala del uno al diez. Cuanto mayor sea el valor Effort, más recursos requiere la prueba.  
#     
# * DataFrame `orders_us`:  
#     * `transactionId`: identificador de pedido.  
#     * `visitorId`: identificador del usuario que realizó el pedido.  
#     * `date`: fecha del pedido.  
#     * `revenue`: ingresos del pedido.  
#     * `group`: el grupo del test A/B al que pertenece el usuario.  
# * DataFrame `visits_us`:  
#     * `date`: la fecha.  
#     * `group`: grupo del test A/B.  
#     * `visits`: el número de visitas en la fecha especificada para el grupo de test A/B especificado.  

# %% [markdown]
# ## Inicialización <a id='inicio'></a>

# %%
# se cargan todas las librerías
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats

# %%
# se descargan los datos completos con los tipos de datos correctos

hypotheses_us = pd.read_csv('files/datasets/hypotheses_us.csv', sep= ';')
orders_us = pd.read_csv('files/datasets/orders_us.csv', parse_dates= ['date'])
visits_us = pd.read_csv('files/datasets/visits_us.csv', parse_dates= ['date'])

# %%
# se muestra la información de cada DataFrame
hypotheses_us.info()

# %%
orders_us.info()

# %%
visits_us.info()

# %%
# se cambian a minúsculas los nombres de las columnas del DataFrame 'hypotheses_us'
# se crea una lista vacia para almcenar los nombres modificados
column_names = []
# se itera sobre cada nombre de columna con un bucle for
for name in hypotheses_us.columns:
    names_lower = name.lower()
    column_names.append(names_lower)

# %%
# se asignan los nuevos nombres de columna
hypotheses_us.columns = column_names

# %%
# se modifica el nombre las columnas 'transactionId' y 'visitorId' del DataFrame orders_us
orders_us = orders_us.rename(columns= {'transactionId':'transaction_id', 'visitorId': 'visitor_id'})

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# Se tienen el tipo de datos correctos en los DataFrames y no hay valores nulos, por tanto, se procede con el análisis.
#     
# </span>
#     
# </div>

# %% [markdown]
# ## Parte 1. Priorizar hipótesis  <a id='hipotheses'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **ICE y RICE:**  
# Impacto, confianza, esfuerzo (ICE) es una de las formas más populares de priorizar
# problemas: `ICE score = (Impact x Confidence) / Effort`
#     
# También existe una forma modificada, RICE: `RICE score = (Reach x Impact x Confidence) / Effort`.
#     
# A partir del DataFrame `hypotheses_us` se calculará ICE y RICE, para priorizar hipótesis. Se ordenarán en orden descendente de prioridad.
#     
#     
# </span>
#     
# </div>

# %%
# se imprime el DataFrame 'hypotheses_us'
hypotheses_us

# %%
# se crea una columna para almacenar el valor de ICE
hypotheses_us['ICE'] = (hypotheses_us['impact'] * hypotheses_us['confidence']) / hypotheses_us['effort']

# %%
# se ordenan en orden descendente de prioridad.
hypotheses_us[['hypothesis', 'ICE']].sort_values(by= 'ICE', ascending= False)

# %%
print('Tres hipótesis más prometedoras con ICE:')
print(hypotheses_us.iloc[8][0])
print(hypotheses_us.iloc[0][0])
print(hypotheses_us.iloc[7][0])

# %%
# se crea una columna para almacenar el valor de RICE
hypotheses_us['RICE'] = (hypotheses_us['reach'] * hypotheses_us['impact'] * hypotheses_us['confidence']) / hypotheses_us['effort']

# %%
# se ordenan en orden descendente de prioridad.
hypotheses_us[['hypothesis', 'RICE']].sort_values(by= 'RICE', ascending= False)

# %%
print('Tres hipótesis más prometedoras con RICE:')
print(hypotheses_us.iloc[7][0])
print(hypotheses_us.iloc[2][0])
print(hypotheses_us.iloc[0][0])

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# En el caso del framework **ICE** las 3 hipótesis más prometedoras son las que tienen los índices 8, 0 y 7, mientras que el framework **RICE** las 3 hipótesis más prometedoras son las que tienen los índices 7, 2 y 0. Las hipótesis 8 y 0 tiene valores muy altos de impacto y confianza tienen una calificación alta, sin embargo, el alcance que tienen es muy bajo su puntaje. Lo anterior significa que se alcanzan a muy pocos usuarios y usuarias, esa una de las principales diferencias entre **ICE** y **RICE**, este último toma en cuenta el alcance de las hipótesis, es decir, a cuántos usuarios/as se alcanzan. Mientras que, en el framework **RICE** la hipótesis 7 ocupa el primer lugar, ya que su puntaje del alcance es mayor que las hipótesis 8 y 0. 
#     
#     
# </span>
#     
# </div>

# %% [markdown]
# ## Parte 2. Análisis de test A/B <a id='test'></a>

# %% [markdown]
# ###  Ingresos Acumulados por Grupo <a id='acumulado_ingreso'></a>

# %%
# para verificar si existen usuarios que estén tanto en el grupo A como en el grupo B se emplea set()
# después se encuentra la instersección de ambos conjuntos con intersection()

# se obtienen conjuntos únicos de visitor_id para cada grupo
visitors_group_A = set(orders_us[orders_us['group'] == 'A']['visitor_id'])
visitors_group_B = set(orders_us[orders_us['group'] == 'B']['visitor_id'])

# Encuentra la intersección de los conjuntos (usuarios presentes en ambos grupos)
common_visitors = visitors_group_A.intersection(visitors_group_B)

# Se muestra la cantidad y los visitor_id que están en ambos grupos
if not common_visitors:
    print("No hay usuarios que estén en ambos grupos A y B.")
else:
    print(f"{len(common_visitors)} usuarios encontrados en ambos grupos:")
    print(common_visitors)

# %%
# ahora se filtra el DataFrame 'orders_us' en donde no se tengan estos usuarios
orders_us = orders_us[~orders_us['visitor_id'].isin(list(common_visitors))]
orders_us.head()

# %%
# se crea una matriz con valores únicos de parejas fecha-grupo con el método drop_duplicates()
datesGroups = orders_us[['date', 'group']].drop_duplicates()
datesGroups.head()

# %%
# se declara la variable ordersAggregated para almacenar: 
# la fecha
# el grupo del test A/B
# el número de pedidos distintos para el grupo de prueba hasta la fecha especificada incluida
# el número de usuarios distintos en el grupo de prueba que realizan al menos un pedido hasta la fecha especificada incluida
# ingresos totales de pedidos en el grupo de prueba hasta la fecha especificada incluida
ordersAggregated = datesGroups.apply(lambda x: orders_us[np.logical_and(orders_us['date'] <= x['date'], orders_us['group'] == x['group'])].agg({'date' : 'max', 'group' : 'max', 'transaction_id' : pd.Series.nunique, 'visitor_id' : pd.Series.nunique, 'revenue' : 'sum'}), axis=1).sort_values(by=['date','group'])
ordersAggregated.head()

# %%
# se hace algo parecido para obtener los datos diarios acumulados agregados sobre los visitantes
# s declara la variable visitorsAggregated para almacenar:
# la fecha
# el grupo del test A/B
# el número de pedidos distintos para el grupo de prueba hasta la fecha especificada incluida
visitorsAggregated = datesGroups.apply(lambda x: visits_us[np.logical_and(visits_us['date'] <= x['date'], visits_us['group'] == x['group'])].agg({'date' : 'max', 'group' : 'max', 'visits' : 'sum'}), axis=1).sort_values(by=['date','group'])
visitorsAggregated.head()

# %%
# se fusionan los dos DataFrames 'ordersAggregated' y 'visitorsAggregated' en uno por las columnas 'date' y 'group'
cumulativeData = ordersAggregated.merge(visitorsAggregated, left_on=['date', 'group'], right_on=['date', 'group'])
# se dan a sus columnas nombres descriptivos
# se asignan los nombres ['date', 'group', 'orders', 'buyers', 'revenue', 'visitors'] a las columnas en cumulativeData
cumulativeData.columns = ['date', 'group', 'orders', 'buyers', 'revenue', 'visitors']
cumulativeData.head()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#       
# Se declaran las variables `cumulativeRevenueA` y `cumulativeRevenueB`, donde se almacenan los datos sobre fechas, ingresos y número de pedidos para los grupos A y B 
#     
#     
# </span>
#     
# </div>

# %%
# DataFrame con pedidos acumulados e ingresos acumulados por día, grupo A
cumulativeRevenueA = cumulativeData[cumulativeData['group']=='A'][['date','revenue', 'orders']]
cumulativeRevenueA.head()

# %%
# DataFrame con pedidos acumulados e ingresos acumulados por día, grupo B
cumulativeRevenueB = cumulativeData[cumulativeData['group']=='B'][['date','revenue', 'orders']]
cumulativeRevenueB.head()

# %%
# ajustar los valores de ancho y alto del gráfico
plt.figure(figsize=(10, 6))
# se traza el gráfico de ingresos del grupo A
plt.plot(cumulativeRevenueA['date'], cumulativeRevenueA['revenue'], label='A')

# se traza el gráfico de ingresos del grupo B
plt.plot(cumulativeRevenueB['date'], cumulativeRevenueB['revenue'], label='B')

plt.legend()
# se rotan las fechas en el eje x a 45 grados
plt.xticks(rotation=45)

# se asigna un nombre
plt.title('Gráfico de Ingresos para los Grupos A y B')
# se nombran los ejes
plt.xlabel('Fecha', fontsize= 12)
plt.ylabel('Ingresos', fontsize= 12)

# se muestra el gráfico
plt.show()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# Los ingresos aumentan durante toda la prueba, sin embargo, el grupo B lo hace con mayor rapidez que el grupo A. Después del 17-08-2019 los ingresos del grupo B aumentan drásticamente, a diferencia del grupo A que lo hace con menor velocidad. Lo anterior se puede deber a un aumento en el número de los pedidos o pedidos que son muy costosos.  
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Tamaño de Pedido Promedio Acumulado por Grupo. <a id='acumulado_pedido'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# ****  
# Ahora se traza el tamaño promedio de compra por grupo. Se dividen los ingresos acumulados entre el número acumulado de pedidos. 
#     
# </span>
#     
# </div>

# %%
# se ajustan los valores de ancho y alto del gráfico
plt.figure(figsize=(10, 6))

# se traza el gráfico del tamaño promedio de compra por el grupo A
plt.plot(cumulativeRevenueA['date'], cumulativeRevenueA['revenue']/cumulativeRevenueA['orders'], label='A')
# se traza el gráfico del tamaño promedio de compra por el grupo B
plt.plot(cumulativeRevenueB['date'], cumulativeRevenueB['revenue']/cumulativeRevenueB['orders'], label='B')

plt.legend()

# se rotan las fechas en el eje x a 45 grados
plt.xticks(rotation=45)

# se asigna un nombre
plt.title('Gráfico del Tamaño Promedio Acumulado de Compra para los Grupos A y B')
# se nombran los ejes
plt.xlabel('Fecha', fontsize= 12)
plt.ylabel('Tamaño de Pedido Promedio', fontsize= 12)

# se muestra el gráfico
plt.show()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# El tamaño promedio de compra del grupo B aumenta mucho depués del 17-08-2019, se aprecia un pico y después disminuye y se estabiliza al final. Mientras que, el grupo A también aumenta pero en menor medida, también al final parece estabilizarse.
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Diferencia relativa en el tamaño de pedido promedio acumulado para el grupo B en comparación con el grupo A. <a id='dif_rel_pedidos'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# ****  
# Se traza un gráfico de diferencia relativa para los tamaños promedio de compra para el grupo B en comparación con el grupo A.  
#     
# </span>
#     
# </div>

# %%
# se reunen los datos en un sólo DataFrame de 'cumulativeRevenueA' y 'cumulativeRevenueB' con el método merge() 
# asi todo el DataFrame resultante contenga las columnas ['date', 'revenueA', 'revenueB', 'ordersA', 'ordersB']
mergedCumulativeRevenue = cumulativeRevenueA.merge(cumulativeRevenueB, left_on='date', right_on='date', how='left', suffixes=['A', 'B'])
mergedCumulativeRevenue.head()

# %%
# se ajustan los valores de ancho y alto del gráfico
plt.figure(figsize=(10, 6))

# trazar un gráfico de diferencia relativa para los tamaños de compra promedio
plt.plot(mergedCumulativeRevenue['date'], (mergedCumulativeRevenue['revenueB']/mergedCumulativeRevenue['ordersB'])/(mergedCumulativeRevenue['revenueA']/mergedCumulativeRevenue['ordersA'])-1)

# agregar el eje X
plt.axhline(y=0, color='black', linestyle='--')

# se rotan las fechas en el eje x a 45 grados
plt.xticks(rotation=45)

# se asigna un nombre
plt.title('Gráfico de Diferencia Relativa para los Tamaños de Compra Promedio')
# se nombran los ejes
plt.xlabel('Fecha', fontsize= 12)
plt.ylabel('Diferencia Relativa', fontsize= 12)

plt.show()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# En algunos puntos o fechas la diferencia entre los segmentos aumenta mucho y después disminuye, se puede deber a compras muy grandes o valores atípicos. Y sólo hay un valor que es menor que 0, después la diferencia aumenta y se vuelve positiva. Como primera suposición pareciera que el grupo B es porcentualmente más grande en comparación con el grupo A. Sin embargo, se deberá hacer un análisis para identificar valores atípicos.  
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Tasa de conversión de cada grupo como la relación entre los pedidos y el número de visitas de cada día. <a id='conversion_acum'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# ****  
# Ahora se agrega la columna 'conversion' al DataFrame `cumulativeData`. Esta columna contiene la relación entre el número de pedidos y el número de usuarios/visitantes para un grupo específico en una fecha específica.  
# Se declaran las variables `cumulativeDataA_` y `cumulativeDataB_`, donde almacenarán los datos de los pedidos en los segmentos A y B. Y se traza el gráfico de conversión acumulada diaria de cada grupo.
#     
# </span>
#     
# </div>

# %%
# se calcula la conversión acumulada
cumulativeData['conversion'] = cumulativeData['orders']/cumulativeData['visitors']

# se seleccionan datos en el grupo A
cumulativeDataA_ = cumulativeData[cumulativeData['group']=='A']

# se seleccionan datos en el grupo B
cumulativeDataB_ = cumulativeData[cumulativeData['group']=='B']

# %%
# se ajustan los valores de ancho y alto del gráfico
plt.figure(figsize=(10, 6))

# se trazan los gráficos
plt.plot(cumulativeDataA_['date'], cumulativeDataA_['conversion'], label='A')
plt.plot(cumulativeDataB_['date'], cumulativeDataB_['conversion'], label='B')

plt.legend()

# se rotan las fechas en el eje x a 45 grados
plt.xticks(rotation=45)

# se asigna un nombre
plt.title('Gráfico de Conversión Acumulada para los Grupos A y B')
# se nombran los ejes
plt.xlabel('Fecha', fontsize= 12)
plt.ylabel('Tamaño de Pedido Promedio', fontsize= 12)


plt.show()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# En un inicio el grupo A tenía una tasa de conversión mayor que el grupo B, después la tasa de conversión del grupo B aumenta y al final se estabiliza, mientras que en el grupo A comienza a disminuir y para el final parece decrecer aún más. En ambos grupos la tasa de conversión fluctua y se observa que aparentemente el grupo B tiene una mayor tasa de conversión.
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Tasas de conversión diarias de los dos grupos. <a id='conversion_diaria'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# ****  
# Ahora se trazará un gráfico de diferencia relativa para las tasas de conversión acumuladas, se unen los DatFrame `cumulativeDataA` y `cumulativeDataB` utilizando el método `merge()`. 
#     
# </span>
#     
# </div>

# %%
# se unen los DataFrame, el DataFrame resultante tiene las columnas ['date', 'conversionA', 'conversionB']
# se guarda en mergedCumulativeConversions
mergedCumulativeConversions = cumulativeDataA_[['date','conversion']].merge(cumulativeDataB_[['date','conversion']], left_on='date', right_on='date', how='left', suffixes=['A', 'B'])
mergedCumulativeConversions.head()

# %%
# se ajustan los valores de ancho y alto del gráfico
plt.figure(figsize=(10, 6))

# se traza la diferencia relativa entre la tasa de conversión acumulada del grupo B en comparación con la del grupo A
plt.plot(mergedCumulativeConversions['date'], mergedCumulativeConversions['conversionB']/mergedCumulativeConversions['conversionA']-1)

# se rotan las fechas en el eje x a 45 grados
plt.xticks(rotation=45)

# se asigna un nombre
plt.title('Gráfico de Diferencia Relativa para las Tasas de Conversión Acumuladas')
# se nombran los ejes
plt.xlabel('Fecha', fontsize= 12)
plt.ylabel('Tasas de Conversión', fontsize= 12)

plt.axhline(y=0, color='black', linestyle='--')

plt.show()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# En un inicio la tasa de conversión del grupo B es menor que el grupo A, posteriormente aumenta y así se mantine, aunque fluctua. No obstante, es mayor de  la tasa de conversión indicando que es más grande en comparación con el grupo A en un 20%. Aunque se hará un análisis de las anomalías que pudieran existir.  
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Valores atípicos y aumentos: valores extremos <a id='atipicos'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# ****  
# Se buscan los datos atípicos, se realiza un gráfico de dispersión y se calculan los percentiles 95 y 99, tanto para el número de pedidos como para los ingresos.  
#     
# </span>
#     
# </div>

# %% [markdown]
# #### Gráfico de dispersión del número de pedidos por usuario <a id='scatter_orders'></a>

# %%
#* se encuentra el número de pedidos por usuario, para hacerlo, se crea un DataFrame con dos columnas:'visitor_id' y 'transaction_id'. 
# el resultado se guarda n ordersByUsers. Ordena los datos por el número de pedidos en orden 
ordersByUsers = (orders_us.drop(['group', 'revenue', 'date'], axis=1).groupby('visitor_id', as_index=False).agg({'transaction_id': pd.Series.nunique}))

# se renombran las columnas
ordersByUsers.columns = ['user_id', 'orders']

# se imprimen 10 filas ordenadas de mayor a menor con base en el número de órdenes
ordersByUsers.sort_values(by='orders', ascending= False).head(10)

# %%
# se traza  un gráfico de dispersión con el número de pedidos por usuario
# se asignan los valores del eje x

# se ajustan los valores de ancho y alto del gráfico
plt.figure(figsize=(8, 6))
x_values = pd.Series(range(0, len(ordersByUsers)))

plt.scatter(x_values, ordersByUsers['orders'])

plt.show()

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Observaciones:**  
# Hay muchos usuarios con 2 y 3 pedidos, por lo tanto se procede a calcular los percentiles 95 y 99 para el número de pedidos por usuario.
#     
# </span>
#     
# </div>

# %%
# con numpy se calculan los percentiles 95 y 99
print(np.percentile(ordersByUsers['orders'], [95, 99]))

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# No más del 5 % de los usuarios/as hicieron más de 1 pedido y no más del 1 % de los/las clientes realizan más de 2 pedidos. Por lo tanto, es razonable establecer 1 pedido por usuario como límite inferior para el número de pedidos y filtrar las anomalías en base a ello. 
#     
# </span>
#     
# </div>

# %% [markdown]
# #### Gráfico de dispersión de los precios de los pedidos <a id='scatter_price'></a>

# %%
# se crea un gráfico de dispersión utilizando el método scatter()
# se guardan los valores para el eje horizontal x_values_revenue: los números generados de observaciones.
x_values_revenue = pd.Series(range(0, len(orders_us['revenue'])))

# se toman los valores del eje vertical de la columna 'revenue' del DataFrame 'orders_us'
plt.figure(figsize=(8, 6))
plt.scatter(x_values_revenue, orders_us['revenue'])
plt.show()

# %%
# con numpy se calculan los percentiles 95 y 99
print(np.percentile(orders_us['revenue'], [95, 99]))

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# No más del 5 % de los usuarios/as hicieron pedidos que costaron más de 414 y no más del 1 % de los/las clientes realizaron pedidos que costaron más de 830. Por lo tanto, es razonable establecer que el costo de los pedidos fue alrededor de 415.
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Significancia estadística de la diferencia en la conversión entre los grupos con los datos en bruto <a id='sig_esta_conversion'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# ****  
# Se crean las variables `ordersByUsersA` y `ordersByUsersB` para almacenar las columnas ['user_id', 'orders']. Para los usuarios con al menos un pedido, se indica el número de pedidos realizados
#     
# </span>
#     
# </div>

# %%
# se almacenan los valores para el grupo A
ordersByUsersA = orders_us[orders_us['group']=='A'].groupby('visitor_id', as_index=False).agg({'transaction_id' : pd.Series.nunique})
ordersByUsersA.columns = ['user_id', 'orders']

# se almacenan los valores para el grupo B
ordersByUsersB = orders_us[orders_us['group']=='B'].groupby('visitor_id', as_index=False).agg({'transaction_id' : pd.Series.nunique})
ordersByUsersB.columns = ['user_id', 'orders']

print('Grupo A')
print(ordersByUsersA.head())
print()
print('Grupo B')
print(ordersByUsersB.head())

# %%
# se declara las variables sampleA y sampleB, con los usuarios que realizaron pedidos y los números de 
# pedidos correspondientes. Los usuarios sin pedidos tendrán un 0
# Lo anterior es necesario para preparar las muestras para la prueba de Mann-Whitney

sampleA = pd.concat([ordersByUsersA['orders'], 
                     pd.Series(0, index=np.arange(visits_us[visits_us['group']=='A']['visits'].sum() 
                     - len(ordersByUsersA['orders'])), name='orders')], axis=0
                    )

sampleB = pd.concat([ordersByUsersB['orders'],
                     pd.Series(0, index=np.arange(visits_us[visits_us['group']=='B']['visits'].sum() 
                     - len(ordersByUsersB['orders'])), name='orders')],axis=0
                   )

# %%
# Se calcula la significancia estadística de la diferencia en la conversión basada en los resultados después 
# Se aplica la prueba de Mann-Whitney
# Se imprime el valor p para comparar la conversión de los grupos 
# se redondea a cinco decimales.
print(f'Valor p: {stats.mannwhitneyu(sampleA, sampleB)[1] :.5f}')

# se calcula e imprime la diferencia relativa en la conversión entre los grupos
print(f'Diferencia relativa en la conversión para el grupo B: {sampleB.mean()/sampleA.mean()-1 :.5f}')

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# El valor de p es de 0.01102 el cual es menor que 0.05, por lo tanto, se rechaza la hipótesis nula ya que hay una diferencia estadísticamente significativa en la conversión entre los grupos, asimismo, con el valor de p se puede decir que hay una probabilidad del 1.102 % de equivocación al rechazar la hipótesis nula. En cuanto a la diferencia relativa, hay un aumento del 15.9 % para el grupo B.
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos en bruto <a id='sig_esta_pedidos'></a>

# %%
# ahora para calcular la importancia estadística de la diferencia en el tamaño medio de los pedidos de los grupos, 
# pasaremos los datos sobre los ingresos al criterio mannwhitneyu()
p_value = stats.mannwhitneyu(orders_us[orders_us['group']=='A']['revenue'], orders_us[orders_us['group']=='B']['revenue']).pvalue

print(f'Valor p: {round(p_value, 5)}')

# se calcula e imprime la diferencia relativa en el tamaño de los pedidos entre los grupos
print(f"Diferencia relativa en el tamaño promedio para el grupo B: {orders_us[orders_us['group']=='B']['revenue'].mean()/orders_us[orders_us['group']=='A']['revenue'].mean()-1 :3f}")

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# EL valor de p es de 0.86223, el cual es mayor que 0.05, por tanto la hipótesis nula no se rechaza. No hay diferencia en el tamaño medio de los grupos. Sin embargo, el tamaño de pedido promedio para el grupo B es mucho más grande que para el grupo A, en un 27.83 %.
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Significancia estadística de la diferencia en la conversión entre los grupos utilizando los datos filtrados. <a id='conversion_filtrado'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
# 
# ****
# Ahora vamos a eliminar las anomalías de nuestros datos.  
# Recodando que los percentiles 95 y 99 para el tamaño promedio de pedido fueron 414 y 830.  
# Para el número de pedidos, los percentiles 95 y 99 fueron de 1 y 2 pedidos.  
#     
# Consideraremos usuarios anómalos a aquellos que realizaron más de 1 pedido o realizaron uno de más de 415. Así, se elimina el 5 % de los usuarios con más pedidos y entre el 1% y el 5% de los pedidos más caros.
#     
# </span>
#     
# </div>

# %%
# se crean slices de datos con los usuarios que realizaron más de dos pedidos (usersWithManyOrders)
usersWithManyOrders = pd.concat([ordersByUsersA[ordersByUsersA['orders'] > 1]['user_id'], ordersByUsersB[ordersByUsersB['orders'] > 1]['user_id']], axis = 0)

# y se filtran los usuarios que realizaron pedidos por más de $500 (usersWithExpensiveOrders)
usersWithExpensiveOrders = orders_us[orders_us['revenue'] > 415]['visitor_id']

# se unen los 'usersWithManyOrders' y 'usersWithExpensiveOrders' en una tabla llamada abnormalUsers
abnormalUsers = pd.concat([usersWithManyOrders, usersWithExpensiveOrders], axis= 0).drop_duplicates().sort_values()

print(abnormalUsers.head())
print()
print(f'Usuarios anómalos: {abnormalUsers.shape[0]}')

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
# 
# ****
# Ahora se calcula la significancia estadística de las diferencias en la conversión entre los grupos con datos filtrados.  
# Primero prepararemos muestras del número de pedidos por usuario para cada grupo de prueba.  
# 
#     
# </span>
#     
# </div>

# %%
# se crean las variables sampleAFiltered y sampleBFiltered para almacenar los datos después de que se hayan eliminado las anomalías.
sampleAFiltered = pd.concat([ordersByUsersA[np.logical_not(ordersByUsersA['user_id'].isin(abnormalUsers))]['orders'], pd.Series(0, index=np.arange(visits_us[visits_us['group']=='A']['visits'].sum() - len(ordersByUsersA['orders'])),name='orders')],axis=0)

sampleBFiltered = pd.concat([ordersByUsersB[np.logical_not(ordersByUsersB['user_id'].isin(abnormalUsers))]['orders'], pd.Series(0, index=np.arange(visits_us[visits_us['group']=='B']['visits'].sum() - len(ordersByUsersB['orders'])),name='orders')],axis=0)

# se aplica el criterio estadístico de Mann-Whitney a las muestras resultantes
p_value_filtered = stats.mannwhitneyu(sampleAFiltered, sampleBFiltered).pvalue
print(f'Valor p: {round(p_value_filtered, 5)}')
print()
print(f'Diferencia relativa en la conversión para el grupo B: {sampleBFiltered.mean()/sampleAFiltered.mean()-1 :.5f}')



# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# El valor de p de la conversión con los datos filtrados no cambiaron mucho, su valor es de 0.01593, por tanto se rechaza la hipótesis nula. La diferencia relativa es de 17.39 % para el grupo B.  
#     
# </span>
#     
# </div>

# %% [markdown]
# ### Significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos filtrados. <a id='pedidos_filtrado'></a>
# 

# %%
# # se aplica el criterio estadístico de Mann-Whitney 
p_value_filtered_orders = stats.mannwhitneyu(orders_us[np.logical_and(orders_us['group']=='A',
                                    np.logical_not(orders_us['visitor_id'].isin(abnormalUsers)))]['revenue'],
                                    orders_us[np.logical_and(orders_us['group']=='B',
                                    np.logical_not(orders_us['visitor_id'].isin(abnormalUsers)))]['revenue']).pvalue

# Diferencia relativa del tamaño de los pedidos
groupA = orders_us[np.logical_and(orders_us['group']=='A', np.logical_not(orders_us['visitor_id'].isin(abnormalUsers)))]['revenue'].mean()
groupB = orders_us[np.logical_and(orders_us['group']=='B',np.logical_not(orders_us['visitor_id'].isin(abnormalUsers)))]['revenue'].mean()

dif_orders_filt = groupB / groupA - 1

print(f'Valor p: {round(p_value_filtered_orders, 5)}')
print()
print(f'Diferencia relativa en el tamaño promedio para el grupo B: {dif_orders_filt :.5f}')

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Conclusiones:**  
# El valor de p disminuyó a 0.77119, el cual contnua siendo menor a 0.05, la diferencia entre los grupos disminuyó a -3.33 %. Por lo tanto, No hay diferencia en el tamaño medio del pedido entre los grupos.
#     
# </span>
#     
# </div>

# %% [markdown]
# ## Resumen y Conclusión General <a id='end'></a>

# %% [markdown]
# <div style="background-color: lightyellow; padding: 10px;">
# 
# <span style="color: darkblue;">  
#     
# **Resumen General de los pasos seguidos:**  
# 1. Se descargaron y se lamacenaron los datos y se prepararon para el análisis.
# 2. Se realizó la priorización de hipótesis con el Framework ICE y RICE.  
# 3. Se hizo un análisis de Test A/B.  
# 4. Se representó gráficamente el ingreso acumulado por grupo.  
# 5. Se representó gráficamente el tamaño de pedido promedio acumulado por grupo.  
# 6. Se representó gráficamente la diferencia relativa en el tamaño de pedido promedio acumulado para el grupo B en comparación con el grupo A.  
# 7. Se calculó la tasa de conversión diaria para cada grupo y se representó gráficamente las tasas de conversión diarias.  
# 8. Se hizo un gráfico de dispersión del número de pedidos por usuario.  
# 9. Se calcularon los percentiles 95 y 99 para el número de pedidos por usuario.  
# 10. En un gráfico se representó la dispersión de los precios de los pedidos.  
# 11. Se calcularon los percentiles 95 y 99 de los precios de los pedidos.  
# 12. Se calculó la significancia estadística de la diferencia en la conversión entre los grupos utilizando los datos en bruto.  
# 13. Se encontró la significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos en bruto.  
# 14. Cálculo de la significancia estadística de la diferencia en la conversión entre los grupos utilizando datos filtrados.  
# 15. Cálculo de la significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando datos filtrados.  
# 
# **Conclusión General:**  
# • Hay una diferencia estadísticamente significativa de acuerdo a los datos sin filtrar y los datos filtrados en la conversión de los usuarios/as. El grupo B tiene una conversión más alta, en los datos sin filtrar la diferencia relativa es de 15.9 % y en los datos filtrados de 17.39 %.  
# 
# • Ni los datos sin filtrar ni los datos filtrados mostraron diferencias estadísticamente significativas en el tamaño promedio de los pedidos entre los grupos.  
# 
# • En el gráfico que muestra la diferencia de conversión entre los grupos se observa que los resultados del grupo B son mejores, en un 20 % más respecto al grupo A en periodo determinado, actualmente es mejor en un 15 % aproximadamente.  
# 
# • El gráfico que muestra la diferencia en el tamaño medio de los pedidos entre los grupos nos dice que los resultados del grupo B están fluctuando constantemente, en algunos días tiene picos muy alto y en otros son muy bajos, en los últimos días disminuye. Por lo tanto, de este gráfico no se pueden sacar conclusiones definitivas.  
# 
# • Con base en los resultados se recomienda parar la prueba y considerar al grupo B como líder respecto al grupo A, al menos en la conversión de usuarios/as.  
#     
# </span>
#     
# </div>

# %%




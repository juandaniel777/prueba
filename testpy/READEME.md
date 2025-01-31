# 📈 Análisis de Precios de Energía

Este proyecto realiza un análisis de los precios de energía durante un periodo específico. Se observa una **tendencia general al alza** en los precios. Sin embargo, para un análisis más robusto, sería ideal extender el rango de fechas y recolectar más datos históricos. Esto permitiría:

- **Identificar patrones estacionales:** Determinar si hay fluctuaciones regulares relacionadas con estaciones del año o días de la semana.
- **Analizar variabilidad:** Evaluar si la volatilidad es normal o está influida por eventos externos.
- **Incluir factores adicionales:** Considerar variables como demanda, disponibilidad de recursos, políticas energéticas o eventos globales.

---

## 📂 **Estructura del Proyecto**

El proyecto consta de un único archivo `pruebat.py`, que realiza las siguientes tareas principales:

1. **Obtención de Datos:**  
   - Se obtienen los datos de precios de energía desde una API.
2. **Procesamiento de Datos:**  
   - Se transforman y limpian los datos obtenidos, asegurando la calidad del análisis.
3. **Tratamiento de Datos Faltantes:**  
   - Se rellenan datos faltantes mediante métodos de interpolación avanzados.
4. **Cálculos de Promedios:**  
   - Se calculan promedios diarios y el promedio móvil de 7 días.
5. **Visualización:**  
   - Se genera una gráfica para analizar la evolución de los precios de energía a lo largo del tiempo.

---

## 📋 **Requisitos**

Para ejecutar el proyecto, asegúrate de contar con los siguientes requisitos:

### **Lenguaje**  
- Python 3.x

### **Librerías Necesarias**  
- `requests`
- `pandas`
- `sqlalchemy`
- `matplotlib`

Puedes instalarlas ejecutando:
```bash
pip install requests pandas sqlalchemy matplotlib

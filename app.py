import streamlit as st

def format_clp(value):
    return f"{value:,.0f}".replace(",", ".")

def parse_clp(value):
    return int(value.replace(".", ""))

def intro():
    st.title("Calculadora de CAC y LTV para Diferentes Modelos de Negocio")
    
    st.markdown("""
    Bienvenido a la calculadora de Customer Acquisition Cost (CAC) y Lifetime Value (LTV) multi-escenario. 
    Esta herramienta te ayudará a entender la rentabilidad de tu modelo de negocio según su tipo específico.

    ### Escenarios disponibles:
    1. **SaaS (Software as a Service)**
    2. **E-commerce**
    3. **Servicios B2B**

    Cada escenario tiene sus propias variables y consideraciones específicas para el cálculo de CAC y LTV.

    ### ¿Por qué son importantes el CAC y el LTV?
    El ratio LTV/CAC te dice si estás ganando más de lo que gastas en adquirir clientes:
    - **< 1**: Estás perdiendo dinero con cada cliente.
    - **1-3**: Tu modelo es marginalmente rentable, pero hay espacio para mejorar.
    - **> 3**: ¡Felicidades! Tu modelo de negocio es saludable y escalable.

    ### Instrucciones
    1. Selecciona tu tipo de negocio.
    2. Ingresa los datos solicitados en pesos chilenos (CLP).
    3. Revisa los resultados y las conclusiones al final de la página.
    4. Experimenta con diferentes valores para ver cómo afectan tus métricas.

    ¡Empecemos!
    """)

    st.markdown("""
    ---
    Creado por [Joaquín Trujillo](https://www.linkedin.com/in/joaquintrujillo/)
    """)

    if st.button("Comenzar el cálculo"):
        st.session_state.page = "scenario_selection"

def scenario_selection():
    st.title("Selección de Escenario")
    scenario = st.selectbox(
        "Elige tu modelo de negocio",
        ("SaaS", "E-commerce", "Servicios B2B")
    )
    if st.button("Continuar"):
        st.session_state.scenario = scenario
        st.session_state.page = "calculator"

def calculate_ltv_saas(monthly_revenue, gross_margin, churn_rate):
    lifetime = 1 / churn_rate
    ltv = monthly_revenue * gross_margin * lifetime
    return ltv

def calculate_ltv_ecommerce(avg_order_value, purchase_frequency, customer_lifespan, gross_margin):
    ltv = avg_order_value * purchase_frequency * customer_lifespan * gross_margin
    return ltv

def calculate_ltv_b2b(annual_contract_value, gross_margin, avg_contract_length):
    ltv = annual_contract_value * gross_margin * avg_contract_length
    return ltv

def calculate_cac(total_acquisition_cost, total_customers):
    return total_acquisition_cost / total_customers

def number_input_clp(label, min_value, value, step):
    input_value = st.text_input(label, value=format_clp(value))
    try:
        return parse_clp(input_value)
    except ValueError:
        st.error(f"Por favor, ingrese un valor válido para {label}")
        return value

def calculator_saas():
    st.header("Cálculo de LTV para SaaS")
    monthly_revenue = number_input_clp("Ingreso mensual por cliente (CLP)", 0, 50000, 1000)
    gross_margin = st.number_input("Margen bruto (%)", min_value=0, max_value=100, value=70)
    churn_rate = st.number_input("Tasa de cancelación mensual (%)", min_value=0, max_value=100, value=5)

    ltv = calculate_ltv_saas(monthly_revenue, gross_margin/100, churn_rate/100)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp("Costo total de adquisición (CLP)", 0, 45000000, 1000000)
    total_customers = st.number_input("Número total de clientes adquiridos", min_value=1, value=200)

    return ltv, calculate_cac(total_acquisition_cost, total_customers)

def calculator_ecommerce():
    st.header("Cálculo de LTV para E-commerce")
    avg_order_value = number_input_clp("Valor promedio de orden (CLP)", 0, 30000, 1000)
    purchase_frequency = st.number_input("Frecuencia de compra anual", min_value=0, value=4)
    customer_lifespan = st.number_input("Vida útil del cliente (años)", min_value=0, value=3)
    gross_margin = st.number_input("Margen bruto (%)", min_value=0, max_value=100, value=30)

    ltv = calculate_ltv_ecommerce(avg_order_value, purchase_frequency, customer_lifespan, gross_margin/100)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp("Costo total de adquisición (CLP)", 0, 15000000, 1000000)
    total_customers = st.number_input("Número total de clientes adquiridos", min_value=1, value=1000)

    return ltv, calculate_cac(total_acquisition_cost, total_customers)

def calculator_b2b():
    st.header("Cálculo de LTV para Servicios B2B")
    annual_contract_value = number_input_clp("Valor anual del contrato (CLP)", 0, 5000000, 1000000)
    gross_margin = st.number_input("Margen bruto (%)", min_value=0, max_value=100, value=60)
    avg_contract_length = st.number_input("Duración promedio del contrato (años)", min_value=0, value=3)

    ltv = calculate_ltv_b2b(annual_contract_value, gross_margin/100, avg_contract_length)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp("Costo total de adquisición (CLP)", 0, 20000000, 1000000)
    total_customers = st.number_input("Número total de clientes adquiridos", min_value=1, value=10)

    return ltv, calculate_cac(total_acquisition_cost, total_customers)

def get_recommendations(ratio, scenario, payback_period):
    general_rec = ""
    specific_rec = ""
    benchmark = ""

    if ratio < 1:
        general_rec = "El modelo de negocio no es sostenible en su estado actual."
        if scenario == "SaaS":
            specific_rec = """
            - Revisa tu estrategia de precios. Considera aumentar el precio o introducir planes premium.
            - Optimiza tus costos de adquisición enfocándote en canales más eficientes.
            - Mejora la retención de clientes para aumentar el lifetime value.
            """
            benchmark = "Para SaaS, se busca generalmente un ratio LTV/CAC de al menos 3:1."
        elif scenario == "E-commerce":
            specific_rec = """
            - Aumenta el valor promedio de orden con técnicas de upselling y cross-selling.
            - Mejora la tasa de conversión de tu sitio web para reducir el CAC.
            - Implementa programas de fidelización para aumentar la frecuencia de compra.
            """
            benchmark = "En e-commerce, un ratio LTV/CAC saludable suele estar entre 3:1 y 4:1."
        else:  # B2B
            specific_rec = """
            - Enfócate en adquirir clientes más grandes o con mayor potencial de crecimiento.
            - Optimiza tu proceso de ventas para reducir el costo de adquisición.
            - Considera ofrecer servicios adicionales para aumentar el valor del contrato.
            """
            benchmark = "Para servicios B2B, se busca un ratio LTV/CAC de 3:1 o mayor, debido a los ciclos de venta más largos."
    elif 1 <= ratio < 3:
        general_rec = "El modelo es marginalmente rentable, pero hay espacio para mejorar."
        if scenario == "SaaS":
            specific_rec = """
            - Implementa estrategias de expansión de ingresos (upselling, cross-selling).
            - Mejora la retención de clientes con mejor onboarding y soporte.
            - Optimiza tus campañas de marketing para reducir el CAC.
            """
        elif scenario == "E-commerce":
            specific_rec = """
            - Mejora tu estrategia de email marketing para aumentar las compras repetidas.
            - Optimiza tu logística para reducir costos y mejorar la satisfacción del cliente.
            - Implementa un programa de referidos para reducir el CAC.
            """
        else:  # B2B
            specific_rec = """
            - Desarrolla una estrategia de cuenta clave para maximizar el valor de los clientes existentes.
            - Mejora tu propuesta de valor para justificar precios más altos.
            - Invierte en marketing de contenidos para generar leads de mayor calidad.
            """
    else:
        general_rec = "Tu modelo de negocio es saludable y rentable."
        if scenario == "SaaS":
            specific_rec = """
            - Considera invertir más agresivamente en adquisición de clientes para escalar.
            - Explora nuevos segmentos de mercado o geografías.
            - Mantén el enfoque en la satisfacción y retención de clientes.
            """
        elif scenario == "E-commerce":
            specific_rec = """
            - Expande tu catálogo de productos o considera la expansión geográfica.
            - Invierte en mejorar la experiencia del cliente para mantener altas tasas de retención.
            - Explora estrategias de marketing más agresivas para capturar más mercado.
            """
        else:  # B2B
            specific_rec = """
            - Considera expandirte a nuevos mercados o industrias.
            - Invierte en I+D para mantenerte ahead de la competencia.
            - Desarrolla un programa de partners para ampliar tu alcance.
            """
    
    payback_rec = f"Tu período de recuperación es de {payback_period:.1f} meses. "
    if payback_period > 12:
        payback_rec += "Considera estrategias para reducir este período a menos de 12 meses para mejorar el flujo de caja."
    elif payback_period < 6:
        payback_rec += "Este es un excelente período de recuperación. Considera si puedes invertir más agresivamente en crecimiento."
    else:
        payback_rec += "Este es un buen período de recuperación. Continúa optimizando para mejorarlo aún más."

    return general_rec, specific_rec, benchmark, payback_rec

def display_results(ltv, cac, scenario):
    st.header("Resultados")
    st.write(f"LTV: CLP {format_clp(ltv)}")
    st.write(f"CAC: CLP {format_clp(cac)}")

    ratio = ltv / cac
    st.write(f"Ratio LTV/CAC: {ratio:.2f}")

    payback_period = cac / (ltv / 12)  # Asumiendo que LTV está en valor anual

    st.header("Conclusiones y Recomendaciones")
    
    general_rec, specific_rec, benchmark, payback_rec = get_recommendations(ratio, scenario, payback_period)
    
    if ratio < 1:
        st.error(general_rec)
    elif 1 <= ratio < 3:
        st.warning(general_rec)
    else:
        st.success(general_rec)
    
    st.write(specific_rec)
    st.info(benchmark)
    st.write(payback_rec)
    
    st.write(f"Período de recuperación: {payback_period:.1f} meses")

def calculator():
    st.title(f"Calculadora de CAC y LTV para {st.session_state.scenario}")

    if st.session_state.scenario == "SaaS":
        ltv, cac = calculator_saas()
    elif st.session_state.scenario == "E-commerce":
        ltv, cac = calculator_ecommerce()
    else:  # Servicios B2B
        ltv, cac = calculator_b2b()

    display_results(ltv, cac, st.session_state.scenario)

    if st.button("Cambiar escenario"):
        st.session_state.page = "scenario_selection"

def main():
    if "page" not in st.session_state:
        st.session_state.page = "intro"

    if st.session_state.page == "intro":
        intro()
    elif st.session_state.page == "scenario_selection":
        scenario_selection()
    elif st.session_state.page == "calculator":
        calculator()

if __name__ == "__main__":
    main()
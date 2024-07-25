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
    4. **Cooperativa**

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
        ("SaaS", "E-commerce", "Servicios B2B", "Cooperativa")
    )
    if st.button("Continuar"):
        st.session_state.scenario = scenario
        st.session_state.page = "calculator"

def number_input_clp(label, min_value, value, step, help_text):
    return st.text_input(
        label,
        value=format_clp(value),
        help=help_text
    )

def calculate_cac(total_acquisition_cost, total_customers):
    return total_acquisition_cost / total_customers

def calculate_ltv_saas(monthly_revenue, gross_margin, churn_rate, expansion_rate, service_cost, conversion_rate):
    net_revenue = monthly_revenue - service_cost
    net_margin = gross_margin - (service_cost / monthly_revenue)
    growth_rate = expansion_rate - churn_rate
    if growth_rate <= 0:
        lifetime = 1 / churn_rate
    else:
        lifetime = (1 / churn_rate) * (1 + (growth_rate / churn_rate))
    ltv = (net_revenue * net_margin * lifetime) / conversion_rate
    return ltv

def calculator_saas():
    st.header("Cálculo de LTV para SaaS")
    
    monthly_revenue = number_input_clp(
        "Ingreso mensual por cliente (CLP)", 0, 50000, 1000,
        "El ingreso promedio que genera un cliente en un mes."
    )
    
    gross_margin = st.number_input(
        "Margen bruto (%)", 
        min_value=0, 
        max_value=100, 
        value=70,
        help="El porcentaje de ingresos que queda después de los costos directos."
    )
    
    churn_rate = st.number_input(
        "Tasa de cancelación mensual (%)", 
        min_value=0, 
        max_value=100, 
        value=5,
        help="El porcentaje de clientes que cancelan su suscripción cada mes."
    )
    
    expansion_rate = st.number_input(
        "Tasa de expansión mensual (%)", 
        min_value=0, 
        max_value=100, 
        value=2,
        help="El porcentaje de crecimiento en ingresos de clientes existentes cada mes."
    )
    
    service_cost = number_input_clp(
        "Costo de servicio por cliente (CLP)", 0, 10000, 1000,
        "El costo directo de servir a un cliente en un mes."
    )
    
    conversion_rate = st.number_input(
        "Tasa de conversión de prueba gratuita a pago (%)", 
        min_value=0, 
        max_value=100, 
        value=20,
        help="El porcentaje de usuarios de prueba que se convierten en clientes de pago."
    )

    ltv = calculate_ltv_saas(parse_clp(monthly_revenue), gross_margin/100, churn_rate/100, expansion_rate/100, parse_clp(service_cost), conversion_rate/100)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp(
        "Costo total de adquisición (CLP)", 0, 45000000, 1000000,
        "El costo total de marketing y ventas para adquirir nuevos clientes."
    )
    total_customers = st.number_input(
        "Número total de clientes adquiridos", 
        min_value=1, 
        value=200,
        help="El número total de nuevos clientes adquiridos en el período."
    )

    return ltv, calculate_cac(parse_clp(total_acquisition_cost), total_customers)

def calculate_ltv_ecommerce(avg_order_value, purchase_frequency, customer_lifespan, gross_margin, return_rate, reorder_rate):
    net_order_value = avg_order_value * (1 - return_rate)
    annual_revenue = net_order_value * purchase_frequency
    lifetime_revenue = annual_revenue * customer_lifespan * (1 + reorder_rate)
    ltv = lifetime_revenue * gross_margin
    return ltv

def calculator_ecommerce():
    st.header("Cálculo de LTV para E-commerce")
    
    avg_order_value = number_input_clp(
        "Valor promedio de orden (CLP)", 0, 30000, 1000,
        "El valor promedio de una orden de compra."
    )
    
    purchase_frequency = st.number_input(
        "Frecuencia de compra anual", 
        min_value=0, 
        value=4,
        help="Cuántas veces al año compra un cliente promedio."
    )
    
    customer_lifespan = st.number_input(
        "Vida útil del cliente (años)", 
        min_value=0, 
        value=3,
        help="Por cuántos años se espera que un cliente siga comprando."
    )
    
    gross_margin = st.number_input(
        "Margen bruto (%)", 
        min_value=0, 
        max_value=100, 
        value=30,
        help="El porcentaje de ingresos que queda después de los costos directos."
    )
    
    return_rate = st.number_input(
        "Tasa de devolución (%)", 
        min_value=0, 
        max_value=100, 
        value=5,
        help="El porcentaje de productos que son devueltos."
    )
    
    reorder_rate = st.number_input(
        "Tasa de recompra (%)", 
        min_value=0, 
        max_value=100, 
        value=30,
        help="El porcentaje de clientes que hacen una segunda compra."
    )

    ltv = calculate_ltv_ecommerce(parse_clp(avg_order_value), purchase_frequency, customer_lifespan, gross_margin/100, return_rate/100, reorder_rate/100)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp(
        "Costo total de adquisición (CLP)", 0, 15000000, 1000000,
        "El costo total de marketing y publicidad para adquirir nuevos clientes."
    )
    total_customers = st.number_input(
        "Número total de clientes adquiridos", 
        min_value=1, 
        value=1000,
        help="El número total de nuevos clientes adquiridos en el período."
    )

    return ltv, calculate_cac(parse_clp(total_acquisition_cost), total_customers)

def calculate_ltv_b2b(annual_contract_value, gross_margin, avg_contract_length, upsell_rate, retention_rate):
    base_ltv = annual_contract_value * gross_margin * avg_contract_length
    upsell_value = base_ltv * upsell_rate * (avg_contract_length - 1)  # Asumimos que el upsell comienza desde el segundo año
    retention_value = base_ltv * retention_rate * (avg_contract_length - 1)  # Valor adicional por retención más allá del contrato inicial
    ltv = base_ltv + upsell_value + retention_value
    return ltv

def calculator_b2b():
    st.header("Cálculo de LTV para Servicios B2B")
    
    annual_contract_value = number_input_clp(
        "Valor anual del contrato (CLP)", 0, 5000000, 1000000,
        "El valor promedio anual de un contrato con un cliente B2B."
    )
    
    gross_margin = st.number_input(
        "Margen bruto (%)", 
        min_value=0, 
        max_value=100, 
        value=60,
        help="El porcentaje de ingresos que queda después de los costos directos del servicio."
    )
    
    avg_contract_length = st.number_input(
        "Duración promedio del contrato (años)", 
        min_value=0, 
        value=3,
        help="La duración promedio de un contrato con un cliente B2B."
    )
    
    upsell_rate = st.number_input(
        "Tasa de upsell anual (%)", 
        min_value=0, 
        max_value=100, 
        value=10,
        help="El porcentaje de aumento en el valor del contrato debido a ventas adicionales cada año."
    )
    
    retention_rate = st.number_input(
        "Tasa de retención después del contrato inicial (%)", 
        min_value=0, 
        max_value=100, 
        value=70,
        help="El porcentaje de clientes que renuevan o extienden su contrato después del período inicial."
    )

    ltv = calculate_ltv_b2b(parse_clp(annual_contract_value), gross_margin/100, avg_contract_length, upsell_rate/100, retention_rate/100)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp(
        "Costo total de adquisición (CLP)", 0, 20000000, 1000000,
        "El costo total de marketing, ventas y proceso de adquisición para nuevos clientes B2B."
    )
    total_customers = st.number_input(
        "Número total de clientes adquiridos", 
        min_value=1, 
        value=10,
        help="El número total de nuevos clientes B2B adquiridos en el período."
    )

    return ltv, calculate_cac(parse_clp(total_acquisition_cost), total_customers)

def calculate_ltv_cooperative(annual_membership_fee, avg_annual_services, gross_margin, avg_membership_duration, service_utilization_rate):
    annual_value = annual_membership_fee + (avg_annual_services * service_utilization_rate)
    ltv = annual_value * gross_margin * avg_membership_duration
    return ltv

def calculator_cooperative():
    st.header("Cálculo de LTV para Cooperativa")
    
    annual_membership_fee = number_input_clp(
        "Cuota anual de membresía (CLP)", 0, 50000, 1000,
        "La cuota que cada miembro paga anualmente para ser parte de la cooperativa."
    )
    
    avg_annual_services = number_input_clp(
        "Promedio de servicios anuales utilizados (CLP)", 0, 500000, 10000,
        "El valor promedio de servicios que un miembro utiliza en un año."
    )
    
    retention_rate = st.number_input(
        "Tasa de retención anual (%)", 
        min_value=0, 
        max_value=100, 
        value=90,
        help="El porcentaje de miembros que permanecen en la cooperativa cada año."
    )
    
    avg_membership_duration = 1 / (1 - retention_rate/100)  # Duración promedio de membresía
    
    gross_margin = st.number_input(
        "Margen bruto (%)", 
        min_value=0, 
        max_value=100, 
        value=40,
        help="El porcentaje de ingresos que queda después de los costos directos de los servicios."
    )
    
    service_utilization_rate = st.number_input(
        "Tasa de utilización de servicios (%)", 
        min_value=0, 
        max_value=100, 
        value=75,
        help="El porcentaje de servicios disponibles que un miembro promedio utiliza."
    )

    ltv = calculate_ltv_cooperative(parse_clp(annual_membership_fee), parse_clp(avg_annual_services), gross_margin/100, avg_membership_duration, service_utilization_rate/100)

    st.header("Cálculo de CAC")
    total_acquisition_cost = number_input_clp(
        "Costo total de adquisición (CLP)", 0, 10000000, 500000,
        "El costo total de marketing y proceso de incorporación para nuevos miembros."
    )
    total_new_members = st.number_input(
        "Número total de nuevos miembros", 
        min_value=1, 
        value=100,
        help="El número total de nuevos miembros incorporados en el período."
    )

    return ltv, calculate_cac(parse_clp(total_acquisition_cost), total_new_members)

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
            - Mejora la retención de clientes y busca oportunidades de expansión de ingresos.
            - Aumenta la tasa de conversión de pruebas gratuitas a clientes de pago.
            """
            benchmark = "Para SaaS, se busca generalmente un ratio LTV/CAC de al menos 3:1."
        elif scenario == "E-commerce":
            specific_rec = """
            - Aumenta el valor promedio de orden con técnicas de upselling y cross-selling.
            - Mejora la tasa de conversión de tu sitio web para reducir el CAC.
            - Implementa programas de fidelización para aumentar la frecuencia de compra y la tasa de recompra.
            - Optimiza tu logística para reducir la tasa de devoluciones.
            """
            benchmark = "En e-commerce, un ratio LTV/CAC saludable suele estar entre 3:1 y 4:1."
        elif scenario == "Servicios B2B":
            specific_rec = """
            - Enfócate en adquirir clientes más grandes o con mayor potencial de crecimiento.
            - Optimiza tu proceso de ventas para reducir el costo de adquisición.
            - Mejora tus estrategias de upselling y cross-selling para aumentar el valor del contrato.
            - Implementa programas de fidelización para aumentar la tasa de retención y renovación de contratos.
            """
            benchmark = "Para servicios B2B, se busca un ratio LTV/CAC de 3:1 o mayor, debido a los ciclos de venta más largos."
        elif scenario == "Cooperativa":
            specific_rec = """
            - Revisa la estructura de cuotas y servicios ofrecidos a los miembros.
            - Optimiza los costos de adquisición de nuevos miembros.
            - Mejora los beneficios para aumentar la retención de miembros y la tasa de utilización de servicios.
            - Considera ofrecer servicios adicionales para aumentar el valor promedio por miembro.
            """
            benchmark = "Para cooperativas, se busca generalmente un ratio LTV/CAC de al menos 3:1, considerando el largo plazo de la membresía."
    elif 1 <= ratio < 3:
        general_rec = "El modelo es marginalmente rentable, pero hay espacio para mejorar."
        # ... [Mantener recomendaciones existentes para cada escenario, adaptándolas a las nuevas variables] ...
    else:
        general_rec = "Tu modelo de negocio es saludable y rentable."
        # ... [Mantener recomendaciones existentes para cada escenario, adaptándolas a las nuevas variables] ...
    
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
    elif st.session_state.scenario == "Servicios B2B":
        ltv, cac = calculator_b2b()
    elif st.session_state.scenario == "Cooperativa":
        ltv, cac = calculator_cooperative()

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

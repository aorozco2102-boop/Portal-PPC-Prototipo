# run_simulation.py
# Importamos las clases desde el otro archivo
from ppc_classes import Anuncio, Usuario, MotorDePago, Portal

def run_corrido_frio():
    # 1. Inicializar el Motor de Pago y el Portal
    motor_pago = MotorDePago()
    portal = Portal(motor_pago)
    print("🌍 Portal Cautivo Inicializado. (Motor de Pago en $0.00)")

    # 2. Configurar Anuncios
    anuncio_login = Anuncio("Banner-Login", "Anunc-A", 0.15, "http://login-promo.com")
    anuncio_post_auth = Anuncio("PopUp-PostAuth", "Anunc-B", 0.50, "http://oferta-premium.com")

    portal.agregar_anuncio(anuncio_login)
    portal.agregar_anuncio(anuncio_post_auth)

    print("\n" + "="*50)
    print("             SIMULACIÓN DE FLUJO (CORRIDO EN FRÍO)")
    print("="*50)

    # --- PASO 1: Visita y Clic en Login (Pre-Auth) ---
    print("▶️ PASO 1: Usuario 'guest' visita el portal cautivo.")
    anuncio_servido = portal.servir_anuncio(momento_clave="LOGIN")
    print(f"   [Sistema] Servido anuncio: '{anuncio_servido.id}'.")

    # Generación de Ingreso 1
    print("\n➡️ PASO 2: El usuario hace clic en el anuncio de Login. (PPC)")
    usuario_guest = portal.usuarios_registrados["guest"]
    motor_pago.procesar_clic(anuncio_servido, usuario_guest)
    print(f"   [Motor] Ingreso registrado: ${anuncio_servido.costo_por_clic:.2f}. Clics de Anuncio: {anuncio_servido.clics_totales}")


    # --- PASO 2: Autenticación ---
    print("\n🔒 PASO 3: Intento de autenticación (Req. A).")
    usuario_sesion = portal.manejar_autenticacion("guest", "pass")

    if usuario_sesion:
        print(f"   ✅ Usuario {usuario_sesion.nombre_usuario} autenticado con éxito.")
        
        # --- PASO 3: Publicidad Post-Auth y Segundo Clic ---
        print("\n🌐 PASO 4: Acceso a Internet concedido. Se sirve publicidad Post-Auth.")
        anuncio_servido = portal.servir_anuncio(momento_clave="POST_AUTH")
        print(f"   [Sistema] Servido anuncio: '{anuncio_servido.id}'.")

        # Generación de Ingreso 2
        print("\n➡️ PASO 5: El usuario hace clic en el anuncio Post-Auth. (PPC)")
        motor_pago.procesar_clic(anuncio_servido, usuario_sesion)
        print(f"   [Motor] Ingreso registrado: ${anuncio_servido.costo_por_clic:.2f}. Clics de Anuncio: {anuncio_servido.clics_totales}")
    else:
        print("❌ Error de autenticación. Flujo detenido.")

    # --- REPORTE FINAL ---
    print("\n" + "="*50)
    print("             REPORTE FINAL DEL SISTEMA")
    print("="*50)
    print(f"💰 Ingresos Totales Generados por PPC: ${motor_pago.ingresos_totales:.2f}")
    print(f"👤 Clics de {usuario_guest.nombre_usuario} (Total): {anuncio_login.clics_totales + anuncio_post_auth.clics_totales}")
    print(f"   Detalle - Anuncio Login: {anuncio_login.clics_totales} clic(s)")
    print(f"   Detalle - Anuncio Post-Auth: {anuncio_post_auth.clics_totales} clic(s)")
    print("="*50)


if __name__ == "__main__":
    run_corrido_frio()
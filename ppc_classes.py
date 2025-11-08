class Anuncio:
    """Representa un anuncio de Pago Por Clic (PPC)."""
    def __init__(self, id_anuncio, anunciante_id, costo_por_clic, url_destino):
        self.id = id_anuncio
        self.anunciante_id = anunciante_id
        self.costo_por_clic = costo_por_clic  # Ingreso generado por cada clic
        self.url_destino = url_destino
        self.clics_totales = 0
        self.activo = True

    def registrar_clic(self):
        """Incrementa el contador de clics."""
        if self.activo:
            self.clics_totales += 1
            # Nota: El motor de pago será el responsable de mostrar el ingreso
            return True
        return False

class Usuario:
    """Representa al usuario que accede al portal cautivo."""
    def __init__(self, nombre_usuario, contrasena):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.autenticado = False
        self.gasto_en_clics = 0.0 # Rastrear la actividad del usuario

    def autenticar(self, password_ingresada):
        """Simula la verificación de credenciales."""
        if password_ingresada == self.contrasena:
            self.autenticado = True
            return True
        return False

class MotorDePago:
    """Gestor central de la lógica de ingresos y contabilidad PPC."""
    def __init__(self):
        self.ingresos_totales = 0.0
        # Registro de clics: {ID_Transaccion: (Anuncio_ID, Costo, Usuario)}
        self.registro_transacciones = {}
        self.transaccion_id_counter = 1000

    def procesar_clic(self, anuncio: Anuncio, usuario: Usuario):
        """Procesa el evento de clic, generando el ingreso y actualizando saldos."""
        if anuncio.registrar_clic():
            costo = anuncio.costo_por_clic
            self.ingresos_totales += costo
            usuario.gasto_en_clics += costo 

            # Registrar la transacción
            self.registro_transacciones[self.transaccion_id_counter] = {
                "anuncio_id": anuncio.id,
                "costo": costo,
                "usuario": usuario.nombre_usuario
            }
            self.transaccion_id_counter += 1

            return True
        return False

class Portal:
    """Simula la interfaz y el punto de acceso central."""
    def __init__(self, motor_pago: MotorDePago):
        self.anuncios = []
        self.motor_pago = motor_pago
        # Usuarios precargados para la simulación
        self.usuarios_registrados = {"admin": Usuario("admin", "1234"), "guest": Usuario("guest", "pass")}

    # REQUISITO A: Manejo de Autenticación
    def manejar_autenticacion(self, nombre, contrasena):
        if nombre in self.usuarios_registrados:
            usuario = self.usuarios_registrados[nombre]
            if usuario.autenticar(contrasena):
                return usuario
        return None

    # REQUISITO B: Mostrar Publicidad
    def servir_anuncio(self, momento_clave="LOGIN"):
        """Selecciona un anuncio basado en el momento de la sesión."""
        if not self.anuncios:
            return None

        # Lógica de selección simple
        if momento_clave == "LOGIN":
            return self.anuncios[0] # Anuncio de bajo costo
        else: # Post-Autenticación
            return self.anuncios[1] # Anuncio de alto costo/relevancia
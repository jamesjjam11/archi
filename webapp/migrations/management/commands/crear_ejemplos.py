from django.core.management.base import BaseCommand
from webapp.models import Secretaria, Unidad, Subunidad

class Command(BaseCommand):
    help = 'Crea ejemplos de Secretarias, Unidades y Subunidades en la base de datos'

    def handle(self, *args, **kwargs):
        # Función para crear ejemplos de instancias
        def crear_ejemplos():
    # Secretarías, jefatura o servicios
            gabinete = Secretaria.objects.create(nombre='GABINETE DE DESPACHO DE GOBERNACION')
            asesores_estrat = Secretaria.objects.create (nombre='ASESORES ESTRATEGICOS')
            seguridad = Secretaria.objects.create (nombre='SEGURIDAD CUIDADANA')
            comunicacion_social = Secretaria.objects.create (nombre='COMUNICACION SOCIAL')
            gestoria = Secretaria.objects.create (nombre='GESTORIA DE LA PAZ')
            secretaria_juridica = Secretaria.objects.create (nombre='SECRETARIA DEP. JURIDICA')
            auditoria_interna = Secretaria.objects.create (nombre='DIR. DEP. AUDITORIA INTERNA')
            secretaria_administrativa = Secretaria.objects.create(nombre='SECRETARIA DEP. ADMINISTRATIVA FINANCIERA')
            secre_desarrollo = Secretaria.objects.create(nombre='SECRETARIA DEP.DE DESARROLLO HUMANO ')
            secret_madre= Secretaria.objects.create(nombre='SECRETARIA DEP. DE LA MADRE TIERRA')
            secre_plani= Secretaria.objects.create(nombre='SECRETARIA DEP. DE PLANIFICACION DEL DESARROLLO')
            secre_coordi= Secretaria.objects.create(nombre='SECRETARIA DEP. DE COORDINACION GENERAL')
            secre_obras = Secretaria.objects.create(nombre='SECRETARIA DEP. DE OBRAS PUBLICAS Y SERVICIOS')
            secre_mine_meta = Secretaria.objects.create(nombre='SECRETARIA DEP. DE MINERIA Y METALURGIA')
            secre_mineria = Secretaria.objects.create(nombre='SECRETARIA DEP. DE MINERIA Y METALUGIA II')
            secre_agrope = Secretaria.objects.create(nombre='SECRETARIA DEP. DE DESARROLLO AGROP Y SEG. ALIMENTARIA')
            secre_industri = Secretaria.objects.create(nombre='SECRETARIA DEP. DE INDUSTRIALIZACION')

            # Unidades y Subunidades para Secretaría Administrativa
            seguridad_cuidadana = Unidad.objects.create(nombre='SEGURIDAD CUIDADANA', secretaria=asesores_estrat)
            juridica = Unidad.objects.create(nombre='JEFE DE UNIDAD', secretaria=secretaria_juridica)
            responsable = Unidad.objects.create(nombre='RESPONSABLE DE AREA', secretaria=auditoria_interna)

            asesor_admin = Unidad.objects.create(nombre='ASESOR ADMIN.', secretaria=secretaria_administrativa)
            asesor_legar = Unidad.objects.create(nombre='ASESOR LEGAL', secretaria=secretaria_administrativa)
            implantacion = Unidad.objects.create(nombre='IMPLANTACION', secretaria=secretaria_administrativa)
            unidad_rrhh = Unidad.objects.create(nombre='UNIDAD DE RECURSOS HUMANOS', secretaria=secretaria_administrativa)
            unidad_administrativa = Unidad.objects.create(nombre='UNIDAD ADMINISTRATIVA', secretaria=secretaria_administrativa)

            Subunidad.objects.create(nombre='CONTRATACIONES', unidad=unidad_administrativa)
            Subunidad.objects.create(nombre='BIENES Y SERVICIOS', unidad=unidad_administrativa)
            Subunidad.objects.create(nombre='ACTIVOS FIJOS', unidad=unidad_administrativa)
            Subunidad.objects.create(nombre='ALMACENES', unidad=unidad_administrativa)
            Subunidad.objects.create(nombre='MANTENIMIENTO', unidad=unidad_administrativa)
            Subunidad.objects.create(nombre='ARCHIVOS', unidad=unidad_administrativa)

            unidad_financiera = Unidad.objects.create(nombre='UNIDAD FINANCIERA', secretaria=secretaria_administrativa)

            Subunidad.objects.create(nombre='PRESUPUESTOS', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='ANALISTA PRESUPUESTOS', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='PINOS TERMINAL', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='TESORERIA', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='CREDITO PUBLICO', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='HABILITADO', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='LIQUIDADOR INGRESOS', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='CONTABILIDAD', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='LIQUIDADROS CONTABLE', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='ANALISTA CONTABLE', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='KARDIXTA', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='ASISTENTE CONTABLE', unidad=unidad_financiera)
            Subunidad.objects.create(nombre='SISTEMAS', unidad=unidad_financiera)

            # Unidades y Subunidades para Secretaría desarrolo
            coordi_inter = Unidad.objects.create(nombre='COORDINADOR INTERSECTORIAL', secretaria=secre_desarrollo)
            codepis = Unidad.objects.create(nombre='CODEPEDIS', secretaria=secre_desarrollo)
            area_social = Unidad.objects.create(nombre='AREA SOCIAL GENERO', secretaria=secre_desarrollo)
            servicio_deporte = Unidad.objects.create(nombre='SERVICIO DEP. DE DEPOR "SE.DE.DE."', secretaria=secre_desarrollo)
            serv_gestion = Unidad.objects.create(nombre='SERVICIO DEP. DE GESTION SOCIAL "SEDEGES"', secretaria=secre_desarrollo)
            serv_salud = Unidad.objects.create(nombre='SERCIVIO DEP. DE SALUD "SEDES"', secretaria=secre_desarrollo)

            # Unidades y Subunidades para Secretaría madre tierra
            asis_juri = Unidad.objects.create(nombre='ASISTENTE JURIDICO',secretaria=secret_madre)
            renca = Unidad.objects.create(nombre='RENCA',secretaria=secret_madre)
            jfe_uni = Unidad.objects.create(nombre='JEFE DE UNIDAD UNASBA',secretaria=secret_madre)
            uni_gesti = Unidad.objects.create(nombre='UNIDAD GESTION AMB. Y USO RR.NN.',secretaria=secret_madre)
            uni_terri = Unidad.objects.create(nombre='UNIDAD GESTION TERRITORIALY MANEJO DE CUENCAS',secretaria=secret_madre)
            centro_docu = Unidad.objects.create(nombre='CENTRO INF. DOCUMENTAL',secretaria=secret_madre)

            #subunidad de unidad de gestion amb 
            Subunidad.objects.create(nombre='GESTION AMB. REG. ING. CIVIL.', unidad=uni_gesti)
            Subunidad.objects.create(nombre='GESTION AMB. REG. ING. METAL MINAS', unidad=uni_gesti)
            Subunidad.objects.create(nombre='GESTION AMB. REG. ING. AGRONOMO', unidad=uni_gesti)
            Subunidad.objects.create(nombre='GESTION AMB. REG. ING. AMBIENTAL', unidad=uni_gesti)
            Subunidad.objects.create(nombre='GESTION AMB. REG. AGRON AMBIENT', unidad=uni_gesti)
            #subunidad de unidad de gestion terri
            Subunidad.objects.create(nombre='MANEJO INTEG. CUENCAS Y REC. HIDRIC USO SUEL', unidad=uni_terri)
            Subunidad.objects.create(nombre='MANEJO INTEG. CUENCAS REC. H.', unidad=uni_terri)
            Subunidad.objects.create(nombre='GESTOR SOCIAL', unidad=uni_terri)

            # Unidades y Subunidades para Secretaría de planificacion
            area_plani = Unidad.objects.create(nombre='AREA DE PLANIFICACION Y PROYECTOS', secretaria=secre_plani)
            area_orga = Unidad.objects.create(nombre='AREA DES. ORGANIZACIONAL', secretaria=secre_plani)
            area_opera = Unidad.objects.create(nombre='AREA PROG. OPERACIONES Y SEGUIMIENTOS', secretaria=secre_plani)

            #subunidad del area de planificacion y proyectos
            Subunidad.objects.create(nombre='MOVIMIENTOS SOCIALES', unidad=area_plani)
            Subunidad.objects.create(nombre='AUTONOMIAS', unidad=area_plani)
            Subunidad.objects.create(nombre='OFICIAL DE GOBIERNO', unidad=area_plani)
            Subunidad.objects.create(nombre='UDAIPO', unidad=area_plani)

            #subunidad del area de desarrllo organizacional
            Subunidad.objects.create(nombre='DES. ORGANIZACIONAL DE REGLAMENTOS', unidad=area_orga)
            Subunidad.objects.create(nombre='DES. ORGANIZACIONAL DE MANUALES', unidad=area_orga)

            #subunidad del area de operaciones y seguimientos
            Subunidad.objects.create(nombre='ANALISTAS ADM. PROYECTOS', unidad=area_opera)
            Subunidad.objects.create(nombre='SIGEPRO', unidad=area_opera)

            # Unidades y Subunidades para Secretaría de de coordinacion
            asesor_leg = Unidad.objects.create(nombre='ASESOR LEGAL JURIDICO',secretaria=secre_coordi)
            delegado_prov = Unidad.objects.create(nombre='DELEGADO PROVINCIAL',secretaria=secre_coordi)
            movim_socia = Unidad.objects.create(nombre='MOVIMIENTOS SOCIALES',secretaria=secre_coordi)
            limites = Unidad.objects.create(nombre='LIMITES',secretaria=secre_coordi)
            autonomo = Unidad.objects.create(nombre='AUTONOMIAS',secretaria=secre_coordi)
            ofic_gob = Unidad.objects.create(nombre='OFICIAL DE GOBIERNO',secretaria=secre_coordi)
            udaipo = Unidad.objects.create(nombre='UDAIPO',secretaria=secre_coordi)

            #subunidad de limites
            Subunidad.objects.create(nombre='ING. GEODESTA PROFESIONAL II', unidad=limites)
            Subunidad.objects.create(nombre='REP. LIMITES TECNICO I', unidad=limites)
            Subunidad.objects.create(nombre='TOPOGRAFO PROFESIONAL II', unidad=limites)

            # Unidades y Subunidades para Secretaría de obras publicas
            econom = Unidad.objects.create(nombre='ECONOMISTA',secretaria=secre_obras)
            serv_camin = Unidad.objects.create(nombre='SERVICIO DEP. DE CAMINOS',secretaria=secre_obras)
            electri_rural = Unidad.objects.create(nombre='ELECTRIFICACION RURAL',secretaria=secre_obras)
            obras_civil = Unidad.objects.create(nombre='OBRAS CIVILES',secretaria=secre_obras)
            infra_vial = Unidad.objects.create(nombre='INFRAESTRUCTURA VIAL',secretaria=secre_obras)

            #subunidad de electrificacion rural
            Subunidad.objects.create(nombre='ING. ELECTRICOS', unidad=electri_rural)

            #subunidad de eobras civiles
            Subunidad.objects.create(nombre='INGENIEROS CIVILES', unidad=obras_civil)
            Subunidad.objects.create(nombre='INGENIEROS ARQUITECTOS', unidad=obras_civil)

            #subunidad de infraestructura vial
            Subunidad.objects.create(nombre='ING. CIVILES', unidad=infra_vial)
            Subunidad.objects.create(nombre='HIDROLOGO', unidad=infra_vial)
            Subunidad.objects.create(nombre='GEOLOGO', unidad=infra_vial)

            # Unidades y Subunidades para Secretaría de mineria y metalur
            unidad_mine = Unidad.objects.create(nombre='UNIDAD MINERA METALURGICA', secretaria=secre_mine_meta)
            unid_planiseg = Unidad.objects.create(nombre='UNID. PLANIFICACION SEG. PROSP. EXPLORACION', secretaria=secre_mine_meta)
            recau_per = Unidad.objects.create(nombre='RECAUDACION PERCEPCION CONTROL RAGALIAS MINERAS', secretaria=secre_mine_meta)

            #subunidad de unidad minera
            Subunidad.objects.create(nombre='CONTROL DE OPERACIONES', unidad=unidad_mine)
            Subunidad.objects.create(nombre='SUP. PLANTAS', unidad=unidad_mine)
            Subunidad.objects.create(nombre='SUP. COMERCIALIZADORES', unidad=unidad_mine)
            Subunidad.objects.create(nombre='LABORATORIOS QUIMICOS MUESTRAS', unidad=unidad_mine)
            Subunidad.objects.create(nombre='CONTROL DE BALANZAS', unidad=unidad_mine)

            #subunidad de planificaciomn y seg. pros
            Subunidad.objects.create(nombre='PROSP EXPLORACION SEG. COPERATIVO', unidad=unid_planiseg)
            Subunidad.objects.create(nombre='PROSP EXPLORACION SEG. S. MINERO', unidad=unid_planiseg)

            #subunidad de minera RECAUDACION PERCEPCION CONTROL RAGALIAS MINERAS
            Subunidad.objects.create(nombre='CONTROL FISCALIZACION', unidad=recau_per)
            Subunidad.objects.create(nombre='PUNTOS DE CONTROL', unidad=recau_per)
            Subunidad.objects.create(nombre='CONTROL DE LIBROS', unidad=recau_per)
            Subunidad.objects.create(nombre='FORMULARIO 101', unidad=recau_per)

            # Unidades y Subunidades para Secretaría de mineria y metalurgia II
            cultura = Unidad.objects.create(nombre='CULTURA', secretaria=secre_mineria)
            turismo = Unidad.objects.create(nombre='TURISMO',secretaria=secre_mineria)

            #subunidad de cultura
            Subunidad.objects.create(nombre='PATRIMONIO MUSEOS Y ARCH. HISTORICOS', unidad=cultura)
            Subunidad.objects.create(nombre='FOMENTOS ARTES Y SABERES', unidad=cultura)

            #subunidad de turismo
            Subunidad.objects.create(nombre='CONTROL DE FISCALIZACION', unidad=turismo)
            Subunidad.objects.create(nombre='PUNTOS DE CONTROL', unidad=turismo)
            Subunidad.objects.create(nombre='CONTROL DE LIBROS', unidad=turismo)
            Subunidad.objects.create(nombre='FORMULARIO 101', unidad=turismo)

            # Unidades y Subunidades para Secretaría de desarrollo agropecuadio
            riego = Unidad.objects.create(nombre='RIEGO', secretaria=secre_agrope)
            riesgos = Unidad.objects.create(nombre='RIESGOS', secretaria=secre_agrope)

            #subunidad de riego
            Subunidad.objects.create(nombre='ING. CIVILES', unidad=riego)
            Subunidad.objects.create(nombre='HIDROLOGO', unidad=riego)
            Subunidad.objects.create(nombre='GEOLOGO', unidad=riego)
            Subunidad.objects.create(nombre='AGRONOMO', unidad=riego)

            #subunidad de riesgos
            Subunidad.objects.create(nombre='GESTACION Y MITIGACION', unidad=riesgos)
            Subunidad.objects.create(nombre='REHABILITACION RECONSTRUCCION', unidad=riesgos)
            Subunidad.objects.create(nombre='PREVENCION ALERTA TEMPRANA', unidad=riesgos)
            Subunidad.objects.create(nombre='APOYO AL DESARROLLO', unidad=riesgos)
            Subunidad.objects.create(nombre='OPERADORES EQUIPO', unidad=riesgos)
            # Unidades y Subunidades para Secretaría de industrializacion
            plani_desa = Unidad.objects.create(nombre='PLANIFICACION DESARROLLO EMPRESAR. PUBLICO', secretaria=secre_industri)
            investiga = Unidad.objects.create(nombre='INVESTIGACION DE MERCADO', secretaria=secre_industri)

            #subunidad de planificacion desarrollo
            Subunidad.objects.create(nombre='PLANIFICACION DESARROLLO EMPRESAR. PRIVADO', unidad=plani_desa)
            Subunidad.objects.create(nombre='INDUSTRIAL MECANICO', unidad=plani_desa)
            Subunidad.objects.create(nombre='INDUISTRIAL ELECTRICO', unidad=plani_desa)
            #subunidad de investigacion de marcado
            Subunidad.objects.create(nombre='PLANIFICACION DESARROLLO MINERO PROSP. E.', unidad=investiga)
            Subunidad.objects.create(nombre='PLANIFICACION DESARROLLO AGROP. E INDUSTRIAL', unidad=investiga)

        # Llamar a tu función crear_ejemplos()
        crear_ejemplos()

        self.stdout.write(self.style.SUCCESS('Se han creado los ejemplos exitosamente'))

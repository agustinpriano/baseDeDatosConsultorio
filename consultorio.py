import sqlite3
import datetime
import os
base=sqlite3.connect('d:\CONHHDORIdddO15-11-17.db')
cur=base.cursor()

TABLA_MEDICOS="""CREATE TABLE MEDICOS(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                      COD_MEDICO INTEGER NOT NULL,
                                      NOMBRE TEXT NOT NULL,
                                      APELLIDO TEXT NOT NULL);"""
TABLA_PACIENTES="""CREATE TABLE PACIENTES(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                      DNI INTEGER NOT NULL,
                                      NOMBRE TEXT NOT NULL,
                                      APELLIDO TEXT NOT NULL);"""

TABLA_TURNOS="""CREATE TABLE TURNOS(
                                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    ID_PACIENTE    INTEGER,
                                    ID_MEDICO  INTEGER,
                                    FECHA  DATE DEFAULT CURRENT_TIMESTAMP,
                                    FECHA_TURNO DATETIME,
                                    FOREIGN KEY(ID_PACIENTE) REFERENCES PACIENTES(ID),
                                    FOREIGN KEY(ID_MEDICO) REFERENCES MEDICOS(ID));"""

def crearTablas():
    cur.execute(TABLA_MEDICOS)
    cur.execute(TABLA_PACIENTES)
    cur.execute(TABLA_TURNOS)

def ingresarMedicos():
    seguir='S'
    while seguir=='S' or seguir=='s':
        print("- DENTISTAS -")
        nombreM = input("Nombre: ")
        apellidoM = input("Apellido: ")
        codM = validezCodMedico()
        nombreM = nombreM.upper()
        apellidoM = apellidoM.upper()
        cur.execute('INSERT INTO MEDICOS(NOMBRE,APELLIDO,COD_MEDICO) VALUES ("{}","{}","{}");'.format(nombreM, apellidoM, codM))
        base.commit()
        seguir = input("¿Desea seguir ingresando? (S/N): ")
        while seguir != 'S' and seguir != 'N' and seguir != 's' and seguir != 'n':
            seguir = input("¿Desea seguir ingresando? (S/N): ")
        os.system("cls")


def ingresarPacientes(dniP):
    seguir = 'S'
    if dniP==0:
        while seguir == 'S' or seguir == 's':
            print("- PACIENTES -")
            nombreP = input("Nombre: ")
            apellidoP = input("Apellido: ")
            if dniP==0:
                dniP=validezDni()
            nombreP = nombreP.upper()
            apellidoP = apellidoP.upper()
            cur.execute('INSERT INTO PACIENTES(NOMBRE,APELLIDO,DNI) VALUES ("{}","{}","{}");'.format(nombreP, apellidoP, dniP))
            base.commit()
            seguir = input("¿Desea seguir ingresando? (S/N): ")
            while seguir!='S' and seguir !='N' and seguir !='s' and seguir !='n' and dniP==0:
                seguir = input("¿Desea seguir ingresando? (S/N): ")
            dniP=0
    if dniP != 0:
        nombreP = input("Nombre: ")
        apellidoP = input("Apellido: ")
        print("DNI: ", dniP)
        nombreP = nombreP.upper()
        apellidoP = apellidoP.upper()
        cur.execute(
                'INSERT INTO PACIENTES(NOMBRE,APELLIDO,DNI) VALUES ("{}","{}","{}");'.format(nombreP, apellidoP, dniP))
        base.commit()

    dniP=0
    os.system("cls")

def validezDni():
    flag=0
    contador=0
    while flag==0:
        dniP = int(input("DNI: "))
        cur.execute('SELECT DNI FROM PACIENTES')
        listaDni=cur.fetchall()
        contador = 0
        for x in range(len(listaDni)):
            if listaDni[x][0]==dniP:
                print("El DNI ingresado no es valido")
            else:
                contador=contador+1
        if contador==len(listaDni):
            flag=1
    return dniP

def validezCodMedico():
    flag = 0
    contador = 0
    while flag == 0:
        codM = int(input("Codigo del medico: "))
        cur.execute('SELECT COD_MEDICO FROM MEDICOS')
        listaCod = cur.fetchall()
        contador = 0
        for x in range(len(listaCod)):
            if listaCod[x][0] == codM:
                print("El codigo de medico ingresado no es valido")
            else:
                contador = contador + 1
        if contador == len(listaCod):
            flag = 1
    return codM

def asignarTurnos():
    listaMedicos=[]
    dniP=int(input("DNI: "))
    ok=0
    while ok!=1:
        cur.execute('SELECT ID FROM PACIENTES WHERE "{}"=DNI;'.format(dniP))
        idP=cur.fetchall()
        if idP==[]:
            print("El paciente no se encuentra en el sistema, regístrelo")
            os.system("cls")
            ingresarPacientes(dniP)
            ok=0
        else:
            print("Esta registrado")
            ok=elegirTurno(idP)


def imprimirListaDeMedicos(lista):
    for x in lista:
        print(x[0], ": ", x[1], " ", x[2])

def validezDoctor(lista):
    idMed = int(input("Medico deseado: "))
    while idMed > len(lista):
        idMed = int(input("Medico deseado: "))
    return idMed


def validezMes(mesActual):
    mesTurno = int(input("Mes: "))
    while mesTurno > 12 or mesTurno < 0 or mesTurno < mesActual or mesTurno >= mesActual + 2:
        if mesTurno < mesActual:
            print("Mes invalido")
        if mesTurno >= mesActual + 2:
            print("Mes invalido; el turno tiene que estar establecido del mes actual a dos meses.")
        mesTurno = int(input("Mes: "))
    return mesTurno


def validezDia(mesTurno, diaActual, mesActual):
    if mesTurno % 2 == 1 or mesTurno == 8:
        flag = 0
        diaTurno = int(input("Dia: "))
        if mesActual == mesTurno:
            if diaActual > diaTurno:
                flag = 1
            else:
                flag = 0
        while diaTurno > 31 or diaTurno < 0 or flag == 1:
            if mesActual == mesTurno:
                if diaActual > diaTurno:
                    flag = 1
                    print("Dia invalido")
                else:
                    flag = 0
            diaTurno = int(input("Dia: "))
    else:
        flag = 0
        diaTurno = int(input("Dia: "))
        if mesActual == mesTurno:
            if diaActual > diaTurno:
                flag = 1
            else:
                flag = 0
        while diaTurno > 30 or diaTurno < 0 or flag == 1:
            if mesActual == mesTurno:
                if diaActual > diaTurno:
                    flag = 1
                    print("Dia invalido")
                else:
                    flag = 0
            diaTurno = int(input("Dia: "))

    return diaTurno


def validezHora():
    horaTurno = int(input("Hora: "))
    while horaTurno > 20 or horaTurno < 8:
        horaTurno = int(input("Hora: "))
    return horaTurno

def elegirTurno(idP):
    turnoOc=0
    turnosDeMedico=[]
    cur.execute('SELECT ID,NOMBRE,APELLIDO FROM MEDICOS;')
    listaMedicos = cur.fetchall()
    cur.execute("SELECT date('now');")
    fechaActual=cur.fetchall()
    fechaActual=fechaActual[0][0]
    fechaActual=fechaActual.split("-")
    añoActual=int(fechaActual[0])
    mesActual=int(fechaActual[1])
    diaActual=int(fechaActual[2])
    imprimirListaDeMedicos(listaMedicos)
    idMed = validezDoctor(listaMedicos)
    mesTurno = validezMes(mesActual)
    diaTurno = validezDia(mesTurno,diaActual,mesActual)
    añoTurno = añoActual
    print("Año: ",añoActual)
    horaTurno=validezHora()
    turno = datetime.datetime(añoTurno, mesTurno, diaTurno, horaTurno)
    turno.strftime("%Y-%m-%d %H:%M:%S")
    idP=idP[0][0]
    turnoOc=chequeoDisponibilidadDelMedico(turno,idMed)
    while turnoOc==1:
        cur.execute('SELECT NOMBRE FROM MEDICOS WHERE "{}"=ID;'.format(idMed))
        nombre=cur.fetchall()
        cur.execute('SELECT APELLIDO FROM MEDICOS WHERE "{}"=ID;'.format(idMed))
        apellido=cur.fetchall()
        print("El turno esta ocupado")
        print("Turnos del medico ",nombre[0][0],"",apellido[0][0],": ")
        turnosDeMedico=mostrarTurnosDeMedico(idMed)
        for x in range(len(turnosDeMedico)):
            print(turnosDeMedico[x][0])
        mesTurno=validezMes(mesActual)
        diaTurno=validezDia(mesTurno,diaActual,mesActual)
        añoTurno = añoActual
        print("Año: ",añoActual)
        horaTurno = validezHora()
        turno = datetime.datetime(añoTurno, mesTurno, diaTurno, horaTurno)
        turno.strftime("%Y-%m-%d %H:%M:%S")
        turnoOc = chequeoDisponibilidadDelMedico(turno, idMed)

    cur.execute(
        'INSERT INTO TURNOS(ID_PACIENTE,ID_MEDICO,FECHA_TURNO) VALUES ("{}","{}","{}");'.format(
            idP, idMed,turno))
    base.commit()
    ok = 1
    return ok

def chequeoDisponibilidadDelMedico(turno,idMed): #Tengo que hacer una query para recorrer los datos del medico
    cur.execute('SELECT FECHA_TURNO FROM TURNOS WHERE "{}"=ID_MEDICO;'.format(idMed))
    ok=0
    listaDeTurnos=cur.fetchall()
    turno=str(turno) #Por que tengo que hacer esto si en la tabla se tendria que guardar como DATETIME y no como string
    for x in listaDeTurnos:
        if x[0]==turno:
            ok=1
    return ok

def mostrarTurnosDeMedico(idMed):
    cur.execute('SELECT FECHA_TURNO FROM TURNOS WHERE "{}"=ID_MEDICO;'.format(idMed))
    listaDeTurnos=cur.fetchall()
    return listaDeTurnos

def verTurnos():
    os.system("cls")
    print("- TURNOS -")
    print("1. Medico")
    print("2. Paciente")
    opcion=int(input(""))
    if opcion==1:
        nombreM=input("Nombre (medico): ")
        apellidoM = input("Apellido (medico): ")
        cur.execute('SELECT ID FROM MEDICOS WHERE "{}"=NOMBRE AND "{}"=APELLIDO;'.format(nombreM,apellidoM))
        idMed=cur.fetchall()
        if idMed==[]:
            print("El medico no tiene ningun turno asignado")
        else:
            idMed = idMed[0][0]
            cur.execute('SELECT FECHA_TURNO FROM TURNOS WHERE "{}"=ID_MEDICO;'.format(idMed))
            listaDeTurnos=cur.fetchall()
            print("Turnos del medico ", nombreM, "", apellidoM, ": ")
            for x in range(len(listaDeTurnos)):
                print(listaDeTurnos[x][0])
    if opcion==2:
        nombreP = input("Nombre (paciente): ")
        apellidoP = input("Apellido (paciente): ")
        cur.execute('SELECT ID FROM PACIENTES WHERE "{}"=NOMBRE AND "{}"=APELLIDO;'.format(nombreP, apellidoP))
        idP=cur.fetchall()
        if idP==[]:
            print("El paciente no tiene ningun turno asignado")
        else:
            idP = idP[0][0]
            cur.execute('SELECT FECHA_TURNO FROM TURNOS WHERE "{}"=ID_PACIENTE;'.format(idP))
            listaDeTurnos = cur.fetchall()
            print("Turnos del paciente ", nombreP, "", apellidoP, ": ")
            for x in range(len(listaDeTurnos)):
                print(listaDeTurnos[x][0])



crearTablas()
seguir='s'
opcion=0
while seguir!='n' and seguir!='N':
    print("Consultorio")
    print("1. Registrar médico")
    print("2. Registrar paciente")
    print("3. Asignar turno")
    print("4. Ver turno/s")
    print("5. Salir")
    opcion = int(input(""))
    os.system("cls")
    if opcion == 1:
        ingresarMedicos()
    if opcion == 2:
        ingresarPacientes(0)
    if opcion==3:
        asignarTurnos()
    if opcion==4:
        verTurnos()
    if opcion!=5:
        seguir=input(("¿Desea continuar en la base de datos? (S/N): "))
        while seguir!='S' and seguir !='N' and seguir !='s' and seguir !='n':
            seguir = input("¿Desea continuar en la base de datos? (S/N): ")
        os.system("cls")
base.commit()

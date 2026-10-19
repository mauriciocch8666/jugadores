from flask import Flask, render_template, request, redirect, url_for
import json
import os

# Crear la aplicación
app = Flask(__name__)

# Ubicación del proyecto
carpeta = os.path.dirname(os.path.abspath(__file__))

# Archivo donde se guardan los jugadores
mauricio = os.path.join(carpeta, "jugadores.json")


# Cargar jugadores (crea el archivo automáticamente si no existe)
def cargar_jugadores():
    if not os.path.exists(mauricio):
        with open(mauricio, "w", encoding="utf-8") as mau:
            json.dump([], mau, ensure_ascii=False)
            
    with open(mauricio, "r", encoding="utf-8") as mau:
        jugadores = json.load(mau)

    return jugadores


# Guardar jugadores
def guardar_jugadores(jugadores):
    with open(mauricio, "w", encoding="utf-8") as mau:
        json.dump(
            jugadores,
            mau,
            indent=4,
            ensure_ascii=False
        )


# Página principal
@app.route("/")
def inicio():
    return render_template("index.html")


# Mostrar jugadores
@app.route("/jugadores")
def mostrar_jugadores():
    jugadores = cargar_jugadores()

    return render_template(
        "jugadores.html",
        jugadores=jugadores
    )


# Registrar jugador
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        jugadores = cargar_jugadores()

        nuevo = {
            "nombre": request.form["nombre"],
            "edad": request.form["edad"],
            "nacionalidad": request.form["nacionalidad"],
            "posicion": request.form["posicion"],
            "numero": request.form["numero"],
            "equipo": request.form["equipo"],
            "valor": request.form["valor"]
        }

        jugadores.append(nuevo)
        guardar_jugadores(jugadores)

        return redirect(url_for("mostrar_jugadores"))

    return render_template("registrar.html")


# Editar jugador
@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar(indice):
    jugadores = cargar_jugadores()

    if indice < 0 or indice >= len(jugadores):
        return redirect(url_for("mostrar_jugadores"))

    if request.method == "POST":
        jugadores[indice]["nombre"] = request.form["nombre"]
        jugadores[indice]["edad"] = request.form["edad"]
        jugadores[indice]["nacionalidad"] = request.form["nacionalidad"]
        jugadores[indice]["posicion"] = request.form["posicion"]
        jugadores[indice]["numero"] = request.form["numero"]
        jugadores[indice]["equipo"] = request.form["equipo"]
        jugadores[indice]["valor"] = request.form["valor"]

        guardar_jugadores(jugadores)

        return redirect(url_for("mostrar_jugadores"))

    jugador = jugadores[indice]

    return render_template(
        "editar.html",
        jugador=jugador,
        indice=indice
    )


# Eliminar jugador
@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):
    jugadores = cargar_jugadores()

    if indice < 0 or indice >= len(jugadores):
        return redirect(url_for("mostrar_jugadores"))

    jugadores.pop(indice)
    guardar_jugadores(jugadores)

    return redirect(url_for("mostrar_jugadores"))


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
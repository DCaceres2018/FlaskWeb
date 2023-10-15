from flask import Flask, render_template, request, redirect, url_for, session
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'
logged_in = False

@app.route('/')
def inicio():
    session.clear()
    return render_template('index.html', login_successful=False)


@app.route('/index')
def index():
    # Verifica si el usuario ha iniciado sesión
    if 'username' in session:
        username = session['username']
        # Obtiene la información de la foto de perfil del usuario desde la base de datos simulada
        user_info = users.get(username)

        # Si el usuario no tiene información de foto de perfil, utiliza una imagen predeterminada
        profile_image = users[username].get("profile_image")
        return render_template('index.html', profile_image=profile_image, login_successful=True)
    else:
        return render_template('index.html', login_successful=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar si el usuario existe en la base de datos y si la contraseña es correcta

        if username in users and users[username].get("password") == password:
            # El usuario ha iniciado sesión correctamente
            logged_in = True
            session['username'] = username
            return redirect(url_for('index', login_successful=True))

        # Si hay un error, establecer un mensaje de error
        error_message = 'El usuario o la contraseña son incorrectos.'
        return render_template('login.html', error_message=error_message)

    # Si el usuario no ha iniciado sesión, muestra el formulario de inicio de sesión
    return render_template('login.html')


users = {
    'user1': {
        'password': '1',
        'profile_image': 'user1-profile.jpg'
    },
    'user2': {
        'password': 'password2',
        'profile_image': 'user-icon.png'
    }
}


@app.route('/upload_profile_image', methods=['POST'])
def upload_profile_image():
    if 'new_profile_image' in request.files:
        new_image = request.files['new_profile_image']

        if new_image.filename != '':
            # Obtiene el nombre del usuario desde la sesión
            username = session['username']

            # Guarda la nueva imagen de perfil con el nombre de usuario
            filename = f'{username}-profile.jpg'
            new_image.save(os.path.join('static', filename))

            # Actualiza la información de la foto de perfil del usuario en la base de datos simulada
            users[username]['profile_image'] = filename

    # Redirige de nuevo a la página de perfil
    return redirect(url_for('index', login_successful=True, ))


@app.route('/profile')
def profile():
    # Obtiene el nombre de usuario desde la sesión
    username = session.get('username')

    # Si el usuario no tiene información de foto de perfil, utiliza una imagen predeterminada
    profile_image = users[username].get("profile_image")

    return render_template('profile.html', profile_image=profile_image)


# Ruta para mostrar la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            error_message = 'Las contraseñas no coinciden.'
            return render_template('register.html', error_message=error_message)

        # Verificar si el usuario ya existe en la base de datos
        if username in users:
            error_message = 'El usuario ya existe.'
            return render_template('register.html', error_message=error_message)

        # Si no hay errores, agregar el usuario a la base de datos (simulado)
        users[username] = {
            'password': password,
            'profile_image': "user-icon.png"
        }
        # Redirigir al usuario a la página de inicio de sesión o mostrar un mensaje de éxito
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html', login_successful=False)


@app.route('/contacto')
def contact():
    return render_template('contacto.html')


@app.route('/reto')
def reto():
    username = session.get('username')

    # Si el usuario no tiene información de foto de perfil, utiliza una imagen predeterminada
    profile_image = users[username].get("profile_image")

    return render_template('reto.html', login_successful=True, profile_image=profile_image)


if __name__ == '__main__':
    app.run()

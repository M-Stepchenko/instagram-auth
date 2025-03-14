from flask import Flask, request, jsonify, render_template_string
from instagrapi import Client
import json

app = Flask(__name__)

def create_session(username, password):
    """Создает сессию и возвращает её в виде текста."""
    cl = Client()
    try:
        cl.login(username, password)
        print("Авторизация успешна!")
        # Сохраняем сессию в виде словаря
        session_data = cl.get_settings()
        return json.dumps(session_data)  # Возвращаем сессию в виде JSON-строки
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None

@app.route("/")
def index():
    """Отображает HTML-страницу."""
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Авторизация Instagram</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            .container {
                max-width: 400px;
                margin: 0 auto;
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
            }
            .output {
                margin-top: 20px;
                padding: 10px;
                background: #f4f4f4;
                border: 1px solid #ccc;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Авторизация Instagram</h1>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Логин" required>
                <input type="password" id="password" placeholder="Пароль" required>
                <button type="submit">Авторизоваться</button>
            </form>
            <div id="output" class="output" style="display: none;">
                <p>Скопируйте этот текст и отправьте его:</p>
                <textarea id="sessionText" rows="10" readonly></textarea>
                <button onclick="copyToClipboard()">Скопировать в буфер обмена</button>
            </div>
        </div>

        <script>
            document.getElementById("loginForm").addEventListener("submit", async (e) => {
                e.preventDefault();

                const username = document.getElementById("username").value;
                const password = document.getElementById("password").value;

                const response = await fetch("/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, password }),
                });

                const result = await response.json();

                if (result.session) {
                    document.getElementById("sessionText").value = result.session;
                    document.getElementById("output").style.display = "block";
                } else {
                    alert(result.error || "Ошибка авторизации");
                }
            });

            function copyToClipboard() {
                const textarea = document.getElementById("sessionText");
                textarea.select();
                document.execCommand("copy");
                alert("Текст скопирован в буфер обмена!");
            }
        </script>
    </body>
    </html>
    """)

@app.route("/login", methods=["POST"])
def login():
    """Обрабатывает запрос на авторизацию."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Логин и пароль обязательны"}), 400

    session_text = create_session(username, password)
    if session_text:
        return jsonify({"session": session_text})
    else:
        return jsonify({"error": "Ошибка авторизации"}), 401

if __name__ == "__main__":
    app.run(debug=True)
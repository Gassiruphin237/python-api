from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("La clé API est manquante. Assurez-vous que le fichier .env contient la clé API.")

# Configuration du SDK avec la clé API
genai.configure(api_key=API_KEY)

# Initialisation de l'application Flask
app = Flask(__name__)

# Appliquer CORS à l'application Flask
CORS(app, resources={r"/*": {"origins": "*"}})

# Création d'un modèle génératif spécifique ('gemini-1.0-pro')
model = genai.GenerativeModel('gemini-1.0-pro')
chat = model.start_chat(history=[])

# Route pour envoyer un message à l'API
@app.route('/send/message', methods=['POST'])
def send_message():
    try:
        # Récupérer les données envoyées dans la requête
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message manquant dans la requête."}), 400

        # Envoyer le message au modèle
        question = data['message'].strip()
        response = chat.send_message(question)

        # Retourner la réponse en JSON
        return jsonify({"response": response.text})

    except genai.types.generation_types.StopCandidateException:
        return jsonify({"error": "Le modèle a détecté un problème avec votre message. Essayez de reformuler."}), 403
    except Exception as e:
        return jsonify({"error": f"Une erreur est survenue : {str(e)}"}), 500

if __name__ == "__main__":
    # Lancement du serveur Flask
    print("Démarrage du serveur ....")
    app.run(debug=True, port=5000)  # API accessible sur http://127.0.0.1:5000/send/message

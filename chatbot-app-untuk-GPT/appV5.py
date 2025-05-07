from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Konfigurasi API Key Gemini
genai.configure(api_key="AIzaSyCXyum_TusrQA1H-HSCpmOy1MsXoSCwz9A")

# Masukkan knowledge base kamu di sini
# Baca knowledge base dari file txt
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    knowledge_base = f.read()

# Inisialisasi model dengan system_instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction= knowledge_base
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "Tidak ada pesan yang dikirim."})

    try:
        response = model.generate_content(user_message)
        raw_text = response.text

        # Format respons:
        formatted = raw_text.replace("* **", "\n• ").replace("**", "")  # ganti bullet Gemini jadi bullet list
        if "Silakan tanyakan" in formatted:
            # Pisahkan sapaan awal dengan jawaban
            parts = formatted.split("Silakan tanyakan", 1)
            greeting = parts[0].strip() + "\n"
            body = "Silakan tanyakan" + parts[1]
            final_response = f"{greeting}\n{body}"
        else:
            final_response = formatted

        return jsonify({"response": final_response.strip()})
    except Exception as e:
        return jsonify({"response": f"Terjadi kesalahan: {str(e)}"})
    
if __name__ == "__main__":
    app.run(debug=True)

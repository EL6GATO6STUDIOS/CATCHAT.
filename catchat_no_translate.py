
import streamlit as st
import datetime
import json
import openai
import os
from pathlib import Path

# API anahtarınızı buraya ekleyin (veya .env dosyasından çekin)
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="CatChat - Patili Yapay Zekâ", layout="wide")

# Başlık
st.title("😺 CatChat - Patili Yapay Zekâ Danışmanın")
st.markdown("Her konuda miyavlar! Tüm konuşmalar kayıt altında. 🐾")

# Kullanıcı adı al
user = st.sidebar.text_input("Kullanıcı Adınız", value="misafir")

# Konuşma geçmişi dosya yolu
data_dir = Path("catchat_logs")
data_dir.mkdir(exist_ok=True)
user_file = data_dir / f"{user}.json"

# Geçmiş konuşmaları yükle
if user_file.exists():
    with open(user_file, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

# Sol panelde geçmiş konuşmalar
st.sidebar.markdown("### Geçmiş Konuşmalar")
for item in history[::-1][:10]:
    with st.sidebar.expander(item['timestamp']):
        st.markdown(f"**Soru:** {item['question']}")
        st.markdown(f"**Yanıt:** {item['answer']}")

# Soru giriş
question = st.text_area("Bir şey sor:", placeholder="Merhaba kedi, bana hava durumu hakkında bilgi verir misin?")

if st.button("😺 Miyavla!"):
    if question.strip():
        try:
            # OpenAI API ile yanıt al
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful and playful cat that responds like a wise and funny feline assistant."},
                    {"role": "user", "content": question}
                ]
            )

            final_answer = f"😺 Miyavvv~ {response['choices'][0]['message']['content']}"

            st.markdown(f"**Yanıt:** {final_answer}")

            # Cevabı kaydet
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history.append({
                "timestamp": now,
                "question": question,
                "answer": final_answer
            })

            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

        except Exception as e:
            st.error(f"Bir patili hata oluştu: {str(e)}")
    else:
        st.warning("Lütfen önce bir soru sor miyav!")

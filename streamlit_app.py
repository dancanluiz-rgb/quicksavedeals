streamlit run app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

st.set_page_config(page_title="QuickSaveDeals", page_icon="🛒")

st.title("🛒 QuickSaveDeals – Seu caçador automático de promoções")
st.caption("Foco EUA + Canadá | 10+ posts por dia | Tudo grátis")

# Bandeira
pais = st.sidebar.selectbox("🌎 País", ["EUA + Canadá", "Brasil (em breve)"])

# Categorias que você pediu
categorias = {
    "🏠 Organização da Casa": ["organizer", "storage box", "shelf organizer"],
    "🤖 Eletrodomésticos": ["robot vacuum", "coffee maker", "4K TV", "air fryer"],
    "💡 Iluminação": ["smart bulb", "LED lamp", "floor lamp"],
    "🔒 Segurança": ["4K security camera", "outdoor camera", "ring doorbell"],
    "🌿 Jardim Interno": ["smart plant waterer", "self watering pot"],
    "💄 Beleza & Skincare": ["cerave", "the ordinary", "la mer", "retinol serum"],
    "🧸 Brinquedos Premium": ["lego set", "hot wheels track", "barbie dreamhouse"]
}

cat_escolhida = st.sidebar.selectbox("Escolha a categoria", list(categorias.keys()))

if st.sidebar.button("🔥 BUSCAR MELHORES DEALS AGORA"):
    with st.spinner("Procurando promoções quentes..."):
        termo = categorias[cat_escolhida][0]
        url = f"https://www.amazon.com/s?k={termo.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            itens = soup.find_all("div", {"data-component-type": "s-search-result"})[:10]
            
            for item in itens:
                titulo = item.h2.text.strip() if item.h2 else "Produto incrível"
                preco = item.find("span", class_="a-price-whole")
                preco = preco.text + item.find("span", class_="a-price-fraction").text if preco else "XX"
                link = "https://amazon.com" + item.find("a", class_="a-link-normal")["href"]
                
                with st.expander(f"💰 {titulo[:70]}..."):
                    st.write(f"**Preço:** ${preco}")
                    st.write(f"[Comprar na Amazon]({link})")
                    
                    estilo = st.radio("Estilo do post", ["Instagram 🔥", "Facebook 📘", "TikTok 🎵"], key=titulo)
                    if estilo == "Instagram 🔥":
                        post = f"🔥 CORRE QUE TÁ BARATO DEMAIS!\n{titulo}\nDe $XXX por só ${preco} 💸\n🚚 Frete grátis Prime\n👉 Link na bio ou comentário!\n#QuickSaveDeals #HomeHacks #BlackFriday"
                    elif estilo == "Facebook 📘":
                        post = f"Olha essa promoção que encontrei:\n{titulo}\nPreço atual: ${preco}\nLink direto aqui → {link}\n#QuickSaveDeals"
                    else:
                        post = f"🚨 DEAL INSANO! {titulo} caindo pra ${preco} 😱\nVeja o vídeo giro no próximo slide 🎥\n#QuickSaveDeals #TikTokDeals"
                    
                    st.text_area("Preview pronto para copiar", post, height=150)
                    if st.button("Salvar este post", key=f"save_{titulo}"):
                        data = datetime.now().strftime("%Y-%m-%d")
                        pasta = f"QuickSaveDeals/{estilo.split()[0]}/{data}"
                        os.makedirs(pasta, exist_ok=True)
                        with open(f"{pasta}/{titulo[:50]}.txt", "w") as f:
                            f.write(post + "\n\nLink: " + link)
                        st.success(f"Post salvo em {pasta}!")
        except:
            st.error("Amazon bloqueou temporariamente. Tente de novo em 1 minutinho!")

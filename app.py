import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import re

st.set_page_config(page_title="Интернет-поисковик", layout="wide")

class InternetResearchAI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_page_content(self, url: str):
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text)
            return text[:2000]
        except:
            return ""
    
    def extract_text_from_image(self, image):
        try:
            width, height = image.size
            return f"Изображение {width}x{height} пикселей. Для текстового анализа требуется установка дополнительных библиотек."
        except:
            return "Ошибка анализа изображения"

def main():
    st.title("🧠 Умный интернет-поисковик")
    st.write("Анализ веб-страниц и изображений")
    
    research_ai = InternetResearchAI()
    
    option = st.radio("Выберите функцию:", 
                     ["📝 Анализ веб-страницы", "📷 Анализ изображений"])
    
    if option == "📝 Анализ веб-страницы":
        st.header("Анализ веб-страницы")
        url = st.text_input("Введите URL страницы:", 
                          placeholder="https://example.com")
        
        if st.button("🔍 Анализировать") and url:
            with st.spinner("Анализируем страницу..."):
                content = research_ai.get_page_content(url)
                
                if content:
                    st.success("Страница проанализирована!")
                    st.write("**Содержание:**", content[:1000] + "...")
                else:
                    st.error("Не удалось получить содержимое страницы")
    
    else:
        st.header("Анализ изображений")
        
        uploaded_file = st.file_uploader("Загрузите изображение", 
                                       type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Загруженное изображение", use_column_width=True)
                
                if st.button("🔍 Анализировать изображение"):
                    with st.spinner("Анализируем изображение..."):
                        image_info = research_ai.extract_text_from_image(image)
                        
                        st.subheader("📊 Информация об изображении:")
                        st.write(image_info)
                        
            except Exception as e:
                st.error(f"Ошибка загрузки изображения: {e}")

if __name__ == "__main__":
    main()
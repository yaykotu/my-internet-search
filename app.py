import streamlit as st
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="Интернет-поисковик", layout="wide")

class InternetResearchAI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_duckduckgo(self, query: str, num_results: int = 5):
        try:
            with DDGS() as ddgs:
                results = []
                for result in ddgs.text(query, max_results=num_results):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'description': result.get('body', '')
                    })
                return results
        except Exception as e:
            return []
    
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
            text = pytesseract.image_to_string(image, lang='rus+eng')
            return text.strip() if text else "Текст не найден"
        except:
            return "Ошибка OCR"

def main():
    st.title("🧠 Умный интернет-поисковик")
    st.write("Ищите информацию в интернете и анализируйте изображения")
    
    research_ai = InternetResearchAI()
    
    option = st.radio("Выберите тип поиска:", 
                     ["📝 Текстовый поиск", "📷 Поиск по изображению"])
    
    if option == "📝 Текстовый поиск":
        text_query = st.text_input("Введите поисковый запрос:", 
                                 placeholder="Например: искусственный интеллект 2024")
        
        if st.button("🔍 Найти") and text_query:
            with st.spinner("Ищем информацию..."):
                results = research_ai.search_duckduckgo(text_query, 5)
                
                if results:
                    st.success(f"Найдено {len(results)} результатов")
                    for i, result in enumerate(results, 1):
                        st.subheader(f"{i}. {result['title']}")
                        st.write(f"**Ссылка:** {result['url']}")
                        st.write(f"**Описание:** {result['description']}")
                        st.write("---")
                else:
                    st.error("Не удалось найти результаты")
    
    else:
        uploaded_file = st.file_uploader("Загрузите изображение", 
                                       type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Загруженное изображение", use_column_width=True)
            
            if st.button("🔍 Анализировать изображение"):
                with st.spinner("Анализируем изображение..."):
                    extracted_text = research_ai.extract_text_from_image(image)
                    
                    if extracted_text and extracted_text not in ["Текст не найден", "Ошибка OCR"]:
                        st.subheader("📝 Извлеченный текст:")
                        st.write(extracted_text)
                    else:
                        st.info("Не удалось извлечь текст из изображения")

if __name__ == "__main__":
    main()
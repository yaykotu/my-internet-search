import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import re

try:
    from duckduckgo_search import DDGS
except ImportError:
    st.error("Библиотека duckduckgo-search не установлена")
    DDGS = None

st.set_page_config(page_title="Интернет-поисковик", layout="wide")

class InternetResearchAI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_duckduckgo(self, query: str, num_results: int = 5):
        if DDGS is None:
            st.error("Библиотека поиска недоступна")
            return []
            
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
            st.error(f"Ошибка поиска: {e}")
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
            # Простой анализ изображения без OCR
            width, height = image.size
            return f"Изображение {width}x{height} пикселей. Для текстового анализа требуется установка дополнительных библиотек."
        except:
            return "Ошибка анализа изображения"

def main():
    st.title("🧠 Умный интернет-поисковик")
    st.write("Ищите информацию в интернете и анализируйте изображения")
    
    if DDGS is None:
        st.warning("Некоторые функции могут быть ограничены из-за отсутствия библиотек поиска")
    
    research_ai = InternetResearchAI()
    
    option = st.radio("Выберите тип поиска:", 
                     ["📝 Текстовый поиск", "📷 Анализ изображений"])
    
    if option == "📝 Текстовый поиск":
        st.header("Текстовый поиск")
        text_query = st.text_input("Введите поисковый запрос:", 
                                 placeholder="Например: искусственный интеллект 2024")
        
        if st.button("🔍 Найти") and text_query:
            with st.spinner("Ищем информацию..."):
                results = research_ai.search_duckduckgo(text_query, 5)
                
                if results:
                    st.success(f"Найдено {len(results)} результатов")
                    for i, result in enumerate(results, 1):
                        with st.expander(f"{i}. {result['title']}"):
                            st.write(f"**Ссылка:** {result['url']}")
                            st.write(f"**Описание:** {result['description']}")
                            
                            content = research_ai.get_page_content(result['url'])
                            if content:
                                st.write("**Содержание:**", content[:500] + "...")
                else:
                    st.error("Не удалось найти результаты или функция поиска недоступна")
    
    else:
        st.header("Анализ изображений")
        st.info("Эта функция показывает базовую информацию об изображении")
        
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
                        
                        st.info("Для извлечения текста с изображения требуется установка дополнительных библиотек на сервере")
                        
            except Exception as e:
                st.error(f"Ошибка загрузки изображения: {e}")

if __name__ == "__main__":
    main()
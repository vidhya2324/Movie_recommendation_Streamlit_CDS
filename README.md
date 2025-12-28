# Movie Recommendation System 🍿

Can’t decide what movie to watch?  
Don’t worry — this app is here to save you from endless scrolling 😄

This is a **Movie Recommendation Web App** built using **Python and Streamlit** that suggests similar movies based on the one you like.

---

## What does this app do?

- Select a movie from the dropdown 🎥
- Click **“Show Recommend”**
- Get **5 similar movies** with posters
- Powered by **NLP + similarity matching**

---

## 🧠 How it works (Simple Explanation)

1. Movie information (genre, overview, keywords) is combined into text
2. **TF-IDF Vectorizer** converts text into numbers
3. **Cosine Similarity** finds how similar movies are
4. Top similar movies are recommended

👉 No deep learning  
👉 No CNN  
👉 Just smart NLP & math 😎

---

## 🛠 Tech Stack

- Python 🐍
- Streamlit 🌐
- Pandas & NumPy
- Scikit-learn
- TMDB API (for posters 🎞)
- Pickle (for saving data)

---

## 🖥 Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/vidhya2324/Movie_recommendation_Streamlit_CDS.git
cd Movie_recommendation_Streamlit_CDS

```
### 2️⃣ Create & activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```


3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```


4️⃣ Run the Streamlit app
```bash
python -m streamlit run app.py
```

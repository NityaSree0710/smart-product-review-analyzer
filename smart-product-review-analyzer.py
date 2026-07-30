import streamlit as st
import pandas as pd
from textblob import TextBlob
from langdetect import detect
from googletrans import Translator
import matplotlib.pyplot as plt


st.set_page_config(page_title=" Product Review Analyzer", layout="centered")
st.title("SMART PRODUCT REVIEW ANALYZER")

translator = Translator()


def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

def get_star_rating(polarity):
    if polarity >= 0.6:
        return 5
    elif polarity >= 0.2:
        return 4
    elif polarity > -0.2:
        return 3
    elif polarity > -0.6:
        return 2
    else:
        return 1

def detect_and_translate(text):
    try:
        lang = detect(text)
        if lang != "en":
            translated = translator.translate(text, dest="en").text
            return lang, translated
        else:
            return "en", text
    except:
        return "unknown", text

def detect_feature(text):
    text = text.lower()
    if "camera" in text:
        return "Camera"
    elif "price" in text or "cost" in text:
        return "Price"
    elif "battery" in text:
        return "Battery"
    elif "design" in text:
        return "Design"
    elif "performance" in text:
        return "Performance"
    else:
        return "General"

def show_stars(rating):
    return "⭐" * int(round(rating))



category = st.selectbox(
    "Select Product Category",
    ["Electronics", "Fashion", "Home Appliances", "Beauty", "Others"]
)

product1 = st.text_input("Enter Product 1 Name")
reviews1 = st.text_area("Enter Reviews for Product 1 (One per line)", height=200)

compare_mode = st.checkbox("Enable Product 2 Comparison")

product2 = ""
reviews2 = ""

if compare_mode:
    product2 = st.text_input("Enter Product 2 Name")
    reviews2 = st.text_area("Enter Reviews for Product 2 (One per line)", height=200)



if st.button("Submit & Analyze"):

    all_data = []

    def process_reviews(product_name, review_text):
        raw_reviews = review_text.split("\n")
        reviews_list = [r.strip() for r in raw_reviews if r.strip() != ""]
        data = []

        for review in reviews_list:
            lang, translated = detect_and_translate(review)
            sentiment, polarity = get_sentiment(translated)
            feature = detect_feature(translated)
            star_rating = get_star_rating(polarity)

            data.append({
                "Category": category,
                "Product": product_name,
                "Original Review": review,
                "Detected Language": lang,
                "Translated Review": translated,
                "Feature": feature,
                "Sentiment": sentiment,
                "Polarity": polarity,
                "Star Rating": star_rating
            })
        return data

    if product1 and reviews1:
        all_data.extend(process_reviews(product1, reviews1))

    if compare_mode and product2 and reviews2:
        all_data.extend(process_reviews(product2, reviews2))

    if len(all_data) == 0:
        st.warning("Please enter product names and reviews.")
    else:
        df = pd.DataFrame(all_data)

        st.success("Analysis Completed Successfully!")
        st.subheader("Review Analysis Result")
        st.dataframe(df, use_container_width=True)

        
        st.subheader("Sentiment Summary")

        summary = df.groupby(["Product", "Sentiment"]).size().unstack(fill_value=0)

        for col in ["Positive", "Negative", "Neutral"]:
            if col not in summary.columns:
                summary[col] = 0

        summary["Total Reviews"] = summary.sum(axis=1)
        summary["Positive %"] = (summary["Positive"] / summary["Total Reviews"]) * 100

        summary["Weighted Score"] = (
            (summary["Positive"] * 1) +
            (summary["Neutral"] * 0.5) -
            (summary["Negative"] * 1)
        ) / summary["Total Reviews"]

        average_rating = df.groupby("Product")["Star Rating"].mean().round(2)
        summary["Average Rating"] = average_rating

        st.dataframe(summary)

        
        st.subheader("Feature-Based Comparison chart")
        for product in average_rating.index:
            st.write(f"**{product}**")
            st.write(f"Average Rating: {average_rating[product]} / 5")
            st.write(show_stars(average_rating[product]))
            st.write("---")

        
        st.subheader("Feature-Based Sentiment Analysis")

        feature_summary = df.groupby(["Product", "Feature", "Sentiment"]).size().unstack(fill_value=0)
        st.dataframe(feature_summary)

       

        st.subheader("Sentiment Comparison Chart")

        summary[["Positive", "Negative", "Neutral"]].plot(kind="bar")
        plt.title("Sentiment Distribution")
        plt.ylabel("Number of Reviews")
        plt.xticks(rotation=0)
        st.pyplot(plt)
        plt.clf()

        st.subheader("Feature-Based Comparion Chart")

        feature_chart = df.groupby(["Product", "Feature"]).size().unstack(fill_value=0)

        feature_chart.plot(kind="bar")
        plt.title("Feature Mention Comparison")
        plt.ylabel("Count")
        plt.xticks(rotation=0)

        st.pyplot(plt)
        plt.clf()
        


        if compare_mode and len(average_rating) == 2:

            products = average_rating.index.tolist()
            p1_rating = average_rating[products[0]]
            p2_rating = average_rating[products[1]]

            st.subheader("Final Comparison Result")

            if p1_rating > p2_rating:
                st.success(f"🏆 {products[0]} is a better choice to buy!")
            elif p2_rating > p1_rating:
                st.success(f"🏆 {products[1]} is a best choice to buy!")
            else:
                st.info("⚖️ Both products are equally good. You can choose either.")

        

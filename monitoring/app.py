import streamlit as st
import requests
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
# testing update from cli 2025-08-16 01.
st.title('FastAPI Monitoring Dashboard')

@st.cache_data
def load_df():
    '''loads the pre-trained model and target names.'''
    training_df = pd.read_csv('IMDB Dataset.csv')
    training_df['source'] = 'IMDB Review'
    training_df['length'] = training_df['review'].str.split().apply(len)
    return training_df

training_df = load_df()
st.header('Click here to refresh results.')
analyze = st.button('Analyze')

if analyze:
    last_refresh = time.strftime('%X, %x, %Z')
    url = 'http://fastapi-container:80/predictions'
    response = requests.get(url)
    response = response.text
    try:
        results_df = pd.read_json(response, lines=True)
        st.text(f'Successfully loaded new data at {last_refresh}')

        results_df['length'] = results_df['request_text'].str.split().apply(len)
        results_df['source'] = 'Request Text'
        combined_df = pd.concat([results_df[['length', 'source']], training_df[['length', 'source']]])

        # Plot to compare new review text lengths to training set.
        fig, ax = plt.subplots()
        sns.kdeplot(data=combined_df, x='length', hue='source', fill=True, common_norm=False, alpha=0.5, ax=ax)
        ax.set_title('Sentence Length Distribution')
        ax.set_xlabel('Number of Words')
        ax.set_ylabel('Density')

        st.pyplot(fig)

        # Plot for target drift analysis
        training_df['sentiment'] = training_df['sentiment'].str.lower()
        results_df['predicted_sentiment'] = results_df['predicted_sentiment'].str.lower()
        train_counts = training_df['sentiment'].value_counts(normalize=True).rename_axis('sentiment').reset_index(name='count')
        train_counts['source'] = 'Training'
        pred_counts = results_df['predicted_sentiment'].value_counts(normalize=True).rename_axis('sentiment').reset_index(name='count')
        pred_counts['source'] = 'Predictions'
        combined_counts = pd.concat([train_counts, pred_counts])
        fig, ax = plt.subplots()
        sns.barplot(data=combined_counts, x='sentiment', y='count', hue='source', ax=ax)
        ax.set_title('Sentiment Distribution: Training vs Predictions')
        ax.set_ylabel('Distribution')
        ax.set_xlabel('Sentiment')

        st.pyplot(fig)

        results_df = results_df.dropna(subset='true_sentiment')
        if results_df.shape[0] >=1:
            results_df['true_sentiment'] = results_df['true_sentiment'].str.lower()
            results_df['predicted_sentiment'] = results_df['predicted_sentiment'].str.lower()

            # Compute metrics
            y_true = results_df['true_sentiment']
            y_pred = results_df['predicted_sentiment']

            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, pos_label='positive', zero_division=0)
            if acc < .8:
                st.error('Warning: model accuracy below 80%')
            st.markdown(f"**Accuracy:** {acc:.2f}")
            st.markdown(f"**Precision (positive class):** {prec:.2f}")

            # Confusion matrix
            cm = confusion_matrix(y_true, y_pred, labels=['positive', 'negative'])

            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                        xticklabels=['Predicted Positive', 'Predicted Negative'],
                        yticklabels=['True Positive', 'True Negative'],
                        ax=ax)
            ax.set_title('Confusion Matrix')
            st.pyplot(fig)

    except:
        st.text('At least one review needs to be entered to retrieve results.')
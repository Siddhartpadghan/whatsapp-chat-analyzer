import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8", errors="ignore")

    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # === Stats ===
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media", num_media_messages)
        col4.metric("Links", num_links)

        # === Monthly Timeline ===
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # === Daily Timeline ===
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # === Activity Map ===
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # === Heatmap ===
        st.title("Weekly Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        if user_heatmap.empty:
            st.write("No data available for heatmap")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)

        # === WordCloud ===
        st.title("WordCloud")
        wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # === Most Common Words ===
        st.title("Most Common Words")
        common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(common_df[0], common_df[1])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # === Emoji Analysis ===
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        if emoji_df.empty:
            st.write("No emojis found")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)

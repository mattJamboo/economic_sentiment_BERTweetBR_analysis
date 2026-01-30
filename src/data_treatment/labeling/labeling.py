import pandas as pd
import os 

def manual_labeling(df, tweet_col='tweet', label_col='sentiment_label',
                     save_path="tweets_rotulados.parquet", save_every=50, ov=False):
    """
    Manual labeling function with option to overwrite or resume.

    Args:
        df (pd.DataFrame): DataFrame containing tweets and labels.
        tweet_col (str): Column name for tweets.
        label_col (str): Column name for sentiment labels.
        save_path (str): Path to save progress CSV.
        save_every (int): Save the DataFrame every N newly labeled tweets.
        ov (bool): If True, overwrite the sentiment_label column.
                   If False, skip already labeled tweets and resume from saved progress.

    Labeling scheme:
        1 = positivo
        0 = neutro
        -1 = negativo
        N/n = stop labeling early
    """

    # Initialize or load labels
    if ov:
        # Overwrite: start fresh
        df[label_col] = pd.NA
    else:
        # Resume mode
        if os.path.exists(save_path):
            print(f"Loading existing progress from {save_path}...")
            saved_df = pd.read_parquet(save_path)
            if label_col in saved_df.columns:
                df[label_col] = saved_df[label_col]
            else:
                df[label_col] = pd.NA
        else:
            if label_col not in df.columns:
                df[label_col] = pd.NA

    total = len(df)
    labeled_count = 0

    for idx, row in df.iterrows():
        # Skip already labeled tweets if ov=False
        if not ov and pd.notna(row[label_col]):
            continue

        tweet = row[tweet_col]
        print(f"\nTweet {idx+1}/{total}:\n{tweet}\n")

        while True:
            label = input("Label this tweet (1=positivo, 0=neutro, -1=negativo, N=stop): ").strip()

            if label.lower() == 'n':
                print("Stopping labeling early. Saving current progress...")
                df.to_parquet(save_path)
                return df

            if label in {'0', '1', '-1'}:
                df.at[idx, label_col] = int(label)
                labeled_count += 1
                break
            else:
                print("Invalid input! Please enter 1, 0, -1, or N to stop.")

        # Save progress every `save_every` newly labeled tweets
        if labeled_count % save_every == 0:
            print(f"Saving progress after labeling {labeled_count} new tweets...")
            df.to_parquet(save_path)

    # Save final progress
    print("Labeling complete. Saving final CSV...")
    df.to_parquet(save_path)
    return df


df = pd.read_parquet(r"C:\\Users\\Mateus Monteleone\\Projects\\ic\\data\\df_rotulação_manual.parquet")

save_path = r"C:\\Users\\Mateus Monteleone\\Projects\\ic\\data\\tweets_rotulados.parquet"

# da = pd.read_parquet(r"C:\\Users\\Mateus Monteleone\\Projects\\ic\\data\\tweets_rotulados.parquet")

# da.at[276, 'sentiment_manual'] = -1

# da.to_parquet(r"C:\\Users\\Mateus Monteleone\\Projects\\ic\\data\\tweets_rotulados.parquet")

# print(da.at[276, 'clean_text'])

df_labeled = manual_labeling(df=df, tweet_col="clean_text", label_col="sentiment_manual", ov=False, save_every=5, save_path=save_path,)

print(df_labeled.head())











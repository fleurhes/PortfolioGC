import asyncio
import random
import csv
from twikit import Client

async def main():
    query = '''(monkeypox OR mpox) lang:en until:2024-11-7 since:2024-11-5 -filter:replies'''
    max_tweets = 500 

    client = Client(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
    )
    client.load_cookies('cookies.json')

    with open('tweets_mpox_preelection.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'text', 'user', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        tweets = await client.search_tweet(query, 'Top')
        total_tweets_collected = 0

        while total_tweets_collected < max_tweets:
            for tweet in tweets:
                writer.writerow({
                    'id': tweet.id,
                    'text': tweet.text,
                    'user': tweet.user.screen_name,
                    'created_at': tweet.created_at
                })
                print(tweet.id, tweet.text, tweet.user.screen_name, tweet.created_at)

                total_tweets_collected += 1
                if total_tweets_collected >= max_tweets:
                    print(f"collected {total_tweets_collected} tweets. done")
                    return  
                await asyncio.sleep(random.randint(8, 15))

            await asyncio.sleep(random.randint(10, 20))
            tweets = await tweets.next()

asyncio.run(main())

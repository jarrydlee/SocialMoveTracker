from django.shortcuts import render
from system.models import *
from django.db import IntegrityError
import requests, urllib, time

# Create your views here.


def home(request):
    posts = Post.objects.all()
    print(len(posts))
    keywords = Keyword.objects.all()

    return render(request, 'test.html', {
        'posts':posts,
        'keywords':keywords
    })


def search(request):
    baseUrl = 'https://search-proxy.massrelevance.com/search.json'

    movies = [
        'Ride%20Along',
        'Endless%20Love',
        'Non-Stop',
        'Neighbors',
        'A%20Million%20Ways%20to%20die%20in%20the%20west',
        'Mrs%20Brown\'s%20Boys',
        'The%20Purge',
        'Get%20on%20up',
        'Lucy',
        'As%20above%20so%20below',
        'the%20loft',
        'search%20party',
        'Ouija'
    ]

    def scrape(title):
        #define variables
        pagination = ''

        # Creating keywords
        keyword = Keyword(
            word = urllib.unquote_plus(title)
        )
        try:
            keyword.save()
        except IntegrityError as e:
            print('duplicate keyword')

        for x in range(0,2):
            # Creating post object
            url = 'https://search-proxy.massrelevance.com/search.json?filter.text="'+ title +'"%20movie&filter.start=-24h&filter.finish=0&view.entities=true&view.entities.limit=100&'+ pagination
            print(url)
            r = requests.get(url)
            rJson = r.json()

            for tweet in rJson['views']['entities']['data']:

                created = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['raw']['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))


                post = Post(
                    post_id = tweet['raw']['id'],
                    text = tweet['raw']['text'],
                    label = '',
                    keyword = keyword,
                    positive = 0,
                    negative = 0,
                    neutral = 0,
                    created_at = created,
                )
                try:
                    post.save()
                except IntegrityError as e:
                    #print('duplicate post')
                    pass

            pagination_text = urllib.quote_plus(rJson['views']['entities']['meta']['pagination']['next_cursor'])

            pagination = 'view.entities.cursor='+ pagination_text

    for title in movies:

        scrape(title)

    return render(request, 'index.html')





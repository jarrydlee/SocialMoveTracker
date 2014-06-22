from datetime import *
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from system import AppProperties
from system.AppProperties import MovieProperties
from system.models import *
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string
import requests, urllib, time
import json

# Create your views here.

def home(request):

    return render(request, 'index.html')

def test(request):
    posts = Post.objects.all()
    print(len(posts))
    keywords = Keyword.objects.all()

    checkTrending(800, 0, "Fast and Furious")

    return render(request, 'index.html', {
        'posts':posts,
        'keywords':keywords
    })


def search(request):
    baseUrl = 'https://search-proxy.massrelevance.com/search.json'


    def scrape(title):
        #define variables
        pagination = ''
        #
        # # Creating keywords
        # keyword = Keyword(
        #     word = title
        # )
        # try:
        #     keyword.save()
        # except IntegrityError as e:
        #     print('duplicate keyword')

        for x in range(0,2):
            # Creating post object
            url = 'https://search-proxy.massrelevance.com/search.json?filter.text="'+ urllib.quote(title).replace("%27", "'") +'"%20movie&filter.start=-2h&filter.finish=0&view.entities=true&view.entities.limit=100&'+ pagination
            r = requests.get(url)
            rJson = r.json()

            for tweet in rJson['views']['entities']['data']:
                print(tweet['raw']['text'])

                # Disgusting way to not call processText on duplicates
                if Post.objects.filter(text=tweet['raw']['text']).first() != None:
                    #print('Already in database')
                    continue

                created = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['raw']['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

                semantics = processText(tweet['raw']['text'])
                sentiment = 0 if semantics['sentiment'] == 'Negative' else 1 if semantics['sentiment'] == 'Neutral' else 2

                post = Post(
                    post_id = tweet['raw']['id'],
                    text = tweet['raw']['text'],
                    keyword = Keyword.objects.get(word=title),
                    semantic = sentiment,
                    confidence = semantics['confidence'],
                    created_at = created,
                )
                try:
                    #print("Success:")
                    post.save()
                except IntegrityError as e:
                    #print('duplicate post')
                    pass

            paginationText = urllib.quote_plus(rJson['views']['entities']['meta']['pagination']['next_cursor'])

            pagination = 'view.entities.cursor='+ paginationText

    def processText(text):
        data = {'txt':text}
        result = requests.post('http://sentiment.vivekn.com/api/text/', data=data)
        result = json.loads(result.content)
        return result['result']

    def getLatestPost(title):
        newest = Post.objects.filter(keyword__word=title).first()
        print(newest.created_at)
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S %z", time.gmtime())
        print(timeNow)
        delta = timeNow - newest.created_at
        print(delta)


    for title in MovieProperties().getMovieList():
        scrape(title)

    return render(request, 'index.html')

def getLineChartData(request):
    movie = request.GET.get('movie', 'ALL')
    movieList = [movie]

    def LineDataFunc(movieList, timeDelta):
        return Post.objects.filter(
            keyword__word__in=movieList
        ).filter(
            created_at__gt=(datetime.now() - timeDelta)
        ).filter(
            created_at__lt=(datetime.now() - timeDelta + timedelta(minutes=60))
        ).count()

    if movie == "ALL":
        movieList = MovieProperties().getMovieList()

    res = dict()
    for x in range(1, 7):
        res['' + str(x)] = LineDataFunc(movieList, timedelta(minutes=(60*x)))

    return HttpResponse(json.dumps(res))

def checkTrending(now, last, movie):
    if (now - last) > 300:
        message = "Hello, " + movie + " is now trending! It has been mentioned " + str(now) + " in the past hour."
        subject = "" + movie + " is trending"

        send_mail(subject, message, '',
        ['richardfyadon@gmail.com'])


def getSidebar(request):
    # Will return a dictionary with an entry for each movie, key is whether the number
    # of posts has increased or decreased
    movieList = MovieProperties().getMovieList()

    def ArrowFunc(movieTitle):
        numLast = Post.objects.filter(
            keyword__word = movieTitle
        ).filter(
            created_at__gt = (datetime.now() - timedelta(minutes=120))
        ).filter(
            created_at__lt = (datetime.now() - timedelta(minutes=60))
        ).count()

        numNow = Post.objects.filter(
            keyword__word = movieTitle
        ).filter(
            created_at__gt = (datetime.now() - timedelta(minutes=60))
        ).filter(
            created_at__lt = datetime.now()
        ).count()

        checkTrending(numNow, numLast, movieTitle)

        if numLast < numNow:
            return 1
        elif numNow < numLast:
            return -1
        else:
            return 0

    res = {movie: ArrowFunc(movie) for movie in movieList}

    return HttpResponse(json.dumps(res))

def getPosts(request):
    movie = request.GET.get('movie', '')
    if movie != '':
        movie = urllib.unquote(movie)
        moviePosts = [post.as_json() for post in Post.objects.order_by('-created_at').filter(keyword__word=movie)]
    else:
        moviePosts = [post.as_json() for post in Post.objects.order_by('-created_at')]

    return HttpResponse(json.dumps(moviePosts))

def getDoughnutData(request):
    res = dict()
    posts = Post.objects.all().values('keyword').annotate(total=Count('keyword')).order_by('-total')[:5]
    for post in posts:
        keyword = Keyword.objects.all().filter(id=post['keyword'])
        res[keyword[0].word] = post['total']

    return HttpResponse(json.dumps(res))

def getBarData(request):
    movie = request.GET.get('movie', 'ALL')
    movieList = [movie]

    def BarDataFunc(movieList, flag):
        sem = 2
        if flag == 'negative':
            sem = 0
        elif flag == 'neutral':
            sem = 1

        return Post.objects.filter(
            keyword__word__in=movieList
        ).filter(
            semantic=sem
        ).count()

    if movie == "ALL":
        movieList = MovieProperties().getMovieList()

    res = dict()
    res['positive'] = BarDataFunc(movieList, 'positive')
    res['negative'] = BarDataFunc(movieList, 'negative')
    res['neutral'] = BarDataFunc(movieList, 'neutral')

    return HttpResponse(json.dumps(res))
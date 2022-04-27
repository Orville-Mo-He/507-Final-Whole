import requests, re
from utils import *
from bs4 import BeautifulSoup
from collections import Counter


# NOTE ———————————————————————
# This script basically builds a website that hosts Modern Love Stories

# This script will request Modern Love Stores from the NYT API.
# Then it uses that information to access the actual page that houses each
# of the stories and scrapes them. It then also uses the stories' pub dates to
# search the NYT API for the front page headlines, accesses their pages,
# and scrapes their content.
#
# Then it uses regex to parse through the articles of each headline (of each
# story), cleans it, and creates a set of words to compare with the other
# articles of that story, the no. of shared words between articles becomes the
# "weight" of the edges between headlines.
#
# At the same time, it also parses the original stories' text and manipulates it
# to form it into a pseudo concrete poems (by inserting spaces and line breaks)

# Most of the above functions and classes are found in utils.



# Finally this script takes all this data and makes a page for each story, where
# I use JS and the P5.JS library to visualize each story's list of headlines as
# an amorphous graph, where each node moves acording to a perlin noise function,
# and where the weights of edges are visualized in the thickness of the line's
# stroke weight.

# Also, aparently loading/reading a local json *file* is virtually impossible
# to do, at least with my rudimentary knowledge of JS and nonexistent knowledge
# of JQUERY, so I just hard baked the data into the script, which meant baking
# the script into the html file.


# ————————————————————————————

HTML_BASE = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://use.typekit.net/cjy3rtu.css">
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>Concrete Poetry of Modern Love: {title}</title>
    <script src="https://cdn.jsdelivr.net/npm/p5@1.4.1/lib/p5.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk="crossorigin="anonymous"></script>
    <script defer src="https://unpkg.com/p5.collide2d"></script>
    <script>
        let data_0 = '{data}'
        let min_max = JSON.parse('{data2}')
        {script_string}
    </script>
</head>

<body>
    <main>
        <div id='left_side'>
            <h1>Concrete Poetry<br>&emsp;&emsp;&emsp;of Modern Love</h1>
            <a id="back" href="index.html">&#8592; back</a>
            <br><br>
            <h2>{title}</h2>
            <br><br>
            <div id='txt'><p>{txt}</p></div>
        </div>
    </main>
</body>
'''

script_string= r'''
        let min = min_max['min']
        let max = min_max['max']

        // some tests
        // console.log(min)

        let data = JSON.parse(data_0)
        let headlines_ie_keys = Object.keys(data);

        // console.log('Data.type')
        // console.log(typeof(data));
        // // object

        // console.log('\nData[0]')
        // console.log(data["Drawn and Caricatured: French Cartoonists on the Campaign Trail"]);
        // // the whole dictionary

        // console.log('\nData[0][0].type')
        // console.log(typeof(data["Drawn and Caricatured: French Cartoonists on the Campaign Trail"]["Star Ferry, ‘Emblem of Hong Kong,’ May Sail Into History After 142 Years"]));
        // // number

        // console.log('\nData[0][0]')
        // console.log(data["Drawn and Caricatured: French Cartoonists on the Campaign Trail"]["Star Ferry, ‘Emblem of Hong Kong,’ May Sail Into History After 142 Years"]);
        // // 96

        // console.log('\nKeys: type, key[1], and headlines_ie_keys.length')
        // console.log(typeof(headlines_ie_keys));
        // // object
        // console.log(headlines_ie_keys[1]);
        // // Star Ferry, ‘Emblem of Hong Kong,’ May Sail Into History After 142 Years

        // console.log(headlines_ie_keys.length);
        // // 10




        // P5 Section





        let x_feeds = []
        let y_feeds = []
        let x_offsets = []
        let y_offsets = []
        let headlines_to_show = []
        let starting_pt, h;
        let whole_h
        let stroke_weight
        let weights_keys


        function setup() {
            starting_pt = 400;
            h = windowHeight;
            whole_h = document.body.scrollHeight;

            // canvas = createCanvas(document.body.clientWidth+(16), document.body.scrollHeight);
            if(h > whole_h){
                canvas = createCanvas(windowWidth, 1.1*h);
            } else if(h < whole_h){
                canvas = createCanvas(windowWidth, 1.1*whole_h);
            };


            canvas.position(0, 0);
            canvas.style('z-index', '-1');
            // console.log(data.headline);
            // console.log('hi')

            textFont('prestige-elite-std')

            for(i=0; i < headlines_ie_keys.length; i++){

                x_offsets[i] = random(0, 0.001);
                y_offsets[i] = random(0, 0.001);

                x_feeds[i] = random(0, 100);
                y_feeds[i] = random(0, 500);

                headlines_to_show[i] = new Headline(String(headlines_ie_keys[i]), x_offsets[i], y_offsets[i], x_feeds[i], y_feeds[i]);

            };
        };

        function windowResized() {

            starting_pt = 300;
            h = windowHeight;
            whole_h = document.body.scrollHeight

            if(h > whole_h){
                resizeCanvas(windowWidth, 1.1*h);
            } else if(h < whole_h){
                resizeCanvas(windowWidth, 1.1*whole_h);
            };    // canvas.style('width', windowWidth);
            // canvas.style('height', document.body.scrollHeight);

        };


        class Headline{

            constructor(_string, _x_offset, _y_offset, _x_feed, _y_feed){
                this._string = _string;
                this.x_offset = _x_offset;
                this.y_offset = _y_offset;
                this.x_feed = _x_feed;
                this.y_feed = _y_feed;
                this.x;
                this.y;
            };

            show(){
                this.place_and_move()
                text(this._string, this.x, this.y, 200, 500);
            };
            place_and_move(){
                this.x = map(noise(this.x_feed), 0, 1, starting_pt, windowWidth);
                this.y = map(noise(this.y_feed), 0, 1, 0, windowHeight);
                this.x_feed += this.x_offset;
                this.y_feed += this.y_offset;
            };
        }

        function draw(){

            background(0);

            rect(0, 0, 500, canvas.height)

            noStroke();

            push()
            textSize(30)
            fill(150, 42, 46)
            text('Headlines of the Day', windowWidth/2, 100)
            for(i=0; i<headlines_ie_keys.length; i++){

                textStyle(BOLD);
                textSize(16)
                headlines_to_show[i].show();

            };
            pop()

            push()
            strokeCap(SQUARE);
            stroke(150, 42, 46, 30);
            fill(150, 42, 46, 30);

            for(i=0; i<headlines_ie_keys.length; i++){

                weights_keys = Object.keys(data[String(headlines_ie_keys[i])])

                for(u=0; u<weights_keys.length; u++){
                    push()
                    stroke_weight = map(data[headlines_ie_keys[i]][weights_keys[u]], min, max, 1, 10)
                    strokeWeight(stroke_weight)
                    line(headlines_to_show[i].x-20, headlines_to_show[i].y, headlines_to_show[u].x-20, headlines_to_show[u].y)
                    pop()
                }
                circle(headlines_to_show[i].x-20, headlines_to_show[i].y, 20)
            };
            pop()
            // separated because if together, there would be no x or y for
            // headlines_to_show[u]

        };


'''

if __name__ == '__main__':

    # —————————————————————————
    # Get everything set up
    nyapi_key = 'QX9HedGAC2o9liyhXAC8KAe6aBWfKAqM'

    # get the first twenty entries of Modern Love.
    ls_requests_1 = get_json_resource(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=headline%3Atiny%20AND%20-headline%3APodcast&q=modern%20love&api-key={nyapi_key}")['response']['docs']
    ls_requests_2 = get_json_resource(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=headline%3Atiny%20AND%20-headline%3APodcast&q=modern%20love&page=2&api-key={nyapi_key}")['response']['docs']

    ls_requests = ls_requests_1 + ls_requests_2
    # write_json('Final/website/data/ls_requests_1.json', ls_requests_1)
    # write_json('Final/website/data/ls_requests_2.json', ls_requests_2)
    write_json('Final/website/data/ls_requests.json', ls_requests)


    # front page requests, that is, news headline requests,
    # which will be formated the specific story's pub date
    fp_requests = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={x}&end_date={x}&fq=type_of_material%3A(%22news%22)%20AND%20section_name%3A(%22World%22)%20AND%20source%3A(%22The%20New%20York%20Times%22)&api-key=QX9HedGAC2o9liyhXAC8KAe6aBWfKAqM'
    # print(fp_requests.format(x = 5))




    to_remove = []
    pub_d_pattern = r"T.*|-" # format such that it can be used in input for headline search
    nope = ["Contests and Prizes", "Awards, Decorations and Honors"]

    for article in ls_requests:
        article['pub_date'] = re.sub(pub_d_pattern, '', article['pub_date'])
        if "Tiny Love Stories" not in article['headline']['main']:
            to_remove.append(article)

        for keyword in article['keywords']:
            for phrase in nope:
                if phrase in keyword['value']:
                    to_remove.append(article)
                    break
    # tiny love returns
    tl_returns = [article for article in ls_requests if article not in to_remove]
    write_json('Final/website/data/tl_returns.json', tl_returns)



    print()

    no = 0
    love_story_instances = []
    all_news = {}

    # for article in tl_returns[:1]: # NOTE set to one so that for easy trail/error

    # this section gets all the headlines for each article in TL Requests.
    for article in tl_returns[:10]:

        """
        NOTE
        NYT limits you to 4,000 requests per day and 10 requests per minute
        so you need to wait 6 secs between calls...
        get all the headlines of that day
        """

        # time.sleep(6)
        # NOTE uncomment ^ for final
        resource_result = get_json_resource(fp_requests.format(x = article['pub_date']))
        # print(resource_result.keys())
        # this is to check if the api properly returned the headlines.
        if 'fault' in resource_result.keys():
            news_list = []
            break

        # make the headline not wonk
        pattern = r"Tiny Love Stories: ‘|’$"
        article['headline'] = re.sub(pattern, '', article['headline']['main'])

        
        # when instantiating a News_Article, it will automatically get the
        # text (scrape site and the whole shubang), create the compare list,
        # and create a json dict of itself

        news_list = [News_Article(headline=result['headline']['main'], web_url=result['web_url'])
            for result in resource_result['response']['docs']
        ]
        all_news[article['headline']] = [news_article.jsoned for news_article in news_list]


        # when instantiating a Love_story, it will automatically grab the story
        # (scrape site and the whole shubang), and, since the news is populated
        # it will also create the edge weights between each node (article) in 
        # the graph.

        love_story_instances.append(
            Love_story(
                headline= article['headline'],
                abstract= article['abstract'],
                url= article['web_url'],
                keywords= article['keywords'],
                pub_date= article["pub_date"],
                news = news_list
            )
        )


    love_stories = [story.jsoned for story in love_story_instances]


    # print(love_story_instances[0].headline)
    # print(love_story_instances[0].text)
    # print(vars(love_story_instances[0]).keys())
    # print(love_story_instances[0].jsonable().keys())
    # for shocker in love_story_instances[0].news:
    #     print(shocker.compare_set)
    #     print()




    for story in love_story_instances:
        story.stir_html_concrete()
        # ^ this manipulates the raw text of the story into a concrete poem.

        story.jsonable()
        # recreate each story's jsoned attribute (in order to include the .concrete attribute)
        with open(f"Final/website/love_story_{love_story_instances.index(story)}.html", 'w', encoding="utf-8") as file_obj:
            file_obj.write(HTML_BASE.format(title = story.headline, txt = story.concrete, data = json.dumps(story.jsoned['weights']), data2 = json.dumps(story.jsoned['min_n_max']), script_string=script_string))
        print(f'<li><a href="love_story_{love_story_instances.index(story)}.html">{story.headline}</a></li>')
        # print(story.jsoned['weights'])


    write_json('Final/website/data/all_news.json', all_news)
    write_json('Final/website/data/love_stories.json', love_stories)


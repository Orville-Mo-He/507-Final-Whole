import requests, re, json, random, copy
from bs4 import BeautifulSoup



def read_json(filepath=None, obj=None, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """
    if filepath:
        with open(filepath, 'r', encoding=encoding) as file_obj:
            return json.load(file_obj)
    if obj:
        return json.loads(obj)

def get_json_resource(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more SWAPI entities to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the SWAPI entity.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path    to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def simple_noise(base, deviation=1):
    val = round(random.gauss(base, deviation))
    while val <= 0 or val == None:
        val = simple_noise(base, deviation)
    return val
    # inspired by:
    # https://pypi.org/project/perlin-noise/

def get_NYT(_url):
    # NOTE For grader:
    # This script relies on having an NYT account (if umich, then you can make
    # one for free), and being able to log in through that.
    # I am not going to provide my login or cookies because, well... duh
    # SO! To test whether or not this code actually scrapes properly,
    # you need to do the following:

    # To get the cookies and headers, you need to go nytimes.com, log in, then
    # inpsect element, and go to network. Refresh the page (with inspect still
    # open) and find the network entry "nytimes.com".
    # Right click on that and copy it as a cURL.
    # then go to https://curlconverter.com/ and convert the cURL into python
    # then copy and paste the converted "cookies" and "headers" here.

    # you should have the following keys.

    cookies = {
        'nyt-a':'',
        'g_state': '',
        'nyt-jkidd': '',
        'SIDNY': '',
        'datadome': '',
        'nyt-gdpr': '',
        'NYT-S': '',
        'nyt-b3-traceid': '',
        'nyt-purr': '',
        'nyt-m': '',
    }

    headers = {
        'authority': '',
        'accept': '',
        'accept-language': '',
        # Requests sorts cookies= alphabetically
        # 'cookie':
        'dnt': '',
        'sec-ch-ua': '" "',
        'sec-ch-ua-mobile': '',
        'sec-ch-ua-platform': '""',
        'sec-fetch-dest': '',
        'sec-fetch-mode': '',
        'sec-fetch-site': '',
        'sec-fetch-user': '',
        'upgrade-insecure-requests': '',
        'user-agent': '',
    }
    return requests.get(_url, headers=headers, cookies=cookies).text

class Love_story:
    def __init__(self, headline=None, abstract=None, url=None, keywords=None, pub_date=None, news=None) -> None:
        self.headline = headline
        self.abstract = abstract
        self.web_url = url
        self.keywords = keywords
        self.pub_date = pub_date
        self.text = self.get_story()
        self.news = news
        self.concrete = None
        self.weights = self.make_weights()
        self.min_n_max = self.min_max()
        self.jsoned = self.jsonable()

        # if self.news:
        #     self.get_news()

    # def get_news(self):
    #     placeholder = []
    #     for entry in self.news:
    #         placeholder.append(

    #         )

    def get_story(self):
        '''
        Get the associated text of the tiny story associated with the title
        '''
        site = get_NYT(self.web_url)
        soup = BeautifulSoup(site, 'html.parser')
        p_tags = soup.find_all('p')
        for p in p_tags:
            if self.headline.lower() in p.text.lower():
                return p.text


    def stir_html_concrete(self):
        string_a = copy.deepcopy(self.text)
        string_a = string_a.split(' ')
        string_b = ''

        for word in string_a:
            to_ret_or_not_to_ret = ['<br>', '', '', '', '', '', '', '', '']
            space = random.choice(to_ret_or_not_to_ret) + '&emsp;'*simple_noise(random.randint(1, 3))
            string_b = string_b + space + word

        self.concrete = string_b
        return string_b


    def jsonable(self):
        ret = {}
        for key, val in self.__dict__.items():
            # if key == 'news':
            #     ret[key] = [article.jsonable() for article in val]
            if key == 'jsoned' or key == 'news':
                pass
            # elif key == 'weights':
            #     ret[key] = f"{(json.dumps(val))}"
            else:
                ret[key] = val
        self.jsoned = ret
        return str(ret)

    # might need a min max for this later in P5
    def make_weights(self):
        weights = {}
        # "graph" of news articles, whereby each article is a node
        # and their edges are weighted by their shared word-space
        if self.news:
            for news_article in self.news:
                weights[news_article.headline] = {}

                for other_article in self.news:
                    if other_article.headline != news_article.headline:
                        weights[news_article.headline][other_article.headline] = len(news_article.compare_set.intersection(other_article.compare_set))
        return weights


    # get min-max values for perlin noise range in P5
    def min_max(self):
        max = 0
        min = 1000
        for entry in self.weights.values():
            for vval in entry.values():
                if vval > max:
                    max = vval
                    continue
                if vval < min:
                    min = vval
        return {
            'max':max,
            'min':min
        }



class News_Article:
    def __init__(self, headline=None, web_url=None) -> None:
        self.headline = headline
        self.web_url = web_url
        self.text = self.get_story()
        self.compare_set = self.to_compare()
        self.jsoned = self.jsonable()

    def get_story(self):
        '''
        Get the associated text of the tiny story associated with the title
        '''
        site = get_NYT(self.web_url)
        soup = BeautifulSoup(site, 'html.parser')

        # join the text in all the p tags (that are the actual story)
        # strip() it. (phrasing...)
        return ('\n'.join([p.text for p in soup.select('p.css-g5piaz.evys1bk0')])).strip()

    def jsonable(self):
        ret = {}
        for key, val in self.__dict__.items():
            if key == 'compare_set':
                ret[key] = list(val)
            elif key == 'jsoned':
                pass
            else:
                ret[key] = val
        return ret

    def to_compare(self):
        to_delete = r"\bdid\b|\bve\b|\bour\b|\btheir\b|\bhis\b|\bhers?\b|\bhim\b|\b\d\b|\bwhich\b|\band\b|\bwe\b|\bwas\b|\bare\b|\bcan\b|\bhad\b|\bus\b|\bthem\b|\bthey\b|\bshe\b|\bhe\b|\bit\b|\baround\b|\bas\b|\bat\b|\bbefore\b|\bbehind\b|\bbelow\b|\bbeneath\b|\bbeside\b|\bbesides\b|\bbetween\b|\bbeyond\b|\bbut\b|\bby\b|\bconcerning\b|\bconsidering\b|\bdespite\b|\bdown\b|\bduring\b|\bexcept\b|\bexcepting\b|\bexcluding\b|\bfollowing\b|\bfor\b|\bfrom\b|\bin\b|\binside\b|\binto\b|\blike\b|\bminus\b|\bnear\b|\bof\b|\boff\b|\bon\b|\bonto\b|\bopposite\b|\boutside\b|\bover\b|\bpast\b|\bper\b|\bplus\b|\bregarding\b|\bround\b|\bsave\b|\bsince\b|\bthan\b|\bthrough\b|\bto\b|\btoward\b|\btowards\b|\bunder\b|\bunderneath\b|\bunlike\b|\buntil\b|\bup\b|\bupon\b|\bversus\b|\bvia\b|\bwith\b|\bwithin\b|\bwithout\b|\ba\b|\ban\b|\bthe\b|\bof\b|\blike\b|\bthat\b"

        # delete all the filler words, break the whole text into a list of words
        # strip all the extra stuff (redundant considering split pat, but still)
        # and convert the list to a set (which gets rid of redundancies and
        # allows for .intersection() later on)
        # result will always contain a '', so get rid of that
        sett = set(re.split('\W+', (re.sub(to_delete, '', self.text.lower())).strip()))
        if '' in sett: sett.remove('')
        return sett


def main():
    # site = get_NYT('https://www.nytimes.com/2022/04/05/style/tiny-modern-love-stories-i-quietly-foolishly-eloped.html?action=click&module=RelatedLinks&pgtype=Article')
    # soup = BeautifulSoup(site, 'html.parser')
    # p_tags = soup.findAll('p')
    # print(p_tags[0].text)

    site = get_NYT('https://www.nytimes.com/2022/04/05/world/europe/zelensky-un-security-council.html')
    soup = BeautifulSoup(site, 'html.parser')
    p = '\n'.join([p.text for p in soup.select('p.evys1bk0')])
    print(p)

    pass




if __name__ == '__main__':
    main()



'''
        // for (var i = 0; i < keys.length; i++)\{
        //     document.getElementbyid
        //     for (var x = 0; x < data[keys[i]].length; x++){
        //     data[keys[i]]}
        //
        // }
'''

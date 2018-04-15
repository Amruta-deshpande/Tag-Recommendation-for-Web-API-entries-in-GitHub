from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import re

def get_data():
    '''
    Fetch the data from the site

    '''
    myurl = 'https://github.com/search?p=4&q=Facebook+live+API&type=Repositories&utf8=%E2%9C%93'
    uClient = uReq(myurl)
    main_page = uClient.read()
    uClient.close()

    page_soup = soup(main_page, "html.parser")
    # title_list = page_soup.findAll("ul", {"class": "repo-list"})

    repository_links=[]
    repository_list1=page_soup.findAll("a",{"class":"v-align-middle"})
    for title in repository_list1:
        repository_links.append(title.get_text())

    # print(title_links1)
    get_readme(repository_links)


def get_readme(repository_links):
    '''
    Read the readme file through beautiful soup
    '''
    baseurl = 'https://github.com/'
    for link in repository_links:
        myurl = baseurl + link
        uClient1 = uReq(myurl)
        main_page = uClient1.read()
        uClient1.close()

        page_soup = soup(main_page, "html.parser")

        #title= page_soup.findAll("span",{"class":"col-11 text-gray-dark mr-2"})
        title = page_soup.findAll("article", {"class": "markdown-body entry-content"})
        #print(title)
        if not title:
            continue
        else:
            title_list = []
            if(title[0].h1==None):
                #print(link)
                str=(re.findall(r'/(\w+)',link))
                title_list.append(str[0])
            else:
                title_list.append(title[0].h1.get_text())
            print('Title :',title_list)


        topics=page_soup.findAll("a",{"class":"topic-tag topic-tag-link"})
        topics_list=[]
        for href in topics:
            topics_list.append(href.get_text().replace('\n', '').replace('\t', '').strip())

        print("Topics:",topics_list)

        readme_article = page_soup.findAll("article", {"class": "markdown-body entry-content"})
        para = readme_article[0].find_all('p')
        if not para:
            continue
        else:
            paradata = []
            for p in para:
                str1=p.get_text()
                if not str1:
                    # /print('null values')
                    continue
                else:
                    paradata.append(p.get_text())
            [i.strip() for i in paradata]
            # print('Title---->',link)
            print('Readme File:',paradata)
            issue_list=get_issues(myurl)
            print('Issues:',issue_list)
            write_to_csv(title_list,topics_list,paradata,issue_list)




def write_to_csv(title_list,topics_list,paradata,issue_list):
    '''
    Write the fetched data to the CSV file
    :param title_list: contains title
    :param topics_list:  contains topic
    :param paradata: contain all the textual data
    :param issue_list: contains list of all the issues
    '''
    #print(title_list)
    title_string=title_list[0]

    topic_string=",".join(str(i) for i in topics_list)
    paradata_string=",".join(str(i) for i in paradata)
    issue_string=",".join(str(i) for i in issue_list)

    row_list=[title_string,topic_string,paradata_string,issue_string]
    with open(r'5000_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row_list)

def get_issues(myurl):
    '''
    Get all the issues through different links
    :param myurl: different urls of issues
    '''
    issue_url = myurl + '/issues'
    uClient2 = uReq(issue_url)
    main_page = uClient2.read()
    uClient2.close()

    page_soup = soup(main_page, "html.parser")
    issue_links = []
    issue_list_page = page_soup.findAll("a", {"class": "link-gray-dark no-underline h4 js-navigation-open"})
    # print(issue_list)
    if len(issue_list_page) > 0:
        for a in issue_list_page:
            # print(a.get_text())
            issue_links.append(a.get_text().replace('\n', '').replace('\t', '').strip())

    return issue_links

def main():
    get_data()

if __name__ == '__main__':
    main()

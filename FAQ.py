
# coding: utf-8

# In[2]:



    requests.get(url)
    res = requests.get(url)
    res.encoding='utf-8'
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(res.text,'html.parser')
  
    tag_name = 'span.question'
    question = soup.select(tag_name)
                
    j = 0
    
    for q in question:
            j=j+1
            q_question = q.text

            print(q_question)
            ii = j
            if j<10:
                ii='0'+str(j)
            tag_name2 = 'div#faq' + str(ii) + ' p'
            answer = soup.select(tag_name2)
            if(answer):
                print(answer[0].text)

for i in range(1,5):
    if i == 1 or i == 4:
        url = 'https://www.fubon.com/life/qa/qa_life_0' + str(i) + '.htm'
        getMessage(url)
        
    
    elif i == 3:
        for j in range(1,10):
            if j<10:
                jj='0'+str(j)
            url = 'https://www.fubon.com/life/qa/qa_life_0' + str(i) + '_'+ str(jj) +'.htm'
            getMessage(url)
            
    elif i == 2:
        for j in range(1,3):
            for k in range(1,17):
                kk=str(k)
                if k<10:
                    kk='0'+str(k)
                url = 'https://www.fubon.com/life/qa/qa_life_0' + str(i) + '_0' + str(j) + '_' + str(kk) + '.htm'
                getMessage(url)
                


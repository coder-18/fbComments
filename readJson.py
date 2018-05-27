import json
import operator


json_list=['BeingSalmanKhan','virat.kohli','DeepikaPadukone','YOYOhoneysingh','shreyaghoshal','SachinTendulkar','priyankachopra','Amitabh\
Bachchan','MadhuriDixitNene']

page_comment_count={}
for page in json_list:
    count = 0
    with open(page+'.json','rb') as f1:
        json_data= json.load(f1)
    for post in json_data['data']:
        count=count+len(post['comments'])
    print page + " -->  " +str(count)
    page_comment_count[page]=count


print page_comment_count
    
sorted_comment = sorted(page_comment_count.items(), key=operator.itemgetter(1),reverse=True)
print sorted_comment
#for item in sorted_comment:
#    print sorted_comment[item]

import json
import facebook
import requests



access_token = 'EAACEdEose0cBAJ8GjClzx23M0hzFLwNgKheDrHI5Gm3cU50l76zYqqUx9THD891EqZCz13QqtPAmMd9bYxH9WfZAte8IeIwjvQOMLDRthhwl4Uw5BuhC76WKNNN2XeZAoGZAICOCHpRnHgTroMnpUZAI90qadvO4LJSKEMrEadHoFRZAnFHVbA631UnNCkLkAZD'






def get_data(query,page_list):
    ''' function which executes query and passes posts for further processing   '''
    graph = facebook.GraphAPI(access_token)
    for page in page_list:
        data_query= page + query
        post = graph.get_object(data_query)
        data = post['posts']['data']  # actual posts
        handles_post(data,page)

    

def handles_post(data,page):
    ''' calls method handle_comments per Fb post and converts data into structure as required     '''
    required_out_dict={}
    required_out_dict['page_id'] = page
    data_list=[]
    for post in data:
        data_list.append(handle_comments(post))
    required_out_dict['data']=data_list
    
    with open(page+'.json','wb') as f1:     # creates json for each page
        json.dump(required_out_dict,f1)
                
    

def handle_comments(post):
    ''' processes comments and extract_useful_fields for handling next pages  '''
        
    post_dict= {}
    post_dict['post_id'] = post['id']
    post_dict['created_at'] = post['created_time']
    if 'comments'  in post.keys(): # with comments extra things are there
        comments_list=post['comments']['data']
        formatted_comment_list=comment_list_generator(comments_list)
        extract_useful_fields(post['comments']['paging'],formatted_comment_list)  # extracting only required fields
            
            
    post_dict['comments']=formatted_comment_list
    
    return post_dict
    
    

def comment_list_generator(comments_list):
    ''' extracts only required fields from comment list'''
    comments=[]
    for comment in comments_list:
        temp_comment_dict={}
        temp_comment_dict['text']=comment['message']
        temp_comment_dict['id']=comment['id']
        temp_comment_dict['created_at']=comment['created_time']
        comments.append(temp_comment_dict)
    return comments

def extract_useful_fields(paging,formatted_comment_list):
    ''' recursively extracts comments for next pages '''
    request_url=paging['next']
    response= requests.get(request_url)
    post=json.loads(response.text)
    #print post.keys()   [u'paging', u'data']    kept this to remember the structure
    if 'data' in post.keys():
        comments_list=post['data']
        formatted_comment_list.extend(comment_list_generator(comments_list))
        if 'paging' in post.keys() and 'next' in post['paging'].keys():
            extract_useful_fields(post['paging'],formatted_comment_list)     # recursively extracting all comments found on next pages
        else:
            return formatted_comment_list
    else:
        return formatted_comment_list

''' currently only next inside post are handled as we got required no. of comments from it. But need to handle next on main page as well'''    

if __name__ == "__main__":

    # list of celebs and entertainment pages
    input_list=['BeingSalmanKhan','virat.kohli','DeepikaPadukone','YOYOhoneysingh','shreyaghoshal','SachinTendulkar','priyankachopra','AmitabhBachchan','MadhuriDixitNene']
    input_list=['DeepikaPadukone']
    
    query='''?fields=posts.limit(10){id,created_time,comments{id,created_time,message}} ''' # change limits here for comments and posts
    get_data(query, input_list)    

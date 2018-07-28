from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import sqlite3
from sqlite3 import Error
 

 
"""
        cur.execute("CREATE TABLE IF NOT EXISTS user_ord(type text,size text,number real)")
        cur.execute("CREATE TABLE IF NOT EXISTS coffee_types(type text,price real)")
        cofee = [('black coffee', '25'),
             ('irish coffee', '25'),
             ('cappuccino', '25'),('macchiato', '25'),('espresso', '25'),('café latte', '25'),('turkish coffee', '25'),('frappuccino', '25'),('iced coffee', '25'),('flat white', '25'),
            ]
        cur.executemany('INSERT INTO coffee_types VALUES(?,?)',cofee) 
       
        #cur.execute("INSERT INTO user_ord VALUES ('black coffee','medium',2)")
        conn.commit()
        cur.execute("SELECT * FROM coffee_types")
        #print cur.fetchone()
        rows = cur.fetchall()

        for row in rows:
            print(row)	
     
        cur.execute("CREATE TABLE coffee")		
       cofee = [('black coffee', '25'),
             ('irish coffee', '25'),
             ('cappuccino', '25'),('macchiato', '25'),('espresso', '25'),('café latte', '25'),('turkish coffee', '25'),('frappuccino', '25'),('iced coffee', '25'),('flat white', '25'),
            ]
        cur.executemany('INSERT INTO coffee VALUES(?,?)',cofee) 
       
"""
     

context = None
conversation=None
t=0

final=[]
order=dict()
finalord=[]
currord=[]
thisord=[]
oldord=[]
def send_tele(response):

    resp = ''
    for text in response['output']['text']:
        resp += text
    print(resp)
    return resp
 
def handle_missing(bot,update):
    global context
    if len(thisord)==0:
        context={'missing':'null','types':'null','size':'null','anything':'yes'}
        return "Would you like to continue ordering? yes or no"
    for ord in thisord:
        print('missing',ord[0])
        if 'number' not in ord[0]:
            print("number isnt here")
            context={'missing':'yes','types':ord[0]['types'],'size':ord[0]['size']}
            val1=ord[0]['types']
            val2=ord[0]['size']
            del thisord[0]
            print("after deletion",thisord)
            return 'How many',val1,val2,'do you need?'
        if 'size' not in ord[0]:
            print("size isnt here")
            context={'missing':'yes','types':ord[0]['types'],'number':ord[0]['number']}
            val1=ord[0]['types']
            print(context)
            del thisord[0]
            return 'Would you like to have',val1, 'it in regular,medium or large?'


def handle_two(bot,update,order):
    global thisord
    thisord=[]
    for i in range(0,len(order),2):
        if order[i]['entity']=='types' and order[i+1]['entity']=='size':
            print(order[i]['value'],':',order[i+1]['value'])
            currord=[{'types':order[i]['value'],'size':order[i+1]['value']}]
            thisord.append(currord)
          
        elif order[i]['entity']=='types' and order[i+1]['entity']=='number':
            print(order[i]['value'],':',order[i+1]['value'])
            currord=[{'types':order[i]['value'],'number':order[i+1]['value']}]
            thisord.append(currord)
        elif order[i]['entity']=='size' and order[i+1]['entity']=='types':
            print(order[i+1]['value'],':',order[i]['value'])
            currord=[{'size':order[i]['value'],'types':order[i+1]['value']}]
            thisord.append(currord)
        elif order[i]['entity']=='number' and order[i+1]['entity']=='types': 
            print(order[i+1]['value'],':',order[i]['value']) 
            currord=[{'number':order[i]['value'],'types':order[i+1]['value']}]
            thisord.append(currord)
        else:
            print('Invalid') 

    print('this ',thisord) 
    val=handle_missing(bot,update)
    return val

def handle_missing_one(bot,update):
    global context
    global oldord
    global thisord
    print('latest',thisord)
    if len(thisord)==0:
        context={'missing':'null','types':'null','size':'null','anything':'yes'}
        return "Would you like to continue ordering? yes or no"
    for ord in thisord:
        if 'size' not in ord[0]:
            print("size isnt here")
            context={'missing':'yes','types':ord[0]['types'],'number':ord[0]['number'],'num':'null'}
            val1=ord[0]['types']
            del thisord[0]
            thisord=oldord.copy()
            return 'Would you like to have',val1, 'it in regular,medium or large?'

def handle_size(bot,update,order):
    global thisord
    global oldord
    oldord=thisord.copy()
    thisord=[]
    for i in range(0,len(order),1):
        if 'types' in order[i] and 'number' in order[i]:
            print(order[i]['types'],':',order[i]['number'])
            currord=[{'types':order[i]['types'],'number':order[i]['number']}]
            thisord.append(currord)
    print('this size',thisord) 
    val=handle_missing_one(bot,update)
    return val

def handle_number():
    global context
    if len(thisord)==0:
        context={'missing':'null','types':'null','size':'null','anything':'yes'}
        return "Would you like to continue ordering? yes or no"
    for ord in thisord:
        if 'number' not in ord[0]:
            context = {'missing': 'yes', 'types': ord[0]['types'], 'num':'null'}
            print('aft context',context)
            val1 = ord[0]['types']
            del thisord[0]
            print("after deletion", thisord)
            return 'How many cups of', val1, 'do you need?'


def handle_one(order):
    global thisord
    thisord = []
    for i in range(len(order)):
        if order[i]['entity']=='types':
            currord=[{'types':order[i]['value']}]
            thisord.append(currord)
    val=handle_number()
    return val

def handle_three(order):
    for i in range(0,len(order),3):
        if order[i]['entity']=='types' and order[i+1]['entity']=='size' and order[i+2]['entity']=='number':
            currord=[{'types':order[i]['value'],'size':order[i+1]['value'],'number':order[i+2]['value']}]
            finalord.append(currord)
        elif order[i]['entity']=='types' and order[i+1]['entity']=='number' and order[i+2]['entity']=='size':
            currord=[{'types':order[i]['value'],'size':order[i+2]['value'],'number':order[i+1]['value']}]
            finalord.append(currord)
        elif order[i]['entity']=='size' and order[i+1]['entity']=='types' and order[i+2]['entity']=='number':
            currord=[{'types':order[i+1]['value'],'size':order[i]['value'],'number':order[i+2]['value']}]
            finalord.append(currord)
        elif order[i]['entity']=='size' and order[i+1]['entity']=='number' and order[i+2]['entity']=='types':
            currord=[{'types':order[i+2]['value'],'size':order[i]['value'],'number':order[i+1]['value']}]
            finalord.append(currord)
        elif order[i]['entity']=='number' and order[i+1]['entity']=='size' and order[i+2]['entity']=='types':
            currord=[{'types':order[i+2]['value'],'size':order[i+1]['value'],'number':order[i]['value']}]
            finalord.append(currord)
        elif order[i]['entity']=='number' and order[i+1]['entity']=='types' and order[i+2]['entity']=='size':
            currord=[{'types':order[i+1]['value'],'size':order[i+2]['value'],'number':order[i]['value']}]
            finalord.append(currord)
        else:
            print('Invalid')
        
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hi!')


def message(bot, update):
    print('Received an update')
    global context 
    global final  
    global conversation 
    conversation= ConversationV1(username='7e8a016b-2c28-4bdd-b6e8-2043febdf43e',  # TODO
                                  password='Bi3ui0yvDAb0',  # TODO
                                  version='2018-02-16')
                                  

    # get response from watson
    response = conversation.message(
        workspace_id='154e610f-03b1-43e9-81c0-268b421b1c80',  # TODO
        input={'text': update.message.text},
        context=context)
    #print(json.dumps(response, indent=2))
    context = response['context']
    order=response['entities']
    #print(response)
    global finalord
    if len(response['intents'])==0 and len(response['entities'])==0:
        resp2=send_tele(response)
        update.message.reply_text(resp2)
    if 'missing' in context and context['missing']=='yes':
        if 'types' in context and 'size' in context:
            currord=[{'types':context['types'],'size':context['size'],'number':order[0]['value']}]
            finalord.append(currord)
            val=handle_missing(bot,update)
            update.message.reply_text(val)
        if 'types' in context and 'number' in context and 'num' not in context:
            
            if len(order)==1 and order[0]['entity']=='size':
                currord=[{'types':context['types'],'number':context['number'],'size':order[0]['value']}]
                finalord.append(currord)
                val = handle_missing(bot, update)
                update.message.reply_text(val)
            else:
                
                for i in range(0,len(order),2):
                    
                    if order[i]['entity']=='size' and order[i+1]['entity']=='number':
                        
                        currord=[{'types':context['types'],'number':order[i+1]['value'],'size':order[i]['value']}]
                        
                        finalord.append(currord)
                    elif order[i]['entity']=='number' and order[i+1]['entity']=='size':
                        
                        currord=[{'types':context['types'],'size':order[i+1]['value'],'number':order[i]['value']}]
                        
                        finalord.append(currord)
                        print(finalord)
                val=handle_missing(bot,update)
                update.message.reply_text(val)
        print(finalord)
        if 'types' in context and 'number' in context and 'num' in context and context['num']=='null':
            
            if len(order)==1 and order[0]['entity']=='size':
                currord=[{'types':context['types'],'number':context['number'],'size':order[0]['value']}]
                finalord.append(currord)
                val=handle_number()
                update.message.reply_text(val)
            else:
                
                for i in range(0,len(order),2):
                    
                    if order[i]['entity']=='size' and order[i+1]['entity']=='number':
                        
                        currord=[{'types':context['types'],'number':order[i+1]['value'],'size':order[i]['value']}]
                        
                        finalord.append(currord)
                    elif order[i]['entity']=='number' and order[i+1]['entity']=='size':
                        
                        currord=[{'types':context['types'],'size':order[i+1]['value'],'number':order[i]['value']}]
                        
                        finalord.append(currord)
                        print(finalord)
                val=handle_number()
                update.message.reply_text(val)
        print('final',finalord)
        if 'types' in context  and 'num' in context and context['num']=='null' and order[0]['entity']=='number' and len(order)==1:
            currord=[{'types':context['types'],'number':order[0]['value']}]
            print(currord)
            val = handle_size(bot,update,currord)
            update.message.reply_text(val)

    elif len(order)==1 and order[0]['entity']=='types':
        val = handle_one(order)
        update.message.reply_text(val)
    elif len(order)>1:
        t=0
        for j in range(len(order)):
            if order[j]['entity']=='types':
                t+=1
        if t==len(order):
            val = handle_one(order)
            update.message.reply_text(val)
        elif len(order)%2 == 0 and len(order)%3==0:
            t=0
            for j in range(len(order)):
                if order[j]['entity']=='types':
                    t+=1

            if (len(order)/t)%3==0:
                handle_three(order)
                update.message.reply_text("Would you like to continue ordering? yes or no")
                context = {'anything': 'yes'}
            elif (len(order)/t)%2==0:
                val=handle_two(bot,update,order)
                update.message.reply_text(val)
        elif len(order)%3 ==0:
            handle_three(order)
            update.message.reply_text("Would you like to continue ordering? yes or no")
            context = {'anything': 'yes'}
        elif len(order)%2==0:
            val=handle_two(bot,update,order)
            update.message.reply_text(val)
        


        
    else: 
        flag=0
        print(response['input']['text'])
        if 'anything' in context and context['anything']=='yes' and response['input']['text'].lower()=='no':
            context={'anything':'null'}  
            flag=1
            final=list()
            for i in range(len(finalord)):
                final.append(finalord[i][0])
            
            for i in range(len(final)):
                for j in range(len(final)):
                    if i!=j and 'deleted' not in final[i] and 'deleted' not in final[j]:
                       
                        
                        if final[i]['types']==final[j]['types'] and final[i]['size']==final[j]['size']:
                            vali=final[i]['types']
                            valj=final[i]['size']
                            valk=int(final[i]['number'])+int(final[j]['number'])
                            
                            
                            final[i]['deleted']=1
                            final[j]['deleted']=1
                            
                            final.append({'types':vali,'size':valj,'number':str(valk)})
                            
                        
                            
            fi=[]
            for i in final:
                if 'deleted' not in i:
                    fi.append(i)
            final=fi

            i = 0
            final_reply = ''
            reply = 'Your order is '
            while i < len(final):
                d = final[i].copy()
                print('d: ', d)
                if 'types' in d and 'size' in d and 'number' in d:
                    final_reply += d['number'] + ' ' + d['types'] + ' in ' + d['size'] + '.'
                    i = i + 1
            final_reply = reply + final_reply + ' Correct?'
            print(final_reply)
            update.message.reply_text(final_reply)
        elif 'anything' in context and context['anything']=='yes' and response['input']['text'].lower()!='no':
            update.message.reply_text('Please place your next order')
        elif response['intents'][0]['intent']=='reorder':
             finalord.clear()
             flag=1
             resp2 = send_tele(response)
             
             update.message.reply_text(resp2)
             
        elif response['intents'][0]['intent']=='get_menu':
            flag=1
            resp2 = send_tele(response)
            update.message.reply_text(resp2)
        elif response['intents'][0]['intent']=='goodbye':
            flag=1
            finalord=[]
            currord=[]
            thisord=[]
            oldord=[]
            resp2 = send_tele(response)
            update.message.reply_text(resp2)
        
        elif response['intents'][0]['intent']=='bye_success':
            flag=1
            print("FINAL ORDER")
            print(final)
            print(len(final))
            
	    #inserting order
            try:
                conn = sqlite3.connect("coffee_order.db")
               
                cur = conn.cursor()
                print(conn ,cur)
                cur.execute("SELect * from user_ord")
                print (cur.fetchone())
                for i in final:
                  
                    print("Entered loop")
                    print(i['types'])
                
                    cur.execute("INSERT INTO user_ord(type,size,number) VALUES(?,?,?)",(i['types'],i['size'],i['number']))
                    conn.commit()
               

                cur.execute("SELECT * FROM user_ord")
       
                rows = cur.fetchall()

                for row in rows:
                    print(row)
                cur.close()
                conn.close()
                print("db closed")
            except:
                print("DB not working")
            finalord.clear()
            currord=[]
            thisord=[]
            oldord=[]
            resp2 = send_tele(response)
            update.message.reply_text(resp2)  
        elif flag==0:
            print('working?')
            resp2 = send_tele(response)
            update.message.reply_text(resp2)   
    # build response
       
    


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')
    
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('613631299:AAGlnBaw_z3gpUyDnzCNAbu2dE6c6ndvrTw')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
   
    main()

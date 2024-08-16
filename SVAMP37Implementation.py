
#SVAMP37 Dataset 
#check it with gpt4 
#check it with the different datasets 

import openai
from openai import OpenAI
from array import *
from openai import OpenAIError
import re

client = OpenAI(api_key='ENTER API KEY HERE')

quesSAC3Bank = [] 
quesCoVEBank = [
    ["Each pack of dvds costs 76 dollars. If there is a discount of 25 dollars on each pack. How much do you have to pay to buy each pack?"],
    ["Dan had $3 left with him after he bought a candy bar. If he had $4 at the start. How much did the candy bar cost?"],
    ["Paco had 26 salty cookies and 17 sweet cookies. He ate 14 sweet cookies and 9 salty cookies. How many salty cookies did Paco have left?"],
    ["43 children were riding on the bus. At the bus stop some children got off the bus. Then there were 21 children left on the bus. How many children got off the bus at the bus stop?"],
    ["28 children were riding on the bus. At the bus stop 82 children got on the bus while some got off the bus. Then there were 30 children altogether on the bus. How many more children got on the bus than those that got off?"],
    ["There were 3 dollars in Olivia's wallet. She collected 49 more dollars from an atm. After she visited a supermarket there were 49 dollars left. How much more money did she collect at the ATM than she spent at the supermarket?"],
    ["Jerry had some action figures on a shelf in his room. Later he added 7 more action figures to the shelf. If there are a total of 10 action figures on his shelf now. How many action figures did he have initially on the shelf?"],
    ["Paco had 41 cookies. He gave 9 cookies to his friend and ate 18 cookies. How many more cookies did he eat than those he gave to his friend?"],
    ["Mary is baking a cake. The recipe calls for 3 cups of sugar, 10 cups of flour, and 15 cups of salt. She already put in 6 cups of flour. How many more cups of flour does she need to add?"],
    ["A waiter had some customers. After 9 customers left, he still had 12 customers. How many customers did he have at the start?"],
]
quesREFBank = [
    ["Each pack of DVDs costs 76 dollars. If there is a discount of 25 dollars on each pack. How much do you have to pay to buy each pack? Just output the amount. Output format should be <num>.<amount>", "What is the total cost for buying multiple packs with the discount applied? Please, list only the total costs formatted as - AMOUNT:<total cost>"],
    ["Dan had $3 left with him after he bought a candy bar. If he had $4 at the start. How much did the candy bar cost? Just output the cost. Output format should be <num>", "What other expenses did Dan have that day? Please, list only the expense amounts formatted as - AMOUNT:<expense>"],
    ["Paco had 26 salty cookies and 17 sweet cookies. He ate 14 sweet cookies and 9 salty cookies. How many salty cookies did Paco have left? Just output the remaining amount. Output format should be <num>", "What was the total number of cookies Paco originally had? Please, list only the total number formatted as - TOTAL:<total cookies>"],
    ["43 children were riding on the bus. At the bus stop some children got off the bus. Then there were 21 children left on the bus. How many children got off the bus at the bus stop? Just output the number. Output format should be <num>", "How many children boarded the bus before the stop? Please, list only the number formatted as - NUMBER:<number>"],
    ["28 children were riding on the bus. At the bus stop 82 children got on the bus while some got off the bus. Then there were 30 children altogether on the bus. How many more children got on the bus than those that got off? Just output the difference. Output format should be <num>", "What was the total number of children on the bus before the stop? Please, list only the number formatted as - NUMBER:<number>"],
    ["There were 3 dollars in Olivia's wallet. She collected 49 more dollars from an ATM. After she visited a supermarket there were 49 dollars left. How much more money did she collect at the ATM than she spent at the supermarket? Just output the difference. Output format should be <num>", "What was the total amount Olivia spent at the supermarket? Please, list only the amount formatted as - AMOUNT:<amount>"],
    ["Jerry had some action figures on a shelf in his room. Later he added 7 more action figures to the shelf. If there are a total of 10 action figures on his shelf now. How many action figures did he have initially on the shelf? Just output the initial amount. Output format should be <num>", "What is the total number of action figures Jerry has now? Please, list only the total number formatted as - TOTAL:<total>"],
    ["Paco had 41 cookies. He gave 9 cookies to his friend and ate 18 cookies. How many more cookies did he eat than those he gave to his friend? Just output the difference. Output format should be <num>", "What is the total number of cookies Paco had initially? Please, list only the total number formatted as - TOTAL:<total>"],
    ["Mary is baking a cake. The recipe calls for 3 cups of sugar, 10 cups of flour, and 15 cups of salt. She already put in 6 cups of flour. How many more cups of flour does she need to add? Just output the additional amount. Output format should be <num>", "What other ingredients are required for the cake recipe? Please, list only the ingredient names and amounts formatted as - INGREDIENT:<ingredient>"],
    ["A waiter had some customers. After 9 customers left, he still had 12 customers. How many customers did he have at the start? Just output the initial number. Output format should be <num>>", "How many customers left the restaurant if there were 12 remaining? Please, list only the number of customers formatted as - NUMBER:<number>"]
]

# Index for one list element: 0: Self-Consistency question, 1-3: SAC3, 4: System content parameter for GPT
quesSAC3Bank.insert(-1, [
    "Each pack of DVDs costs 76 dollars. If there is a discount of 25 dollars on each pack, how much do you have to pay to buy each pack?",
    "What is the final price of a DVD pack that costs 76 dollars after applying a 25 dollar discount?",
    "If a pack of DVDs originally costs 76 dollars and there’s a 25 dollar discount, what is the amount to be paid?",
    "Can you calculate the price of a DVD pack if the original price is 76 dollars and there’s a 25 dollar discount?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])
quesSAC3Bank.insert(-1, [
    "Dan had $3 left with him after he bought a candy bar. If he had $4 at the start, how much did the candy bar cost?",
    "What is the price of the candy bar if Dan started with $4 and ended up with $3?",
    "How much did Dan spend on the candy bar if he had $4 initially and $3 remaining?",
    "Can you determine the cost of the candy bar given that Dan had $4 to begin with and $3 left afterward?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "Paco had 26 salty cookies and 17 sweet cookies. He ate 14 sweet cookies and 9 salty cookies. How many salty cookies did Paco have left?",
    "After eating 9 salty cookies from an initial 26, how many salty cookies does Paco have remaining?",
    "If Paco started with 26 salty cookies and ate 9 of them, how many salty cookies are left?",
    "Given that Paco ate 9 salty cookies out of 26, what is the number of salty cookies he still has?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "43 children were riding on the bus. At the bus stop, some children got off the bus. Then there were 21 children left on the bus. How many children got off the bus at the bus stop?",
    "If there were 43 children on the bus and 21 remained after some got off, how many children exited the bus?",
    "What is the number of children who got off the bus if 21 were left from an initial 43?",
    "Can you calculate how many children left the bus if there were 43 children initially and 21 were left afterward?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "28 children were riding on the bus. At the bus stop, 82 children got on the bus while some got off the bus. Then there were 30 children altogether on the bus. How many more children got on the bus than those that got off?",
    "If there were initially 28 children on the bus and 82 new children boarded while the total number became 30, how many more children got on the bus compared to those who got off?",
    "How many additional children boarded the bus compared to the number of children who exited, given that the final count was 30 after 82 new children got on?",
    "Can you determine the difference between the number of children who boarded the bus and those who got off if there were 28 children initially and the total became 30 after some changes?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "There were 3 dollars in Olivia's wallet. She collected 49 more dollars from an ATM. After she visited a supermarket, there were 49 dollars left. How much more money did she collect at the ATM than she spent at the supermarket?",
    "If Olivia ended up with 49 dollars after spending at the supermarket and had 3 dollars initially, how much more did she withdraw from the ATM compared to what she spent?",
    "What is the difference between the amount Olivia collected from the ATM and the amount she spent at the supermarket, given she had 49 dollars left after shopping?",
    "Can you calculate how much more money Olivia withdrew from the ATM than she spent at the supermarket if she had 3 dollars initially and had 49 dollars remaining after her purchase?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "Jerry had some action figures on a shelf in his room. Later he added 7 more action figures to the shelf. If there are a total of 10 action figures on his shelf now, how many action figures did he have initially on the shelf?",
    "If Jerry now has 10 action figures on his shelf after adding 7 more, how many action figures did he originally have before adding the new ones?",
    "What is the initial number of action figures on Jerry’s shelf if he added 7 to reach a total of 10?",
    "Can you determine the number of action figures Jerry had before adding 7 more, given that the total count is now 10?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "Paco had 41 cookies. He gave 9 cookies to his friend and ate 18 cookies. How many more cookies did he eat than those he gave to his friend?",
    "If Paco ate 18 cookies and gave 9 cookies to his friend, how many more cookies did he eat compared to those he gave away?",
    "What is the difference between the number of cookies Paco ate and the number he gave to his friend?",
    "Can you calculate how many more cookies Paco consumed than he gave to his friend if he ate 18 cookies and gave away 9?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "Mary is baking a cake. The recipe calls for 3 cups of sugar, 10 cups of flour, and 15 cups of salt. She already put in 6 cups of flour. How many more cups of flour does she need to add?",
    "If Mary has already added 6 cups of flour to her cake batter and the recipe requires a total of 10 cups, how many more cups of flour does she need to add?",
    "What is the additional amount of flour Mary needs to add if the recipe requires 10 cups and she has already added 6 cups?",
    "Can you determine how many more cups of flour are needed if Mary has put in 6 cups out of the 10 cups required by the recipe?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

quesSAC3Bank.insert(-1, [
    "A waiter had some customers. After 9 customers left, he still had 12 customers. How many customers did he have at the start?",
    "If a waiter ended up with 12 customers after 9 left, how many customers were there initially?",
    "What was the original number of customers if 9 left and 12 remained?",
    "Can you calculate the number of customers the waiter had before 9 left if he had 12 remaining afterward?",
    "You are a virtual assistant, generate the most accurate and precise answer based on common knowledge or general facts."
])

#quesREFBank.append(["List 5 existing references related to 'Artificial intelligence: Planning and Scheduling'. Just output the titles. Output format should be <num.><title>"]) # No context in paper, we can add this if necessary

# SAC3 Paper: https://arxiv.org/pdf/2311.01740
def runSAC3(questionList, startIndex, endIndex, GPTversion): 
  print("--------------------------------------------------\nSAC3\n--------------------------------------------------\n")
  index = 0
  for index in range(startIndex, endIndex):
    # Self-Consistency
    print("Self-Consistency")
    print("Q: " + str(questionList[index][0]))
    for x in range(0, 3):
      completion = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][0]}
      ]
      )   

      print(str(x+1) + ") " + str(completion.choices[0].message.content) + "\n---\n")

    print("\n\n")

    # SAC3
    print("SAC3")
    
    print("Q: " + str(questionList[index][1]))
    completion = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][1]}
      ]
    )
    print(str(completion.choices[0].message.content) + "\n")


    print("Q: " + str(questionList[index][2]))
    completion2 = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][2]}
      ]
    )
    print(str(completion2.choices[0].message.content)+ "\n")


    print("Q: " + str(questionList[index][3]))
    completion3 = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][3]}
      ]
    )
    print(str(completion3.choices[0].message.content)+ "\n")
    print("\n\n ----- END OF QUESTION ----- \n\n")

# CoVE paper: https://arxiv.org/pdf/2309.11495
def runCoVe(questionList, startIndex, endIndex, GPTversion):
  print("--------------------------------------------------\nCHAIN OF VERIFICATION (COV3)\n--------------------------------------------------\n")
  index = 0
  systemContent = "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
  for index in range(startIndex, endIndex):
      # ask the baseline question
    print("Q: " + str(questionList[index]))
    completion = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "user", "content": questionList[index]},
        {"role": "system", "content": systemContent}
      ]
    )
    baselineResponse = str(completion.choices[0].message.content)
    print("BASELINE RESPONSE: \n" +baselineResponse + "\n\n\n")

    # generate 5 verification (CoVe) questions
    completion = client.chat.completions.create(
    model=GPTversion,
    messages=[
       {"role": "user", "content": "The baseline question is: " + str(questionList[index]) + "\n The baseline response generated by ChatGPT is: " + baselineResponse + "\n Based on the original query and the baseline response, generate a series of 5 verification questions that test the factual claims in the original baseline response" },
       {"role": "system", "content": systemContent}
      ]
    )
    verificationResponse = str(completion.choices[0].message.content) + "\n"

    # execute verifications (using the factor method)
    completion = client.chat.completions.create(
    model=GPTversion,
    messages=[
       {"role": "user", "content": "The verification questions are: " + verificationResponse + "\n Generate responses for these questions."},
       {"role": "system", "content": systemContent}
      ]
    )
    verExecuteResponse = str(completion.choices[0].message.content)
    print("VERIFICATION QUESTIONS: \n" +verificationResponse + "\nVERIFICATION ANSWERS: \n" + verExecuteResponse + "\n\n\n")

    # verify (using factor+revise)
    completion = client.chat.completions.create(
    model=GPTversion,
    messages=[
       {"role": "user", "content": "The verification questions are: " + verificationResponse + "\n The verification response was: " + verExecuteResponse + "\n Given this content, answer the baseline question again: " + questionList[index]},
       {"role": "system", "content": systemContent}
      ]
    )
    revisedResponse = str(completion.choices[0].message.content)
    print("REVISED BASELINE ANSWER: \n" +revisedResponse + "\n----------------------------------------------------------------\n")

# Hallucinating References Paper: https://arxiv.org/pdf/2305.18248
def runREF(questionList, startIndex, endIndex, GPTversion):
  print("--------------------------------------------------\n REFERENCES \n--------------------------------------------------\n")
  index = 0
  systemContent = ""
  all_scores = []
  
  #Changed: 
  def askQuestion(content, systemContent, client1):
    try:
        print(f"Requesting completion with model: {GPTversion}")
        print(f"System Content: {systemContent}")
        print(f"User Content: {content}")

         # Ensure both systemContent and content are strings
        if not isinstance(systemContent, str):
            raise ValueError("systemContent must be a string")
        if not isinstance(content, str):
            raise ValueError("content must be a string")

        completion = client1.chat.completions.create(
            model=GPTversion,
            messages=[
                {"role": "system", "content": systemContent},
                {"role": "user", "content": content}
            ]
        )
        response_content = str(completion.choices[0].message.content)
        print(f"Response Content: {response_content}")
        return response_content
    except openai.BadRequestError as e:
        print(f"Invalid Request Error: {e}")
    except openai.AuthenticationError as e:
        print(f"Authentication Error: {e}")
    except openai.InternalServerError as e:
        print(f"Rate Limit Error: {e}")
    except openai.RateLimitError as e:
        print(f"OpenAI API Error: {e}")
    except Exception as e:
        print(f"General Error: {e}")
    return None

        
  for index in range(startIndex, endIndex):
    # ask the baseline question
    print("Q: " + str(questionList[index][0]))
    baselineResponses = askQuestion(questionList[index][0], systemContent,client)
    print("BASELINE RESPONSE: \n" +baselineResponses + "\n\n\n")

    # For each reference, Check DQ[1-3] and IQ
    repeated_ask = 3 #This is randomly chosen by MaGK
    DQs_yes = [0]*3
    #Changed: added a counter variable to keep track of how many times the result is yes 
    numberOfYes = 0
    IQ1s = []
    baselineResponsesString = baselineResponses
    baselineResponses = baselineResponses.split('\n') ## This is not tested and may need to be reworked
    for title, baselineResponse in enumerate(baselineResponses): # For each reference
        
        # Repeatedly ask Direct Questions about the reference
        for i in range(repeated_ask):
            # DQ1: Does the reference exist?
            DQ1_question = "Is the answer " + baselineResponse+ " true regarding the question '" +  questionList[index][0] +  "'. ? Ignore the previous output format command and just output just yes/no."
            DQ1 = askQuestion(DQ1_question, systemContent,client)
            if 'yes' in DQ1.lower():
                DQs_yes[0] +=1
                numberOfYes +=1 
                
            
            # DQ2: Provide a reference, Does the reference exist?
            DQ2_question = "Give a mathmatical property that proves, " + baselineResponse + " , is the answer to '"+ questionList[index][0] + " '. Does the property exist? Ignore the previous output format command and just output just yes/no." 
            DQ2 = askQuestion(DQ2_question, systemContent, client)
            if 'yes' in DQ2.lower():
                DQs_yes[1] +=1
                numberOfYes +=1 
        
            
            # DQ3: This reference was provided by an LM, Does the reference exist?
            #DQ3_question = "A language model generated references related to a research topic with the following answer: "+baselineResponsesString+" Does the reference with title #"+ str(title + 1) +" exist? Output just yes/no."
            
            DQ3_question = "A language model generated the following answer to a math problem: '" +baselineResponsesString+ "'. Does this match the correct solution for the question' " + questionList[index][0] + " ' Ignore the previous output format command and just output just yes/no."
            DQ3 = askQuestion(DQ3_question, systemContent, client)
            if 'yes' in DQ3.lower():
                DQs_yes[2] +=1
                numberOfYes +=1 
            
        # Calculated the groundedness rate and score *** check this ****
        DQs_grounded = [value / repeated_ask for value in DQs_yes]
        # Changed to DQs_yes instead of DQs_grounded is grounded is not a list
        DQ_score = sum(DQs_grounded)/3 ## Get Average of all DQs
        DQs_yes = [0]*3
    
        
        # Repeatedly ask j indirect Questions about the reference
        for i in range(repeated_ask):
            # IQ1:
            #CHANGED: originally had DQ1 question instead of IQ1 question
            clientUpdated = OpenAI(api_key='ENTER API KEY HERE')
            IQ1_question = "Do not answer this in Yes or No format. Instead, provide minimal mathematical steps needed to solve this problem. Each step should be one line long and you don't need to explain the step: '" + questionList[index][0] + "' in a format like '5 + x = 3, 3 - 5 = x, x = -2'. Do not include the original problem in your answer."
            IQ1 = askQuestion(IQ1_question, systemContent, clientUpdated)
            IQ1s.append(IQ1)
            #print("These are the IQ's currently being stored" + '\n')
            #print(IQ1s)
            
        # Find Overlap of IQ responses
        this_IQs = IQ1s
        overlap_IQ_total = 0
        pairs = 0
        for i in range(len(this_IQs)):
            for j in range(i+1, len(this_IQs)):
                IQ_i = this_IQs[i]
                IQ_j = this_IQs[j]
                overlap_question = "Below are what should be two lists of steps. On a scale of 0-100%, how much overlap is there in the steps (ignore minor variations that would result in the same final answer such as 3+5 is 8 and 5+3 is 8)? Answer with a number between 0 and 100. Also, provide a justification. Output format should be ANS: <ans> JUSTIFICATION: <justification>. \n" + str(IQ_i) + "\n" + str(IQ_j)
                overlap_IQ = askQuestion(overlap_question, systemContent, clientUpdated)
                print("Overlap IQ Response:", overlap_IQ)
                # Changed: added a match variable to group them only if a number is found 
                match = re.search(r'(\d+)%', overlap_IQ)
                if match:
                    overlap_IQ_val = match.group(1)  # Get the numeric part of the match
                    overlap_IQ_total += float(overlap_IQ_val)
                else:
                    print("No numeric match found in the response.")
                #overlap_IQ_val = re.search(r'\d+', overlap_IQ).group(0) #Get First Number in response
                pairs += 1
        IQ_score = overlap_IQ_total/pairs/100 #Get Average overlap as a percentage
        
        # Calculate IQ + DQ score
        IQ_DQ_score = (IQ_score + DQ_score)/2
        
        # Changed: Removed the [] outside of the score values 
        this_ref_scores = [IQ_score] + [DQs_grounded] + [DQ_score] + [IQ_DQ_score]
        
        print("SCORES FOR : ",baselineResponse)
        print("[ IQ, \t DQ1, \t DQ2, \t DQ3, \t DQ, \t IQ+DQ ]")
        print(this_ref_scores)
        
        # Save scores to list of all reference scores 
        # Changed to append instead of insert
        all_scores.append(this_ref_scores)
        IQ1s.clear() #  
  

#runSAC3(quesSAC3Bank, 0, len(quesSAC3Bank), "gpt-3.5-turbo-0125")
#runCoVe(quesCoVEBank, 0, len(quesCoVEBank), "gpt-3.5-turbo-0125")
runREF(quesREFBank, 0, len(quesREFBank), "gpt-3.5-turbo-0125")

# future tasks: implement risk score, implement two more methods (based on provided papers)


#NQ-OPEN Dataset 
#check it with gpt4 
#check it with the different datasets 

import openai
from openai import OpenAI
from array import *
from openai import OpenAIError
import re

client = OpenAI(api_key='ENTER KEY HERE ')

quesSAC3Bank = [] 
quesCoVEBank = ["Where did they film hot tub time machine", "who has the right of way in international waters", "who does annie work for attack on titan", "when was the immigration reform and control act passed", "when was puerto rico added to the usa", "who has been chosen for best supporting actress in 64 national filmfare award", "which side of the white house is the front", "names of the metropolitan municipalities in south africa", "who's hosting the super bowl in 2019", "in which year vivo launch its first phone in india"]
quesREFBank = [["Where did they film hot tub time machine. Just output the name of the place. Output format should be <name> ", "What landmarks are at this location. Please, list only the movie names formatted as - NAMES:<movie title>"], ["Who has the right of way in international waters. Just output the rule name. Output format should be <rule>", "What governing body enforces this rule? Please, list only the body names formatted as - NAMES:<governing body>"], ["Who does Annie work for in Attack on Titan. Just output the organization name. Output format should be <organization>", "What other characters are associated with this organization? Please, list only the names formatted as - NAMES:<character name>"], ["When was the Immigration Reform and Control Act passed. Just output the year. Output format should be <year>", "What were the major provisions of this act? Please, list only the provision names formatted as - NAMES:<provision>"]
,["When was Puerto Rico added to the USA. Just output the year. Output format should be <year>", "What other territories were acquired around the same time? Please, list only the names formatted as - NAMES:<territory name>"], ["Who has been chosen for Best Supporting Actress in the 64th National Filmfare Award. Just output the actress's name. Output format should be <actress>", "What movies was she nominated for? Please, list only the movie names formatted as - NAMES:<movie title>"], ["Which side of the White House is the front. Just output the side name. Output format should be <side>", "What notable events have taken place on this side? Please, list only the event names formatted as - NAMES:<event>"], ["Names of the metropolitan municipalities in South Africa. Just output the names. Output format should be <municipality>", "What are the largest cities in these municipalities? Please, list only the city names formatted as - NAMES:<city name>"], ["Who's hosting the Super Bowl in 2019. Just output the city name. Output format should be <city>", "What other major sports events has this city hosted? Please, list only the event names formatted as - NAMES:<event>"], ["In which year did Vivo launch its first phone in India. Just output the year. Output format should be <year>", "What models did they release that year? Please, list only the model names formatted as - NAMES:<model>"] ]

# Index for one list element: 0: Self-Consistency question, 1-3: SAC3, 4: System content parameter for GPT
quesSAC3Bank.insert(-1, ["where did they film hot tub time machine?",
                 "What are the filming locations for the movie Hot Tub Time Machine?",
"Can you tell me where Hot Tub Time Machine was filmed?",
"In which locations was the movie Hot Tub Time Machine shot?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["who has the right of way in international waters?",
                 "Which vessels have the right of way when navigating international waters?",
"How is the right of way determined for ships in international waters?",
"In international waters, who is given priority in terms of right of way?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["Who does annie work for attack on titan?",
                 "Which organization or group is Annie aligned with in Attack on Titan?",
"In Attack on Titan, who is Annie secretly working for?",
"What is the faction that Annie is associated with in Attack on Titan?",
"You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["When was the immigration reform and control act passed?",
                 "In what year was the Immigration Reform and Control Act enacted?",
"When did the Immigration Reform and Control Act become law?",
"What is the date of the passage of the Immigration Reform and Control Act?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["When was puerto rico added to the usa?",
                 "In what year did Puerto Rico become a part of the United States?",
"When did Puerto Rico officially become a U.S. territory?",
"What is the date when Puerto Rico was incorporated into the United States?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["Who has been chosen for best supporting actress in 64 national filmfare award?",
                 "Which actress won the Best Supporting Actress award at the 64th National Filmfare Awards?",
"Who received the Best Supporting Actress honor at the 64th National Filmfare Awards?",
"At the 64th National Filmfare Awards, who was awarded Best Supporting Actress?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["Which side of the white house is the front?",
                 "What is considered the front side of the White House?",
"Which side of the White House faces the main entrance?",
"On which side of the White House is the front facade located?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["What are the names of the metropolitan municipalities in south africa?",
                 "What are the names of the metropolitan municipalities in South Africa?",
"Can you list the metropolitan municipalities in South Africa?",
"Which municipalities in South Africa are classified as metropoitan?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["Who's hosting the super bowl in 2019?",
                "Which city is hosting the Super Bowl in 2019?",
"Who is the host of the 2019 Super Bowl?",
"Where will the 2019 Super Bowl be held?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
                 ])
quesSAC3Bank.insert(-1, ["In which year vivo launch its first phone in india?",
                "What year did Vivo introduce its first smartphone in India?",
"When did Vivo release its debut phone in the Indian market?",
"In which year was Vivo's first phone launched in India?",
                 "You are a virtual political assistant, generate the most accurate and precise answer based on common knowledge or general facts."
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
            DQ1_question = "Is the answer " + baselineResponse+ " true regarding the question " +  questionList[index][0] + "? Output just yes/no."
            DQ1 = askQuestion(DQ1_question, systemContent,client)
            if 'yes' in DQ1.lower():
                DQs_yes[0] +=1
                numberOfYes +=1 
                
            
            # DQ2: Provide a reference, Does the reference exist?
            DQ2_question = "Give a article/piece of literature that proves, " + baselineResponse + " , is the answer to "+ questionList[index][0] + " Does the article/piece of literature exist? Output just yes/no."
            DQ2 = askQuestion(DQ2_question, systemContent, client)
            if 'yes' in DQ2.lower():
                DQs_yes[1] +=1
                numberOfYes +=1 
        
            
            # DQ3: This reference was provided by an LM, Does the reference exist?
            DQ3_question = "A language model generated references related to a general question with the following answer: "+baselineResponsesString+" Does the answer with title #"+ str(title + 1) +" exist? Output just yes/no."
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
            clientUpdated = OpenAI(api_key='ENTER KEY HERE')
            IQ1_question = "Do not answer this in Yes or No format. Instead give me a list. " +  questionList[index][1] +  " The answer to the previous question that this question is related to is " + baselineResponse + "? Do not mention the reference in the answer."
            IQ1 = askQuestion(IQ1_question, systemContent, clientUpdated)

            IQ1s.append(IQ1)
            #print("These are the IQ's currently being stored" + '\n')
            print(IQ1s)
            
        # Find Overlap of IQ responses
        this_IQs = IQ1s
        overlap_IQ_total = 0
        pairs = 0
        for i in range(len(this_IQs)):
            for j in range(i+1, len(this_IQs)):
                IQ_i = this_IQs[i]
                IQ_j = this_IQs[j]
                overlap_question = "Below are what should be two lists of names. On a scale of 0-100%, how much overlap is there in the names (ignore minor variations such as middle initials or accents)? Answer with a number between 0 and 100. Also, provide a justification. Output format should be ANS: <ans> JUSTIFICATION: <justification>. \n" + str(IQ_i) + "\n" + str(IQ_j)
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
  

runSAC3(quesSAC3Bank, 0, len(quesSAC3Bank), "gpt-3.5-turbo-0125")
runCoVe(quesCoVEBank, 0, len(quesCoVEBank), "gpt-3.5-turbo-0125")
runREF(quesREFBank, 0, len(quesREFBank), "gpt-3.5-turbo-0125")

# future tasks: implement risk score, implement two more methods (based on provided papers)

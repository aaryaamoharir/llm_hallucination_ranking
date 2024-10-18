import openai
from openai import OpenAI
from array import *
from openai import OpenAIError
import re

client = OpenAI(api_key='API KEY HERE')

quesSAC3Bank = [] 
quesCoVEBank = [
    "Which American-born Sinclair won the Nobel Prize for Literature in 1930?",
    "Where in England was Dame Judi Dench born?",
    "In which decade did Billboard magazine first publish an American hit chart?",
    "From which country did Angola achieve independence in 1975?",
    "Which city does David Soul come from?",
    "Who won Super Bowl XX?",
    "Which was the first European country to abolish capital punishment?",
    "In which country did the widespread use of ISDN begin in 1988?",
    "What is Bruce Willis' real first name?",
    "Which William wrote the novel 'Lord Of The Flies'?"
]
quesREFBank = [
    ["Which American-born Sinclair won the Nobel Prize for Literature in 1930? Just output the full name. Output format should be <full name>", 
     "What other notable works did this author produce? Please, list only the titles formatted as - NAMES:<work title>"], 
    ["Where in England was Dame Judi Dench born? Just output the city name. Output format should be <city>", 
     "What notable landmarks are associated with this city? Please, list only the landmarks formatted as - NAMES:<landmark>"], 
    ["In which decade did Billboard magazine first publish an American hit chart? Just output the decade. Output format should be <decade>", 
     "What was the title of the first chart published? Please, list only the title formatted as - NAMES:<chart title>"], 
    ["From which country did Angola achieve independence in 1975? Just output the country name. Output format should be <country>", 
     "What were the major events leading up to this country's independence? Please, list only the events formatted as - NAMES:<event>"], 
    ["Which city does David Soul come from? Just output the city name. Output format should be <city>", 
     "What famous people are also from this city? Please, list only the names formatted as - NAMES:<celebrity name>"], 
    ["Who won Super Bowl XX? Just output the winning team's name. Output format should be <team>", 
     "What was the final score of Super Bowl XX? Please, list only the score formatted as - SCORE:<score>"], 
    ["Which was the first European country to abolish capital punishment? Just output the country name. Output format should be <country>", 
     "In what year did this country abolish capital punishment? Please, list only the year formatted as - YEAR:<year>"], 
    ["In which country did the widespread use of ISDN begin in 1988? Just output the country name. Output format should be <country>", 
     "What technological advancements followed the widespread use of ISDN in this country? Please, list only the advancements formatted as - NAMES:<advancement>"], 
    ["What is Bruce Willis' real first name? Just output the first name. Output format should be <first name>", 
     "In which movie did Bruce Willis first gain major recognition? Please, list only the movie title formatted as - NAMES:<movie title>"], 
    ["Which William wrote the novel 'Lord Of The Flies'? Just output the full name. Output format should be <full name>", 
     "What other novels did this author write? Please, list only the titles formatted as - NAMES:<novel title>"]
]

# Index for one list element: 0: Self-Consistency question, 1-3: SAC3, 4: System content parameter for GPT
quesSAC3Bank.insert(-1, ["Which American-born Sinclair won the Nobel Prize for Literature in 1930?",
                         "What are the major achievements of Sinclair who won the Nobel Prize for Literature in 1930?",
                         "Can you provide details about Sinclair who won the Nobel Prize for Literature in 1930?",
                         "In which fields did Sinclair, Nobel Prize winner in 1930, contribute significantly?",
                         "You are a virtual literary historian, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["Where in England was Dame Judi Dench born?",
                         "What is the birthplace of Dame Judi Dench?",
                         "Can you tell me about the location where Dame Judi Dench was born?",
                         "In which city in England was Dame Judi Dench born?",
                         "You are a virtual celebrity historian, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["In which decade did Billboard magazine first publish an American hit chart?",
                         "What decade marks the inception of Billboard magazine's American hit chart?",
                         "Can you provide the decade when Billboard first started publishing American hit charts?",
                         "In which decade did Billboard magazine begin its American hit chart publication?",
                         "You are a virtual music industry expert, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["From which country did Angola achieve independence in 1975?",
                         "What country was Angola under before gaining independence in 1975?",
                         "Can you tell me the nation from which Angola gained independence in 1975?",
                         "From which colonial power did Angola gain its independence in 1975?",
                         "You are a virtual historian, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["Which city does David Soul come from?",
                         "What is the city of origin for David Soul?",
                         "Can you provide the name of the city where David Soul was born?",
                         "In which city was David Soul originally from?",
                         "You are a virtual celebrity expert, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["Who won Super Bowl XX?",
                         "What team emerged victorious in Super Bowl XX?",
                         "Can you tell me the winner of Super Bowl XX?",
                         "Which team claimed the title in Super Bowl XX?",
                         "You are a virtual sports historian, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["Which was the first European country to abolish capital punishment?",
                         "What was the first European nation to eliminate capital punishment?",
                         "Can you provide the name of the first European country that abolished capital punishment?",
                         "In which European country was capital punishment first abolished?",
                         "You are a virtual legal historian, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["In which country did the widespread use of ISDN begin in 1988?",
                         "What country first adopted widespread use of ISDN in 1988?",
                         "Can you tell me which country began using ISDN widely in 1988?",
                         "In which nation did ISDN see widespread implementation starting in 1988?",
                         "You are a virtual technology historian, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["What is Bruce Willis' real first name?",
                         "What is the birth name of Bruce Willis?",
                         "Can you provide the first name Bruce Willis was given at birth?",
                         "In which name was Bruce Willis born?",
                         "You are a virtual celebrity expert, generate the most accurate and precise answer based on common knowledge or general facts."
                        ])

quesSAC3Bank.insert(-1, ["Which William wrote the novel 'Lord Of The Flies'?",
                         "Who is the author of the novel 'Lord Of The Flies'?",
                         "Can you tell me the full name of the William who wrote 'Lord Of The Flies'?",
                         "What is the complete name of the William who authored 'Lord Of The Flies'?",
                         "You are a virtual literary expert, generate the most accurate and precise answer based on common knowledge or general facts."
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
            DQ1_question = "Is the answer " + baselineResponse+ " true regarding the question " +  questionList[index][0] + "?Ignore the previous output format command and just output just yes/no depending on if the statement was true or false."
            DQ1 = askQuestion(DQ1_question, systemContent,client)
            if 'yes' in DQ1.lower():
                DQs_yes[0] +=1
                numberOfYes +=1 
                
            
            # DQ2: Provide a reference, Does the reference exist?
            DQ2_question = "Give a article/piece of literature that proves, " + baselineResponse + " , is the answer to "+ questionList[index][0] + " Does the article/piece of literature exist? Ignore the previous output format command and just output just yes/no depending on if the reference exists or doesn't."
            DQ2 = askQuestion(DQ2_question, systemContent, client)
            if 'yes' in DQ2.lower():
                DQs_yes[1] +=1
                numberOfYes +=1 
        
            
            # DQ3: This reference was provided by an LM, Does the reference exist?
            DQ3_question = "A language model generated references related to a general question with the following answer: "+baselineResponsesString+". Does the answer exist? Ignore the previous output format command and just output just yes/no."
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
            clientUpdated = OpenAI(api_key='API KEY HERE')
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
  

#runSAC3(quesSAC3Bank, 0, len(quesSAC3Bank), "gpt-3.5-turbo-0125")
#runCoVe(quesCoVEBank, 0, len(quesCoVEBank), "gpt-3.5-turbo-0125")
runREF(quesREFBank, 0, len(quesREFBank), "gpt-3.5-turbo-0125")

# future tasks: implement risk score, implement two more methods (based on provided papers)

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render
from django.template import loader
from dotenv import load_dotenv
import requests
from django.http import HttpResponse
from django import template
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from openai import OpenAI
from .models import Medication
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Create your views here.

def homeAction(request):
    allMedications = Medication.objects.all()
    context = {"medications": allMedications}

    return render (request,'home.html',context)

def submitMed(request):
    if request.method == 'POST':
        # Get the JSON data from the request
        medication_prompt = request.POST.get('medication')
        prompt = medication_prompt + "Please return the type of medication; dosage amount number and unit they said only;  and the frequency they said converted to hours,only the quantity no units;  in a json formatted response formatted like this { medication type: , dosage: { amount: a number with units, frequnecy: a number converted to hours}} "
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
        temperature=0.7,
        max_tokens=40)
        response_data = response.choices[0].message.content
        
        try:
    # Convert string to JSON
            response_json = json.loads(response_data) 
            medicationName = response_json['medication type']

            dosageAmountInfo = response_json['dosage']['amount'].split(' ')
            dosageAmount = dosageAmountInfo[0]
            dosageUnit = ' '.join(dosageAmountInfo[1:])
            dosageFrequencyHours = response_json['dosage']['frequency']
            
            newMedication = Medication(
                            medicationName = medicationName,
                            dosageAmount = dosageAmount,
                            dosageUnit = dosageUnit,
                            dosageFrequency = dosageFrequencyHours)

            newMedication.save()

        except json.JSONDecodeError:
            # If parsing fails, return the raw text in case of unexpected response format
            return JsonResponse({'error': 'Invalid JSON response', 'message': response_data}, status=500)


        return JsonResponse(response_json)
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)
#please add 50 mg of advil every 2 hours


def medInfo(request):
    if request.method == 'POST':

        medicationName = request.POST['medicationName']
        print(medicationName)
        url = 'https://api.fda.gov/drug/label.json'
        params = {  'search': f'openfda.brand_name:"{medicationName}"',  
                    'limit': 1}  

        response = requests.get(url,params=params)
        if response.status_code == 200:
            data = response.json()
            
            return JsonResponse(data)
            


        
        else:
            return JsonResponse({'error': 'Failed to retrieve data from OpenFDA'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)



def analyzeWarnings(request):
    print("here")
    if request.method == 'POST':
        allMedications = Medication.objects.all()
        if len(allMedications) == 1:
            response_json = {'results':"No warnings"}
            return JsonResponse(response_json)

        prevMedications = allMedications[0:len(allMedications)-1]
        
    
        warnings = request.POST['warnings']
        if not warnings:
            return JsonResponse({'error': 'Warnings not provided'}, status=400)

        prompt = ""
        
        prompt+= "Here are all my previous medications "
        for med in prevMedications:
            prompt+= f'{med.medicationName}, '

        prompt+= "Here is the medication being added: "
        prompt+= allMedications.last().medicationName
        prompt+= "Here are the warnings for taking this medication: "
        prompt+= warnings
        prompt+= """If you see any of my previous medications in the warnings that i gave that shouldn't be taken with this added medication, 
                    for each of these selected previous medication on a new line,  please  say "The added medication (name of it) taken with
                    the selected previous medication (the medication name) is ... then categorize the risk as low, medium or high depending on the warning semantics
                    So the format of ur response should be: {Added medication} taken with {selected previous medication} is {low or medium or high} risk. 
                    If no previous medications are in the warnings, then jsut simply say 'no warnings'. Please structure your response as a multiline string"""

        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
        temperature=0,
        max_tokens=100)
        response_data = response.choices[0].message.content
        response_json = {'results':response_data}
        return JsonResponse(response_json)


    return JsonResponse({'error': 'Invalid request'}, status=400)
        






import pandas as pd
from transformers import BertTokenizer
import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_description(description):
    # Tokenizing the description and adding necessary padding and truncation
    # The tokenizer converts the text into token IDs that BERT understands
    return tokenizer(description, padding='max_length', truncation=True, max_length=128, return_tensors='pt')


class DrugInteractionDataset(Dataset):
    def __init__(self,df,vocab,tokenizer=tokenizer):
        self.df = df
        self.tokenizer = tokenizer
        self.vocab = vocab

    def __len__(self):
        return len(self.df)

    def __getitem__(self,idx):
        #get input
        drug1 = self.df.iloc[idx]['Drug1']
        drug2 = self.df.iloc[idx]['Drug2']
        drug1_description = self.df.iloc[idx]['Drug1 Description']
        drug2_description = self.df.iloc[idx]['Drug2 Description']
        interaction_risk = self.df.iloc[idx]['Interaction Risk (1-10)']
        
        #convert inputs to tensor (compatible for model)
        drug1 = self.vocab.get(drug1,-1)
        drug2 = self.vocab.get(drug2,-1)
        drug1_description_token = tokenize_description(drug1_description)
        drug2_description_token = tokenize_description(drug2_description)
        interaction_risk = int(interaction_risk)
        interaction_risk = torch.tensor(interaction_risk, dtype = torch.long)



        return {
            'drug1':drug1,
            'drug2':drug2,
            'drug1_description':drug1_description_token,
            'drug2_description':drug2_description_token,
            'interaction_risk':interaction_risk

        }


import torch
from torch import nn
import torch.optim as optim

import pandas as pd
import numpy as np
from ml_dataset import DrugInteractionDataset
from ml_model import DrugInteractionModel
from torch.utils.data import DataLoader

def uniqueDrugs(df):
    """
    Given a DataFrame with 'Drug1' and 'Drug2' columns,
    return the number of unique drug names.
    """
    unique_drugs = pd.concat([df["Drug1"], df["Drug2"]]).unique()
    return len(unique_drugs), {drug: idx for idx, drug in enumerate(unique_drugs)}




def main():
    #load in dataset
    file_path = './dataset/drug_interactions.csv'
    df = pd.read_csv(file_path, dtype=str, low_memory=False)
    num_unique_drugs, drug_vocab = uniqueDrugs(df)

    dataset = DrugInteractionDataset(df = df,vocab=drug_vocab)

    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    #load in model
    model = DrugInteractionModel(num_embeddings = num_unique_drugs)
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model.to(device)

    #load in hyperparameters
    criterion = nn.MSELoss()  # Since risk score is continuous
    optimizer = optim.AdamW(model.parameters(), lr=2e-5)
    num_epochs = 10 

    #train model

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in dataloader:
            #extract inputs to feed into model
            drug1 = batch['drug1']
            drug2 = batch['drug2']
            drug1_description = batch['drug1_description']
            drug2_description = batch['drug2_description']


            drug1_input_ids = drug1_description['input_ids'].squeeze(1)
            drug2_input_ids = drug2_description['input_ids'].squeeze(1)
            drug1_attention_mask = drug1_description['attention_mask'].squeeze(1)
            drug2_attention_mask = drug2_description['attention_mask'].squeeze(1)
            risk = batch['interaction_risk'].unsqueeze(1)
            
            #compute loss
            normalized_risk = (risk - 1) / 9.0 
            predicted_risk = model(drug1, drug2, drug1_input_ids, drug2_input_ids,drug1_attention_mask, drug2_attention_mask)            
            loss = criterion(predicted_risk,normalized_risk)
            total_loss += loss.item()

            #optimization
            optimizer.zero_grad()
            loss.backward() 
            optimizer.step() 
        
        avgLoss = total_loss/len(dataloader)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avgLoss:.4f}")









                                                            
    







if __name__ == '__main__':
    main()

#Source of data: https://www.kaggle.com/datasets/devildev89/drug-bank-5110?select=drugbank_clean.csv


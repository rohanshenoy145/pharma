
import torch 
from torch import nn
from transformers import BertTokenizer, BertModel

embedding_dim = 64

class DrugInteractionModel(nn.Module):
    def __init__(self,num_embeddings,embedding_dim = 64):
        super(DrugInteractionModel, self).__init__()
        #bagging embedding for drug names
        self.name_embedder = nn.Embedding(num_embeddings,embedding_dim)

        #Bert model for embedding drug descriptions
        self.bert_embedder = BertModel.from_pretrained('bert-base-uncased')

        #Feedforward neural network
        self.fc1 = nn.Linear(embedding_dim*2 + 768*2,256)
        self.relu1 = nn.ReLU()

        self.fc2 = nn.Linear(256,128)
        self.relu2 = nn.ReLU()

        self.fc3 = nn.Linear(128,64)
        self.relu3 = nn.ReLU()

        self.fc4 = nn.Linear(64,1)


    def forward(self, drug1, drug2, drug1_description, drug2_description, 
                drug1_desc_attention_mask, drug2_desc_attention_mask):
        #Drug name embeddings
        drug1_emb = self.name_embedder(drug1)
        drug2_emb = self.name_embedder(drug2)

        #Drug description embeddings
        drug1_desc_emb = self.bert_embedder(input_ids=drug1_description,attention_mask =drug1_desc_attention_mask).pooler_output
        drug2_desc_emb = self.bert_embedder(input_ids=drug2_description,attention_mask =drug2_desc_attention_mask).pooler_output

        #concantenated input 
        conc = torch.cat((drug1_emb,drug2_emb,drug1_desc_emb,drug2_desc_emb),dim=1)

        #Feed into NN

        x = self.fc1(conc)
        x = self.relu1(x)
       
        x = self.fc2(x)
        x = self.relu2(x)

        x = self.fc3(x)
        x = self.relu3(x)

        risk_score = self.fc4(x)

        return risk_score







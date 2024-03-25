import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
import torch

df = pd.read_csv('chatbox/model/data.csv', header=None, names=['metin'])

df['metin'] = df['metin'].str.replace(r'^\d+\s*', '', regex=True)
df['metin'] = df['metin'].str.lower()

# Etiketleme: + ile başlayanları "soru", - ile başlayanları "cevap" olarak etiketle
df['etiket'] = df['metin'].apply(lambda x: 'soru' if x.startswith('+') else 'cevap')

X = df['metin']  # Metin verileri
Y = df['etiket']  # Etiketler (soru veya cevap)

model_name = "EleutherAI/gpt-neo-1.3B"  # İlgili modelin adını belirtin
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.add_special_tokens({'pad_token': '[PAD]'})

tokenized_data = []

for text in df['metin']:
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    tokenized_data.append(tokens)

# Modeli yükle (Önceden eğitilmiş veya eğitilmiş modeli yükleyin)
chatbot_model = AutoModelForCausalLM.from_pretrained(model_name)

# Özelleştirdiğiniz modelin adını ve yolu belirtin
model_name = "chatbot_model.pth"

# Modeli kaydet
chatbot_model.save_pretrained(model_name)


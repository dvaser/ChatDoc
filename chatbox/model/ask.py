from transformers import AutoModelForCausalLM, AutoTokenizer

# Modeli yükle
model_name = "chatbot_model.pth"
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")  # Kullandığınız tokenizer'ı yükleyin

# Dolgu belirteci eklemek için aşağıdaki satırı kullanabilirsiniz
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

loaded_model = AutoModelForCausalLM.from_pretrained(model_name)

def ask(sentence):
    # Kullanıcının girişini modelle verin
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)

    # Modelden tahmin yapın
    response = loaded_model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=150)

    # Modelin ürettiği yanıtı alın ve gösterin
    bot_response = tokenizer.decode(response[0], skip_special_tokens=True)

    return bot_response


user_input = "Merhaba, nasılsınız?"
response = ask(user_input)
print("Chatbot Response:", response)
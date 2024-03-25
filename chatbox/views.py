from django.shortcuts import render, redirect
from user.models import Message
from user.models import Document
from user.forms import DocumentForm
from django.contrib import messages
from .model.ask import ask
from user.forms import ImageUploadForm
from django.contrib.auth import get_user

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def chat(request):
    user = get_user(request)  # Get the logged-in user object

    doc = None
    if request.method == 'POST':

        try:
            if user:
                name = request.POST.get('name')
                surname = request.POST.get('surname')
                email = request.POST.get('email')
                
                # Document Type Files
                form = DocumentForm(request.POST, request.FILES)
                if form.is_valid():
                    doc_file = form.save(commit=False)
                    doc_file.user_id = user.id
                    file = doc_file.file
                    file_extension = file.name.split('.')[-1]
                    file_name = file.name[0:-(len(file_extension)+1)] 
                    if file_extension in ['pdf', 'doc', 'txt', 'docx']:
                        doc_file.title = file_name
                        doc_file.type = file_extension
                        doc_file.save()
                        user.documents.add(doc_file)
                        messages.success(request, 'Belge yüklendi.')
                    else:
                        messages.error(request, 'Geçersiz dosya uzantısı. Sadece PDF, DOC, TXT ve DOCX dosyaları yükleyebilirsiniz.')
                else:
                    messages.error(request, 'Form geçersiz. Lütfen tüm gerekli alanları doldurun.')

                # Document
                document_id = request.POST.get('document_id')
                if document_id != '' or None:
                    try:
                        doc = Document.objects.get(id=document_id)
                    except Document.DoesNotExist:
                        doc = None

                # Message
                sender = f"{user.first_name} {user.last_name}" 
                message = request.POST.get('message') 
                isChatBox = False
                if doc is not None and message:
                    messageSave = Message.objects.create(sender=sender, message=message, isChatBox=isChatBox, document_id=doc.id)
                    doc.messages.add(messageSave)
                    
                    sender = 'CHATDOC'
                    try:
                        gptMessage = ask(message)
                    except:
                        gptMessage = "Anlamadım, tekrar söyler misin?"
                    isChatBox = True

                    if gptMessage:
                        gptMessageSave = Message.objects.create(sender=sender, message=gptMessage, isChatBox=isChatBox, document_id=doc.id)
                        doc.messages.add(gptMessageSave)

                    message = False
                    gptMessage = False

                # Info Update
                try:
                    name = request.POST.get('name')
                    surname = request.POST.get('surname')
                    email = request.POST.get('email')

                    if ((name is not None) or (surname is not None) or (email is not None)):
                        # Kullanıcının bilgilerini güncelle
                        user.first_name = name
                        user.last_name = surname
                        user.email = email
                        user.save()
                except:
                    print("hata")

                # Image Files
                image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
                if image_form.is_valid():
                    image_form.save()  # Save the image

                    # Redirect to the desired page after image upload
                    return render(request, 'chatbox/chat.html', {'user':user, "activeDoc":doc})
        
        except Exception as ex:
            print(ex)

    return render(request, 'chatbox/chat.html', {'user':user, "activeDoc":doc})

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Transaction
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user:
            pass
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.input_message = data.get('message')
        self.chat_id = int(data.get('chat_id'))
        model_selected = data.get('model_selected')
        type = data.get('type')
        Document = data.get('documents')

        from .LLM.llm import LLM_reply
        from .LLM import IfPdf
        from .LLM.Summarization import summarizer, Chunking,text_chunks
        
        if Document:
            
            if int(type) == 1:
                context = await IfPdf.context(Document,self.input_message)
                self.result = await LLM_reply(self.input_message,context= context ,ModelName= model_selected)
                await self.send(text_data=json.dumps({'result': self.result, 'type': 'qa', 'end': 1}))
            else:
                chunks = await Chunking(Document)
                self.result = []
                count = len(chunks)
                for i, chunk in enumerate(chunks, start=1):
                    progress = (i / count) * 100
                    progress = round(progress, 2)

                    chunk_result = await summarizer(chunk,ModelName = model_selected)
                    self.result.append(chunk_result)
                    await self.send(text_data=json.dumps({'result': chunk_result, 'type': 'summarization', 'progress': progress, 'end': 0}))
                self.result = " ".join(self.result)
                await self.send(text_data=json.dumps({'result': "", 'type': 'summarization', 'end': 1}))
            await self.Transaction()
        else:
            if int(type) == 1:
                print("consumer")
                self.result = await LLM_reply(self.input_message,ModelName= model_selected)
                await self.send(text_data=json.dumps({'result': self.result, 'type': 'qa', 'end': 1}))
            else:
                chunks = await text_chunks(self.input_message)
                self.result = []
                count = len(chunks)
                for i, chunk in enumerate(chunks, start=1):
                    progress = (i / count) * 100
                    progress = round(progress, 2)
                    chunk_result = await summarizer(chunk,ModelName = model_selected)
                    self.result.append(chunk_result)
                    await self.send(text_data=json.dumps({'result': chunk_result, 'type': 'summarization', 'progress': progress, 'end': 0}))
                self.result = "<br>".join(self.result)
                await self.send(text_data=json.dumps({'result': "", 'type': 'summarization', 'end': 1}))
            await self.Transaction()

    @database_sync_to_async
    def Transaction(self):
        chat = Chat.objects.get(id=self.chat_id)
        if not chat.title:
            chat.title = self.input_message[:15]
        chat.save()
        return Transaction.objects.create(chat_id=self.chat_id, input_prompt=self.input_message, output=self.result)

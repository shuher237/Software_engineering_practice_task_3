from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from transformers import pipeline
from pydantic import BaseModel


class Item(BaseModel):
    text: str


app = FastAPI()
templates = Jinja2Templates(directory='templates/')
classifier = pipeline("sentiment-analysis")
translator_ru_en = pipeline("translation_ru_to_en",
                            model="Helsinki-NLP/opus-mt-ru-en")
translator_en_ru = pipeline("translation_en_to_ru",
                            model="Helsinki-NLP/opus-mt-en-ru")


@app.get('/')
def root(request: Request):
    result = 'Type a text.'
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post('/')
def form_post(request: Request, text: str = Form(...), option: str = Form(...)):
    if text == "":
        result = 'Type a text!'
        return templates.TemplateResponse('form.html', context={'request': request, 'result': result})
    else:
        if option == "0":
            result = classifier(text)[0]
            return templates.TemplateResponse('form.html', context={'request': request, 'result': result,
                                                                    'text': text, 'option_id': 'option1'})
        elif option == "1":
            result = translator_ru_en(text)[0]
            return templates.TemplateResponse('form.html', context={'request': request, 'result': result,
                                                                    'text': text, 'option_id': 'option2'})
        else:
            result = translator_en_ru(text)[0]
            return templates.TemplateResponse('form.html', context={'request': request, 'result': result,
                                                                    'text': text, 'option_id': 'option3'})


@app.post("/predict")
def predict(item: Item):
    return classifier(item.text)[0]


@app.post('/translation_ru_en')
def form_post(item: Item):
    return translator_ru_en(item.text)[0]


@app.post('/translation_en_ru')
def form_post(item: Item):
    return translator_en_ru(item.text)[0]

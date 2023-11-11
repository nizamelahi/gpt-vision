import openai
import base64
import fitz  #use  pip install PyMuPDF

openai.api_key = ""
pdf_name="bartender-resume-example.pdf"

def load_pdf_to_base64img(pdf_path: str, image_path: str):
    pdf_document = fitz.open(pdf_path)
    first_page = pdf_document.load_page(0)
    pixmap = first_page.get_pixmap()
    pixmap.save(image_path)
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyse_image(image,question,is_url=True):
    if is_url:
        content = {"type":"image_url","image_url":image}
    else:
        content = {"type":"image_url",
                   "image_url":{
                            "url": f"data:image/png;base64,{image}",
                            "detail": "low"
                        }}
    
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role":"user",
                "content":[
                    {"type":"text","text":question},
                    content,
                ],
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message['content']

if __name__ == "__main__":
    loaded_img=load_pdf_to_base64img(pdf_name,"pdf_pg1.png")
    question="describe this image"
    response=analyse_image(loaded_img,question,is_url=False)
    print(response)

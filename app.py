from flask import * 
from openai import OpenAI


# Initialising flask
app = Flask(__name__) 


client = OpenAI(
    api_key="your own paid key"
)


# Defining the route for the main() funtion
@app.route("/", methods=["POST", "GET"]) 
def main():
    content_local = ""
    type_local = ""
    emotion_local = ""
    title_local = ""
    if (request.method == 'POST'):
        type_local = request.form.get("type")
        emotion_local = request.form.get("emotion")
        title_local = request.form["title"]

        prompt = create_prompt(type_local, emotion_local, title_local)

        res = get_answer(prompt)

        if res:
            content_local = res.choices[0].message.content
        
    return render_template("home.html", content = content_local, title = title_local, type = type_local, emotion = emotion_local) #rendering our home.html contained within /templates


def create_prompt(type, emotion, title):

    if type == "answer":
        type = "question-to-answer"
    elif type == "confirm_email":
        type = "confirmation email"
    elif type == "cancel_email":
        type = "cancellation email"
    elif type == "instagram":
        type = "post for instagram"
    elif type == "facebook":
        type = "post for facebook"
    elif type == "tik_tok":
        type = "post for tik tok"
    elif type == "amazon_description":
        type = "amazon product description"
    elif type == "amazon_title":
        type = "amazon product title"
    elif type == "ecommerce":
        type = "ecommerce product description"
    else:
        type = type

    prompt = f'''Write text. The text must be written in {type} format.
        The text must be written with {emotion}.
        The title of text must be "{title}" and don't change or add anything and write with bigger font than content!
        We want this content to be high searchable.
        Write the text naturally and avoid comments or words(for example: SEO-Optimized Content) that are not related to the topic.
        Don't involve unnecessary symbols such as ---, ###, **, and so on.
        Add line breaks, dashes and indentations to make the text easy to read and understand.
        Must consider to accurately distinguish between title, content, paragraphes and so on.
        Write the new sentences on the new rows.'''

    return prompt


def get_answer(prompt):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = [
            {"role": "system", "content": 'You write text based on my prompt.'
            },
            {"role": "user", "content": prompt},
        ]
    )


if __name__ == "__main__": 
    # Running flask
    app.run(debug = True, port = 4949) 
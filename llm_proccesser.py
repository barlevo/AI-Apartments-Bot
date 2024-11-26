import openai
import os
from openai import OpenAI



def summarize_apartment_post(raw_text):
    """
    Use GPT-4 to summarize an apartment post into structured data.

    Args:
        raw_text (str): The raw text of the post.

    Returns:
        dict: A structured summary of the apartment details.
    """

    client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)
    prompt = f"""
    Extract apartment details from the following raw text. Return the information in English in the following structured format:
    **Number of rooms**:
    **Address**: (Street and number. only if no street name Extract other indicator of location (place near by, neighborhood, etc))
    **Price**: (in ILS)
    **Specifications**: (livingroom, balcony, solar heater, etc.)
    **Contact information**:
    **Entry date**: (if available)

    **phrase** - means that the phrase will be outputted in bold 
    
    Post:
    {raw_text}
    """

    print(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant skilled in summarizing apartment listings."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )

    structured_summary = response.choices[0].message.content
    print(structured_summary)
    return structured_summary

# Example usage
# if __name__ == "__main__":



#     raw_post = """
#     מתפנה דירת 3 חדרי שינה ברב הרצוג 4 (על הרב ברלין/ עזה).
#     צמוד לרחוב עזה, עמק המצלבה ותחנות אוטובוס למרכז העיר ולקמפוסים השונים בעיר.
#     בדירה 3 חדרי שינה גדולים, מרפסת חיצונית, מרפסת סגורה, סלון קטן ודוד שמש.
#     מציעים למכירה מכונת כביסה וטלוויזיה שנקנו כשנכנסו לדירה וחלק מהציוד בחדרים.
#     שכ"ד 1900 לשותף, ועד 50 (לכל הדירה). כניסה ב01/09.
#     מראים בשלישי בערב בתיאום מראש. מוזמנים לפנות בפרטי.
#     """
#     summary = summarize_apartment_post(raw_post)
#     print("Structured Summary:")
#     print(summary)

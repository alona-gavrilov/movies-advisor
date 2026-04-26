import json
import psycopg2
import os

model = None
def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("/opt/model")
    return model


def get_embedding(text):
    if not text:
        return None
    else:
        model = get_model()
        return model.encode(text).tolist()

def get_command(i1):

    query = f"""
    SELECT 
        title,
        release_date,
        genres,
        overview,
        keywords,
        1-(embedding_combined <-> %s::vector) as similarity 
    FROM movies_kaggle_db5000
    ORDER BY similarity DESC
    LIMIT 5;
    """
    return query, (i1,)
    

def handler(event, context):
    
    # Parse JSON body safely
    body = json.loads(event.get("body", "{}"))
    
    # embed the query:
    pingMode = body.get("ping", None)
    genre = body.get("genre", None)
    overview = body.get("overview", None)
    keywords = body.get("keywords", None)
    
    if pingMode:
        conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=5432
        )
        cur = conn.cursor()
        cur.execute("SELECT title FROM movies_kaggle_db5000 LIMIT 1")
        cur.close()
        conn.close()
        return {'statusCode': 200, 'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },'body': json.dumps({"pingMode":"successful"})}     

    combined_input = " ".join(part for part in [genre, overview, keywords] if part)
    if not combined_input:
         return {'statusCode': 200, 'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },'body': json.dumps({})}

    combined_input_embedded = get_embedding(combined_input)     
    execute_command, params = get_command(combined_input_embedded)

    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=5432
    )
    cur = conn.cursor()
    cur.execute(execute_command, params)
    rows = cur.fetchall()
    formatted_rows = []
    for row in rows:
        formatted_rows.append({"title":row[0],
                                "release_date":row[1],
                                "genre":row[2],
                                "overview":row[3],
                                "keywords":row[4],
                                "sim_score":round(row[5],3)})             
    cur.close()
    conn.close()
    return {'statusCode': 200, 'headers': {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Methods": "OPTIONS,POST"
    },'body': json.dumps(formatted_rows)}




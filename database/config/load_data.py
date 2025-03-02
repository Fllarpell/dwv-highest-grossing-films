import json

from ..config import Session, create_tables
from ..models.models import Film

def load_data_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_data_to_db(data):
    session = Session()
    
    for film in data:
        if 'title' in film and 'year' in film and 'directors' in film and 'box_office' in film and 'countries' in film and 'image_urls' in film:
            new_film = Film(
                title=film["title"],
                release_year=film["year"],
                director=', '.join(film["directors"]),
                box_office=film['box_office'],
                country=', '.join(film["countries"]),
                image_url= film['image_urls'][0]
            )
            session.add(new_film)

    session.commit()
    session.close()

def save_film_to_db(film):
    required_keys = ['title', 'year', 'directors', 'box_office', 'countries', 'image_urls']
    if not all(key in film for key in required_keys):
        return

    title_formatted = film["title"].replace(" ", "_")
    ext = film["image_urls"][0].split(".")[-1]
    image_path = film["image_urls"][0]

    session = Session()
    try:
        new_film = Film(
            title=film["title"],
            release_year=film["year"],
            director=', '.join(film["directors"]),
            box_office=film["box_office"],
            country=', '.join(film["countries"]),
            image_url=image_path
        )
        session.add(new_film)
        session.commit()

    except Exception as e:
        session.rollback()
        print("error:", e)
    finally:
        session.close()
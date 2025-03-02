import json
from sqlalchemy import select

from ..config import engine, Session
from ..models.models import Film


def get_data_from_db():
    session = Session()
    
    query = select(Film)
    results = session.execute(query)
    films = results.scalars().all()
    
    data = []
    for film in films:
        data.append({
            'title': film.title,
            'box_office': film.box_office
        })
    
    session.close()
    return data

def export_to_json(filename):
    session = Session()
    query = select(Film)
    results = session.execute(query)
    films = results.scalars().all()
    session.close()

    films_data = [
        {
            'title': film.title,
            'release_year': film.release_year,
            'director': film.director,
            'box_office': film.box_office,
            'country': film.country,
            'image_url': film.image_url
        }
        for film in films
    ]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(films_data, f, ensure_ascii=False, indent=4)


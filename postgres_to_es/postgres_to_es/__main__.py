import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing

from etl.etl import etl
from etl.extractors.filmwork.filmwork_extractor import FilmworkExtractor
from etl.extractors.filmwork.filmwork_genre_extractor import FilmworkGenreExtractor
from etl.extractors.filmwork.filmwork_person_extractor import FilmworkPersonExtractor
from etl.extractors.genre.genre_extractor import GenreExtractor
from etl.extractors.person.person_extractor import PersonExtractor
from etl.loaders.filmwork.filmwork_loader import FilmworkLoader
from etl.loaders.genre.genre_loader import GenreLoader
from etl.loaders.person.person_loader import PersonLoader
from etl.transformers.filmwork.filmwork_transformer import FilmworkTransformer
from etl.transformers.genre.genre_transformer import GenreTransformer
from etl.transformers.person.person_transformer import PersonTransformer
from helpers.logger import LoggerFactory
from settings import Settings
from storage_clients.elasticsearch_client import ElasticsearchClient

logger = LoggerFactory().get_logger()


def main():
    settings = Settings()

    with closing(ElasticsearchClient(settings.elasticsearch_dsn)) as elk_conn:
        for (index, index_file) in (
            (settings.elasticsearch_indexes.movies, settings.elasticsearch_indexes.movies_file),
            (settings.elasticsearch_indexes.genres, settings.elasticsearch_indexes.genres_file),
            (settings.elasticsearch_indexes.persons, settings.elasticsearch_indexes.persons_file),
        ):
            if not elk_conn.index_exists(index):
                logger.warn("ELK index `%s` is missing", index)
                with open(index_file) as f:
                    data = json.load(f)
                    elk_conn.index_create(index, body=data)

                logger.warn("ELK index `%s` created", index)

    with ThreadPoolExecutor() as pool:
        future_list = [
            pool.submit(
                etl,
                settings=settings,
                elk_index=settings.elasticsearch_indexes.movies,
                extractor_type=FilmworkGenreExtractor,
                transformer_type=FilmworkTransformer,
                loader_type=FilmworkLoader,
                state_key="genre_to_film_work",
            ),
            pool.submit(
                etl,
                settings=settings,
                elk_index=settings.elasticsearch_indexes.movies,
                extractor_type=FilmworkPersonExtractor,
                transformer_type=FilmworkTransformer,
                loader_type=FilmworkLoader,
                state_key="person_to_film_work",
            ),
            pool.submit(
                etl,
                settings=settings,
                elk_index=settings.elasticsearch_indexes.movies,
                extractor_type=FilmworkExtractor,
                transformer_type=FilmworkTransformer,
                loader_type=FilmworkLoader,
                state_key="film_work",
            ),
            pool.submit(
                etl,
                settings=settings,
                elk_index=settings.elasticsearch_indexes.genres,
                extractor_type=GenreExtractor,
                transformer_type=GenreTransformer,
                loader_type=GenreLoader,
                state_key="genre",
            ),
            pool.submit(
                etl,
                settings=settings,
                elk_index=settings.elasticsearch_indexes.persons,
                extractor_type=PersonExtractor,
                transformer_type=PersonTransformer,
                loader_type=PersonLoader,
                state_key="person",
            ),
        ]
        logger.critical("ETL started")

        # noinspection PyBroadException
        try:
            for future in future_list:
                future.result()
        except Exception:
            logger.exception("Some task failed")


main()

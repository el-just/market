import json
from sqlalchemy.sql import select, func, literal_column, text

import db
import utils


class Market:
    request = None
    conn = None

    def __init__(self, request=None, conn=None):
        self.request = request
        self.conn = conn


    async def list(self, category=None, paused=False,
                   search_text=None):
        category = int(category) if category is not None else 0
        categories = [
            None,
            ["'фрукты'", "'ягоды'"],
            ["'овощи'"],
            ["'зелень'"],
            ["'грибы'"],
            ["'орехи'", "'крупы'"],
        ]
        labels_query = "labels.name in (%s)"%','.join(categories[category]) \
                if categories[category] is not None and search_text is None \
                else 'true'
        labels_sort_query = """
                , (select ARRAY (
                        select unnest(array_agg(labels.name))
                        intersect 
                        select unnest(ARRAY[%s])
                    )
                ) as intersection_count
                """%(','.join(categories[category])) \
                        if search_text is not None else ''
        labels_sort_field = """
                , (
                    select
                        coalesce(
                            array_length(max(prdcts.intersection_count), 1), 0)
                    from links primary_links
                        left join prdcts on
                            prdcts.entity_id = primary_links.subject_id
                    where
                        primary_links.object_id = parent_offers.entity_id
                ) as intersection_count
                """ if search_text is not None else ''

        labels_sort = " intersection_count desc, " if search_text is not None \
                else ''

        search_query = "and offers.name ilike ('%' || :search_text || '%')" \
                .format(search_text=search_text) if search_text is not None \
                        else ''
        search_query = search_query + ' and entities.paused is not True' \
                if paused is False else search_query

        search_params = {"search_text":search_text} if search_text is not None \
                        else {}

        query = '''
            with label_links as (
                select
                    links.*
                from links
                    left join
                        labels on labels.entity_id = links.subject_id
                where %s
            ),

            prdcts as (
                select
                    products.*
                    , entities.name as entity_name
                    , manufacturers.name as manufacturer_name
                    , array_agg(ARRAY[labels.name, labels.id::varchar]) as labels
                    %s
                from label_links
                    left join products
                        on products.entity_id = label_links.object_id
                    left join manufacturers
                        on products.manufacturer_id = manufacturers.id
                    left join labels 
                        on labels.entity_id = label_links.subject_id
                    left join entities 
                        on products.entity_id = entities.id
                group by
                    products.id, entities.name, manufacturers.name
            ),

            parent_offers as (
                select
                    offers.*
                    , entities.name as entity_name
                    , entities.declensions as declensions
                    , entities.paused as entity_paused
                from offers
                    left join links
                        on links.object_id = offers.entity_id
                    left join prdcts
                        on links.subject_id = prdcts.entity_id
                    left join entities
                        on entities.id = offers.entity_id
                where
                    prdcts.id in (select prdcts.id from prdcts)
                    %s
                group by
                    offers.id
                    , entities.name
                    , entities.declensions
                    , entities.paused
            )

            select
                parent_offers.*
                , (
                    select
                        json_agg(x)
                    from (
                        select 
                            prdcts.*
                        from links primary_links
                            left join prdcts on
                                prdcts.entity_id = primary_links.subject_id
                        where
                            primary_links.object_id = parent_offers.entity_id
                    ) x
                ) as products
                ,(
                    select
                        json_agg(y)
                    from (
                        select
                            offers.*
                            , entities.name as entity_name
                            , entities.declensions as declensions
                        from
                            offers
                            left join entities on
                                entities.id = offers.entity_id
                        where
                            offers.parent_id = parent_offers.id
                        group by offers.id, entities.name, entities.declensions
                        order by offers.weight nulls last
                    ) y
                ) as formats
                %s
            from parent_offers
            order by %s parent_offers.name
        '''%(labels_query, labels_sort_query, search_query,
                labels_sort_field, labels_sort)

        data = await self.conn.execute(text(query), search_params)
        offers = await data.fetchall()

        return [ {
            "offer": {
                "id": row["id"],
                "entity_id": row["entity_id"],
                "name": row["name"],
                },
            "entity": {
                "id": row["entity_id"],
                "name": row["entity_name"],
                "paused": row["entity_paused"],
                "declensions": row["declensions"],
                },
            "products": [{
                "product": {
                    "id": product["id"],
                    "entity_id": product["entity_id"],
                    "name": product["name"],
                    "description": product["description"],
                    "img": product['img'],
                    "manufacturer_id": product['manufacturer_id'],
                },
                "entity": {
                        "id": product["entity_id"],
                        "name": product["entity_name"],
                },
                "manufacturer": {
                    "id": product["manufacturer_id"],
                    "name": product["manufacturer_name"],
                },
                "labels": [{
                    "label":{
                        "id": int(label[1]),
                        "name": label[0],
                        }
                    }for label in product["labels"]],
                } for product in row["products"]],
            "formats": [{
                    "offer": {
                        "id": format["id"],
                        "entity_id": format["entity_id"],
                        "name": format["name"],
                        "is_node": format["is_node"],
                        "parent_id": format["parent_id"],
                        "weight": format["weight"],
                        "price": format["price"],
                        "count_type": format["count_type"],
                    },
                    "entity": {
                        "id": format["entity_id"],
                        "name": format["entity_name"],
                        "declensions": format["declensions"],
                    },
                } for format in row["formats"]],
            } for row in offers]

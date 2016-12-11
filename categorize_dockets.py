from collections import defaultdict
import lib.mongo
import logging

def categorize_dockets():
    """Gathers the categories of all dockets in the database; updates the
    categories collection accordingly."""

    num_dockets = defaultdict(lambda: 0)  # {category_id: count}
    num_open_for_comment = defaultdict(lambda: 0)  # {category_id: count}

    for docket in lib.mongo.dockets.find():
        docket_id = docket.get('docketId', '')
        category_id = docket.get('categoryId', '')
        open_for_comment = docket.get('openForComment', None)

        num_dockets[category_id] += 1
        if open_for_comment:
            num_open_for_comment[category_id] += 1

    categories = []
    for category_id in num_dockets.keys():
        category = {
            'categoryId': category_id,
            'numDockets': num_dockets[category_id],
            'numOpenForComment': num_open_for_comment[category_id]
        }
        logging.info(repr(category))
        categories.append(category)

    logging.info('updating %d categories...' % len(categories))
    lib.mongo.rewrite_categories(categories)
    logging.info('done!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    categorize_dockets()

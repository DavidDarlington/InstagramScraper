from operator import itemgetter


def search_locations(query, observer, location_repo):

    def success(places):
        if places is None or len(places) == 0:
            error = ValueError("No locations found for query '{0}'".format(query))
            observer.no_locations_found(error)
            return

        sorted_places = sorted(places, key=itemgetter('position'))

        observer.search_locations_success(sorted_places)

    def failure(exception):
        observer.search_locations_error(exception)

    location_repo.search(query=query,
                         success=success,
                         failure=failure)


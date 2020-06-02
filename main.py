## Perform the imports
from __future__ import print_function
import swagger_client
import swagger_client.configuration as config
from swagger_client.rest import ApiException
from pprint import pprint

## Configure API key authorization: api_key
configuration = config.Configuration()
configuration.api_key['key'] = '3fccaaf9-1e62-4a69-ae2c-7c4ec49ec955'


## create an instance of the API class
api_instance = swagger_client.GeocodingApi(swagger_client.ApiClient(configuration))
q = 'q_example' # str | If you do forward geocoding, this is `required` and is a textual description of the address you are looking for. (optional)
locale = 'locale_example' # str | Display the search results for the specified locale. Currently French (fr), English (en), German (de) and Italian (it) are supported. If the locale wasn't found the default (en) is used. (optional)
limit = 56 # int | Specify the maximum number of results to return (optional)
reverse = True  # bool | It is `required` to be `true` if you want to do a reverse geocoding request. If it is `true`, `point` must be defined as well, and `q` must not be used. (optional)
debug = True # bool | If `true`, the output will be formatted. (optional)
point = 'point_example' # str | _Forward geocoding_: The location bias in the format 'latitude,longitude' e.g. point=45.93272,11.58803. _Reverse geocoding_: The location to find amenities, cities. (optional)
provider = 'provider_example' # str | The provider parameter is currently under development and can fall back to `default` at any time. The intend is to provide alternatives to our default geocoder. Each provider has its own strenghts and might fit better for certain scenarios, so it's worth to compare the different providers. To try it append the `provider`parameter to the URL like `&provider=nominatim`, the result structure should be identical in all cases - if not, please report this back to us. Keep in mind that some providers do not support certain parameters or don't return some fields, for example `osm_id` and `osm_type` are not supported by every geocoding provider. If you would like to use additional parameters of one of the providers, but it's not available for the GraphHopper Geocoding, yet? Please contact us.  The credit costs can be different for all providers - see [here](https://support.graphhopper.com/support/solutions/articles/44000718211-what-is-one-credit-) for more information about it.  Currently, only the default provider and gisgraphy supports autocompletion of partial search strings.  All providers support normal \"forward\" geocoding and reverse geocoding via `reverse=true`.  #### Default (`provider=default`)  This provider returns results of our internal geocoding engine, as described above.  #### Nominatim (`provider=nominatim`)  The GraphHopper Directions API uses a commercially hosted Nominatim geocoder. You can try this provider [here](https://nominatim.openstreetmap.org/). The provider does **not** fall under the [restrictions](https://operations.osmfoundation.org/policies/nominatim/) of the Nominatim instance hosted by OpenStreetMap.  In addition to the above documented parameters Nominatim allows to use the following parameters, which can be used as documented [here](https://wiki.openstreetmap.org/wiki/Nominatim#Parameters):  * viewbox * viewboxlbrt * bounded  #### OpenCage Data (`provider=opencagedata`)  This provider returns results from the OpenCageData geocoder which you can try [here](https://geocoder.opencagedata.com/demo).  In addition to the above documented parameters OpenCage Data allows to use the following parameters, which can be used as documented [here](https://geocoder.opencagedata.com/api#forward-opt):  * countrycode * bounds  #### Gisgraphy (`provider=gisgraphy`)  This provider returns results from the Gisgraphy geocoder which you can try [here](https://services.gisgraphy.com/static/leaflet/index.html).  **Limitations:** Gisgraphy does not return tags from OSM nor an extent. The locale parameter is currently not supported for Gisgraphy.  Gisgraphy has a special autocomplete API, which you can use by adding `autocomplete=true` (does not work with `reverse=true`). The autocomplete API is optimized on predicting text input, but returns less information.  In addition to the above documented parameters Gisgraphy allows to use the following parameters, which can be used as documented [here](http://www.gisgraphy.com/documentation/user-guide.php):  * radius * country  (optional)

try:
    # Execute a geocoding request
    api_response = api_instance.get_geocode(q=q, locale=locale, limit=limit, reverse=reverse, debug=debug, point=point, provider=provider)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeocodingApi->get_geocode: %s\n" % e)
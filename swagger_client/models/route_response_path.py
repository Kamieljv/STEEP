# coding: utf-8

"""
    GraphHopper Directions API

     With the [GraphHopper Directions API](https://www.graphhopper.com/products/) you can integrate A-to-B route planning, turn-by-turn navigation, route optimization, isochrone calculations and other tools in your application.  The GraphHopper Directions API consists of the following RESTful web services:   * [Routing](#tag/Routing-API),  * [Route Optimization](#tag/Route-Optimization-API),  * [Isochrone](#tag/Isochrone-API),  * [Map Matching](#tag/Map-Matching-API),  * [Matrix](#tag/Matrix-API) and  * [Geocoding](#tag/Geocoding-API).  # Explore our APIs  To play and see the Route Optimization in action try our [route editor](https://graphhopper.com/blog/2015/07/21/graphhoppers-new-route-optimization-editor/)  which available in the [dashboard](https://graphhopper.com/dashboard/). See how the Routing and Geocoding is integrated in  our route planner website [GraphHopper Maps](https://graphhopper.com/maps) ([sources](https://github.com/graphhopper/graphhopper/tree/0.12/web/src/main/resources/assets)).  And [see below](#section/Explore-our-APIs/Insomnia) for a collection of requests for [Insomnia](https://insomnia.rest/) and [Postman](https://www.getpostman.com/). The request file contains all example requests from this documentation.  ## Get started  1. To use the GraphHopper Directions API you sign up [here](https://graphhopper.com/dashboard/#/register) and create an API key. 2. Read the documentation of the desired API part below. 3. Start using the GraphHopper Directions API. [Our API clients](#section/Explore-our-APIs/API-Clients) can speed up the integration.  To use the GraphHopper Directions API commercially, you can buy paid package [in the dashboard](https://graphhopper.com/dashboard/#/pricing).  ## Contact Us  If you have problems or questions see the following information:   * [FAQ](https://graphhopper.com/api/1/docs/FAQ/)  * [Public forum](https://discuss.graphhopper.com/c/directions-api)       * [Contact us](https://www.graphhopper.com/contact-form/)  To get informed about the newest features and development follow us at [twitter](https://twitter.com/graphhopper/) or [our blog](https://graphhopper.com/blog/).  Furthermore you can watch [this git repository](https://github.com/graphhopper/directions-api-doc) of this documentation, sign up at our [dashboard](https://graphhopper.com/dashboard/) to get the newsletter or sign up at [our forum](https://discuss.graphhopper.com/c/directions-api). Pick the channel you like most.  ## API Client Libraries  To speed up development and make coding easier, we offer the following client libraries:   * [JavaScript client](https://github.com/graphhopper/directions-api-js-client) - try the [live examples](https://graphhopper.com/api/1/examples/)  * [Others](https://github.com/graphhopper/directions-api-clients) like C#, Ruby, PHP, Python, ... automatically created for the Route Optimization  ### Bandwidth reduction  If you create your own client, make sure it supports http/2 and gzipped responses for best speed.  If you use the Matrix or Route Optimization and want to solve large problems, we recommend you to reduce bandwidth by [compressing your POST request](https://gist.github.com/karussell/82851e303ea7b3459b2dea01f18949f4) and specifying the header as follows: `Content-Encoding: gzip`.  ## Insomnia  To explore our APIs with [Insomnia](https://insomnia.rest/), follow these steps:  1. Open Insomnia and Import [our workspace](https://raw.githubusercontent.com/graphhopper/directions-api-doc/master/web/restclients/GraphHopper-Direction-API-Insomnia.json). 2. Specify [your API key](https://graphhopper.com/dashboard/#/register) in your workspace: Manage Environments -> Base Environment -> `\"api_key\": your API key` 3. Start exploring  ![Insomnia](./img/insomnia.png)  ## Postman  To explore our APIs with [Postman](https://www.getpostman.com/), follow these steps:  1. Import our [request collections](https://raw.githubusercontent.com/graphhopper/directions-api-doc/master/web/restclients/graphhopper_directions_api.postman_collection.json) as well as our [environment file](https://raw.githubusercontent.com/graphhopper/directions-api-doc/master/web/restclients/graphhopper_directions_api.postman_environment.json). 2. Specify [your API key](https://graphhopper.com/dashboard/#/register) in your environment: `\"api_key\": your API key` 3. Start exploring  ![Postman](./img/postman.png)  # Map Data and Routing Profiles  Currently, our main data source is [OpenStreetMap](https://www.openstreetmap.org). We also integrated other network data providers. This chapter gives an overview about the options you have.  ## OpenStreetMap  #### Geographical Coverage  [OpenStreetMap](https://www.openstreetmap.org) covers the entire world. If you want to convince yourself whether we can offer appropriate data for your region, please visit [GraphHopper Maps](https://graphhopper.com/maps/). You can edit and modify OpenStreetMap data if you find that important information is missing, for example, a weight restriction for a bridge. [Here](https://wiki.openstreetmap.org/wiki/Beginners%27_guide) is a beginner's guide that shows how to add data.  If you edited data, we usually consider your data after 1 week at latest.  #### Supported Vehicle Profiles  The Routing, Matrix and Route Optimizations support the following vehicle profiles:  Name       | Description           | Restrictions              | Icon -----------|:----------------------|:--------------------------|:--------------------------------------------------------- car        | Car mode              | car access                | ![car image](https://graphhopper.com/maps/img/car.png) small_truck| Small truck like a Mercedes Sprinter, Ford Transit or Iveco Daily | height=2.7m, width=2+0.4m, length=5.5m, weight=2080+1400 kg | ![small truck image](https://graphhopper.com/maps/img/small_truck.png) truck      | Truck like a MAN or Mercedes-Benz Actros | height=3.7m, width=2.6+0.5m, length=12m, weight=13000 + 13000 kg, hgv=yes, 3 Axes | ![truck image](https://graphhopper.com/maps/img/truck.png) scooter    | Moped mode | Fast inner city, often used for food delivery, is able to ignore certain bollards, maximum speed of roughly 50km/h | ![scooter image](https://graphhopper.com/maps/img/scooter.png) foot       | Pedestrian or walking | foot access         | ![foot image](https://graphhopper.com/maps/img/foot.png) hike       | Pedestrian or walking with priority for more beautiful hiking tours and potentially a bit longer than `foot`  | foot access         | ![hike image](https://graphhopper.com/maps/img/hike.png) bike       | Trekking bike avoiding hills | bike access  | ![bike image](https://graphhopper.com/maps/img/bike.png) mtb        | Mountainbike          | bike access         | ![Mountainbike image](https://graphhopper.com/maps/img/mtb.png) racingbike| Bike preferring roads | bike access         | ![racingbike image](https://graphhopper.com/maps/img/racingbike.png)  **Please note, that turn restrictions are considered only with `ch.disable=true`.**  For the free package you can only choose from `car`, `bike` or `foot`.  We also offer a sophisticated `motorcycle` profile powered by the [Kurviger](https://kurviger.de/en) Routing. Kurviger favors curves and slopes while avoiding cities and highways.  Also we offer custom vehicle profiles with different properties, different speed profiles or different access options. To find out more about custom profiles, please [contact us](https://www.graphhopper.com/contact-form/).  ## TomTom  If you need to consider traffic, you can purchase the TomTom add-on.  Please note:   * Currently we only offer this for our [Route Optimization](#tag/Route-Optimization-API).  * This add-on uses the TomTom road network and historical traffic information only. Live traffic is not yet considered. Read more about [how this works](https://www.graphhopper.com/blog/2017/11/06/time-dependent-optimization/).  * Additionally to our terms your end users need to accept the [TomTom Eula](https://www.graphhopper.com/tomtom-end-user-license-agreement/).  * We do *not* use the TomTom web services. We only use their data with our software.   [Contact us](https://www.graphhopper.com/contact-form/) for more details.  #### Geographical Coverage  We offer  - Europe including Russia - North, Central and South America - Saudi Arabia - United Arab Emirates - South Africa - Australia  #### Supported Vehicle Profiles  Name       | Description           | Restrictions              | Icon -----------|:----------------------|:--------------------------|:--------------------------------------------------------- car        | Car mode              | car access                | ![car image](https://graphhopper.com/maps/img/car.png) small_truck| Small truck like a Mercedes Sprinter, Ford Transit or Iveco Daily | height=2.7m, width=2+0.4m, length=5.5m, weight=2080+1400 kg | ![small truck image](https://graphhopper.com/maps/img/small_truck.png)   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@graphhopper.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six
# from swagger_client.models.object import Object  # noqa: F401,E501
from swagger_client.models.route_response_path_instructions import RouteResponsePathInstructions  # noqa: F401,E501


class RouteResponsePath(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'distance': 'float',
        'time': 'int',
        'ascend': 'float',
        'descend': 'float',
        'points': 'Object',
        'snapped_waypoints': 'Object',
        'points_encoded': 'bool',
        'bbox': 'list[float]',
        'instructions': 'list[RouteResponsePathInstructions]',
        'details': 'object',
        'points_order': 'list[int]'
    }

    attribute_map = {
        'distance': 'distance',
        'time': 'time',
        'ascend': 'ascend',
        'descend': 'descend',
        'points': 'points',
        'snapped_waypoints': 'snapped_waypoints',
        'points_encoded': 'points_encoded',
        'bbox': 'bbox',
        'instructions': 'instructions',
        'details': 'details',
        'points_order': 'points_order'
    }

    def __init__(self, distance=None, time=None, ascend=None, descend=None, points=None, snapped_waypoints=None, points_encoded=None, bbox=None, instructions=None, details=None, points_order=None):  # noqa: E501
        """RouteResponsePath - a model defined in Swagger"""  # noqa: E501
        self._distance = None
        self._time = None
        self._ascend = None
        self._descend = None
        self._points = None
        self._snapped_waypoints = None
        self._points_encoded = None
        self._bbox = None
        self._instructions = None
        self._details = None
        self._points_order = None
        self.discriminator = None
        if distance is not None:
            self.distance = distance
        if time is not None:
            self.time = time
        if ascend is not None:
            self.ascend = ascend
        if descend is not None:
            self.descend = descend
        if points is not None:
            self.points = points
        if snapped_waypoints is not None:
            self.snapped_waypoints = snapped_waypoints
        if points_encoded is not None:
            self.points_encoded = points_encoded
        if bbox is not None:
            self.bbox = bbox
        if instructions is not None:
            self.instructions = instructions
        if details is not None:
            self.details = details
        if points_order is not None:
            self.points_order = points_order

    @property
    def distance(self):
        """Gets the distance of this RouteResponsePath.  # noqa: E501

        The total distance, in meters.   # noqa: E501

        :return: The distance of this RouteResponsePath.  # noqa: E501
        :rtype: float
        """
        return self._distance

    @distance.setter
    def distance(self, distance):
        """Sets the distance of this RouteResponsePath.

        The total distance, in meters.   # noqa: E501

        :param distance: The distance of this RouteResponsePath.  # noqa: E501
        :type: float
        """

        self._distance = distance

    @property
    def time(self):
        """Gets the time of this RouteResponsePath.  # noqa: E501

        The total travel time, in milliseconds.   # noqa: E501

        :return: The time of this RouteResponsePath.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this RouteResponsePath.

        The total travel time, in milliseconds.   # noqa: E501

        :param time: The time of this RouteResponsePath.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def ascend(self):
        """Gets the ascend of this RouteResponsePath.  # noqa: E501

        The total ascent, in meters.   # noqa: E501

        :return: The ascend of this RouteResponsePath.  # noqa: E501
        :rtype: float
        """
        return self._ascend

    @ascend.setter
    def ascend(self, ascend):
        """Sets the ascend of this RouteResponsePath.

        The total ascent, in meters.   # noqa: E501

        :param ascend: The ascend of this RouteResponsePath.  # noqa: E501
        :type: float
        """

        self._ascend = ascend

    @property
    def descend(self):
        """Gets the descend of this RouteResponsePath.  # noqa: E501

        The total descent, in meters.   # noqa: E501

        :return: The descend of this RouteResponsePath.  # noqa: E501
        :rtype: float
        """
        return self._descend

    @descend.setter
    def descend(self, descend):
        """Sets the descend of this RouteResponsePath.

        The total descent, in meters.   # noqa: E501

        :param descend: The descend of this RouteResponsePath.  # noqa: E501
        :type: float
        """

        self._descend = descend

    @property
    def points(self):
        """Gets the points of this RouteResponsePath.  # noqa: E501


        :return: The points of this RouteResponsePath.  # noqa: E501
        :rtype: Object
        """
        return self._points

    @points.setter
    def points(self, points):
        """Sets the points of this RouteResponsePath.


        :param points: The points of this RouteResponsePath.  # noqa: E501
        :type: Object
        """

        self._points = points

    @property
    def snapped_waypoints(self):
        """Gets the snapped_waypoints of this RouteResponsePath.  # noqa: E501


        :return: The snapped_waypoints of this RouteResponsePath.  # noqa: E501
        :rtype: Object
        """
        return self._snapped_waypoints

    @snapped_waypoints.setter
    def snapped_waypoints(self, snapped_waypoints):
        """Sets the snapped_waypoints of this RouteResponsePath.


        :param snapped_waypoints: The snapped_waypoints of this RouteResponsePath.  # noqa: E501
        :type: Object
        """

        self._snapped_waypoints = snapped_waypoints

    @property
    def points_encoded(self):
        """Gets the points_encoded of this RouteResponsePath.  # noqa: E501

        Whether the `points` and `snapped_waypoints` fields are polyline-encoded strings rather than JSON arrays of coordinates. See the field description for more information on the two formats.   # noqa: E501

        :return: The points_encoded of this RouteResponsePath.  # noqa: E501
        :rtype: bool
        """
        return self._points_encoded

    @points_encoded.setter
    def points_encoded(self, points_encoded):
        """Sets the points_encoded of this RouteResponsePath.

        Whether the `points` and `snapped_waypoints` fields are polyline-encoded strings rather than JSON arrays of coordinates. See the field description for more information on the two formats.   # noqa: E501

        :param points_encoded: The points_encoded of this RouteResponsePath.  # noqa: E501
        :type: bool
        """

        self._points_encoded = points_encoded

    @property
    def bbox(self):
        """Gets the bbox of this RouteResponsePath.  # noqa: E501

        The bounding box of the route geometry. Format: `[minLon, minLat, maxLon, maxLat]`.   # noqa: E501

        :return: The bbox of this RouteResponsePath.  # noqa: E501
        :rtype: list[float]
        """
        return self._bbox

    @bbox.setter
    def bbox(self, bbox):
        """Sets the bbox of this RouteResponsePath.

        The bounding box of the route geometry. Format: `[minLon, minLat, maxLon, maxLat]`.   # noqa: E501

        :param bbox: The bbox of this RouteResponsePath.  # noqa: E501
        :type: list[float]
        """

        self._bbox = bbox

    @property
    def instructions(self):
        """Gets the instructions of this RouteResponsePath.  # noqa: E501

        The instructions for this route. This feature is under active development, and our instructions can sometimes be misleading, so be mindful when using them for navigation.   # noqa: E501

        :return: The instructions of this RouteResponsePath.  # noqa: E501
        :rtype: list[RouteResponsePathInstructions]
        """
        return self._instructions

    @instructions.setter
    def instructions(self, instructions):
        """Sets the instructions of this RouteResponsePath.

        The instructions for this route. This feature is under active development, and our instructions can sometimes be misleading, so be mindful when using them for navigation.   # noqa: E501

        :param instructions: The instructions of this RouteResponsePath.  # noqa: E501
        :type: list[RouteResponsePathInstructions]
        """

        self._instructions = instructions

    @property
    def details(self):
        """Gets the details of this RouteResponsePath.  # noqa: E501

        Details, as requested with the `details` parameter. Consider the value `{\"street_name\": [[0,2,\"Frankfurter Straße\"],[2,6,\"Zollweg\"]]}`. In this example, the route uses two streets: The first, Frankfurter Straße, is used between `points[0]` and `points[2]`, and the second, Zollweg, between `points[2]` and `points[6]`. See [here](https://discuss.graphhopper.com/t/2539) for discussion.   # noqa: E501

        :return: The details of this RouteResponsePath.  # noqa: E501
        :rtype: object
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this RouteResponsePath.

        Details, as requested with the `details` parameter. Consider the value `{\"street_name\": [[0,2,\"Frankfurter Straße\"],[2,6,\"Zollweg\"]]}`. In this example, the route uses two streets: The first, Frankfurter Straße, is used between `points[0]` and `points[2]`, and the second, Zollweg, between `points[2]` and `points[6]`. See [here](https://discuss.graphhopper.com/t/2539) for discussion.   # noqa: E501

        :param details: The details of this RouteResponsePath.  # noqa: E501
        :type: object
        """

        self._details = details

    @property
    def points_order(self):
        """Gets the points_order of this RouteResponsePath.  # noqa: E501

        An array of indices (zero-based), specifiying the order in which the input points are visited. Only present if the `optimize` parameter was used.   # noqa: E501

        :return: The points_order of this RouteResponsePath.  # noqa: E501
        :rtype: list[int]
        """
        return self._points_order

    @points_order.setter
    def points_order(self, points_order):
        """Sets the points_order of this RouteResponsePath.

        An array of indices (zero-based), specifiying the order in which the input points are visited. Only present if the `optimize` parameter was used.   # noqa: E501

        :param points_order: The points_order of this RouteResponsePath.  # noqa: E501
        :type: list[int]
        """

        self._points_order = points_order

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(RouteResponsePath, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RouteResponsePath):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
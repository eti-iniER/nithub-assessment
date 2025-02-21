# E-commerce API

This is my implementation of a simple e-commerce backend and API, as described in the NitHub Backend Internship probation task. I've implemented industry-standard practices such as:

-   Rate limiting
-   Query optimization (following Django's ORM best practices)
-   Security and permissions handling
-   Admin customization
-   Testing

I'll discuss each aspect of the implementation below.

## 0. Code structure

-   **Business logic and API layer:** I opted to keep business logic in managers, querysets, and models, in that order. This means that the core functionality of the application is decoupled from the API implementation. The API is purely a view layer; business logic entirely resides in the `core` application.

-   **Tests:** I followed general conventions of keeping all tests in a separate folder, outside of the application. I also made extensive use of factories and fixtures using the Pytest testing framework.

## 1. API implementation

I took full advantage of Django REST Framework's features, most notably **ViewSets**. This allowed me to implement the required endpoints in a short amount of time, and focus more on optimization and security.

I followed RESTful naming conventions as well; endpoints are named after collections of nouns, and the actions are inferred from the request type instead of being explicitly stated in the URI.

I also ensured the application is properly localized; the default timezone was set to "Africa/Lagos", and the default currency unit is the Kobo.

## 2. Authentication and permissions

For token authentication, I chose to use DRF Simple JWT, a popular library for integrating JSON Web Token-based authentication into Django REST Framework. I configured custom token lifecycles (see `settings.py`) to a reasonable expiry period.

Unauthenticated/anonymous users can only perform limited actions, such as viewing the available product catalogue, and creating user accounts.

I have also implemented basic password reset functionality.

## 3. Optimizations

It is very easy to abuse Django's powerful ORM and write very inefficient queries. I've worked hard to ensure that this is not the case with this API.

-   First, I relied on database-level operations where possible:

    -   Used **querysets** wherever possible, which are lazy-evaluated and will not run any operations until data is required. This also speeds up _batch operations_, which come in handy when processing large orders, and sidesteps the notorious problem of race conditions.

    -   Used **aggregation functions** like Sum() instead of iterating over querysets. This keeps operations at the database level, which is typically faster than performing them in Python.

    -   Used **query expressions** like F() to keep updates at the database level. This also helps to avoid race conditions, and reduces the need to handle them explicitly using atomic transactions.

-   I decided to handle currency/price values using _integers_ (via PositiveIntegerField), as opposed to using FloatField or DecimalField. This was a conscious choice; since the application is based in Nigeria, I used the **kobo** as the lowest currency denomination. Conversions to and from the naira are handled by utility functions (defined in `core.utils.py`).

While DecimalField would have been equally appropriate, I felt that this was a premature optimization, and would make performing typical operations more cumbersome, since it would necessitate importing the Decimal type and exclusively performing operations on Decimal fields with Decimal values.

I believed that this was a reasonable tradeoff.

## 4. Rate limiting

I configured request throttles and scope-based rate limits. I also created custom throttles for sensitive request types, such as creating users and placing orders.

In particular, I ensured that anonymous users had a _lower_ rate limit than authenticated users. This is favourable, as it means that in a high-load situation such as a flash sale, authenticated users will be given priority.

## 5. Administration and management

I extensively customized the Django admin panel, to ensure that site administrators could easily use the application as-is, without the need for a custom frontend.

-   **Search:** Product, Order and User instances are all searchable by various reasonable parameters.
-   **Filtering:** Orders can be filtered by date, Products can be filtered by stock quantity, and Users can be filtered by role
-   **Currency formatting:** Prices are displayed in Naira, despite being represented internally as Kobo.

## 6. Utility scripts

Following recommended practices, I decided to implement utility scripts as custom management commands. To run the CSV migration, for example, you only need to run `python manage.py import_from_csv ./path/to/csv/file.csv`.

This bypasses the need for authentication (as only system administrators can run the management script) and speeds up the process, since we can communicate directly with Django's ORM without the API as a middleman.

## Final remarks

I have learnt a lot throughout this task, most notably how to better test my backend applications using Pytest. I have also consulted a multitude of resources in the process, including the Django/DRF docs, StackOverflow, [RealPython](https://realpython.com), several Medium articles, and of course, our dear friend ChatGPT.

No matter the outcome of this process, I'm grateful to have been considered, thankful for the opportunity to grow and expand my skillset, and look forward to further collaboration with the NitHub organization.

Thanks!

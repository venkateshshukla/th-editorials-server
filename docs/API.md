### Request to `/api/list`

A `POST` request to `api/list` with a `timestamp` attribute of latest article
would be replied with a `JSON` consisting of the following

|    | Key | Explanation |
|----|-----|-------------|
| 1. | `r_timestamp`	| the timestamp of the recieved request |
| 2. | `u_timestamp`	| the updated timestamp, i.e, the timestamp of the latest article being sent |
| 3. | `num`		| the total number of entries being sent |
| 4. | `entries`	| a list of articles |

Each `article` have the following keys

|    | Key | Explanation |
|----|-----|-------------|
| 1. | `author`		| the author of the article |
| 2. | `key`		| an identifier to be used in further request to api/news |
| 3. | `kind`		| the kind of article being sent. opinion/letter/op-ed etc. |
| 4. | `print_date`	| a printable string having date of the article |
| 5. | `timestamp`	| the timestamp of the article being sent |
| 6. | `title`		| the title of the article |

##### Filtering articles based on their kinds

Optionally, the `POST` request might have an attribute `kinds` consisting of a
list of article kinds that are needed. This would cause filtering of the results
as per request.

Valid values of `kinds` attribute in `POST` request are as follows:

| `kinds` | Explanation |
|-------|-------------|
| 'default' | Articles of kind which are default are chosen. Refer to the table below for default kinds. |
| 'all' | Articles of all supported kinds are chosen. |
| a list of strings containing a subset of values present in the table below | Articles of requested supported kinds. |

Comprehensive list of supported kinds of articles are as follows:

| Supported kinds of articles | Default/Non-default |
|-------------------------------|---------------------|
| 'blogs' | Non Default |
| 'cartoon' | Non Default |
| 'columns' | Default |
| 'editorial' | Default |
| 'interview' | Default |
| 'lead' | Default |
| 'letters' | Non Default |
| 'op-ed' | Default |
| 'open-page' | Default |
| 'Readers-Editor' | Non Default |
| 'sunday-anchor' | Default |

### Request to `/api/news`

A `POST` request to `api/news` with a `key` attribute of required article
(obtained from a request to `api/list`) would be replied with a `JSON`
consisting of the following

|    | Key | Explanation |
|----|-----|-------------|
| 1. | `key`		| The key of the article sent in the request |
| 2. | `kind`		| The kind of the article |
| 3. | `snippet`	| The html snippet of the article |
| 4. | `error` (client error) | The reason for client side error |

In case of errors, the status code tell you about the error.

In case of client side error, the received JSON consists of `error` attribute
explaining the error.

### Request to api/list

A `POST` request to `api/list` with a `timestamp` attribute of latest article
would be replied with a `JSON` consisting of the following

1. `r_timestamp`	the timestamp of the recieved request
2. `u_timestamp`	the updated timestamp, i.e, the timestamp of the latest article being sent
3. `num`		the total number of entries being sent
4. `entries`		a list of articles

Each `article` have the following keys

1. `author`	the author of the article
1. `key`	an identifier to be used in further request to api/news
2. `kind`	the kind of article being sent. opinion/letter/op-ed etc.
3. `timestamp`	the timestamp of the article being sent
4. `title`	the title of the article

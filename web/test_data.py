# Auth codes
data_auth = "TESTAUTHCODE"
data_auth_admin = "TESTAUTHADMINCODE"

data_accounts_post_good = {
    "key": data_auth_admin,
    "username": "mike+testpromopuffin@westerncapelabs.com",
    "password": "testweak"
}

data_accounts_put_good = {
    "key": data_auth_admin,
    "username": "user1@example.com",
    "password": "testweak"
}

data_accounts_data = {
    "uuid_1": {
        "username": "user1@example.com",
        "password": "bcryptedhash",
        "key": "thisandthat",
    },
    "uuid_2": {
        "username": "user2@example.com",
        "password": "bcryptedhash",
        "key": "thisandthat",
    },
    "uuid_3": {
        "username": "user3@example.com",
        "password": "bcryptedhash",
        "key": "thisandthat",
    },
}

data_campaigns_post_good = {
    "name": "OneTheWayCampaign",
    "start": "2013-05-21T19:12:04.781440",
    "end": "2013-05-21T19:12:04.781462",
}

data_campaigns_put_good = {
    "name": "OneTheWayCampaign",
    "start": "2013-05-21T19:12:04.781440",
    "end": "2013-06-21T19:12:04.781462",
}

data_campaigns_data = {
    "uuid_1": {
        "name": "Campaign1",
        "start": "2013-05-21T19:12:04.781440",
        "end": "2013-05-21T19:12:04.781462",
        "status": "running",
    },
    "uuid_2": {
        "name": "Campaign2",
        "start": "2013-05-21T19:12:04.781440",
        "end": "2013-05-21T19:12:04.781462",
    },
    "uuid_3": {
        "name": "Campaign3",
        "start": "2013-05-21T19:12:04.781440",
        "end": "2013-05-21T19:12:04.781462",
    },   
}

data_campaigns_status_post_good = {
    "name": "Campaign1",
    "start": "2013-05-21T19:12:04.781440",
    "end": "2013-05-21T19:12:04.781462",
    "status": "halted",
}

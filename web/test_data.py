# Auth codes
data_auth = "TESTAUTHCODE"
data_auth_admin = "TESTAUTHADMINCODE"

data_accounts_post_good = {
    "api_key": data_auth_admin,
    "username": "mike+testpromopuffin@westerncapelabs.com",
    "password": "testweak"
}

data_accounts_put_good = {
    "api_key": data_auth_admin,
    "username": "user1@example.com",
    "password": "testweak"
}

data_accounts_data = {
    "uuid_1": {
        "username": "user1@example.com",
        "password": "bcryptedhash",
        "api_key": "thisandthat",
    },
    "uuid_2": {
        "username": "user2@example.com",
        "password": "bcryptedhash",
        "api_key": "thisandthat",
    },
    "uuid_3": {
        "username": "user3@example.com",
        "password": "bcryptedhash",
        "api_key": "thisandthat",
    },
}

data_campaigns_post_good = {
    "name": "OneTheWayCampaign",
    "start": "2013-05-21T19:12:04.781440",
    "end": "2013-05-21T19:12:04.781462",
    "account_id": "uuid_1",
}

data_campaigns_put_good = {
    "name": "OneTheWayCampaign",
    "start": "2013-05-21T19:12:04.781440",
    "end": "2013-06-21T19:12:04.781462",
    "account_id": "uuid_1",
}

data_campaigns_data = {
    "uuid_1": {
        "name": "Campaign1",
        "start": "2013-05-21T19:12:04.781440",
        "end": "2013-05-21T19:12:04.781462",
        "status": "running",
        "account_id": "uuid_1",
    },
    "uuid_2": {
        "name": "Campaign2",
        "start": "2013-05-21T19:12:04.781440",
        "end": "2013-05-21T19:12:04.781462",
        "account_id": "uuid_2",
    },
    "uuid_3": {
        "name": "Campaign3",
        "start": "2013-05-21T19:12:04.781440",
        "end": "2013-05-21T19:12:04.781462",
        "account_id": "uuid_3",
    },
}

data_campaigns_status_post_good = {
    "name": "Campaign1",
    "start": "2013-05-21T19:12:04.781440",
    "end": "2013-05-21T19:12:04.781462",
    "account_id": "uuid_1",
    "status": "halted",
}

data_campaigns_codes_data = {
    "uuid_1": {
        'campaign_id': 'uuid_1',
        'code': 'ACT-EKL-ABCDEF',
        'friendly_code': 'FREESHIPPING',
        "description": "A friendly name of the code",
        "status": "available",
        "value_type": "percentage",
        "value_amount": 50.00,
        "value_currency": "ZAR",
        "minimum": 250.00,
        "minimum_currency": "ZAR",
        "total": 50.00,
        "history": [],
        "remaining": 28.00,
    },
    "uuid_2": {
        'campaign_id': 'uuid_2',
        'code': 'ACT-EMD-ABCOSX',
        'friendly_code': 'FREESHIPPING',
        "description": "A friendly name of the code",
        "status": "unused",
        "value_type": "fixed",
        "value_amount": 50.00,
        "value_currency": "ZAR",
        "minimum": 250.00,
        "minimum_currency": "ZAR",
        "total": 50.00,
        "history": [],
        "remaining": 0.00,
    },
    "uuid_3": {
        'campaign_id': 'uuid_3',
        'code': 'QWZ-EMD-ABCDEF',
        'friendly_code': 'FREESHIPPING',
        "description": "A friendly name of the code",
        "status": "availiable",
        "value_type": "fixed",
        "value_amount": 50.00,
        "value_currency": "ZAR",
        "minimum": 250.00,
        "minimum_currency": "ZAR",
        "total": 50.00,
        "history": [],
        "remaining": 28.00,
    },
}

data_campaigns_codes_post_good = {
    'campaign_id': 'uuid_1',
    'code': 'ABC-DEF-GIJKLM',
    'friendly_code': 'DISCOUNTS',
    "description": "A friendly name of the code",
    "status": "availiable",
    "value_type": "fixed",
    "value_amount": 50.00,
    "value_currency": "ZAR",
    "minimum": 250.00,
    "minimum_currency": "ZAR",
    "total": 50.00,
    "remaining": 28.00,
}

data_campaigns_codes_put_good = {
    'campaign_id': 'uuid_1',
    'code': 'ABC-DEF-GIJKLM',
    'friendly_code': 'DISCOUNTS',
    "description": "A friendly name of the code",
    "status": "redeemed",
    "value_type": "fixed",
    "value_amount": 50.00,
    "value_currency": "ZAR",
    "minimum": 250.00,
    "minimum_currency": "ZAR",
    "total": 50.00,
    "remaining": 28.00,
}

data_validation_post_percentage_good = {
    'code_id': "uuid_1",
    'api_key': "thisandthat",
    "code": "ACT-EKL-ABCDEF",
    "friendly_code": "FREESHIPPING",
    "transaction_amount": 500.00,
    "transaction_currency": "ZAR",
}

data_validation_post_fixed_good = {
    'code_id': "uuid_2",
    'api_key': "thisandthat",
    "code": "ACT-EMD-ABCOSX",
    "friendly_code": "FREESHIPPING",
    "transaction_amount": 500.00,
    "transaction_currency": "ZAR",
}

data_validation_post_bad = {
    'code_id': "uuid_1",
    'api_key': "dsfjskdfjsl",
    "code": "ACT-EKL-ABEDTF",
    "friendly_code": "FREESHIPPING",
    "transaction_amount": 500.00,
    "transaction_currency": "USD",
}

data_redeem_percentage_good = {
    'code_id': "uuid_1",
    'api_key': "thisandthat",
    "code": "ACT-EKL-ABCDEF",
    "friendly_code": "FREESHIPPING",
    "transaction_amount": 500.00,
    "transaction_currency": "ZAR",
}

data_redeem_percentage_bad = {
    'code_id': "uuid_2",
    'api_key': "thisandthat",
    "code": "ACT-EMD-ABCOSX",
    "friendly_code": "FREESHIPPING",
    "transaction_amount": 500.00,
    "transaction_currency": "ZAR",
}

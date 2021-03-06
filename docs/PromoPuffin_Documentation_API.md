# Promopuffin Core Docs

This is work-in-progress documention for promopuffin-core the API behind promopuffin.
 

## API Design

### Accounts /accounts

    "uuid_1" = {
        username: "email@example.org",
        password: "BCRYPT_value",
        api_key: "some_key"
    }

#### /accounts	

* GET: List all accounts (auth admin only)
* POST: Create new account (auth admin only)

#### /accounts/{id}

* GET: Return account details (auth admin or self)
* PUT: Update details (where account_id = {id})
* DELETE: Delete {id} (where auth admin or self is {id})

#### /accounts/search

* GET: Take q and scope values and search accounts based on input (default limit 10, offset 0 - can be overridden)

### Campaigns /campaigns

    "uuid_1" = {
        name: "Friendly name",
        start: YYYY-MM-DDTHH:MM:SS,
        end: YYYY-MM-DDTHH:MM:SS,
        account_id: "uuid",
     }

#### /campaigns

* GET: List all campaigns (auth admin only)
* POST: Create new campaign (auth admin only)

#### /campaigns/{id}

* GET: Return campaign details (auth admin or self)
* PUT: Update {id} if exists (auth admin or self)
* DELETE: Delete {id} if auth admin or self is {id}

#### /campaign/search

* GET: Take q and scope values and search campaigns based on input (default limit 10, offset 0 - can be overridden)

#### /campaign/{id}/status

    {
        status: "running",
    }

* GET: Returns a status of campaign (error, pending, running, halted) - auth admin or self is {id}
* POST: Request a status change to pending/running/halted (auth admin or self is {id})

### Codes /campaigns/{id}/codes

   "uuid_1" =  {
        "campaign_id": "uuid" (link to campaign),
        "code": "ACT-CMP-ABCDE" (unique sys-wide),
        "friendly_code": "FREESHIPPING" (unique in campaign)
        "description": "A friendly name of the code",
        "status": "unused/available/redeemed/expired",
        "value_type": "fixed/percentage",
        "value_amount": 50.00,
        "value_currency": "ZAR",
        "minimum": 250.00,
        "total": 50.00,
        "history": {} (collection of timestaps for redeemed vouchers),
        "remaining": 28.00,
    }

#### /campaigns/{id}/codes

* GET: Returns all codes associated with a campaign (auth admin only or self is {id})
* POST: Creates a new code for a campaign, linked to campaign_id (auth admin only or self is {id})

#### /campaigns/{id}/codes/{id}

* GET: Return code details (auth admin or self)
* PUT: Update {id} if exists (auth admin or self), cannot change the campaign id, with which this code is associated with at the moment.
* DELETE: Delete {id} if auth admin or self is {id}


### Validate /validate

Need to supply code related data for validation.

	{
		"code_id": "uuid" (used to locate code data),
		"api_key": "34239840239849238098423",
		"code": "ACT-CMP-ABCDE",
		"friendly_code": "FREESHIPPING",
		"transaction_amount": 500.00,
		"transaction_currency": "ZAR",
	}

#### /validate

* POST: Takes a series of codes related variables and returns true/false

Returns If True:

	{
		"valid": true,
		"value_type": "fixed/percentage",
		"value_amount": 50.00,
		"value_currency": "ZAR", 
	}

or If False:

    {
        "valid": false,
        "errors": [] (list of error msgs),
    }

### Redeem /redeem

Validates and Redeems promo voucher 

    {
    	"api_key": "34239840239849238098423",
    	"code": "ACT-CMP-ABCDE",
    	"friendly_code": "FREESHIPPING",
    	"transaction_amount": 500.00,
    	"transaction_currency": "ZAR",
    }

#### /redeem/{id}

* POST: Takes series of code data, validates and updates campaign voucher availability(auth admin or campaign {id} who has {api_key})

Returns:

    {
        "redeemed": True/False,
        "status": "unused/available/redeemed/expired",
        "total": 50.00,
        "remaining": 28.00,
    }
     

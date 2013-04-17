# Promopuffin Core Docs

This is work-in-progress documention for promopuffin-core the API behind promopuffin.
 

## API Design

### Accounts /accounts

#### /accounts

* GET: List all accounts (auth admin only)
* POST: Create new account

#### /accounts/{id}

* GET: Return account details (auth admin or self)
* PUT: Update {id} if exists (auth admin or self)
* DELETE: Delete {id} if auth admin or self is {id}

#### /accounts/search

* GET: Take q and scope values and search accounts based on input (default limit 10, offset 0 - can be overridden)

### Campaigns

	{
		campaign_id: 12345678,
		name: "Friendly name",
		start: YYYY-MM-DDTHH:MM:SS,
		end: YYYY-MM-DDTHH:MM:SS,
	}

#### /campaigns

* GET: List all campaigns (auth admin only)
* POST: Create new campaign

#### /campaign/search

GET: Take q and scope values and search campaigns based on input (default limit 10, offset 0 - can be overridden)

#### /campaigns/{id}

* GET: Return campaign details (auth admin or self)
* PUT: Update {id} if exists (auth admin or self)
* DELETE: Delete {id} if auth admin or self is {id}

#### /campaign/{id}/status

	{
		status: "running",
	}

* GET: Returns a status of campaign (error, pending, running, halted)
* POST: Request a status change to pending/running/halted

### Codes /codes

	{
		"code": "ACT-CMP-ABCDE" (unique sys-wide),
		"friendly_code": "FREESHIPPING" (unique in campaign)
		"type": "fixed/percentage",
		"description": "A friendly name of the code",
		"status": "unused/available/redeemed/expired",
		"value_type": "fixed/percentage",
		"value_amount": 50.00,
		"value_currency": "ZAR",
		"minimum": 250.00,
		"minimum_currency": "ZAR",
		
	}

#### /codes


### Validate /validate

#### /validate

GET/POST: Takes a series of variables and returns true/false

	{
		"api_key": "34239840239849238098423",
		"code": "ACT-CMP-ABCDE",
		"friendly_code": "FREESHIPPING",
		"transaction_amount": 500.00,
		"transaction_currency": "ZAR",
	}

Returns:

	{
		"valid": true,
		"value_type": "fixed/percentage",
		"value_amount": 50.00,
		"value_currency": "ZAR", 
	}
	
### Auth /auth

Helper endpoint to validate auth keys






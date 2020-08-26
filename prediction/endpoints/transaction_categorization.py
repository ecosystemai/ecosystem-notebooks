GET_TRANSACTIONS = {
	"type": "post",
	"endpoint": "/getTransactions",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

GET_TRANSACTIONS_CAT_PREDICTED = {
	"type": "post",
	"endpoint": "/getTransactionsCatPredicted",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

GET_TRANSACTIONS_PROCESSED = {
	"type": "get",
	"endpoint": "/getTransactionsProcessed",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
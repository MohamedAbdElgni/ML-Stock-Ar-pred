from model_s import StockModel


db_name = "stocks.sqlite"

ls_tick = {
    "Apple": "AAPL",
    "IBM": "IBM",
    "Microsoft": "MSFT",
    "Google": "GOOG",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "META": "META",
}


for table_name in ls_tick.keys():

    print(f"Training model for {table_name}")

    model = StockModel(table_name=table_name, order=(5, 0, 0))

    model.train_model(cut=0.80, returns=True)

    model.insert_pred_table()

    print(
        f"Model for {table_name} trained and inserted into the database under name [{table_name}_pred]")
    
print("All models trained and inserted into the database")




    
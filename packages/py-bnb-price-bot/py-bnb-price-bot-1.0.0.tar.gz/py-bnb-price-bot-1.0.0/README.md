# Telegram Bot for Binance Price Fetching

This Telegram bot allows you to fetch the current price of cryptocurrencies from the Binance API.

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/crypto9coin/binance-telegram-bot.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Obtain a Telegram bot token from the BotFather on Telegram and replace `TELEGRAM_TOKEN` in `bot.py` with your bot token.

4. Run the bot:

    ```bash
    python bot.py
    ```

## Usage

1. Start a conversation with your bot on Telegram.

2. Use the `/price` command followed by the symbol of the cryptocurrency you want to fetch the price for. For example:

    ```
    /price BTCUSDT
    ```

3. The bot will reply with the current price of the specified cryptocurrency.

## Contributing

Contributions are welcome! If you have any suggestions or find any issues, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
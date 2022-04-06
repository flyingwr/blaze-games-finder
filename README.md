### **Note**
Unexpectedly, this program had to be updated: It was then managing to retrieve the data of each game running on [Double](https://blaze.com/pt/games/double]) by using WebSockets, but now is just making a single HTTP request to Blaze API since some inner things changed.

For some odd reason <font size=1>(they might be trying to hide something? 🤔)</font>, the seed of each game running on Double **is no longer being included on the page**.

Despite of that, it's still possible to get the last games seeds by fetching them through the [API](https://blaze.com/api/roulette_games/recent).

### **Usage example (Double)**
In order to make it work, there must be a seed grabbed of a game.
* Calculate a single seed
    ```python
    from utils import calc_seed

    seed = "d28341d85a7c182a6a58dfd1d4a21a1fe4fa06f3ba18ae0fe9575ac2fff0d153"

    if __name__ == "__main__":
        print(calc_seed(seed))
    ```

    Output:
    ```JS
    {'color': 'white', 'roll': 0, 'server_seed': 'd28341d85a7c182a6a58dfd1d4a21a1fe4fa06f3ba18ae0fe9575ac2fff0d153'}
    ```

* Calculate a prior amount of seeds
    ```python
    from utils import calc_seed, get_previous_seeds

    seed = "d28341d85a7c182a6a58dfd1d4a21a1fe4fa06f3ba18ae0fe9575ac2fff0d153"

    if __name__ == "__main__":
        print(list(map(calc_seed, get_previous_seeds(seed, 10))))
    ```

    Output:
    ```json
    [{'color': 'white', 'roll': 0, 'server_seed': 'd28341d85a7c182a6a58dfd1d4a21a1fe4fa06f3ba18ae0fe9575ac2fff0d153'}, {'color': 'red', 'roll': 4, 'server_seed': '0fd4e2ed5b0c472547024feccded18e75eafce1769830c4b8cbae1e9ff49bd39'}, {'color': 'black', 'roll': 8, 'server_seed': 'f19b0de8d6f870bf34a3e96691aee9a9234744b44d071fd1663a0ee984d3c221'}, {'color': 'black', 'roll': 10, 'server_seed': '4f8b5b62a975331c8c42f88c3f462aa34606c85c3837229a597350f6d4066b73'}, {'color': 'red', 'roll': 1, 'server_seed': 'b0f9a5935760671035f5340939137aa550836a6421860aabd9e55d2b5a110235'}, {'color': 'red', 'roll': 7, 'server_seed': '9d4e2b55087b1ec4f555a1824bf85b98c6ab4c246f8233e826cfddc9e21e4703'}, {'color': 'red', 'roll': 3, 'server_seed': '8a0609f36e8771f7f0d10951d8808ab6f4d83896f360d5427a734604c8e74406'}, {'color': 'black', 'roll': 13, 'server_seed': 'fd65bd9d22861f08ee8603114e683e1251b278a2c69d8c67b88ca4feefe24450'}, {'color': 'white', 'roll': 0, 'server_seed': '78b3e25fd4bf658279b635d535075579e0f015b97dbc20a80dd6f2259c42523f'}, {'color': 'black', 'roll': 13, 'server_seed': '450e1d2443fccda94449d211722dbfb12e7c69e4c1a0eb373c8eb005c4bd7cca'}, {'color': 'black', 'roll': 8, 'server_seed': '2d278ba09ea882b859e5bb94e63f3ae21f731d1f5a8769967b797c5cabc356e9'}]
    ```
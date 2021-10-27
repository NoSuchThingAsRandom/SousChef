<script>
    import Header from "./Header.svelte";
    import {onMount} from "svelte";
    import Item from "./Item.svelte";
    import {getData} from "./data";
    import {getExtraData} from "./extraData";
    import {Accordion, AccordionSection, Button, Card, H1, H2, H3, Label} from "attractions"
    //,,,Soft Drinks,Sharers,
    // ,,Snacks,Cold Sandwiches,Hot Sandwiches,,,,
    // ,,Mineral,,,,,Alcopops,
    // ,,,Energy Drinks,
    // ,,Iced Drinks,Other Sales,


    let sortedCategories = {
        "Spirits": ["Liqueurs", "Rum", "Gin", "Bourbon", "Vodka", "Spirits Other", "Whisky"],
        "Hot Drinks": ["Tea", "Coffee", "Hot Chocolate", "Hot Drinks Other"],
        "Cocktails": ["Cocktail Pitchers", "Alcoholic Cocktails", "Mocktails", "Alcopops"],
        "Soft Drinks": ["Canned Soft Drinks", "Soft Drinks", "Mineral", "Energy Drinks", "Iced Drinks"],
        "Food": ["Mains", "Pizzas", "Breakfast", "Jacket Potatoes", "Food Specials", "Light Bites", "Desserts", "Sides", "Sharers", "Snacks", "Hot Sandwiches", "Cold Sandwiches"],
        "On Tap": ["Draft Beer Craft", "Packaged Beer", "Packaged Beer No Low", "Draft Cider", "Draft Beer", "Bottled Cider"],
        "Wine": ["Red Wine", "Rose Wine", "White Wine", "Sparkling Wine/Champagne"],
        "The Black Market ;)": ["No Longer Used DF", "No Longer Used Wet", "Post Mix", "Other Sales"],
        "Search": ["Results"]
    };
    let basket = {};
    let basketTotal = 0.00;
    let selectedCategory = "";
    let oldSelectedCategory = "";
    let menuCategories = Object.keys(sortedCategories);
    let menu = {};
    let extras = {};
    let showDialog = false;
    let searchItems = [];
    let showSearch = false;
    onMount(() => {
        let seen = new Set();
        console.log(menu[""])
        let data = getData();
        menu["Search"] = {};
        for (let item of data) {
            if (seen.has(item["name"])) {
                continue;
            }
            seen.add(item["name"]);
            let found = false;
            for (const [main_categorisation, sub_cat_items] of Object.entries(sortedCategories)) {
                for (const item_type of sub_cat_items) {
                    if (item_type === item["course_name"]) {
                        if (menu[main_categorisation] === undefined) {
                            menu[main_categorisation] = {};
                        }
                        if (menu[main_categorisation][item_type] === undefined) {
                            menu[main_categorisation][item_type] = [];
                        }
                        menu[main_categorisation][item_type].push(item);
                        found = true;
                        break;
                    }
                }
                if (found) {
                    break;
                }
            }
            if (!found) {
                console.log("Not found: ", item);
                menu[item["course_name"]] = [item];
                menuCategories.push(item["course_name"]);
            }
        }
        let rawExtra = getExtraData();
        for (let name of Object.keys(rawExtra)) {
            extras[name] = {"prices": [], "index": []};
            for (const [index, price] of rawExtra[name]) {
                extras[name]["prices"].push(price);
                extras[name]["index"].push(index);
            }
        }
        console.log(menu);
    });

    async function execute() {
        console.log("TODO Submit basket!")
        console.log(basket);
        console.log("Making request");
        const response = await fetch("http://127.0.0.1:5000/execute_order", {
            method: "POST",
            headers: {"Accept": "application/json", "Content-Type": "application/json"},
            body: JSON.stringify(basket)
        });
        console.log(response);
    }

    function getRndInteger(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function deleteFromBasket(item) {
        basketTotal -= item["price"];
        delete basket[item["id"]];
        basket = basket;

    }

    function randomItems() {
        console.log("Generate random items!")
        let category = Object.keys(menu)[getRndInteger(0, Object.keys(menu).length)];
        let sub_category = Object.keys(menu[category])[getRndInteger(0, Object.keys(menu[category]).length)];
        let item = menu[category][sub_category][getRndInteger(0, (menu[category][sub_category]).length)];
        let quantity = getRndInteger(0, 10);
        let price = parseFloat(item["price"]) * quantity;
        let extra_count = getRndInteger(0, 10);
        let extrasChosen = [];
        console.log("Chose: ", item, " with quanity: ", quantity);
        for (let i = 0; i < extra_count; i++) {
            let index = getRndInteger(0, Object.keys(extras).length);
            let key = Object.keys(extras)[index];
            console.log("Indwex: ", index, " key: ", key);
            let extra = extras[key];
            let extraVariant = getRndInteger(0, extra["prices"].length);
            console.log(extra);
            let parsedExtra = {'name': key, 'id': extra['index'][extraVariant], 'price': extra['prices'][extraVariant]};
            console.log(parsedExtra);
            price += parseFloat(extra['prices'][extraVariant]);
            extrasChosen.push(parsedExtra);
        }
        let value = {
            "id": item["pos_item_id"],
            "name": item["name"],
            "quantity": quantity,
            "price": price,
            "extras": extrasChosen
        };
        console.log("Adding: ", value);
        basket[item["pos_item_id"]] = value;
        basketTotal += price;
    }

    function applySearch(value) {
        value = value["detail"];

        console.log("Searching for:", value);
        let items = [];
        for (let key of Object.keys(menu)) {
            if (key === "Search") {
                continue;
            }

            for (let subKey of Object.keys(menu[key])) {
                for (let item of menu[key][subKey]) {
                    if (item["name"].toLowerCase().includes(value.toLowerCase())) {
                        items.push(item);
                    }
                }
            }

        }
        menu["Search"]["Results"] = items;
        menu = menu;
        console.log(menu);
        showSearch = true;
    }

    $:if (oldSelectedCategory !== selectedCategory) {
        showSearch = false;
    }
</script>
<Header bind:menuCategories={menuCategories} bind:selectedCategory="{selectedCategory}" on:execute={execute}
        on:search={(value)=>applySearch(value)}
        on:lucky={randomItems}/>

<div style="display: flex;justify-content: space-between">
    <div style="width: 60%;margin-left: 2em">
        {#if showSearch}
            <Card outlined style="margin-top:2em ">
                <H2>Results:</H2>
                {#each menu["Search"]["Results"] as item}
                    <Item bind:item={item} bind:extras on:basketUpdate={(data)=>{
                            basket[data["detail"]["id"]]=data["detail"];
                            basketTotal+=data["detail"]["price"];
                                    console.log(basket);
                        }}/>
                {/each}
            </Card>
        {:else }
            {#if menu[selectedCategory] !== null && menu[selectedCategory] !== undefined}
                <Accordion>
                    {#each Object.keys(menu[selectedCategory]) as subKey}
                        <Card outlined style="margin-top:2em ">
                            <AccordionSection let:toggle>
                                <div slot="handle">
                                    <Button on:click={toggle}>
                                        {subKey}
                                    </Button>
                                </div>
                                {#each menu[selectedCategory][subKey] as item}
                                    <Item bind:item={item} bind:extras on:basketUpdate={(data)=>{
                            basket[data["detail"]["id"]]=data["detail"];
                            basketTotal+=data["detail"]["price"];
                                    console.log(basket);
                        }}/>
                                {/each}
                            </AccordionSection>
                        </Card>
                    {/each}
                </Accordion>
            {/if}
        {/if}

    </div>
    <Card outline style="width: 30%;padding: 2em;margin: 2em">

        <H1>Basket - £{parseFloat(basketTotal).toFixed(2)}</H1>

        {#if Object.values(basket).length === 0}
            <Card>
                <H2>Select some items :(</H2>
            </Card>
        {/if}
        {#each Object.values(basket) as basketItem}
            <Card>
                <div style="display: flex">
                    <H2>{basketItem["quantity"]} X {basketItem["name"]} (ID: {basketItem["id"]}) - Total:
                        £{parseFloat(basketItem["price"]).toFixed(2)}</H2>
                    <Button style="color: red;margin-left: auto" on:click={()=>{deleteFromBasket(basketItem)}}>X
                    </Button>
                </div>
                <H3>Extras: </H3>
                {#each Array.from(basketItem["extras"].values()) as e}
                    <Label style="margin-left: 1em">{e["name"]} - (ID: {e["id"]}) -
                        £{parseFloat(e["price"]).toFixed(2)}</Label>
                {/each}
            </Card>
        {/each}
    </Card>
</div>

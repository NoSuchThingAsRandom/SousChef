<script>
    import {Button, Card, Checkbox, Dialog, Divider, H3, Label, Modal, TextField} from "attractions";
    import {createEventDispatcher} from "svelte";

    export let extras;
    export let item;
    let extraNames = Object.keys(extras);
    let showExtras = false;
    let chosenExtras = {};
    let searchTerm = "";
    let quantity = 1;

    const dispatch = createEventDispatcher();

    function selectExtra(value) {
        if (value["checked"]) {
            chosenExtras[value["value"]["id"]] = (value["value"]);
        } else {
            delete chosenExtras[value["value"]["id"]];
            chosenExtras = chosenExtras;
        }
    }

    function addAll() {
        console.log("Adding all extras");
        for (let extra of Object.keys(extras)) {
            for (let index = 0; index < extras[extra]["prices"].length; index++) {
                selectExtra({
                    "value": {
                        'name': extra,
                        'id': extras[extra]['index'][index],
                        'price': extras[extra]['prices'][index]
                    }, "checked": true

                });
            }
        }
    }

    function addAllFree() {
        console.log("Adding all free extras");
        for (let extra of Object.keys(extras)) {
            for (let index = 0; index < extras[extra]["prices"].length; index++) {
                if (parseFloat(extras[extra]["prices"][index]) === 0.00) {
                    selectExtra({
                        "value": {
                            'name': extra,
                            'id': extras[extra]['index'][index],
                            'price': extras[extra]['prices'][index]
                        }, "checked": true
                    });
                }
            }
        }
    }

    function isExtraSelected(value) {
        return Object.keys(chosenExtras).includes(value.toString());
    }

    function filterExtras() {
        extraNames = Object.keys(extras);
        extraNames = extraNames.filter((value => {
            return value.toLowerCase().includes(searchTerm.toLowerCase())
        }));
    }

    function updateBasket() {
        console.log("Adding item ", item["name"], " with quantity ", quantity, " and extras: ", chosenExtras);
        let price = parseFloat(item["price"]) * parseFloat(quantity);
        let extrasParsed = [];
        for (let jsonE of Object.values(chosenExtras)) {
            console.log(jsonE);
            let e = jsonE;
            price += parseFloat(e["price"]);
            extrasParsed.push(e);
        }
        dispatch("basketUpdate", {
            "id": item["pos_item_id"],
            "name": item["name"],
            "quantity": quantity,
            "price": price,
            "extras": extrasParsed
        });
        showExtras = false;
    }
</script>
<Card style="margin-top: 2em">
    <div style="display: flex;justify-content: space-between">
        <H3 style="align-self: flex-start">{item["name"]}</H3>
        <H3 style="align-self: flex-end">£{parseFloat(item["price"]).toFixed(2)}</H3>
    </div>
    <Button filled on:click={()=>{
        showExtras=true;

    }} style="margin-top: 1em">Buy!
    </Button>

    {#if showExtras}
        <Modal bind:open={showExtras} class="sc" let:closeCallback>
            <Dialog title="{item['name']}" style="width:100%;">
                <span>
                <H3>Quantity</H3>
                <TextField bind:value={quantity}
                           error="{(isNaN(quantity) ||  (parseInt(quantity)<0)) && 'It only accepts positive numbers, but there is no size checks...'}"
                           label="Quantity" outline
                           placeholder="1"/>
                    </span>
                <Divider/>
                <H3>Extras:</H3>
                <div style="display: flex">
                    <TextField style="height: 4em" bind:value={searchTerm} on:input={filterExtras} outline
                               placeholder="Search for an extra"/>
                    <Button filled style="margin: 0.5em" on:click={addAll}>Add All</Button>
                    <Button filled style="margin: 0.5em" on:click={addAllFree}>Add All Free</Button>
                </div>
                <div style="height: 30em; overflow-y: scroll">
                    {#key chosenExtras}
                        {#each extraNames as extra}
                            <Card style="margin: 0.5em">
                                <Label>{extra} has {extras[extra]["prices"].length}
                                    version{extras[extra]["prices"].length === 0 ? "s" : ""}:</Label>
                                {#each extras[extra]["prices"] as price,i}
                                    <Checkbox
                                            on:change={(value,selected)=>{selectExtra({"value":JSON.parse(value["detail"]["value"]),"checked":value["detail"]["checked"]},selected)}}
                                            style="margin-top: 2em"
                                            value="{JSON.stringify({'name':extra,'id':extras[extra]['index'][i],'price':extras[extra]['prices'][i]})}"
                                            checked="{isExtraSelected(extras[extra]['index'][i])}">
                                        <Label small style="margin-left: 1em">ID: {extras[extra]["index"][i]} @
                                            £{parseFloat(price).toFixed(2)}</Label>
                                    </Checkbox>

                                {/each}
                            </Card>

                        {/each}
                    {/key}
                </div>
                <div style="display: flex">
                    <Button on:click={updateBasket}>Submit</Button>
                    <Button on:click={()=>showExtras=false}>Exit</Button>
                </div>
            </Dialog>
        </Modal>
    {/if}
</Card>
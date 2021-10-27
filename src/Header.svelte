<script>
    import {Button, Card, H2, Headline, Subhead, Tabs, TextField} from "attractions";
    import {createEventDispatcher} from "svelte";

    const dispatch = createEventDispatcher();
    export let selectedCategory;
    export let menuCategories;
    let searchQuery="";
    const items = [{href: '/', text: 'Home'},
        {href: '/docs', text: 'Docs'},
        {text: 'Components'},
    ];
</script>
<Card outline style="display: flex;justify-content: flex-start">
    <div style="align-self: flex-start;width: 60%">
        <Headline>YUSousChef</Headline>
        <Subhead>Better deals than if you were shagging the chef!</Subhead>
        <div style="display: flex">
            <Tabs bind:value={selectedCategory} items="{menuCategories}" name="menu" style=""/>
        </div>
    </div>
    <div style=";width: 40%;display: flex;align-items: flex-start">
        <div style="margin-left: auto;width: 60%">
        <TextField style="height: 4em;width: 100%" bind:value={searchQuery} on:input={dispatch("search",searchQuery)} outline
                   placeholder="Search for an item"/>
        </div>
        <Button style="margin-left: 5%;height: 4em;" filled on:click={()=>{dispatch("lucky")}}>I'm feeling lucky!</Button>
        <Button style="margin-left: 5%;height: 4em;" filled on:click={()=>{dispatch("execute")}}>Submit Order</Button>
    </div>
</Card>

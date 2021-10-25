<script>
    import {Button, Card, H2,Headline, Subhead, Tabs} from "attractions";
    import {createEventDispatcher} from "svelte";

    const dispatch = createEventDispatcher();
    export let selectedCategory;
    export let menuCategories;
    const items = [{href: '/', text: 'Home'},
        {href: '/docs', text: 'Docs'},
        {text: 'Components'},
    ];
</script>
<Card outline style="display: flex;justify-content: flex-start">
    <div style="align-self: flex-start">
        <Headline>YUSousChef</Headline>
        <Subhead>Better deals than if you were shagging the chef!</Subhead>
        <div style="display: flex">
            <Tabs bind:value={selectedCategory} items="{menuCategories}" name="menu" style=""/>
        </div>
    </div>

    <Button style="margin-left: auto;height: 3em;width: 10em" filled on:click={()=>{dispatch("lucky")}}>I'm feeling lucky!</Button>
    <Button style="margin-left: auto;height: 3em;width: 10em" filled on:click={()=>{dispatch("execute")}}>EXECUTE</Button>
</Card>
<div>

    <!--    <Breadcrumbs {items}>
            <div let:item slot="item">
                {#if item.href === '/'}
                    <Button href="/" round small>
                        <HomeIcon size="20"/>
                    </Button>
                {:else}
                    <Chip>{item.text}</Chip>
                {/if}
            </div>
            <ArrowRightIcon size="20" slot="separator"/>
        </Breadcrumbs>-->
</div>